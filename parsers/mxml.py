import json
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom
from random import randrange

def get_meta(map : dict, key : str):

    if(not (key in map["metadata"])):
        return ""

    if(len(map["metadata"][key]) == 1):
        return map["metadata"][key][0]
    else:
        return map["metadata"][key]

def set_meta(map : dict, key : str, value : any):
    if(key in map["metadata"]):
        map["metadata"][key].append(value)
    else :
        map["metadata"][key] = []
        map["metadata"][key].append(value)


def json_to_mxml(json_question : str, quiz : ElementTree) -> str:
    """
    Generates the Moodle XML entry for the given question

    :param jsonQuestion: a question stored in JSON format
    :param quiz: the quiz to which the question is added
    :return: a quiz stored in MXML format containing json_question
    """
    # creating the hierarchy
    json_obj = json.loads(json_question)
    question = ElementTree.SubElement(quiz, 'question')
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

def mxml_to_json(xml: ElementTree.Element,
                 reviewer: str = "n/a",
                 author: str = "n/a",
                 date: str = "n/a",
                 topics: str = "n/a",
                 difficulty: str = "0") -> str:
    """
    Generates a question in JSON format from MXML object

    :param xml: a question stored in MXML format
    :param reviewer: string that can contain the initials of the reviewer
    :param author: string that can contain the initials of the question author
    :param year: int that can contain the year the question was originally created
    :param topics: string of comma separated values representing the topics related to the question
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

    # Add tags
    set_meta(question, "created_on", date)
    set_meta(question, "last_used", date)
    set_meta(question, "reviewed_by", reviewer)
    set_meta(question, "created_by", author)
    set_meta(question, "topic", topics)
    set_meta(question, "difficulty", difficulty)

    # Iterate through all elements of a single question
    for element in xml.iter('question'):
        if element.attrib["type"] == 'multichoice':
            # Get question statement and assign it to dictionary
            statement = element.find("questiontext").find("text").text
            question["statement"] = statement + "\n"

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

                
    
    question["correctAnswersNo"] = correct_ans
    return json.dumps(question, indent=2)
