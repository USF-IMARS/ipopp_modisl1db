#!/bin/bash -e
# Installs all the stations in a given SPA, by calling
# NISGS_ROOT/ncs/bin/installSPA.sh with the directory this file
# is sitting in.
# Takes no arguments - assumes it's running from NISGS_ROOT/SPA/spa_directory

# First find out where we are.  bash needs *load-truename* so bad...

case $0 in
         /*)  SHELLFILE=$0 ;;
        ./*)  SHELLFILE=${PWD}${0#.} ;;
        ../*) SHELLFILE=${PWD%/*}${0#..} ;;
          *)  SHELLFILE=$(type -P $0) ; if [ ${SHELLFILE:0:1} != "/" ]; then SHELLFILE=${PWD}/$SHELLFILE ; fi ;;
esac
SHELLDIR=${SHELLFILE%/*}
NCS_HOME=${SHELLDIR}/../../ncs

# Throw a fit if we can't find the install script
if [[ ! ( -f $NCS_HOME/bin/installSPA.sh ) ]]
    then
    echo Can\'t find the NCS install script
    echo Are you sure this was unpacked in the SPA directory'?'
    exit -1
fi

$NCS_HOME/bin/installSPA.sh $SHELLDIR $*
