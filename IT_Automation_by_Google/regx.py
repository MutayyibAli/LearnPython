"""A script to practice regular expressions in Python."""

# Import libraries
import csv
import re
import os


def contains_domain(address, domain):
    """Returns True if the email address contains the given domain,
    in the domain position, false if not.
    """
    domain_pattern = r"[\w\.-]+@" + domain + "$"
    if re.match(domain_pattern, address):
        return True
    return False


def replace_domain(address, old_domain, new_domain):
    """Replaces the old domain with the new domain in the received address."""
    old_domain_pattern = r"" + old_domain + "$"
    address = re.sub(old_domain_pattern, new_domain, address)
    return address


def main():
    """Processes the list of emails, replacing any instances of the
    old domain with the new domain.
    """
    old_domain, new_domain = "abc.edu", "xyz.edu"
    data_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_location = os.path.join(data_directory, "user_emails.csv")
    report_file = os.path.join(data_directory, "updated_user_emails.csv")

    user_email_list = []
    old_domain_email_list = []
    new_domain_email_list = []

    with open(csv_file_location, "r", encoding="utf-8") as file:
        user_data_list = list(csv.reader(file))

        for data in user_data_list:
            user_email_list.append(data[1].strip())

        for email_address in user_email_list:
            if contains_domain(email_address, old_domain):
                old_domain_email_list.append(email_address)
                replaced_email = replace_domain(email_address, old_domain, new_domain)
                new_domain_email_list.append(replaced_email)

        email_index = 1
        for user in user_data_list:
            for old_domain, new_domain in zip(
                old_domain_email_list, new_domain_email_list
            ):
                if user[email_index] == " " + old_domain:
                    user[email_index] = " " + new_domain

        file.close()

    with open(report_file, "w+", encoding="utf-8", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(user_data_list)
        output_file.close()


main()
