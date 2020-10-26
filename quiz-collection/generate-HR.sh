#!/bin/bash
# Usage ./generate_U_HR.sh extraTag1,extraTag2,...,extraTagN

# Merging all *.xml files in the input folder so they can be sent as input
# to the MXML to HR parser python3 script

inputFiles=./inputs/*.xml
HR=./raw_hr/HR

auto_year=0
auto_topic=0
while getopts ":e:u:ytch" opt; do
  case ${opt} in
    h ) #Help message
        echo "-e tag1,tag2,...,tagN \
Add extra arguments separated by comma topics,reviewed_by" ;
        echo "-y Auto insert year if contained in input filename \
(eg. ./input/2019.xml)" ;
        echo "-u username If reviewed_by tag is present, auto assign \
name of reviewer" ;
        echo "-c Clean old HR files" ;
        echo "-t Auto Assign topic tag values for each question based \
on Dictionary"

        exit 0
        ;;
    # Clean old files before creating new ones
    c ) 
        ./clean.sh -u
        ;;
    # Additional tags that fit within the "tags" list
    e ) 
        extraTags=$OPTARG
        ;;
    # Automatically add username of reviewer in tags list
    # ! Only effective if "reviewed_by" tag is given to -e arg
    u ) 
        reviewer=$OPTARG 
        ;;
    # Automatically add created and last used tags using the
    # year stored in the filename
    y ) 
        auto_year=1 
        ;;
    # Automatically adds chapter tags to questions
    t ) 
        auto_topic=1
        ;;
    \? ) 
        echo -e "Option \033[0;31m$OPTARG\033[0m not recognized, \
use \033[0;31m./generate-HR -h\033[0m for help";
        exit 0
        ;;
  esac
done

# Checking if output folder exists, otherwise, create it
if [ ! -d "./raw_hr/" ]; then
    mkdir "./raw_hr/"
fi

# Checking if XML input files exist and confirm their number
if [ -d "./inputs" ] && [ $(ls $inputFiles | wc -l) -gt 0 ]; then
    echo "Found $(ls $inputFiles | wc -l) file(s) to be processed"
else
    echo "No input files found, make sure there are \
valid MXML files in \"./inputs/\" and rerun this script!"
    echo "Usage: ./generate-HR.sh extraTag1,extraTag2,...,extraTagN "
    exit 1
fi

i=0
scriptDir=./parser-mxml-hr/mxml-hr.py
for inputFile in $inputFiles
do 
    if [ $auto_year -eq 1 ]; then
        if ! $(echo "$inputFile" | grep -o -e "[2][0][0-2][0-9]") 2> /dev/null ; then
            year=$(echo "$inputFile" | grep -o -e "[2][0][0-2][0-9]")
        else
            echo "No valid year found in filename $inputFile, \
assigning 0 as default value"
            year=0
        fi
    else
        year=0
    fi

    echo "Processing $inputFile file number $i"
    # Manual usage: python3 msml-hr.py -i input_file -o output_file -e tag1,tag2,...,tagN [-u str -y -t -c]
    python3 "$scriptDir" -i "$inputFile" -o "$HR$i.hr" -e \
            "$extraTags" -y "$year" -u "$reviewer"
    
    if [ $auto_topic -eq 1 ]; then
        python3 auto-topic/auto-topic.py -i "$HR$i.hr" -o $(echo "$HR""_aa_$i.hr")
        rm "$HR$i.hr"
    fi

    let "i+=1"
done