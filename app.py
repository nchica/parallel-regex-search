import csv
import os
import re
import sys

from os.path import join
from glob import glob

DIRECTORY_TO_CHECK = "."
EXTENSIONS = ['*.txt', '*.log']
HEADERS = ["Filepath", "Line Number", "Line"]


def prompt_arguments():
    response = input("Enter a regex string: ")
    num_threads = input("Enter number of threads: ")
    return (response, num_threads)


def string_contains_regex_str(string_to_search, regex_str):
    return bool(re.search(regex_str, string_to_search, re.M | re.I))


def get_filepaths_to_check():
    filepaths_to_check = []
    for ext in EXTENSIONS:
        filepaths_to_check.extend(glob(join(DIRECTORY_TO_CHECK, ext)))
    return filepaths_to_check


def check_file_for_regex_str(filepath, regex_str):
    results = []
    with open(filepath) as file_to_check:
        line_num = 1
        lines_in_file = file_to_check.readlines()
        for line in lines_in_file:
            if string_contains_regex_str(line, regex_str):
                formatted_line = line.rstrip('\n')
                results.append([filepath, line_num, formatted_line])
            line_num += 1
    return {'frequency': len(results), 'results': results}


def print_data_to_csv(filepath, data, headers=None):
    with open(filepath, mode="w", newline='') as data_file:
        data_writer = csv.writer(data_file)
        if headers:
            data_writer.writerow(headers)
        data_writer.writerows(data)


def main():
    # Prompt arguments if not provided in command line args
    if len(sys.argv) < 3:
        regex_str, num_threads = prompt_arguments()
    else:
        regex_str = sys.argv[1]
        num_threads = sys.argv[2]

    filepaths_to_check = get_filepaths_to_check()

    overview = [["Filepath", f"Frequency of {regex_str}"]]
    results = [HEADERS]

    for filepath in filepaths_to_check:
        regex_check_results = check_file_for_regex_str(filepath, regex_str)
        overview.append([filepath, regex_check_results["frequency"]])
        results.extend(regex_check_results["results"])

    print_data_to_csv("results.csv", results)
    print_data_to_csv("overview.csv", overview)


if __name__ == '__main__':
    main()
