import sys
import random
import datetime
import json
import pymongo
import logging
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom

log_format = '%(levelname)s: %(message)s'
logging.basicConfig(format=log_format)

def openJsonConfig():
    """
    Opens the 'config.json' file and loads it into memory

    :return: JSON config file
    """
    try:
        with open('config.json') as json_file:
            conf = json.load(json_file)
    except:
        print('\033[0;31m' + 'error: ' + '\033[0m' + 'config.json file can\'t be opened')
        sys.exit(2)

    return conf


def getCollection(db_ip, db_name, db_collection):
    """
    Connects to the specified MongoDB database collection and provides
    a MongoDB collection object which can be used to fetch data from
    the database.

    :param db_ip: Database IP
    :param db_name: Database name
    :param db_collection: Database collection
    :return: MongoDB collection object
    """
    client = pymongo.MongoClient(db_ip)
    col = client[db_name][db_collection]

    return col


def selectDifficulty(questions, difficulty):
    """
    Iterates through an array of questions and keeps only the ones
    that are matching the specified difficulty.

    :param questions: array of questions stored in JSON
    :param difficulty: a number from 1 to 3
    :return: filtered array of questions stored in JSON
    """
    response = []
    for itr in questions:
        if itr["difficulty"] == difficulty:
            response.append(itr)

    return response


def submitQuery(collection, query):
    """
    Sends a query to the MongoDB database collection and gets
    the matching elements out of it.

    :param collection: MongoDB collection object
    :param query: MongoDB find query
    :return: Array of elements which satisfy the given query
    """
    response = []
    cursor = collection.find(query)
    for document in cursor:
        response.append(document)

    return response


def selectTags(questions, tags):
    """
    Iterates through an array of questions and returns only those that
    match at least one required tag.

    :param questions: Array of questions stored in json
    :param tags: List of required tags for the selected questions
    :return: Array of questions filtered on required tags
    """
    response = []
    for itr in questions:
        if any(item in itr["tags"] for item in tags):
            response.append(itr)

    return response


def selectQuestions(questions, size, max_size):
    """
    Takes an array of questions, sorts them according to the creation
    date and returns a random selection of 'size' questions from a
    pool created with the first 'max_size' sorted questions.

    :param questions: Array of questions stored in JSON
    :param size: Number of returned questions
    :param max_size: Size of the random-selection pool
    :return: Filtered array of questions stored in JSON
    """

    pool = sorted(questions, key=lambda question: question["createdOn"], reverse=True)

    if max_size < len(pool):
        selection = random.sample(pool[0:max_size], size)
    else:
        if size < len(pool):
            selection = random.sample(pool, size)
        else:
            selection = pool

    return selection

def selectYear(questions, year):
    """
    Iterates through an array of questions and returns a list of
    questions that have been last used in the specified year.

    :param questions: Array of questions stored in JSON
    :param year: A number that indicates the year to be filtered
    :return: Filtered array of questions stored in JSON
    """
    response = []
    for itr in questions:
        if itr["lastUsed"].year == year:
            response.append(itr)
    return response

def generateQuiz(questions, quiz_settings):
    """
    Using the quiz settings from the configuration file, selects
    the questions according to difficulty and topics, trying to
    use questions that were never used, or that were used a long time
    ago.

    :param questions: Array of questions stored in JSON
    :param quiz_settings: Dictionary that describes the quiz
    :return: Array of questions stored in JSON, representing the generated quiz
    """
    quiz = []
    difficulties = ['easy', 'medium', 'hard']
    now = datetime.datetime.now()
    current_year = now.year

    for difficulty in difficulties:
        difficulty_pool = selectDifficulty(questions, difficulties.index(difficulty) + 1)
        required_questions = quiz_settings[difficulty]

        for year in range(1970, current_year + 1):
            # the range should include the current year, that's why I added 1
            year_pool = selectYear(difficulty_pool, year)
            tags_pool = selectTags(year_pool, quiz_settings['chapters'])
            selection = selectQuestions(tags_pool, required_questions, quiz_settings['questions'])

            required_questions = required_questions - len(selection)
            quiz = quiz + selection
            """
                When we reach the required number of questions with a certain difficulty,
                we move on to the next level of difficulty.
            """
            if required_questions == 0:
                break

    return quiz

