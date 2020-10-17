import json
import pymongo
import sys


def openJsonConfig():
    try:
        with open('config.json') as json_file:
            conf = json.load(json_file)
    except:
        print('\033[0;31m' + 'error: ' + '\033[0m' + 'config.json file can\'t be opened')
        sys.exit(2)

    return conf


def getCollection(db_ip, db_name, db_collection):
    client = pymongo.MongoClient(db_ip)
    col = client[db_name][db_collection]
    return col


def submitQuery(collection, query):
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
