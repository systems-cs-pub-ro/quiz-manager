import json
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom
from random import randrange

def get_meta(question_dict : dict, key : str):

    if(not (key in question_dict["metadata"])):
        return ""

    if(len(question_dict["metadata"][key]) == 1):
        return question_dict["metadata"][key][0]
    else:
        return question_dict["metadata"][key]

def set_meta(question_dict : dict, key : str, value : any):
    if(key in question_dict["metadata"]):
        question_dict["metadata"][key].append(value)
    else :
        question_dict["metadata"][key] = []
        question_dict["metadata"][key].append(value)

def quiz_json_to_mxml(json_arr : list):
    quizMXML = ElementTree.Element('quiz')
    for mxml_elem in list(map(json_to_mxml, json_arr)):
        quizMXML.append(mxml_elem)

    roughXML = ElementTree.tostring(quizMXML)
    reparsed = minidom.parseString(roughXML)
    prettyXML = reparsed.toprettyxml()
    return prettyXML

def quiz_mxml_to_json(file_content : ElementTree.Element):
    mxml_element_tree = ElementTree.fromstring(file_content)
    return list(map(mxml_to_json, mxml_element_tree))

def json_to_mxml(json_question : str) -> ElementTree.Element:
    """
    Generates the Moodle XML entry for the given question

    :param jsonQuestion: a question stored in JSON format
    :param quiz: the quiz to which the question is added
    :return: a quiz stored in MXML format containing json_question
    """
    # creating the hierarchy
    json_obj = json.loads(json_question)
    question = ElementTree.SubElement(ElementTree.Element("quiz"), 'question')
    nameText = ElementTree.SubElement(ElementTree.SubElement(question, 'name'), 'text')
    questionText = ElementTree.SubElement(question, 'questiontext')
    tags = ElementTree.SubElement(question, 'tags')
    questionTextText = ElementTree.SubElement(questionText, 'text')
    question.set('type', 'multichoice')
    questionText.set('format', 'html')
    questionTextText.text = json_obj['statement'][:-1]
    nameText.text = json_obj['statement'][:-1]

    single = ElementTree.SubElement(question, 'single')
    if json_obj['correct_answers_no'] > 1:
        single.text = 'false'
    else:
        single.text = 'true'

    # adding the difficulty tag
    tag = ElementTree.SubElement(tags, 'tag')
    tagText = ElementTree.SubElement(tag, 'text')
    tagText.text = 'difficulty=' + get_meta(json_obj,"difficulty")

    # adding other tags
    for jsonTag in json_obj["metadata"]:
        tag = ElementTree.SubElement(tags, 'tag')
        tagText = ElementTree.SubElement(tag, 'text')
        tagText.text = jsonTag + "=" + get_meta(json_obj, jsonTag)

    # adding the answers in the file
    for jsonAnswer in json_obj['answers']:
        answer = ElementTree.SubElement(question, 'answer')
        answerText = ElementTree.SubElement(answer, 'text')
        answerText.text = jsonAnswer['statement'][:-1]
        answer.set('fraction', str(jsonAnswer['grade'] * 100))
        answer.set('format', "html")
    
    return question

def mxml_to_json(xml: ElementTree.Element) -> str:
    """
    Generates a question in JSON format from MXML object

    :param xml: a question stored in MXML format
    :return: the question stored in JSON format
    """
    # Template question to be completed with necessary info and returned
    question = {
        "statement": "",
        "metadata": {},
        "answers": [
            # {
            #     "statement": "",
            #     "correct": False,
            #     "grade": 0.0
            # }
        ],
        "correct_answers_no": 0
    }


    # Iterate through all elements of a single question
    for element in xml.iter('question'):
        if element.attrib["type"] == 'multichoice':
            # Get question statement and assign it to dictionary
            statement = element.find("questiontext").find("text").text
            question["statement"] = statement + "\n"

            if(element.find("tags") != None):
                for tag in element.find("tags").iter("tag"):
                    tag_pair = tag.find("text").text.split("=")
                    set_meta(question, tag_pair[0], tag_pair[1])

            # Prepare counter for correct answer number
            correct_ans = 0
            for answer in element.iter('answer'):
                # Get the answer statement
                ans_statement = answer.find("text").text
                # Process correct and wrong answers accordingly
                if float(answer.attrib['fraction']) > 0:
                    question["answers"].append(
                        {
                            "statement": ans_statement + "\n",
                            "correct": True,
                            "grade": float(answer.attrib['fraction']) / 100
                        }
                    )
                    correct_ans += 1
                else:
                    question["answers"].append(
                        {
                            "statement": ans_statement + "\n",
                            "correct": False,
                            "grade": float(answer.attrib['fraction']) / 100
                        }
                    )

                
    
    question["correct_answers_no"] = correct_ans
    return json.dumps(question, indent=2)
