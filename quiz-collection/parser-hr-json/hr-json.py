import json
import sys

# UTILITY FUNCTION TO CAST VALUES WHEN PROCESSING TAGS
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

# Load the Structure file (needed to determine types of tags) 
def loadStructure():
    try:
        structure = open("./structure.json", "r")
    except:
        print("Structure file not found!")
        sys.exit(0)

    return json.load(structure)

# Returns a list of "key" : value pairs
def getTagList(line, question):
    tags = list()
    pairs = line.split(';')

    for pair in pairs: 
        key = pair.split(':')[0]

        # Check if end of tagline was reached ('\n')
        if(ord(key[0]) is 10) : continue

        value = pair.split(':')[1].rstrip()
        # Convert value from string to appropiate type (found in structure.json) 
        # Else generate a list and append it to the "tags"
        if question.get(key) is not None:
            value = cast(value, type(question[key]))
        else:
            value = cast(value, list)
            # First value will be the tag name to avoid any confusion
            value.insert(0, key)

        tags.append({key:value})

    return tags

def tagAssign(question, tags) : 

    # Will assign each tag to the question dict
    # If tag key is not found in dict keys it will be assigned to "tags" by default
    for i in range(len(tags)):
        key = next(iter(tags[i]))

        if question.get(key) == None:
            question["tags"].append(tags[i][key])
        else :
            question[key] = tags[i][key]

def getAnswers(iFileHandle, question):

    line = iFileHandle.readline()
    newAnswer = question["answers"].pop(0)

    # Generate an answer list that will later be assigned to the question
    answerList = list()
    correctAnswersNo = 0

    # Looping through all the answers
    while(line != '\n'):
        # Initialising a new answer to be added to the answer list
        newAnswer = dict(newAnswer)

        newAnswer["statement"] = line[2:].rstrip()
        if line[0] == '+' : 
            newAnswer["correct"] = True
            correctAnswersNo += 1
        else : 
            newAnswer["correct"] = False
            newAnswer["grade"] = -0.5
        
        answerList.append(newAnswer)
        line = iFileHandle.readline()

    # After the number of correct answers is known, a grade can be assigned to each correct answer
    for answer in answerList:
        if answer["correct"] is True : answer["grade"] = 1/correctAnswersNo

    question["answers"].append(answerList)
    question["correctAnswersNo"] = correctAnswersNo

def genJSON(outputFile, quiz):
    # Generare document JSON din lista de intrebari
    with open(outputFile, 'w', encoding='utf8') as json_file:
        json.dump(quiz, json_file, ensure_ascii=False, indent=4)

def main(argv):

    # All questions will be stored in this list
    quiz = list()
    # Saving template
    
    # CHECK IF INPUT FILE EXISTS AND OPEN INPUT FILE
    inputFile = argv[0]
    try:
        iFileHandle = open(inputFile, "r")
    except:
        print("No Human Readable Format Question File has been inputted/found - use 'python3 hr-json.py input_file'")
        sys.exit(0)


    line = iFileHandle.readline()
    # Read all questions and stop at EOF
    while line :
        # newQuestion that will be added to the question list
        # default template loaded
        newQuestion = loadStructure()
        
        # Read the question's tag line
        tags = getTagList(line,newQuestion)

        # ADD ALL TAGS TO QUESTION
        tagAssign(newQuestion,tags)
        
        # READING QUESTION STATEMENT UNTIL + or - IS FOUND
        line = iFileHandle.readline()
        while(1):
            pos = iFileHandle.tell()
            newQuestion["statement"] += line
            line = iFileHandle.readline()
            if(line[0] == "+" or line[0] == "-"):
                #REVERT FILE POINTER SO FIRST ANSWER IS NOT LOST
                iFileHandle.seek(pos)
                break

        # READING ANSWERS 
        getAnswers(iFileHandle, newQuestion)
        quiz.append(newQuestion)
        line = iFileHandle.readline()


    # Generate JSON file
    genJSON("./json_output/output.json", quiz)

if __name__ == "__main__":
    main(sys.argv[1:])
