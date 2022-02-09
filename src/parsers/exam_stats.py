"""
    Module that handles parsing exam statistics from csv to json
"""

import csv
from io import StringIO

"""
Utility function that can find certain headers for answer csv tables
:param input: entire input file
:param offset: where to start search
:return: index of next header
"""


def find_ans_header(input: str, offset=0):
    fst_str = "\"Model de răspuns\",\"Credit parțial\",Count,Frecvență"
    snd_str = "\"Parte a întrebării\",Răspuns,\"Credit parțial\",Count,Frecvență"
    fst_idx = input.find(fst_str, offset)
    snd_idx = input.find(snd_str, offset)
    idx = 0

    if fst_idx == -1:
        return snd_idx
    if snd_idx == -1:
        return fst_idx

    if fst_idx >= snd_idx:
        idx = snd_idx
    else:
        idx = fst_idx

    return idx


"""
Parser that returns a dictionary containining statistics about exam given as
input
:param input_file: statistics file of exam
:return: dictionary containing exam statistics
"""


def exam_parser(input_file: str):
    exam = {}
    csvfile = open(input_file, newline='')
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        exam["exam_name"] = row["\ufeff\"Numele chestionarului\""]
        exam["course_name"] = row["Nume curs"]
        exam["opened_at"] = row["Deschide testul"]
        exam["closed_at"] = row["Închide testul"]
        exam["total_attempts"] = row["Number of complete graded first attempts"]
        exam["average_grade"] = row["Average grade of last attempts"]
        exam["median_grade"] = row["Median grade (for highest graded attempt)"]
        exam["score_dist_skew"] = row["Score distribution skewness (for highest graded attempt)"]
        exam["score_dist_kurt"] = row["Score distribution kurtosis (for highest graded attempt)"]
        exam["internal_consistency_coeficient"] = row[
            "Coeficientul de consistență internă (for highest graded attempt)"]
        exam["error_ratio"] = row["Error ratio (for highest graded attempt)"]
        exam["error_standard"] = row["Eroare standard (pentru highest graded attempt)"]
        exam["questions"] = []
        break
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    num_questions = 0
    for row in reader:
        num_questions += 1
        break_flag = False
        for name in reader.fieldnames:
            if name == "Q#":
                try:
                    int(row[name])
                except:
                    break_flag = True
            if break_flag:
                break
            exam["questions"].append({
                "question_name": row["Numele întrebării"],
                "attempts": row["Încercări"],
                "facility_index": row["Facility index"],
                "standard_deviation": row["Deviație standard"],
                "random_guess_score": row["Random guess score"],
                "intended_weight": row["Intended weight"],
                "effective_weight": row["Effective weight"],
                "discrimination_index": row["Discrimination index"],
                "discrimination_efficency": row["Discriminative efficiency"],
                "answers": []
            })

        if break_flag:
            break

    # Answers
    csvfile.close()
    all_file = open(
        input_file, newline='').read()

    next_index = 0
    question_num = 0
    while(1):
        index = find_ans_header(all_file, next_index)
        next_index = find_ans_header(all_file, index + 1) - 1

        # Get slice containing only answers
        answers_csv = all_file[index:next_index]

        if(len(answers_csv) == 0):
            break

        reader = csv.DictReader(StringIO(answers_csv),
                                delimiter=',', quotechar='"')
        for row in reader:

            anstext = "Răspuns"
            if "Model de răspuns" in row.keys():
                anstext = "Model de răspuns"

            exam["questions"][question_num]["answers"].append({
                "answer_text": row[anstext],
                "partial_credit": row["Credit parțial"],
                "count": row["Count"],
                "frequency": row["Frecvență"]
            })
        question_num += 1
    return exam
