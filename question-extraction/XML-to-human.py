import sys, getopt
import xml.etree.ElementTree as ET

def main(argv):
    infile_name = ''
    outfile_name = ''

# Parse the arguments given to the script
    try:
        opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('XML-to-human.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('XML-to-human.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            infile_name = arg
        elif opt in ("-o", "--ofile"):
            outfile_name = arg

    outfile = open(outfile_name, "w")

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

            outfile.write(name + '\n')
            outfile.write(answers + '\n')
        
    
    outfile.close()

if __name__ == "__main__":
    main(sys.argv[1:])