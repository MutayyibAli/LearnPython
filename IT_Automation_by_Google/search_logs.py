"""Search for the user specified logs in the log file"""

import re
import sys
import os


def error_search(log_file):
    error = input("What is the error? ")
    error_list = []

    with open(log_file, mode="r", encoding="UTF-8") as file:
        for log in file.readlines():
            error_patterns = ["error"]
            for i in range(len(error.split(" "))):
                error_patterns.append(r"{}".format(error.split(" ")[i].lower()))

            match = True
            for error_pattern in error_patterns:
                if not re.search(error_pattern, log.lower()):
                    match = False

            if match:
                error_list.append(log)
        file.close()
    return error_list


def file_output(returned_errors):
    data_directory = os.path.dirname(os.path.abspath(__file__))
    log_file_location = os.path.join(data_directory, "searched_logs.log")
    with open(log_file_location, "w", encoding="UTF-8") as file:
        for error in returned_errors:
            file.write(error)
        file.close()


# To run the program, pass the log file as an argument to the script.
# Example: python search_logs.py <log_file>
if __name__ == "__main__":
    logs = sys.argv[1]
    errors = error_search(logs)
    file_output(errors)
    sys.exit(0)
