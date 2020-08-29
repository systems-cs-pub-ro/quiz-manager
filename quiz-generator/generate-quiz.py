import json
import pymongo
import sys


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


if __name__ == '__main__':
    config = openJsonConfig()
    quiz_settings = config['quiz-settings']
    db_settings = config['database-settings']

    try:
        question_collection = \
            getCollection(db_settings['database-ip'], db_settings['database-name'], db_settings['question-collection'])
    except:
        print('\033[0;31m' + 'error: ' + '\033[0m' + 'Connection to question-collection failed. Check database settings.')
    try:
        test_collection = \
            getCollection(db_settings['database-ip'], db_settings['database-name'], db_settings['test-collection'])
    except:
        print('\033[0;31m' + 'error: ' + '\033[0m' + 'Connection to test-collection failed. Check database settings.')
