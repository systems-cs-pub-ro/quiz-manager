# Question collection

    Question collector that parses questions given in MXML 
    format to both JSON format and Human Readable format
    
## TODO

`Higher priority but not impending functionality`
- [ ] Update [diagram & description](https://docs.google.com/document/d/1DNxUeg9AO2ejrw2RFQzYi7kO0eiYQOsAQjMJmb_iclo/edit) in USO Google Drive directory

`Mostly things that would be helpful/nice to add but not completely necessary for now`
- [ ] Install script and run script that can run both JSON and HR parser scripts
- [ ] Support for multiple quiz types
- [ ] Improve AutoTopic dict via word cloud generator from course/lab
- [ ] Check for valid `structure.json` file
- [ ] Filter for more unwanted words/substrings (currently only "Nu stiu / Nu raspund"
- [ ] Allow for more customization via `config.json` file


## Basic Usage

  1) Move MXML file(s) in `./inputs/` directory
  2) Run `./generate-HR.sh` script to parse MXML to Human Readable
  3) Run `./generate-JSON.sh` script to parse Human Readable to JSON
  4) Run `./clean.sh` script to clean outputs/inputs (Optional)
  
## Parsing MXML to Human Readable format

> **./generate-HR.sh**

  Input Folder: `./inputs/`
  
  Output Folder: `./raw_hr/`
  
  Arguments:

|Opt.|Description |
|---|---|
|`-e tag1,tag2,...,tagN` | Add extra arguments separated by comma 			topics,reviewed_by`
|`-y` | Auto insert year if contained in input filename (eg. `./input/2019.xml`)  
|`-u username` | If `reviewed_by` tag is present, auto assign name of reviewer 
|`-c`| Clean old HR files 
|`-t`| Auto Assign `topic` tag values for each question based on Dictionary 

> **Human Readable Format**
``` 
  tag1:value1;tag2:value2;...;tagN:valueN;
  statement
  + correct answer
  - wrong answer
```
## Parsing Human Readable format to JSON

> **./generate-JSON.sh**

  Input Folder: `./raw_hr/`
  
  Output Folder: `./json_output/`
  
  Arguments:

|Opt.|Description |
|---|---|
|`-c` | Clean old JSON output files before creating new ones
|`-m` | Merge all JSON output files into a single file

> **Structure file (structure.json)**

    The structure file describes a single JSON object (question)
    There are a couple of mandatory tags which are basic for a question

        MANDATORY TAGS: statement:String
                        tags:Dictionary of dictionaries
                        answers:List of strings
                        correctAnswersNo: Number
    
    All other tags that are not mandatory or written explicitly (therefore
    added using the `-e` option for ./generate-HR) in the 
    structure.json file will be added as a dictionary in "tags"
    
**Default structure.json file used for this project**
```python
   {
      -----  V Project Specific Tags V  -----
      "createdOn":"",
      "lastUsed":"",
      "difficulty":0,
      -----  V    Mandatory Tags     V  -----
      "statement":"",
      "tags" : {
      },
      "answers": [
          {
              "statement":"", 
              "correct":false, 
              "grade":0.0 
          }
      ],
      "correctAnswersNo":0
    }
```

## Clean script

> **./clean.sh**

  Input Folder: `-`
  
  Output Folder: `-`
  
  Arguments:
  
|Opt.|Description |
|---|---|
|`-i` | Remove old XML input files
|`-j` | Remove old JSON output files
|`-u` | Remove old Human Readable files