def json2mXML(jsonQuestion, quiz):
    """
    Generates the Moodle XML entry for the given question

    :param jsonQuestion: a question stored in JSON
    :param quiz: the quiz to which the question is added
    :return: the question stored in mXML
    """
    # creating the hierarchy
    question = ElementTree.SubElement(quiz, 'question')
    questionText = ElementTree.SubElement(question, 'questionText')
    tags = ElementTree.SubElement(question, 'tags')  
    questionTextText = ElementTree.SubElement(questionText, 'text')
    question.set('type', 'multichoice')
    questionText.set('format', 'html')
    questionTextText.text = jsonQuestion['statement']
    
    # adding the difficulty tag
    tag = ElementTree.SubElement(tags, 'tag')
    tagText = ElementTree.SubElement(tag, 'text')
    tagText.text = 'Dificulty=' + str(jsonQuestion['difficulty'])

    # adding other tags
    for jsonTag in jsonQuestion['tags']:
        if jsonTag['key']:
            tag = ElementTree.SubElement(tags, 'tag')
            tagText = ElementTree.SubElement(tag, 'text')
            tagText.text = jsonTag['key'] + ":" + ','.join(jsonTag['values'])

    # adding the answers in the file
    for jsonAnswer in jsonQuestion['answers']:
        answer = ElementTree.SubElement(question, 'answer')
        answerText = ElementTree.SubElement(answer, 'text')
        answerText.text = jsonAnswer['statement']
        answer.set('fraction', str(jsonAnswer['grade']))

    return quiz


if __name__ == '__main__':
    config = openJsonConfig()
    quiz_settings = config['quiz-settings']
    db_settings = config['database-settings']

    try:
        question_collection = \
            getCollection(db_settings['database-ip'], db_settings['database-name'],
                          db_settings['question-collection'])
    except:
        logging.error('Connection to question-collection failed. Check database settings.')
        sys.exit(2)
    try:
        quiz_collection = \
            getCollection(db_settings['database-ip'], db_settings['database-name'],
                          db_settings['quiz-collection'])
    except:
        logging.error('Connection to quiz-collection failed. Check database settings.')
        sys.exit(2)

    questions = submitQuery(question_collection, {})

    quiz = generateQuiz(questions, quiz_settings)

    # Save question IDs into a quiz document which is inserted into quiz database
    if db_settings['updateQuizCollection'] and len(quiz) > 0:
        quizDoc = {}

        quizIDs = []
        for question in quiz:
            quizIDs.append(question['_id'])

            # Update lastUsed field for every question in the generated quiz
            question_collection.update_one({"_id": question['_id']}, { "$set": {"lastUsed": datetime.datetime.now()} })

        quizDoc.update({"quizIDs": quizIDs})
        quizDoc.update({"generatedOn": datetime.datetime.now()})
        quiz_collection.insert_one(quizDoc)

    quizMXML = ElementTree.Element('quiz')

    for question in quiz:
        quizMXML = json2mXML(question, quizMXML)

    roughXML = ElementTree.tostring(quizMXML)
    reparsed = minidom.parseString(roughXML)
    prettyXML = reparsed.toprettyxml(indent="  ")

    # makes a strin with current date and time
    now = datetime.datetime.now()
    strTime = now.strftime("%d%m%Y_%H%M%S")

    # filename pattern: "Quiz_DDMMYYYY_HHMMSS.xml"
    filename = "Quiz_" + strTime + ".xml"

    moodleXMLFile = open(filename, "w")
    moodleXMLFile.write(prettyXML)
