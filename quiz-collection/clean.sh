#!/bin/bash

XML=./inputs/*.xml
JSON=./json_output/*.json
HR=./raw_hr/*.hr


while getopts ":ijuh" opt; do
  case ${opt} in
    h ) #Help message
        echo "-j Clean old JSON files" ;
        echo "-i Clean old XML files" ;
        echo "-u Clean old HR files" ;

        exit 0
        ;;
    j ) # Remove old JSON output files
          rm $JSON 2>/dev/null
        ;;
    i ) # Remove old XML input files
        rm $XML 2>/dev/null
        ;;
    u ) # Remove old Human Readable files
        rm $HR 2>/dev/null
        ;;
    \?) #Warn
        echo "Use ./clean -h for help"
        ;;
  esac
done

# Default message in case no args present
if [[ $1 == "" ]]; then 
  echo "Use ./clean -h for help"
  exit 0
fi


# In case files don't exist 
# Just exit without any error code 
exit 0
