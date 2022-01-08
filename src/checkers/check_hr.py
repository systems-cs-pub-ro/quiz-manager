import re
import sys
import logging
import configparser


difficulty_range = []
topics = []
answers_options = {}


def print_error(filename: str, line_idx: int, error_msg: str):
    """
        Default error printer
    """

    logger = logging.getLogger("checker")
    logger.setLevel(logging.ERROR)
    logger.error(filename + ", line " + str(line_idx) + error_msg)


def read_config(config_filename: str):
    """
        Function that reads the configurable options used when
        running the specific check.
    """

    config = configparser.ConfigParser()
    config.sections()
    if config_filename != None:
        config.read(config_filename)
    else:
        config.read("config/checker.conf")

    for topic in config["configuration"]["topics"].split(","):
        topics.append(topic)

    difficulty_strings = config["configuration"]["difficulty"].split("-")
    difficulty_range.append(int(difficulty_strings[0]))
    difficulty_range.append(int(difficulty_strings[1]))

    answers_strings = config["configuration"]["answers"].split("),")
    for answer_string in answers_strings:
        answer_string = answer_string.replace("(", "")
        answer_string = answer_string.replace(")", "")
        answer_string = answer_string.replace(",", "")
        option = answer_string.split(" ")
        answers_options[int(option[0])] = int(option[1])


def check_common(filename: str, file: int) -> int:
    """
        Common questions check implementation.
    """

    return_value = 0
    line_idx = 0

    # Check metadata line
    line = file.readline()
    line_idx += 1
    date_match = "created_on:[0-9]{4}-[0-9]{2}-[0-9]{2};"
    difficulty_match = "difficulty:[0-9]+;"
    text_match = "[-a-zA-Z0-9_]+"
    topic_match = "topic:" + text_match + ";"
    tags_match = "(tags:(" + text_match + ",)*" + text_match + ";)*"
    if not re.match(date_match + difficulty_match + topic_match + tags_match + "$", line):
        print_error(filename, line_idx, ": Wrong format in metadata line!\n")
        return_value = 1

    # Check if question statement exists
    line_idx += 1
    line = file.readline()
    if "+-".find(line[0]) != -1:
        print_error(filename, line_idx, ": Missing question statement!\n")
        return_value = 1
    while "+-".find(line[0]) == -1:
        line_idx += 1
        line = file.readline()

    # Check answers syntax
    while line != "\n":
        if "+-".find(line[0]) != -1:
            if line[1] != " ":
                print_error(filename, line_idx, ": Missing space between +/- and text!\n")
                return_value = 1
        line = file.readline()

    return return_value


def check_specific(filename: str, file: int, config_filename: str) -> int:
    """
        Specific questions check implementation.
    """

    return_value = 0
    line_idx = 0

    # Get specifications to check from configuration file
    read_config(config_filename)

    # Get metadata line
    line = file.readline()
    line_idx += 1

    # Check difficulty range
    metadata = line.split(";")
    difficulty = int(metadata[1].split(":")[1])
    if (difficulty < difficulty_range[0]  or difficulty > difficulty_range[1]):
        print_error(filename, line_idx, ": Difficulty doesn't fit in the configured range!\n")
        return_value = 1

    # Check topic validity
    topic = metadata[2].split(":")[1]
    if not topic in topics:
        print_error(filename, line_idx, ": Invalid topic!\n")

    # Go to answers section
    while "+-".find(line[0]) == -1:
        line_idx += 1
        line = file.readline()

    # Check correct / total answers ratio
    correct_answers = 0
    wrong_answers = 0
    while line != "\n":
        if line[0] == "+":
            correct_answers += 1
        elif line[0] == "-":
            wrong_answers += 1
        line_idx += 1
        line = file.readline()

    answers_number_ok = False
    answers_ratio_ok = False
    for total_answers in answers_options.items():
        if (correct_answers + wrong_answers) == total_answers:
            answers_number_ok = True
            if correct_answers == answers_options[total_answers]:
                answers_ratio_ok = True
            break

    if not answers_number_ok:
        print_error(filename, line_idx, ": Wrong answers number at the question above!\n")
    elif not answers_ratio_ok:
        print_error(filename, line_idx,
                ": Wrong correct / wrong answers ratio at the question above!\n")

    return return_value


if __name__ == "__main__":
    with open(sys.argv[1]) as hr_fd:
        check_common(sys.argv[1], hr_fd)
    with open(sys.argv[1]) as hr_fd:
        check_specific(sys.argv[1], hr_fd)
