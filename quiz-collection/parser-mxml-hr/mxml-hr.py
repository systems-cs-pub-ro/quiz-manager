# Acesta este codul lui Cristian Vijelie pe care l-am modificat pentru adugarea tag line-ului la intrebarile in format human readable
# Codul a fost obtinut din urmatorul commit: 
# https://github.com/systems-cs-pub-ro/quiz-manager/commit/18f149cabcf544be87f920e4f4becca7c9f86c3d
# usage: python3 mxml-hr.py -i <input file> -o <output file> -e <tag1,tag2,...>

import json
import sys, getopt
import xml.etree.ElementTree as ET

# Load the Structure file (needed to determine types of tags) 
def loadStructure():
    try:
        structure = open("./structure.json", "r")
    except:
        print("File not found!")
        sys.exit(0)

    return json.load(structure)

def genTagline(structure,extraTags):

    # Creating a list of custom and extra keys in structure file    
    
    keyList = list(structure.keys())
    if len(extraTags) > 0 :
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

        if structure.get(key) is None :
            tagline += key + ':' + ' ' + ';'
        else :
            tagline += key + ':' + str(structure[key]) + ';'

    return tagline

def main(argv):
    infile_name = ''
    outfile_name = ''

# Parse the arguments given to the script
    extraTags = str()
    try:
        opts, _ = getopt.getopt(argv,"hi:eo:",["ifile=","ofile=","etags="])
    except getopt.GetoptError:
        print('XML-to-human.py -i <inputfile> -o <outputfile>!')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('XML-to-human.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            infile_name = arg
        elif opt in ("-o", "--ofile"):
            outfile_name = arg
        elif opt in ("-e", "--etags"):
            extraTags = arg

    outfile = open(outfile_name, "w")

# Load structure file
    structure = loadStructure()
    tagline = genTagline(structure,extraTags)

# Parse the XML file
    tree = ET.parse(infile_name)
    root = tree.getroot()

# Extract the question name and answers and add them to the file
# The answers which have a positive fraction will have '+' in front of them,
# to mark them as correct. Otherwise, a '-' will be placed.

    for element in root.iter('question'):
        if element.attrib['type'] == 'multichoice':
            
            name = element[1][0].text
            answers = ""
            for answer in element.iter('answer'):
                if float(answer.attrib['fraction']) > 0:
                    answers += ('+ ' + answer[0].text + '\n')
                else:
                    answers += ('- ' + answer[0].text + '\n')

            outfile.write(tagline + '\n')
            outfile.write(name + '\n')
            outfile.write(answers + '\n')
        
    
    outfile.close()

if __name__ == "__main__":
    main(sys.argv[1:])