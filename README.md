# Quiz Manager

Quiz Manager manages quizzes designed to work with the [Quiz Manager Moodle Plugin](https://github.com/systems-cs-pub-ro/quiz-manager-moodle).

## Requirements

All the commands that install the prerequisites are found inside the [Makefile](./Makefile) `install` rule that can be run with the following command:

```sh
make install
```

## Usage

You can run the script using the following command:

```sh
python3 src/quiz_manager.py
```

`quiz_manager.py` has multiple subcommands.
To find out more about each subcommand you can use the `--help` option.

### Converting from one format to another

For the moment, the quiz-manager supports conversions between three file types: `JSON`, `HR` and `MXML`.

To convert a file from `$input_type` to `$output_type` run the following command:
```sh
python3 src/quiz_manager.py convert -i $input_file -o $output_file --input-format $input_type --output-format $output_type
```
The `--input_format` and `--output_format` arguments can be omitted only if the input / output file name contains a supported extension (eg. `.json`, `.hr` or `.mxml`)

## Question Format

Quiz Manager works with questions in a custom format, named *human-readable format*, or *hr*.
These questions are to be created and stored in repositories specific to each class / course.

Each question in *hr* format consists of three parts:

1. the metadata
1. the statement
1. the answers

Consider the sample question below:

```
created_on:2021-03-09;difficulty:1;topic:boot;
Acronimul BIOS vine de la:
- Brand Input/Output System
+ Basic Input/Output System
- Basic Input/Outstanding Source
- Be Input/Output System
```

### Metadata

The first line in the sample above is the metadata:

```
created_on:2021-03-09;difficulty:1;topic:boot;
```

It consists of key-value items defining properties of the question, in the format:

```
key1:value1;key2:value2;...;keyN:valueN;
```

If multiple values are assigned for a key, they will be separated by comma.

Possible keys are:

* `created_on` (**required**): question creation date; the format is `YYYY-MM-DD` (e.g. `2021-03-09` for March 9, 2021).
* `topic` (**required**): chapter / topic for the question
* `tags` (**optional**): keywords for the question content, more fine-grained than the chapter / topic
* `difficulty` (**required**): a numeric value for the question difficulty; a higher number means a more difficult question

**The metadata line must end with a semicolon (`;`).**

Topics, tags and difficulty are specific to each class / course that uses Quiz Manager.

### Statement

The second line in the sample above is the statement:

```
Acronimul BIOS vine de la:
```

The statement is a character string delimited by the metadata line and the first answer line.
That is, a statement may be single-line or multi-line (newlines may be part of the statement line).
It ends when the first answer starts.

### Answers

The last four lines in the sample above are the answers:

```
- Brand Input/Output System
+ Basic Input/Output System
- Basic Input/Outstanding Source
- Be Input/Output System
```

Each answer starts with `+ ` (`plus` and `blank`) for a correct answer or with `- ` (`minus` and `blank`) for a wrong answer.
The actual answer is a character string following `+ ` or `- `.
Answers may be single-line or multi-line.
Answers are delimited by the next answer or by an empty line marking the start of the next question.

The number of answers and the number of correct answers are specific to each class / course that uses Quiz Manager.
