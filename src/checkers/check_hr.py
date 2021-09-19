import re
import sys
import logging

topics = ["shell", "Topic1", "Topic2", "Topic3"]

def print_error(filename: str, line_idx: int, error_msg: str):
    logger = logging.getLogger("checker")
    logger.setLevel(logging.ERROR)
    logger.error(filename + ", line " + str(line_idx) + error_msg)


def check_common(filename: str, file: int) -> int:
    return_value = 0
    line_idx = 0

    # Check metadata line
    line = file.readline()
    line_idx += 1
    date_match = "created-on:[0-9]{4}-[0-9]{2}-[0-9]{2};"
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


def check_specific(filename: str, file: int) -> int:
    return_value = 0
    line_idx = 0

    # Get metadata line
    line = file.readline()
    line_idx += 1

    # Check difficulty range
    metadata = line.split(";")
    difficulty = int(metadata[1].split(":")[1])
    if (difficulty < 1  or difficulty > 3):
        print_error(filename, line_idx, ": Difficulty doesn't fit in configured range!\n") 
        return_value = 1
    
    # Check topic validity
    topic = metadata[2].split(":")[1]
    if (not topic in topics):
        print_error(filename, line_idx, ": Invalid topic!\n")

    # Go to answers section
    while "+-".find(line[0]) == -1:
        line_idx += 1
        line = file.readline()
    
    # Check correct / total answers ratio
    correct_answers = 0
    wrong_answers = 0
    while (line != "\n"):
        if line[0] == "+":
            correct_answers += 1
        elif line[0] == "-":
            wrong_answers += 1
        line_idx += 1
        line = file.readline()
    if (
            (correct_answers == 1 and (correct_answers + wrong_answers) != 4) or
            (correct_answers == 2 and (correct_answers + wrong_answers) != 5) or
            (correct_answers == 3 and (correct_answers + wrong_answers) != 7)
        ):
        print_error(filename, line_idx, ": Wrong correct / wrong answers ratio at the question above!\n")
    else:
        print_error(filename, line_idx, ": Wrong answers number at the question above!\n")
 
    return return_value


def checker_menu(filename: str):
    with open(sys.argv[1]) as hr_fd:
        check_common(sys.argv[1], hr_fd)


if __name__ == "__main__":
    with open(sys.argv[1]) as hr_fd:
        check_common(sys.argv[1], hr_fd)
    with open(sys.argv[1]) as hr_fd:
        check_specific(sys.argv[1], hr_fd)
