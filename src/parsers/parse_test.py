from xml.dom import minidom
import hr
import mxml
import xml.etree.ElementTree as ElementTree

hr_file = open("./test_inputs/hr_test_input.hr")
hr_file_content = hr_file.read()

converted_hr_to_json = hr.quiz_hr_to_json(hr_file_content)
for conv in converted_hr_to_json:
    print(conv)

converted_json_to_hr = hr.quiz_json_to_hr(converted_hr_to_json)
for conv in converted_json_to_hr:
    print(conv)

mxml_file = open("./test_inputs/mxml_test_input.xml")
mxml_file_content = mxml_file.read()

converted_json_to_mxml = mxml.quiz_json_to_mxml(converted_hr_to_json)

print(converted_json_to_mxml)

converted_mxml_to_json = mxml.quiz_mxml_to_json(mxml_file_content)
for conv in converted_mxml_to_json:
    print(conv)
