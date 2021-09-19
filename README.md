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

The `quiz_manager.py` has multiple subcommands.
To find out more about each subcommand you can use the `--help` option.
