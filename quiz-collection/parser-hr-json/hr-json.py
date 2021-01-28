import json
import sys
import getopt


# Utility function for casting types of tags
def cast(variable, type):
    if type is str:
        return str(variable)
    elif type is bool:
        return bool(variable)
    elif type is int:
        return int(variable)
    elif type is float:
        return float(variable)
    elif type is list:
        return list(variable.split(','))

    return variable


# Returns a list of "key" : value pairs
def getTagList(line, question):
    tags = list()
    pairs = line.split(';')

    for pair in pairs:
        key = pair.split(':')[0]

        # Check if end of tagline was reached ('\n')
        if ord(key[0]) == 10:
            continue
        
        value = pair.split(':',1)[1].rstrip()

        if(key == "createdOn" or key == "lastUsed"):
            value += "T00:00:00"
        
# Convert value from string to appropiate type (found in structure.json)
# Else generate a list and append it to "tags"
        if question.get(key) is not None:
            value = cast(value, type(question[key]))
        else:
            value = cast(value, list)

        tags.append({key: value})

    return tags


# Will assign each tag to the question dict
# If tag key is not found in dict keys it will be assigned to "tags" by default
def tagAssign(question, tags):
    for i in range(len(tags)):
        key = next(iter(tags[i]))
        if question.get(key) is None:
            question["tags"].append({"key":key , "values":tags[i].get(key)})
        else:
            question[key] = tags[i][key]


# Generate an answer list that will later be assigned to the question
def getAnswers(file_handle, question):
    line = file_handle.readline()

    # Popping empty answer copied from structure file
    new_answer = question["answers"].pop(0)
    answer_list = list()
    correctAnswersNo = 0
    # Looping through all the answers
    while(line != '\n'):

        # Check for end of file
        if(line == ""):
            break
        
        # Read an answer's statement until meeting another answer
        # Or until meeting a line which contains only \n'
        while(line[0] != "+" and line[0] != "-"):
            new_answer["statement"] += line
            print(new_answer["statement"])
            pos = file_handle.tell()
            line = file_handle.readline()
            if(line == "\n"):
                file_handle.seek(pos)
                break
            
        # Initialising a new answer to be added to the answer list
        new_answer = dict(new_answer)
        
        if(line != "\n"):
            new_answer["statement"] = line[2:]
            if line[0] == '+':
                new_answer["correct"] = True
                correctAnswersNo += 1
            else:
                new_answer["correct"] = False
                new_answer["grade"] = -0.5

            answer_list.append(new_answer)
        line = file_handle.readline()

            

# After the number of correct answers is known
# a grade can be assigned to each correct answer
    for answer in answer_list:
        if answer["correct"] is True:
            answer["grade"] = 1/correctAnswersNo

    question["answers"] = answer_list
    question["correctAnswersNo"] = correctAnswersNo


# Generate the JSON file using a list of questions
def gen_JSON(output_file, quiz):
    with open(output_file, 'w', encoding='utf8') as json_file:
        json.dump(quiz, json_file, ensure_ascii=False, indent=4)


def main(argv):
    # All questions will be stored in this list
    quiz = list()

    # Check if input file exists and import it
    infile_name = ''
    outfile_name = ''

    try:
        opts, _ = getopt.getopt(argv, "i:o:")
    except getopt.GetoptError:
        print('Bad arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i"):
            infile_name = arg
        elif opt in ("-o"):
            outfile_name = arg

    outfile = open(outfile_name, "w")

    try:
        file_handle = open(infile_name, "r")
    except FileNotFoundError:
        print("No Human Readable Format Question \
File has been inputted/found")
        sys.exit(0)

    line = file_handle.readline()
    # Read all questions and stop at EOF
    while line:
        # new_question that will be added to the question list
        # default template loaded
        new_question = {
            "createdOn": "",
            "lastUsed": "",
            "difficulty": 0,

            "statement": "",
            "tags" : [
            ],
            "answers": [
                {
                    "statement": "",
                    "correct": False,
                    "grade": 0.0
                }
            ],
            "correctAnswersNo": 0
        }

        # Read the question's tag line
        tags = getTagList(line, new_question)

        # Add all tags to question
        tagAssign(new_question, tags)

        # Reading question statement
        line = file_handle.readline()
        while(1):
            pos = file_handle.tell()
            new_question["statement"] += line
            line = file_handle.readline()
            if(line[0] == "+" or line[0] == "-"):
                # Revert file pointer so first answer is not lost
                file_handle.seek(pos)
                break

        # Reading answers
        getAnswers(file_handle, new_question)
        quiz.append(new_question)
        line = file_handle.readline()

    # Generate JSON file
    gen_JSON(outfile_name, quiz)


if __name__ == "__main__":
    main(sys.argv[1:])
