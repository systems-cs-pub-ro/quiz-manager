import datetime
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
    :return: the question stored in mXML
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

if __name__ == '__main__':
    try:
        with open('../test_questions.json') as json_file:
            questions = json.load(json_file)
    except:
        print("JSON could not be loaded")
        sys.exit(1)

    quizMXML = ElementTree.Element('quiz')

    for question in questions:
        quizMXML = json2mXML(question, quizMXML)

    roughXML = ElementTree.tostring(quizMXML)
    reparsed = minidom.parseString(roughXML)
    prettyXML = reparsed.toprettyxml(indent="  ")

    # makes a strin with current date and time
    now = datetime.datetime.now()
    strTime = now.strftime("%d%m%Y_%H%M%S")

    # filename pattern: "Quiz_DDMMYYYY_HHMMSS.xml"
    filename = "Questions_" + strTime + ".xml"

    moodleXMLFile = open(filename, "w")
    moodleXMLFile.write(prettyXML)
