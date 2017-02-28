"""
Routines to parse HDF4 file metadata.

"""

import re
import modules.DictUtils as du
import sys

def dumpMetadata(filename):
    """Dump file metadata:
        Use 'hdp dumpsds' for hdf4 files
        Use 'h5dump -Au' for hdf5 files
        read ASCII header from MERIS N1 files
    """
    import os
    import subprocess

    # does input file exist?
    if not os.path.isfile(filename):
        print "Can't find input file '" + filename + "'."
        return None

    # does executable exist?
    hdp = os.path.join(os.getenv('LIB3_BIN'), 'hdp')
    h5dump = os.path.join(os.getenv('LIB3_BIN'), 'h5dump')
    mimecmd = ['file','--brief',filename]
    mime = subprocess.Popen(mimecmd, stdout=subprocess.PIPE).communicate()[0]
    
    if re.search('Hierarchical.*version.4',mime):
        if not (os.path.isfile(hdp) and os.access(hdp, os.X_OK)):
            print hdp, "is not executable."
            return None

        # dump file header
        cmd = [hdp, 'dumpsds', '-h', '-s', filename]
        f = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        contents = f.read()

        return contents
    elif re.search('Hierarchical.*version.5',mime):
        if not (os.path.isfile(h5dump) and os.access(h5dump, os.X_OK)):
            print h5dump, "is not executable."
            return None

        # dump file header
        cmd = [h5dump,  '-Au', filename]
        f = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        return f.read()
    else:
        fb = open(filename,'r',1)
        line1 = fb.readline()
        fb.close()

        if (re.search("HDF_UserBlock",line1)):


            if not (os.path.isfile(h5dump) and os.access(h5dump, os.X_OK)):
                print h5dump, "is not executable."
                return None

            # dump file header
            cmd = [h5dump,  '-Au', filename]
            f = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
            return f.read()
        else:
            header = []
            fb = open(filename,'r',100)
            for line in fb.readlines(100):
                line = line.strip()
                if not len(line):
                    continue
                header.append(line)
                if re.search('LAST_LAST_LONG',line):
                    break
            fb.close()
            return header

def readMetadata(filename):
    """
    read retrieved (via dumpMetadata) file metadata into dictionary
    """
    # todo: MERIS N1 files?
    text = dumpMetadata(filename)
    # Added text == [] & changed exit() to sys.exit()    -Matt, Feb. 15, 2012
    # Kept an exit here (instead of making it a return) as already
    # existing programs assume the output from this function is good.
    if text is None or text == '' or text == []:
        sys.exit()

    attrs = None

    # extract meaningful parts
    if isinstance(text, list):
        if re.search('PRODUCT',text[0]):
            attrs = {}
            for line in text:
                (key,value) = str(line).split('=')
                attrs[key] = str(value).strip('"')
            return attrs
        elif text[0][0:4] == 'CWIF':
            return {'Title': 'SeaWiFS Level-0'}
    elif re.search('<\?xml', text):
        # if hdf5 file
        attrs = get_xml_attr(text)
    else:
        #if hdf4 file
        file_attr_re = re.compile('File attributes:(.+?)\n', re.MULTILINE | re.DOTALL)
        file_attr_results = file_attr_re.search(text)
        if file_attr_results != None:
            file_attr_var_re = re.compile('File attributes:(.+?)\nVariable', re.MULTILINE | re.DOTALL)
            file_attr_var_results = file_attr_var_re.search(text)
            if file_attr_var_results != None:
                allmeta = file_attr_var_results.group(1)
                # remove spaces around "=" to speed future searches
                allmeta = re.sub(r'\s*=\s*', '=', allmeta)
                # parse each file attribute
                attrs = get_odl_attr(allmeta)
            else:
                attrs = get_attr(text)
    return attrs

def get_attr(text):
    attrs = {}
    lines = text.split('\n')
    attr_pattern = re.compile('^\s*Attr\d+: Name = ')
    value_pattern = re.compile('^\s*Value = ')
    in_attr = False
    for line in lines:
        if re.match(attr_pattern, line):
            in_attr = True
            attr_name = line.split('=')[1].strip()
        elif in_attr:
            if re.match(value_pattern, line):
                val = str(line).split('=')[1].strip()
                attrs[attr_name] = val
    return attrs

def get_odl_attr(metatext):
    """
    get interesting bits from ODL formatted metadata
    """
    attrs = {}
    pattern = r'^\s*Attr\d+: Name=(.+?)\s*Type=(.+?)\s*Count=(.+?)\s*Value=(.+?)$'
    reAttr = re.compile(pattern, re.MULTILINE | re.DOTALL)

    for att in reAttr.finditer(metatext):
        name, dtype, count, value = att.groups()

        if 'char' in dtype:
            # interpret ASCII codes
            value = re.sub(r'\\000', '', value)   # null
            value = re.sub(r'\\011', '\t', value) # horizontal tab
            value = re.sub(r'\\012', '\n', value) # newline

        else:
            # add commas between array elements so they'll evaluate correctly
            if eval(count) > 1:
                value = ','.join(value.split())
                # evaluate string to numerical type
            value = set_type(value)

        if 'Metadata.' in name:
            # interpret ODL heirarchy
            value = parse_odl(value)

        # add attribute to dictionary
        attrs[name] = value

    # eliminate redundant info, then return dictionary.
    prune_odl(attrs)
    return attrs

def get_xml_attr(metaxml):
    """
    parse xml formatted metadata
    """
    from BeautifulSoup import BeautifulStoneSoup
    attrSoup = BeautifulStoneSoup(metaxml)
    attrs = attrSoup.findAll('attribute')
    attr = {}
    for i in attrs:
        attr[str(i.attrs[0][1]).strip()] = (str(i.contents[5].contents[1].contents[0]).strip()).strip('"')
    return attr


def parse_odl(text):
    """Recursively extract ODL groups and objects."""

    # descend into GROUP/OBJECT heirarchy
    pattern = r"(GROUP|OBJECT)=(.+?)$(.+?)END_\1=\2"
    reODL = re.compile(pattern, re.MULTILINE | re.DOTALL)
    items = {}
    blocks = reODL.findall(text)
    for block in blocks:
        key = block[1]
        value = block[2]
        items[key] = parse_odl(value)

    # get value(s) at innermost level
    if not len(items.keys()):
        for line in text.splitlines(): get_value(line, items)

    return items


def get_value(text, items=None):
    """Interpret text as key/value pairs, if possible."""
    if items is None:
        items = {}
    try:
        key, value = [i.strip() for i in text.split('=', 1)]
        items[key] = set_type(value)
    except ValueError:
        pass
    return items


def set_type(value):
    """Parse string value into correct type"""
    try:
        return eval(value)
    except (NameError, SyntaxError, TypeError):
        return value  # leave unchanged anything that can't be evaluated


def prune_odl(metadict):
    du.delete_key(metadict, 'StructMetadata.[0-9]')
    du.delete_key(metadict, '(NUM_VAL|CLASS)')
    du.promote_value(metadict, '.*VALUE')
    du.reassign_keys_in_dict(metadict,
                             'ADDITIONALATTRIBUTENAME', 'INFORMATIONCONTENT')
    du.flatten_dict(metadict)
    return
