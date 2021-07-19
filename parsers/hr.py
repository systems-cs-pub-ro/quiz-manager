import json
import re


def json_to_hr(json_obj: str) -> str:
    json_q = json.loads(json_obj)

    # Adding Tagline
    hr = ""
    hr += "createdOn" + ":" + json_q["createdOn"] + ";"
    hr += "lastUsed" + ":" + json_q["lastUsed"] + ";"
    hr += "difficulty" + ":" + str(json_q["difficulty"]) + ";"
    for tag in json_q["tags"]:
        hr += tag["key"] + ":"
        for item in tag["values"]:
            hr += item + ","
        hr = hr[:-1] + ";"
    hr += "\n"

    # Adding Statement
    hr += json_q["statement"]

    # Adding Answers
    for answer in json_q["answers"]:
        stmt = answer["statement"]
        correct = "+" if answer["correct"] else "-"
        hr += correct + " " + stmt
    return hr

def from_hr(hr: str) -> str:
    '''
    Generate a single JSON object from a question in HR format

    hr - parameter of type str, contains a single question in HR format 
    return - JSON object as string
    '''
    # Copy object to prevent side effects in caller
    hr_copy = str(hr).rstrip()

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

    # Assign tags
    partition = hr_copy.partition("\n")
    for tag in partition[0].split(";"):
        splitTags = tag.split(":")
        if(len(splitTags) < 2):
            break
        key = splitTags[0]
        value = splitTags[1]

        # If the key has been declared in template
        if(key in question.keys()):
            question[key] = value
        else:
            misc_tag = dict()
            misc_tag[key] = value.split(",")
            question["tags"].append(misc_tag)

    # Get question statement
    # Find where the answer section starts
    answers_index = min(partition[2].find("+"), partition[2].find("-"))
    statement = partition[2][:answers_index]
    question["statement"] = statement

    # Assign Answers
    answer_list = re.split(r"\n", partition[2][answers_index:])
    # Get number of correct answers to compute grade awarded for each
    # correct answer
    question["correctAnswersNo"] = len(
        [ans for ans in answer_list if ans[0] == "+"])

    # Preliminary pass through answer list to concatenate multiline answers
    for i in range(1, len(answer_list)):
        if answer_list[i][0] != "+" and answer_list[i][0] != "-":
            answer_list[i - 1] += "\n" + answer_list[i]
            continue

    # Remove continuations of multiline answers from list
    answer_list = [answer for answer in answer_list if not (
        answer[0] != "+" and answer[0] != "-")]

    grade = 1 / (question["correctAnswersNo"] * 1.0)

    # Add answers to answer list in JSON object
    for answer in answer_list:
        if(answer[0] == "+"):
            question["answers"].append(
                {
                    "statement": answer[2:] + "\n",
                    "correct": True,
                    "grade": grade
                }
            )
        elif(answer[0] == "-"):
            question["answers"].append(
                {
                    "statement": answer[2:] + "\n",
                    "correct": False,
                    "grade": -0.5
                }
            )

    return json.dumps(question, indent=4)
