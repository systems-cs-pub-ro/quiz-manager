import sys
import random
import datetime
import json
import pymongo


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


def selectQuestions(questions, size, maxSize):
    """
    Takes an array of questions, sorts them according to the creation
    date and returns a random selection of 'size' questions from a
    pool created with the first 'maxSize' sorted questions.

    :param questions: Array of questions stored in JSON
    :param size: Number of returned questions
    :param maxSize: Size of the random-selection pool
    :return: Filtered array of questions stored in JSON
    """
    pool = []
    selection = []

    pool = sorted(questions, key=lambda question: question["createdOn"], reverse=True)

    if maxSize < len(pool):
        selection = random.sample(pool[0:maxSize], size)
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


if __name__ == '__main__':
    config = openJsonConfig()
    quiz_settings = config['quiz-settings']
    db_settings = config['database-settings']

    try:
        question_collection = \
            getCollection(db_settings['database-ip'], db_settings['database-name'],
                          db_settings['question-collection'])
    except:
        print('\033[0;31m' + 'error: ' + '\033[0m' +
              'Connection to question-collection failed. Check database settings.')
    try:
        test_collection = \
            getCollection(db_settings['database-ip'], db_settings['database-name'],
                          db_settings['test-collection'])
    except:
        print('\033[0;31m' + 'error: ' + '\033[0m' +
              'Connection to test-collection failed. Check database settings.')

    questions = submitQuery(question_collection, {})

    quiz = generateQuiz(questions, quiz_settings)

    for question in quiz:
        print(question)
