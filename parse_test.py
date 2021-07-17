import json
from xml.dom import minidom
import parsing.hr as hr
import parsing.mxml as mxml
import xml.etree.ElementTree as ElementTree

hr_file = open("./test_inputs/hr_test_input.hr")
mxml_file = open("./test_inputs/mxml_test_input.hr.xml")

# Testing HR > JSON
hr_question = hr_file.read().split("\n\n")
for hr_elem in hr_question:
    print("\nHR > JSON TEST", "\n")
    print(hr.from_hr(hr_elem))

# Testing MXML > JSON
mxml_str = mxml_file.read()
mxml_question = ElementTree.fromstring(mxml_str)
json_mxml_arr = []
for mxml_elem in mxml_question:
    if mxml_elem.tag == "question":
        json_mxml_arr.append(mxml.from_mxml(mxml_elem))

print("\nMXML > JSON TEST", "\n", json_mxml_arr[0])
# Testing JSON > HR
res = hr.to_hr(json_mxml_arr[0])
print("\nJSON > HR TEST")
print(res)

# Testing JSON > MXML
quizMXML = ElementTree.Element('quiz')
res = mxml.to_mxml(json_mxml_arr[0], quizMXML)

# Pretty formatting
roughXML = ElementTree.tostring(quizMXML)
reparsed = minidom.parseString(roughXML)
prettyXML = reparsed.toprettyxml()
print("\nJSON > MXML TEST", "\n")
print(prettyXML)