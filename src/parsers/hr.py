"""
Module that handles parsing HR files and converting them to JSON
"""

import json
import re


def get_meta(question_dict: dict, key: str):
    """
    Get metadata from question_dict
    :param question_dict: dictionary that contains question metadata
    :param key: the key that will be searched in the dictionary
    :return: the value associated with key from question dict
    """
    if not key in question_dict["metadata"]:
        return ""
    if len(question_dict["metadata"][key]) == 1:
        return question_dict["metadata"][key][0]
    return question_dict["metadata"][key]


def quiz_hr_to_json(file_content: str):
    """
    Converts a HR quiz to JSON quiz
    :param file_content: a quiz stored in HR format
    :return: a quiz stored in JSON format
    """
    question_arr = file_content.split("\n\n")
    question_arr_json = list(map(hr_to_json, question_arr))
    return question_arr_json


def quiz_json_to_hr(json_arr: list):
    """
    Converts a JSON quiz to HR quiz
    :param file_content: a quiz stored in JSON format
    :return: a quiz stored in HR format
    """
    return list(map(json_to_hr, json_arr))


def json_to_hr(json_obj: str) -> str:
    """
    Generates a question in HR format from JSON string
    :param json_obj: a question stored in JSON format
    :return: a string representing a question in HR format
    """
    json_q = json.loads(json_obj)
    # Adding Tagline
    hr_q = ""

    for tag in json_q["metadata"]:
        hr_q += tag + ":"
        for item in json_q["metadata"][tag]:
            hr_q += item + ","
        hr_q = hr_q[:-1] + ";"
    hr_q += "\n"

    # Adding Statement
    hr_q += json_q["statement"]

    # Adding Answers
    for answer in json_q["answers"]:
        stmt = answer["statement"]
        correct = "+" if answer["correct"] else "-"
        hr_q += correct + " " + stmt
    return hr_q


def hr_to_json(hr_q: str) -> str:
    """
    Generates a JSON string for the given HR question
    :param hr: a string representing a question in HR format
    :return: string representing a question in JSON format
    """

    # Copy object to prevent side effects in caller
    hr_copy = str(hr_q).rstrip()

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
        "correct_answers_no": 0,
    }

    # Assign tags
    partition = hr_copy.partition("\n")
    for tag in partition[0].split(";"):
        split_tags = tag.split(":")
        if len(split_tags) < 2:
            break
        key = split_tags[0]
        value = split_tags[1]

        # If the key has been declared in template
        if key in question:
            question[key] = value
        else:
            question["metadata"][key] = value.split(",")

    # Get question statement
    # Find where the answer section starts
    answers_index = min(partition[2].find("\n+"), partition[2].find("\n-"))
    statement = partition[2][: answers_index + 1]
    question["statement"] = statement

    # Assign Answers
    answer_list = re.split(r"\n", partition[2][answers_index + 1 :])

    # Get number of correct answers to compute grade awarded for each
    # correct answer
    question["correct_answers_no"] = len([ans for ans in answer_list if ans[0] == "+"])

    # Preliminary pass through answer list to concatenate multiline answers
    for i in range(1, len(answer_list)):
        if answer_list[i][0] != "+" and answer_list[i][0] != "-":
            answer_list[i - 1] += "\n" + answer_list[i]
            continue

    # Remove continuations of multiline answers from list
    answer_list = [
        answer for answer in answer_list if not (answer[0] != "+" and answer[0] != "-")
    ]

    grade = 1 / (question["correct_answers_no"] * 1.0)
    # Add answers to answer list in JSON object
    for answer in answer_list:
        if answer[0] == "+":
            question["answers"].append(
                {"statement": answer[2:] + "\n", "correct": True, "grade": grade}
            )
        elif answer[0] == "-":
            question["answers"].append(
                {"statement": answer[2:] + "\n", "correct": False, "grade": -0.5}
            )

    return json.dumps(question, indent=4)
