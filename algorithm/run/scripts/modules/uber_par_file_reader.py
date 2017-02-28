
"""
Functions for reading the parameter file for the uber processor.
"""

import re
import sys

__author__ = 'melliott'

SECTION_HEADER_TEXT = 'section'

def get_sect_key(line):
    """
    Returns the section name from a line of text.
    The line is expected to be of the form '# section SECTION_NAME' (without the quotes).
    """
    sect_key = ''
    sect_key = re.sub('\s*\[\s*', '', line)
    sect_key = re.sub('\s*\]\s*', '', sect_key)
    return sect_key

def is_section_header(line):
    """
    Returns True if a line is the header for a new section; returns False otherwise.
    """
    section_pattern = '\s*\[\s*\S+.*\]\s*'               # + SECTION_HEADER_TEXT + '.*\s*'
    compiled_pattern = re.compile(section_pattern, re.IGNORECASE)
    if re.search(compiled_pattern, line.strip()):
        return True
    else:
        return False

def is_whole_line_comment(line):
    """
    Returns True if an entire line is a comment; returns False otherwise.
    """
    if line.lstrip()[0:1] == '#':
        return True
    else:
        return False

def read_par_file(par_name, acceptable_single_keys):
    """
    Parses a parameter file, returning the contents in a dictionary of
    dictionaries.  The "outer" dictionary contains each section.  The "inner"
    dictionaries contain the parameter/value pairs.
    """
    par_results = {}
    sect_key = None
    sect_dict = {}
    with open(par_name, 'rt') as par_file:
        for line in par_file.readlines():
            line = line.strip()
#            print "Processing line: '{0}'".format(line)
            if not is_whole_line_comment(line):
                if is_section_header(line):
                    if sect_key != None:
                        par_results[sect_key] = sect_dict
                    sect_dict = {}
                    sect_key = get_sect_key(line)
                else:
                    if sect_key != None:
                        if line.find('='):
                            key, val = line.split('=', 2)
                            if key == 'par':
                                if 'par' in sect_dict:
                                    sect_dict['par'].append(val.strip())
                                else:
                                    sect_dict['par'] = [val.strip()]
                            else:
                                if key not in sect_dict:
                                    sect_dict[key] = val.strip()
                                else:
                                    sys.exit('Duplicate entry found for {0} in {1}'.format(key), par_name)
                        elif line.strip in acceptable_single_keys:
                            sect_dict[key] = 'True'
                        else:
                            err_msg = 'Found entry {0} with no value in {1}'.format(key, par_name)
                            sys.exit(err_msg)
                    else:
                        err_msg = 'Error in {0}, no section header found!'.format(par_name)
                        sys.exit(err_msg)
        if sect_key != '':
            par_results[sect_key] = sect_dict
    return par_results

