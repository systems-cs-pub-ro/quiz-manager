import os
import sys
import json
import pymongo
from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb+srv://%s:%s@%s' % (os.getenv(
        "MONGODB_USERNAME"), os.getenv("MONGODB_PASSWORD"), os.getenv("MONGODB_URL")))
    db = client[os.getenv("MONGODB_DATABASE")]
    questions = db["questions"]

    for file in sys.argv[1:]:
        if (not os.path.isfile(file)):
            print('File %s could not be found' % (file))
            continue
        f = open(file, 'r', encoding="utf-8")
        data = f.read()
        json_data = json.loads(data)
        if type(json_data) is list:
            questions.insert_many(json_data)
        else:
            questions.insert_one(json_data)
