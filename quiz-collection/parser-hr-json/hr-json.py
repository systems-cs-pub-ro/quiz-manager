import json
import sys

def main(argv):

    # In lista quiz se vor stoca toate intrebarile
    quiz = list()

    #continue only if both input and output file names were provided
    if len(argv) >= 2 :
        inputFile = argv[0]
        outputFile = argv[1]
    else :
        print("Missing output or input file names")
        sys.exit(0)

    #open input file
    try:
        iFileHandle = open(inputFile, "r")
    except:
        print("File not found!")
        sys.exit(0)

    line = iFileHandle.readline()

    while line:

        #initializare dictionar pentru intrebare
        question = {
        "year":"n/a",
        "last_used":"n/a",
        "difficulty":"n/a",
        "course":"n/a",
        "author":"n/a",
        "review":"n/a",
        "statement":"n/a",
        "answers":[],
        "answer_count":0,
        "correct_ans":[]
        }

        # Tag-urile Intrebarii
        tags = line.replace(':', ',')
        tags = tags.split(',')

        for i in range(0, len(tags), 2):
            question[tags[i]] = tags[i + 1] 
        
        # Enuntul Intrebarii
        question["statement"] = iFileHandle.readline().strip()
        
        # Raspunsurile Intrebarii
        line = iFileHandle.readline()
        while line != "\n":
            question["answers"].append(line.rstrip())
            # Raspunsurile sunt indexate incepand de la numarul 1!
            question["answer_count"] = question["answer_count"] + 1

            # Se retin doar indecsii fiecarui raspuns corect
            if line[0] == '+':
                question["correct_ans"].append(question["answer_count"])
            
            line = iFileHandle.readline()

        # Se adauga intreabarea prelucrata la lista de intrebari
        quiz.append(question)

        # Se incepe prelucrarea urmatoarei intrebari/se ajunge la finalul fisierului de input
        line = iFileHandle.readline()


    # Generare document JSON din lista de intrebari
    with open(outputFile, 'w', encoding='utf8') as json_file:
        json.dump(quiz, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
