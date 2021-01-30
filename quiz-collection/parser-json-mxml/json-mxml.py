import datetime
import getopt
import json
import sys
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom
from random import randrange

def json2mXML(jsonQuestion, quiz):
    """
    Generates the Moodle XML entry for the given question

    :param jsonQuestion: a question stored in JSON
    :param quiz: the quiz to which the question is added
    :return: the quiz stored in mXML
    """
    # creating the hierarchy
    question = ElementTree.SubElement(quiz, 'question')
    nameText = ElementTree.SubElement(ElementTree.SubElement(question, 'name'), 'text')
    questionText = ElementTree.SubElement(question, 'questiontext')
    tags = ElementTree.SubElement(question, 'tags')
    questionTextText = ElementTree.SubElement(questionText, 'text')
    question.set('type', 'multichoice')
    questionText.set('format', 'html')
    questionTextText.text = jsonQuestion['statement']
    nameText.text = jsonQuestion['statement'][:75] + '...'

    single = ElementTree.SubElement(question, 'single')
    if jsonQuestion['correctAnswersNo'] > 1:
        single.text = 'false'
    else:
        single.text = 'true'

    # adding the difficulty tag
    tag = ElementTree.SubElement(tags, 'tag')
    tagText = ElementTree.SubElement(tag, 'text')
    tagText.text = 'difficulty=' + str(jsonQuestion['difficulty'])

    # adding other tags
    for jsonTag in jsonQuestion['tags']:
        if jsonTag['key'] == 'topics' and len(jsonTag['values']) > 0:
            tag = ElementTree.SubElement(tags, 'tag')
            tagText = ElementTree.SubElement(tag, 'text')
            tagText.text = 'topic=' + jsonTag['values'][randrange(len(jsonTag['values']))]

    # adding the answers in the file
    for jsonAnswer in jsonQuestion['answers']:
        answer = ElementTree.SubElement(question, 'answer')
        answerText = ElementTree.SubElement(answer, 'text')
        answerText.text = jsonAnswer['statement']
        answer.set('fraction', str(jsonAnswer['grade'] * 100))
        answer.set('format', "html")

    return quiz

def getArgs(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Invalid command arguments\nUsage: python3 json-mxml.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: python3 json-mxml.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    return input_file, output_file

if __name__ == '__main__':
    input_file, output_file = getArgs(sys.argv[1:])
    try:
        with open(input_file) as json_file:
            questions = json.load(json_file)
    except:
        print("Invalid input file\nUsage: python3 json-mxml.py -i <inputfile> -o <outputfile>")
        sys.exit(1)

    quizMXML = ElementTree.Element('quiz')

    for question in questions:
        quizMXML = json2mXML(question, quizMXML)

    roughXML = ElementTree.tostring(quizMXML)
    reparsed = minidom.parseString(roughXML)
    prettyXML = reparsed.toprettyxml(indent="  ")

    try:
        with open(output_file, "w") as mxml_file:
            mxml_file.write(prettyXML)
    except:
        print("Invalid output file\nUsage: python3 json-mxml.py -i <inputfile> -o <outputfile>")
        sys.exit(1)
