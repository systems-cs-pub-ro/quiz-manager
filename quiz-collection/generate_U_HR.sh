#!/bin/bash
EXTRA_TAGS=$1

# USAGE ./generate_U_HR.sh <extraTag1,extraTag2,...>

#MERGING ALL INPUT FILES INTO A SINGLE XML FILE TO BE FED TO "mxml-hr.py" SCRIPT
#PY SCRIPT GENERATES UNANNOTATED HUMAN READABLE QUIZ FILE
INPUT_FOLDER=./inputs/*.xml
SCRIPT=./parser-mxml-hr/mxml-hr.py
XML=./not_annotated_xml/xml_whole.xml
HR=./not_annotated_hr/hr_wip.hr

touch $XML
i=0

for inputFile in $INPUT_FOLDER
do
    echo "Processing" $inputFile " file number " $i
    if [ $i -eq 0 ]; then
        cat $inputFile | head -n -1 >> $XML
    elif [ $i -lt $(ls inputs | wc -l) ] && [ $i -gt 0 ]; then
        cat $inputFile | tail -n +3 | head -n -1 >> $XML
    else
        cat $inputFile | tail -n +3 >> $XML
    fi
    let "i+=1"
done

if [ $(ls inputs | wc -l) -le 2 ]  ; then
    echo "</quiz>" >> $XML
fi

# RUNNING SCRIPT
# Manual usage: python3 msml-hr.py -i <input file> -o <output file> -e <tag1,tag2,...>

python3 $SCRIPT -i $XML -o $HR --etags=$EXTRA_TAGS


