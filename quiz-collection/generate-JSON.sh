#!/bin/bash

inputFiles=./raw_hr/*.hr
JSON=./json_output/JSON
JSONFiles=./json_output/


merge=0
while getopts ":cmh" opt; do
  case ${opt} in
    h ) # Help Message
    echo "-c Clean old JSON output files before creating new ones" ;
    echo "-m Merge all JSON output files into a single file" ; 
    
    exit 0
    ;;
    c ) # Clean old files before creating new ones
        ./clean.sh -j
        ;;
    m ) # Merge all output files into a single file 
        merge=1
        ;;
    \? ) # Warn Message
        echo -e "Option \033[0;31m$OPTARG\033[0m not recognized, \
use \033[0;31m./generate-JSON -h\033[0m for help" ;
        exit 0
        ;;
  esac
done

# Generate each JSON output file
i=0
scriptDir=./parser-hr-json/hr-json.py
for inputFile in $inputFiles
do
    python3 $scriptDir -i "$inputFile" -o "$JSON""_out$i.json"
    let "i+=1"
done


if [ $merge -eq 1 ]; then
    # Create merge file and add first bracket for list
    mergeFile="${JSON}merged.json"
    touch $mergeFile
    echo "[" >> $mergeFile

    for jsonFile in $(ls ./json_output/ | grep -e "JSON_.*.json") 
    do
        jsonFile=${JSONFiles}$jsonFile
        cat $jsonFile  | tail -n+2 | head -n-1 >> $mergeFile
        echo "," >> $mergeFile
        rm $jsonFile
    done
    temp="./json_output/merge.temp"
    touch $temp 
    cat $mergeFile > $temp
    sed '$ s/.$//' $mergeFile > $temp
    cat $temp > $mergeFile
    echo "]" >> $mergeFile
    rm $temp
fi