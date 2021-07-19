import json
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom
from random import randrange

def json_to_mxml(json_question : str, quiz : ElementTree) -> str:
    """
    Generates the Moodle XML entry for the given question

    :param jsonQuestion: a question stored in JSON
    :param quiz: the quiz to which the question is added
    :return: the quiz stored in mXML
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
    if json_obj['correctAnswersNo'] > 1:
        single.text = 'false'
    else:
        single.text = 'true'

    # adding the difficulty tag
    tag = ElementTree.SubElement(tags, 'tag')
    tagText = ElementTree.SubElement(tag, 'text')
    tagText.text = 'difficulty=' + str(json_obj['difficulty'])

    # adding other tags
    for jsonTag in json_obj['tags']:
        tag = ElementTree.SubElement(tags, 'tag')
        tagText = ElementTree.SubElement(tag, 'text')
        tagText.text = jsonTag["key"] + "=" + jsonTag['values'][randrange(len(jsonTag['values']))]

    # adding the answers in the file
    for jsonAnswer in json_obj['answers']:
        answer = ElementTree.SubElement(question, 'answer')
        answerText = ElementTree.SubElement(answer, 'text')
        answerText.text = jsonAnswer['statement'][2:-1]
        answer.set('fraction', str(jsonAnswer['grade'] * 100))
        answer.set('format', "html")
    
    return quiz

def mxml_to_json(xml: ElementTree.Element,
                 reviewer: str = "n/a",
                 author: str = "n/a",
                 year: int = 2021,
                 topics: str = "n/a") -> str:
    '''
    Generate a single JSON object from a question in MXML format
    '''
    # Template question to be completed with necessary info and returned
    question = {
        "createdOn": "",
        "lastUsed": "",
        "difficulty": 0,

        "statement": "",
        "tags": [
        ],
        "answers": [
            # {
            #     "statement": "",
            #     "correct": False,
            #     "grade": 0.0
            # }
        ],
        "correctAnswersNo": 0
    }

    # Add tags
    date = str(year) + "-01-" + "01"
    question["createdOn"] = date
    question["lastUsed"] = date
    question["tags"].append({
        "key": "reviewed_by",
        "values": [
            reviewer
        ]
    })
    question["tags"].append({
        "key": "author",
        "values": [
            author
        ]
    })
    question["tags"].append({
        "key": "topics",
        "values": [
            topics
        ]
    })

    # Add undesirable answers to filter
    # TODO discuss moving filter to a separate file and read from that
    filter = []
    filter.append("Nu știu / Nu răspund".upper())
    filter.append("Nu știu/Nu răspund".upper())

    # Iterate through all elements of a single question
    for element in xml.iter('question'):
        if element.attrib["type"] == 'multichoice':
            # Get question statement and assign it to dictionary
            statement = element.find("questiontext").find("text").text
            question["statement"] = statement + "\n"

            # Prepare counter for correct answer number
            correct_ans = 0
            for answer in element.iter('answer'):
                # Get the answer statement and check if it can be found in the
                # filter
                ans_statement = answer.find("text").text
                if (ans_statement.upper() in filter):
                    continue

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
