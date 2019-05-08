import os
import re
import sys

from os.path import join
from glob import glob

DIRECTORY_TO_CHECK = "."
EXTENSIONS = ['*.txt', '*.log']


def prompt_regex_string():
    response = input("Enter a regex string: ")
    return response


def string_contains_regex_str(string_to_search, regex_str):
    return bool(re.search(regex_str, string_to_search, re.M | re.I))


def get_filepaths_to_check():
    filepaths_to_check = []
    for ext in EXTENSIONS:
        filepaths_to_check.extend(glob(join(DIRECTORY_TO_CHECK, ext)))
    return filepaths_to_check


def check_file_for_regex_str(filepath, regex_str):
    with open(filepath) as file_to_check:
        for line in file_to_check:
            if string_contains_regex_str(line, regex_str):
                formatted_line = line.rstrip('\n')
                print(f"{filepath} -- {formatted_line}")


def main():
    # Prompt regex string if not provided as command line arg
    regex_str = prompt_regex_string() if len(sys.argv) <= 1 else sys.argv[1]

    filepaths_to_check = get_filepaths_to_check()

    for filepath in filepaths_to_check:
        check_file_for_regex_str(filepath, regex_str)


if __name__ == '__main__':
    main()
