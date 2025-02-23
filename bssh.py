import re
import os
import csv
import sys
import readline
import ipaddress

from pathlib import Path
from termcolor import colored
from prettytable.colortable import ColorTable, Themes

# CSV file location/name
home_directory = Path.home()
db_file= f'{home_directory}/.config/.bssh.csv'

# Create the CSV file and write the header if it dosen't exist
def create_db():
    if not os.path.exists(db_file):
        with open(db_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'name', 'domain', 'port', 'user', 'keyFile']) # Write the header

def is_valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def is_valid_domain(domain):
    # Regex for validating a domain name
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]'
    return re.match(pattern, domain) is not None

def is_valid_port(port):
    # Regex for check port validity
    pattern = r'^(6553[0-5]|[0-5]?[0-9]{0,4}|[1-5][0-9]{0,4}|[0-6][0-5][0-5][0-9]|[0-6][0-5][0-5][0-9])$'
    return re.match(pattern, str(port)) is not None

def is_have_keyfile(host):
    if not host[5] == "":
        return True
    return False

def print_all_record():
    # Create a PrettyTable object and format it
    table = ColorTable(theme=Themes.PASTEL)
    table.padding_width = 3

    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader) # Read the header
        table.field_names = header # Set the header for the table

        for row in reader:
            table.add_row(row)
    
    print(table)

def get_record_by_id(id):
    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if int(row[0]) == id:
                return row

def is_valid_id(id_to_find):
    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        # Get the last ID from the last row
        id = 0
        for row in reader:
            id = int(row[0]) # Assuming ID is the first column
        if id_to_find <= id:
            return True
        return False

def get_next_id():
    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        # Get the last ID from the last row
        last_id = 0
        for row in reader:
            last_id = int(row[0]) # Assuming ID is the first column
        return last_id + 1 # Increment the last ID

def add_record(name, domain, port, user, keyfile):
    new_id = get_next_id()
    with open(db_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_id, name, domain, port, user, keyfile])

def edit_record(id, name, domain, port, user, keyfile):
    with open(db_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Loop through the rows, modify the value where ID is equal to
    for row in rows:
        if int(row['ID']) == id:
            row['name'] = name
            row['domain'] = domain
            row['port'] = port
            row['user'] = user
            row['keyFile'] = keyfile

    # Write the modified data back to the CSV file
    with open(db_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def delete_record_by_id(record_id):
    records = []

    # Read all records from the CSV file
    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header
        records.append(header)  # Keep the header
        for row in reader:
            if int(row[0]) != record_id:  # Skip the record with the specified ID
                records.append(row)
    # Rearrange IDs
    for index, row in enumerate(records[1:], start=1): # Start from 1 to skip header
        row[0] = index # Readding ID
    
    # Write the updated records back to the CSV file
    with open(db_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(records)
    
def display_menu():
    print()
    print(colored("========== Main Menu ==========", 'yellow'))
    print(colored("0. Exit", 'yellow'))
    print(colored("1. Add new SSH connection.", 'yellow'))
    print(colored("2. Edit existing SSH connection.", 'yellow'))
    print(colored("3. Delete SSH connection.", 'red'))
    print(colored("================================", 'yellow'))

def main():
    create_db()
    try:
        while True:
            print()
            print_all_record()
            choice = input(colored("Enter the number of the SSH connection you want to connect. CTRL+C to exit. [m] for menu: ", 'yellow'))

            if choice.isdigit() and is_valid_id(int(choice)) and int(choice) > 0:
                host = get_record_by_id(int(choice))
                
                command = f"ssh -p {host[3]} {host[4]}@{host[2]}"
                if is_have_keyfile(host):
                    command = f"ssh -i {host[5]} -p {host[3]} {host[4]}@{host[2]}"
                    print(colored(f"Connecting to: {host[4]}@{host[2]} ssh-key: {host[5]}", 'green'))
                else:
                    print(colored(f"Connecting to: {host[4]}@{host[2]}", 'green'))

                # Run the command
                os.system(command)
                sys.exit(0)

            elif choice == "m":
                while True:
                    display_menu()
                    choice = input(colored("Please select an option (0-3): ", 'yellow'))

                    if choice == '0':
                        # Exit from the program
                        print("0")
                        sys.exit(0)
                    elif choice == "1":
                        # Add new record
                        name = input(colored("Name: ", 'yellow'))
                        domain = input(colored("Domain or IP: ", 'yellow'))
                        if not (is_valid_ipv4(domain) or is_valid_domain(domain)):
                            print(colored(f"Invalid domain or IP address: {domain}", 'red'))
                            break
                        port = input(colored("Port: ", 'yellow'))
                        if not is_valid_port(port):
                            print(colored(f"Invalid port: {port}", 'red'))
                            break
                        user = input(colored("User: ", 'yellow'))
                        key = input(colored("KeyFile: ", 'yellow'))
                        add_record(name, domain, int(port), user, key)
                        break
                    elif choice == "2":
                        # Edit existing record
                        id = input(colored("Please select an ID to edit connection: ", 'yellow'))
                        if not is_valid_id(int(id)):
                            print(colored(f"There is no souch ID: {id}", 'red'))
                            break
                        record = get_record_by_id(int(id))
                        print(colored(record,'green'))

                        name = input(f"Enter new name (enter to keep {record[1]}): ")
                        if not name:
                            name = record[1]
                        domain = input(f"Enter new name (enter to keep {record[2]}): ")
                        if not domain:
                            domain = record[2]
                        if not (is_valid_ipv4(domain) or is_valid_domain(domain)):
                            print(colored(f"Invalid domain or IP address: {domain}", 'red'))
                            break
                        port = input(f"Enter new name (enter to keep {record[3]}): ")
                        if not port:
                            port = int(record[3])
                        if not is_valid_port(port):
                            print(colored(f"Invalid port: {port}", 'red'))
                            break
                        user = input(f"Enter new name (enter to keep {record[4]}): ")
                        if not user:
                            user = record[4]
                        key = input(f"Enter new name (enter to keep {record[5]}): ")
                        if not key:
                            key = record[5]

                        edit_record(int(id),name,domain,int(port),user,key)
        
                        break
                    elif choice == "3":
                        # Delete existing record
                        id = input(colored("DELETE saved SSH connection, ID: ", 'red'))
                        if id.isdigit() and is_valid_id(int(id)):
                            record = get_record_by_id(int(id))
                            delete_record_by_id(int(id))
                            print(colored(f"Record successfully deleted: {record}", 'green'))
                        print(colored("Invalid choice. Please try again.", 'red'))
                        break
                    else:
                        print(colored("Invalid choice. Please try again.", 'red'))
            else:
                print(colored("Invalid choice, exiting...", 'red'))
                sys.exit(1)
    except KeyboardInterrupt:
        print()
        sys.exit(0)

if __name__ == "__main__":
    main()
