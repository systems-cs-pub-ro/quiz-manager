import json
import sys
import getopt
import xml.etree.ElementTree as ET
import unicodedata
import re
from topicDict import topicDict, topicList


# Used for better comparison of dict words vs statement words
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    # unicode is a default on python 3
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")

    return str(text)


def readQuestion(line, file_handle):
    question = {"tagline": "", "statement": "", "answers": []}

    # Reading question tagline
    question["tagline"] = line

    # Reading question statement
    line = file_handle.readline()
    while(1):
        pos = file_handle.tell()
        question["statement"] += line
        line = file_handle.readline()
        if(line[0] == "+" or line[0] == "-"):
            # Revert file pointer so first answer is not lost
            file_handle.seek(pos)
            break

    # Reading answers
    line = file_handle.readline()
    while(ord(line[0]) != 10):
        if line[0] == '+' or line[0] == '-':
            question["answers"].append(line)
        line = file_handle.readline()
        if len(line) == 0:
            break

    return question


# Remove unwanted characters impending keyword finding
def filter(bin):
    for i in range(len(bin)):
        bin[i] = bin[i].replace("/", " ")
        bin[i] = bin[i].replace("?", " ")
        bin[i] = bin[i].replace(",", " ")
        bin[i] = bin[i].replace("(", " ")
        bin[i] = bin[i].replace(")", " ")
        bin[i] = bin[i].replace("</pre>", " ")
        bin[i] = bin[i].replace("<p>", " ")
        bin[i] = bin[i].replace("</p>", " ")
        bin[i] = bin[i].replace("<br>", " ")
        bin[i] = bin[i].replace("</br>", " ")
        bin[i] = bin[i].replace("\"", " ")
        bin[i] = bin[i].replace("-", " ")


def main(argv):
    input_file = ''
    output_file = ''
# Parse the arguments given to the script
    try:
        opts, _ = getopt.getopt(argv, "i:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    outfile = open(output_file, "w")

# Opening input file
    try:
        file_handle = open(input_file, "r")
    except file_handle is None:
        sys.exit(0)

# Read questions and add them to a word bin
    line = file_handle.readline()
    while(line):
        question = readQuestion(line, file_handle)
        line = file_handle.readline()

        bin = strip_accents(question["statement"]) + " "

        negatedFlag = "+"
        if(bin.find("NU") >= 0):
            negatedFlag = "-"

        for ans in question["answers"]:
            if ans[0] == negatedFlag:
                bin += " " + ans[1:]

        bin = bin.rstrip().lower().split()
        filter(bin)

        topicCount = dict()
        topicCount = topicCount.fromkeys(topicList)

        occurences = 0
        for topic in topicList:
            for value in topicDict[topic]:
                value = strip_accents(value).lower()
                if(value in bin):
                    if(topicCount[topic] is None):
                        topicCount[topic] = 1
                    else:
                        topicCount[topic] += 1
                    occurences += 1

        topicTag = ""
        for topic in topicCount:
            if (topicCount[topic] is not None):
                topicTag += topic + ","

        newTag = "topics:" + topicTag[:-1]
        if(len(topicTag) == 0):
            newTag = "topics:n/a"
        question["tagline"] = re.sub("topics:[a-zA-Z,/_]*",newTag,question["tagline"])
        question["tagline"] = question["tagline"][:-1]
        outfile.write(question["tagline"] + "\n")
        outfile.write(question["statement"])
        for ans in question["answers"]:
            outfile.write(ans)
        outfile.write("\n")


if __name__ == "__main__":
    main(sys.argv[1:])
