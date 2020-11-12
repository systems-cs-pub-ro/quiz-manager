# Code originally written by Cristian Vijelie
# Modifications were made to add a tagline to the aiken human readable format
# Original code was obtained from the following commit:
# https://github.com/systems-cs-pub-ro/quiz-manager/commit/18f149cabcf544be87f920e4f4becca7c9f86c3d
# usage: python3 mxml-hr.py -i <input file> -o <output file> -e <tag1,tag2,...>

import json
import sys
import getopt
from datetime import datetime
import xml.etree.ElementTree as ET


# Load the Structure file (needed to determine types of tags)
def loadStructure():
    try:
        structure = open("./structure.json", "r")
    except structure is None:
        print("File not found!")
        sys.exit(0)

    return json.load(structure)


def genTagline(structure, extraTags, reviewed_by):
    # Create a list of keys as found in structure file
    keyList = list(structure.keys())
    if len(extraTags) > 0:
        extraTags = extraTags.split(',')
        keyList += extraTags
    tagline = ""
    # Removing mandatory tags as they are assumed to exist
    # anyway and will be automatically completed by hr to json script
    keyList.remove("statement")
    keyList.remove("tags")
    keyList.remove("answers")
    keyList.remove("correctAnswersNo")

    for key in keyList:
        if structure.get(key) is None:
            if key == "reviewed_by" and reviewed_by is not "":
                tagline += key + ':' + reviewed_by + ';'
            else:
                tagline += key + ':' + 'n/a' + ';'
        else:
            tagline += key + ':' + str(structure[key]) + ';'

    return tagline


def main(argv):
    infile_name = ''
    outfile_name = ''
    reviewed_by = "n/a"
# Parse the arguments given to the script
    extraTags = str()
    try:
        opts, _ = getopt.getopt(argv, "hi:e:o:y:u:")
    except getopt.GetoptError:
        print('Bad arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i"):
            infile_name = arg
        elif opt in ("-o"):
            outfile_name = arg
        elif opt in ("-e"):
            extraTags = arg
        elif opt in ("-y"):
            year = arg
        elif opt in ("-u"):
            reviewed_by = arg

    outfile = open(outfile_name, "w")

# Load structure file
    structure = loadStructure()
    print()
    if year is not "0":
        date = datetime.date(datetime(int(year), 1, 1))
        structure["createdOn"] = date
        structure["lastUsed"] = date

    tagline = genTagline(structure, extraTags, reviewed_by)

# Parse the XML file
    tree = ET.parse(infile_name)
    root = tree.getroot()

# Extract the question name and answers and add them to the file
# The answers which have a positive fraction will have '+' in front of them,
# to mark them as correct. Otherwise, a '-' will be placed.
    filter = []
    filter.append("Nu știu / Nu răspund".upper())
    filter.append("Nu știu/Nu răspund".upper())

    for element in root.iter('question'):
        if element.attrib['type'] == 'multichoice':
            statement = element[1][0].text
            answers = ""
            for answer in element.iter('answer'):
                if (answer[0].text.upper() in filter):
                    continue
                if float(answer.attrib['fraction']) > 0:
                    answers += ('+ ' + answer[0].text + '\n')
                else:
                    answers += ('- ' + answer[0].text + '\n')

            outfile.write(tagline + '\n')
            outfile.write(statement + '\n')
            outfile.write(answers + '\n')

    outfile.close()


if __name__ == "__main__":
    main(sys.argv[1:])
