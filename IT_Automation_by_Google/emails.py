"""Script to be used for learning unit testing."""

import sys
import os
import csv


def populate_dictionary(filename):
    """Populate a dictionary with name/email pairs for easy lookup."""
    email_dict = {}
    with open(filename, encoding="UTF-8") as csv_file:
        lines = csv.reader(csv_file, delimiter=",")
        for row in lines:
            name = str(row[0].lower())
            email_dict[name] = row[1]
    return email_dict


def find_email(argv):
    """Return an email address based on the username given."""
    # Create the username based on the command line input.
    try:
        fullname = str(argv[1] + " " + argv[2])
        # Preprocess the data
        data_directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_location = os.path.join(data_directory, "user_emails.csv")
        email_dict = populate_dictionary(csv_file_location)
        # Find and print the email
        if email_dict.get(fullname.lower()):
            return email_dict.get(fullname.lower()).strip()
        else:
            return "No email address found"
    except IndexError:
        return "Missing parameters"


def main():
    print(find_email(sys.argv))


if __name__ == "__main__":
    main()
