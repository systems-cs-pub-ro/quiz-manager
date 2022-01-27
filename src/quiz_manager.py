"""
    Quiz Manager is a script that helps with the convertion and generation of quizzes.
"""

import sys
import click
from parsers import hr
from parsers import mxml
from checkers import check_hr


@click.group()
def cli():
    """
    Entrypoint of the application
    """


@cli.command()
@click.option(
    "-i", "--input-file", "input_file_path", required=True, help="Input file path"
)
@click.option(
    "-o", "--output-file", "output_file_path", required=True, help="Output file path"
)
@click.option(
    "-if",
    "--input-format",
    type=click.Choice(["JSON", "HR", "MXML"], case_sensitive=False),
    help="The input format",
)
@click.option(
    "-of",
    "--output-format",
    type=click.Choice(["JSON", "HR", "MXML"], case_sensitive=False),
    help="The output format",
)
def convert(input_file_path, output_file_path, input_format, output_format):
    """
    Converts files to different formats.
    """
    if input_format is None:
        if input_file_path.split(".")[-1].lower() in ["json", "hr", "mxml"]:
            input_format = input_file_path.split(".")[-1].upper()
        else:
            raise click.UsageError(
                "Input format can't be extracted from input"
                " file extention. Use --input-format to specify the input format."
            )

    if output_format is None:
        if output_file_path.split(".")[-1].lower() in ["json", "hr", "mxml"]:
            output_format = output_file_path.split(".")[-1].upper()
        else:
            raise click.UsageError(
                "Output format can't be extracted from output"
                " file extention. Use --output-format to specify the output format."
            )

    print(f"Converting from {input_format} to {output_format}")
    print(f"Paths:\n\tinput: {input_file_path}\n\toutput: {output_file_path}")

    with open(input_file_path, "r", encoding="UTF-8") as input_file:
        input_content = input_file.read()

    conversion = ""
    if input_format == "JSON":
        if output_format == "HR":
            conversion = hr.quiz_json_to_hr(input_content)
        elif output_format == "MXML":
            conversion = mxml.quiz_json_to_mxml(input_content)
    elif input_format == "HR":
        if output_format == "JSON":
            conversion = hr.quiz_hr_to_json(input_content)
        elif output_format == "MXML":
            conversion = mxml.quiz_json_to_mxml(hr.quiz_hr_to_json(input_content))
    elif input_format == "MXML":
        if output_format == "JSON":
            conversion = mxml.quiz_mxml_to_json(input_content)
        elif output_format == "HR":
            conversion = hr.quiz_json_to_hr(mxml.quiz_mxml_to_json(input_content))

    with open(output_file_path, "w", encoding="UTF-8") as output_file:
        output_file.write(conversion)


@cli.command()
@click.option(
    "-t",
    "--type",
    "type",
    type=click.Choice(["common", "specific"]),
    required=True,
    help="Type of the check that will be performed.\
        Choose common for basic identation and syntax check. Choose specific\
        for checking configurable parameters, according to a config file.",
)
@click.option(
    "-i", "--input_file", "input_file", required=True, help="The file to be checked."
)
@click.option(
    "-cf",
    "--config_file",
    "config_file",
    required=False,
    help="Custom location for the configuration file.",
)
def check(type, input_file, config_file):
    """
    Checks the hr file provided as an input.
    """
    with open(input_file) as file:
        if type == "common":
            sys.exit(check_hr.check_common(input_file, file))
        else:
            sys.exit(check_hr.check_specific(input_file, file, config_file))


if __name__ == "__main__":
    cli()
