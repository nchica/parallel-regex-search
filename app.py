import csv
import os
import re
import sys
import threading

from os.path import join
from glob import glob

DIRECTORY_TO_CHECK = "."
EXTENSIONS = ['*.txt', '*.log']
HEADERS = ["Filepath", "Line Number", "Line"]

thread_data = []


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


def check_lines_for_regex_str(filepath, lines, regex_str, thread_lock=None):
    results = []
    line_num = 1
    for line in lines:
        if string_contains_regex_str(line, regex_str):
            formatted_line = line.rstrip('\n')
            results.append([filepath, line_num, formatted_line])
        line_num += 1

    if thread_lock:
        global thread_data
        thread_lock.acquire()
        thread_data.extend(results)
        thread_lock.release()
    else:
        return results


def check_file_for_regex_str(filepath, regex_str, num_threads=1):
    results = []
    lock = threading.Lock() if num_threads > 1 else None
    with open(filepath, errors='ignore') as file_to_check:
        lines_in_file = file_to_check.readlines()
        if num_threads == 1:
            results = check_lines_for_regex_str(
                filepath, lines_in_file, regex_str, lock)
        else:
            lines_per_thread = int(len(lines_in_file) / num_threads)
            print(f"File: {filepath}")
            threads = []
            for thread_num in range(num_threads):
                start_index = thread_num * lines_per_thread
                end_index = ((thread_num + 1) * lines_per_thread
                             if thread_num < num_threads - 1
                             else len(lines_in_file))
                print(f"Thread {thread_num} - {start_index}:{end_index}")
                lines_to_search = lines_in_file[start_index:end_index]
                thread_obj = threading.Thread(
                    target=check_lines_for_regex_str,
                    args=(filepath, lines_to_search, regex_str, lock))
                thread_obj.start()
                threads.append(thread_obj)
            for thread in threads:
                thread.join()
            global thread_data
            results = thread_data
            thread_data = []

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
        num_threads = int(sys.argv[2]) or 1

    filepaths_to_check = get_filepaths_to_check()

    overview = [["Filepath", f"Frequency of {regex_str}"]]
    results = [HEADERS]

    for filepath in filepaths_to_check:
        regex_check_results = check_file_for_regex_str(
            filepath, regex_str, num_threads)
        overview.append([filepath, regex_check_results["frequency"]])
        results.extend(regex_check_results["results"])

    print_data_to_csv("results.csv", results)
    print_data_to_csv("overview.csv", overview)


if __name__ == '__main__':
    main()
