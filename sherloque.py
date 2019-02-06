#!/usr/bin/env python3
import time
import argparse
import json
import os
import sys

# Print with colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Json array storing target's information
data = {
  "Target":{
    "First name": "",
    "Last name": "",
    "Nickname": "",
    "Date of birth (MMDDYYYY)": "",
    "Place of birth": "",
    "Current living place": "",
    "Current department number": "",
    "Security awareness (1-3)": "To be implemented soon"
  },
  "Holidays":{
    "Memorable journey - City": "",
    "Memorable journey - Department number": "",
    "Usual place - City": "",
    "Usual place - Department number": ""
  },
  "Areas of interest":{
    "Passion": "",
    "Favorite sport": "",
    "Supported team": "",
    "Idol": ""
  },
  "Company":{
    "Name": "",
    "Arrival date (MMDDYYYY)": ""
  },
  "Family":{
    "Partner's first name": "",
    "Partner's date of birth (MMDDYYYY)": "",
    "Kid's name": "",
    "Kid's date of birth (MMDDYYYY)": "",
    "Pet's name": ""
  }
}

# These constants are used to iterate over the json object 'data'
NB_FIELDS = {
        'Menu': 5,
        'Target': 8,
        'Areas of interest': 4,
        'Holidays': 4,
        'Company': 2,
        'Family': 5
        }


# Stores the output filename if -o parameter is set
# By default, the output is printed
WRITE_OUTPUT = False
OUTPUT_FILENAME = ''

# Stores the export filename if -e parameter is set
EXPORT_INFO = False
EXPORT_FILENAME = ''

# Initializes the parser
def init_parser():
    parser = argparse.ArgumentParser(prog='./sherloque.py',description='Sherloque is a tool for generating target-specific password lists.')
    parser.add_argument('-v','--version', action='version', version='Sherloque version 0.1')
    parser.add_argument("-j", "--json", action="store", help="Import a json file containing information about the target.")
    parser.add_argument("-o", "--output", action="store", help="Output file for the generated password list.")
    parser.add_argument("-e", "--export", action="store", help="Export target information as a json file when generating the wordlist (for future reuse).")
    args = parser.parse_args()


    if args.output:
        global WRITE_OUTPUT
        global OUTPUT_FILENAME
        WRITE_OUTPUT = True
        OUTPUT_FILENAME = args.output

    if args.export:
        global EXPORT_FILENAME
        global EXPORT_INFO
        EXPORT_INFO = True
        EXPORT_FILENAME = args.export

    if args.json:
        parse_json_input(args.json)
        run_app()
    else:
        run_app()

# Clears the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Prints the banner
def print_banner():
    banner = """
    ███████╗██╗  ██╗███████╗██████╗ ██╗      ██████╗  ██████╗ ██╗   ██╗███████╗
    ██╔════╝██║  ██║██╔════╝██╔══██╗██║     ██╔═══██╗██╔═══██╗██║   ██║██╔════╝
    ███████╗███████║█████╗  ██████╔╝██║     ██║   ██║██║   ██║██║   ██║█████╗
    ╚════██║██╔══██║██╔══╝  ██╔══██╗██║     ██║   ██║██║▄▄ ██║██║   ██║██╔══╝
    ███████║██║  ██║███████╗██║  ██║███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗
    ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚══▀▀═╝  ╚═════╝ ╚══════╝
    """
    print(banner)
    print("                                                              by BoiteAKlou")


# Parses a json file and checks its structure, then imports it into data
def parse_json_input(filepath):
    try:
        with open(filepath) as json_file:
            imported_data = json.load(json_file)
            try:
                for domain in imported_data:
                    if domain in data:
                        for subfield in imported_data[domain]:
                            if subfield in data[domain].keys():
                                data[domain][subfield] = imported_data[domain][subfield]
                            else:
                                print("[+] ERROR: Subfield ",subfield," doesn't belong to the template")
                    else:
                        print("[+] ERROR: Domain ",domain," doesn't belong to the template")
            except KeyError:
                print("[+] ERROR: Something went wrong, check that the json file is conform to the template.")
                json_file.close()
                sys.exit(1)
            json_file.close()
    except IOError:
        print("[+] ERROR: Unable to read the json file. Exiting...\n")
        sys.exit(1)


# Exports target information as a json file
def export_json_info(filepath):
    print("\n[+] Saving target information to "+filepath+".")
    try:
        with open(filepath, "w+") as f:
            json.dump(data,f)
            print("[+] Target information successfully exported.")
            f.close()
    except IOError:
        print("[+] ERROR: Unable to create file on disk. Exiting...\n")
        sys.exit(1)


# Writes the wordlist to a file
def save_wordlist(wordlist, filename):
    print("\n[+] Saving wordlist to "+filename+".")
    try:
        with open(filename, "w+") as f:
            for word in wordlist:
                f.write(word+"\n")
            f.close()
        print("[+] Wordlist successfully generated in "+filename+".")
    except IOError:
        print("[+] ERROR: Unable to create file on disk. Exiting...\n")
        sys.exit(1)


# Asks for user input and sanitizes it before returning it
def user_input(message,nbChoices):
    print(message)
    choice = input("> ")
    if choice == 'q':
        sys.exit(0)
    while((choice not in [str(i) for i in range(0,nbChoices-1)]) and choice != 'e' and choice != 'b' and choice != 'h' and choice != 'help' and (choice != 'G' and data)):
        print("Invalid entry, please try again.")
        choice = input("> ")
        if choice == 'q':
            sys.exit(0)
    return choice

# Displays the main menu
def display_menu():
    print(bcolors.HEADER+"+-----------+"+bcolors.ENDC)
    print(bcolors.HEADER+"| Main menu |"+bcolors.ENDC)
    print(bcolors.HEADER+"+-----------+"+bcolors.ENDC+"\n")
    print(bcolors.BOLD+"Available categories:"+bcolors.ENDC+"\n")
    print("[0] "+bcolors.WARNING+"Target"+bcolors.ENDC)
    print("[1] "+bcolors.WARNING+"Family"+bcolors.ENDC)
    print("[2] "+bcolors.WARNING+"Company"+bcolors.ENDC)
    print("[3] "+bcolors.WARNING+"Holidays"+bcolors.ENDC)
    print("[4] "+bcolors.WARNING+"Areas of interest\n"+bcolors.ENDC)
    #print("[5] Targeted service\n") TO BE IMPLEMENTED

    print(bcolors.BOLD+"Options:"+bcolors.ENDC+"\n")
    if data:
        print(bcolors.OKBLUE+"[G] Generate the wordlist"+bcolors.ENDC)
    print("[h] Help")
    print("[e] Export information as json")
    print(bcolors.FAIL+"[q] Exit"+bcolors.ENDC)
    print("\n\n")


# Displays the current state of data dict
def display_current_data(key):
    print(bcolors.BOLD+"Currently stored data:\n"+bcolors.ENDC)
    counter = 0
    for field in data[key]:
        print("["+str(counter)+"] "+bcolors.WARNING+field+": "+bcolors.ENDC+data[key][field])
        counter+=1
    print()


# Asks for personal data and stores it into data dict
def update_data(key):
    terminated = False
    while not terminated:
        clear_screen()
        print_banner()
        title = key+" topic"
        print(bcolors.HEADER+"+-"+("-"*len(title))+"-+"+bcolors.ENDC)
        print(bcolors.HEADER+"| "+key+" topic |"+bcolors.ENDC)
        print(bcolors.HEADER+"+-"+("-"*len(title))+"-+"+bcolors.ENDC+"\n")
        display_current_data(key)
        print(bcolors.BOLD+"Options:"+bcolors.ENDC+"\n")
        print(bcolors.OKGREEN+"[b] Back to main menu"+bcolors.ENDC)
        print("[h] Help")
        print(bcolors.FAIL+"[q] Exit"+bcolors.ENDC)
        print("\n\n")
        choice = user_input("Select a "+bcolors.WARNING+"field"+bcolors.ENDC+" to modify or type "+bcolors.OKGREEN+"'b'"+bcolors.ENDC+" to go back to main menu:",NB_FIELDS[key]+1)
        # Go back to main menu
        if choice == 'b':
            terminated = True
        elif choice == 'e':
            continue
        elif choice == 'h' or choice =='help':
            display_help()
        else:
            int_choice = int(choice)
            if int_choice in range(0,NB_FIELDS[key]+1):
                counter = 0
                for field in data[key]:
                    if counter == int_choice:
                        print("Enter a new value for: "+bcolors.WARNING+field+bcolors.ENDC+" (ENTER to leave blank)")
                        data[key][field] = input("> ").replace(" ","")
                        if 'Date' in field and data[key][field] != '':
                            while not data[key][field].isdigit() or len(data[key][field]) != 8:
                                print("Wrong format, must be (MMDDYYYY)")
                                data[key][field] = input("> ")
                                if(data[key][field] == '' or data[key][field] == 'q' or data[key][field] == 'quit'):
                                    data[key][field] == ''
                                    break
                        break
                    else:
                        counter+=1



# Displays a short help
def display_help():
    clear_screen()
    print_banner()
    print(bcolors.HEADER+"+-----------+"+bcolors.ENDC)
    print(bcolors.HEADER+"| Help page |"+bcolors.ENDC)
    print(bcolors.HEADER+"+-----------+"+bcolors.ENDC+"\n")
    print("This program allows you to create a custom wordlist based on your knowledge of the target.\n")
    print("* Enter the index of the topic you want to fill in.")
    print("* Modify the field of your choice by typing its index in the list and assigning it a new value.")
    print("* Empty fields won't be taken into account when generating the wordlist.")
    print("* Once done, type 'b' to go back to the main menu and choose another topic.")
    print("* When you're finished, enter 'G' inside the main menu to generate the wordlist.\n\n")
    input("Hit ENTER to leave...")


# Run the main application in interactive mode
def run_app():
    terminated = False
    while not terminated:
        clear_screen()
        print_banner()
        display_menu()
        choice = user_input("Please pick a "+bcolors.WARNING+"topic"+bcolors.ENDC+" to fill in or select an option:",NB_FIELDS['Menu']+1)
        if choice == 'h' or choice == 'help':
            display_help()
        elif choice == '0':
            update_data('Target')
        elif choice == '1':
            update_data('Family')
        elif choice == '2':
            update_data('Company')
        elif choice == '3':
            update_data('Holidays')
        elif choice == '4':
            update_data('Areas of interest')
        # Coming soon
        #elif choice == '5':
        #    update_data('Targeted service')
        elif choice == 'G':
            terminated = True
            generate_wordlist()
        elif choice == 'b':
            continue
        elif choice == 'e':
            export_json_info("export.json")
            time.sleep(1.5)
        else:
            print("Something went wrong... Exiting.")
            sys.exit(1)


##########################################################
# Combination functions used for generating the wordlist #
##########################################################

def combine_with_date(str1, date):
    res = []
    day = date[:2]
    month = date[2:4]
    year = date[4:]
    last_digits_year = year[2:]
    res.append(str1+last_digits_year)
    res.append(str1+year)
    res.append(str1+month)
    res.append(str1+day)
    res.append(str1+day+month)
    res.append(str1+day+month+year)
    return res

def combine_firstname_lastname(firstname, lastname):
    res = []
    res.append(firstname) # john
    res.append(lastname) # doe
    res.append(firstname+lastname[0]) # johnd
    res.append(lastname+firstname[0]) # doej
    res.append(firstname+lastname) # johndoe
    res.append(lastname+firstname) # doejohn

    return res

# Combines a string and a department number
def combine_with_department(str1, dptnumber):
    res = []
    res.append(str1+dptnumber)
    res.append(dptnumber+str1)

    return res






########################
# Generation functions #
########################

# Generates wordlist entries relative to the target
def generate_target_wordlist():
    target_wordlist = []

    # First name + last name
    # Initials
    if data['Target'].get('First name') and data['Target'].get('Last name'):
        # lowercases
        target_wordlist += combine_firstname_lastname(data['Target'].get('First name').lower(), data['Target'].get('Last name').lower())
        # capitalized
        target_wordlist += combine_firstname_lastname(data['Target'].get('First name').capitalize(), data['Target'].get('Last name').capitalize())
        #initials
        target_wordlist.append(data['Target'].get('First name')[0].lower() + data['Target'].get('Last name')[0].lower())
        target_wordlist.append(data['Target'].get('Last name')[0].lower() + data['Target'].get('First name')[0].lower())
        target_wordlist.append(data['Target'].get('First name')[0].capitalize() + data['Target'].get('Last name')[0].lower())
        target_wordlist.append(data['Target'].get('Last name')[0].capitalize() + data['Target'].get('First name')[0].lower())
        target_wordlist.append(data['Target'].get('First name')[0].capitalize() + data['Target'].get('Last name')[0].capitalize())
        target_wordlist.append(data['Target'].get('Last name')[0].capitalize() + data['Target'].get('First name')[0].capitalize())
        target_wordlist.append(data['Target'].get('First name')[0].lower() + data['Target'].get('Last name')[0].lower())
        target_wordlist.append(data['Target'].get('Last name')[0].lower() + data['Target'].get('First name')[0].lower())
    elif data['Target'].get('First name'):
        # Only first name set
        target_wordlist.append(data['Target'].get('First name').lower())
        target_wordlist.append(data['Target'].get('First name').capitalize())
    elif data['Target'].get('Last name'):
        # Only last name set
        target_wordlist.append(data['Target'].get('Last name').lower())
        target_wordlist.append(data['Target'].get('Last name').capitalize())

    # (First name AND/OR last name) + date of birth
    if (data['Target'].get('First name') or data['Target'].get('Last name')) and data['Target'].get('Date of birth (MMDDYYYY)'):
        res = []
        for word in target_wordlist:
            res += combine_with_date(word,data['Target'].get('Date of birth (MMDDYYYY)'))

        target_wordlist += res

    # first name + Current department number
    if data['Target'].get('First name') and data['Target'].get('Current department number'):
        target_wordlist += combine_with_department(data['Target'].get('First name').lower(),data['Target'].get('Current department number'))
        target_wordlist += combine_with_department(data['Target'].get('First name').capitalize(),data['Target'].get('Current department number'))

    # Knickname + date of birth
    if data['Target'].get('Knickname') and data['Target'].get('Date of birth (MMDDYYYY)'):
        target_wordlist += combine_with_date(data['Target'].get('Knickname'),data['Target'].get('Date of birth (MMDDYYYY)'))

    # Knickname + Current department number
    if data['Target'].get('Knickname') and data['Target'].get('Current department number'):
        target_wordlist += combine_with_department(data['Target'].get('Knickname'),data['Target'].get('Current department number'))

    # Knickname only
    if data['Target'].get('Knickname'):
        target_wordlist.append(data['Target'].get('Knickname'))

    # Initials + Current department number
    if data['Target'].get('First name') and data['Target'].get('Last name') and data['Target'].get('Current department number'):
        target_wordlist += combine_with_department(data['Target'].get('First name').lower()+data['Target'].get('Last name').lower(),data['Target'].get('Current department number'))
        target_wordlist += combine_with_department(data['Target'].get('Last name').lower()+data['Target'].get('First name').lower(),data['Target'].get('Current department number'))
        target_wordlist += combine_with_department(data['Target'].get('First name').capitalize()+data['Target'].get('Last name').lower(),data['Target'].get('Current department number'))
        target_wordlist += combine_with_department(data['Target'].get('Last name').capitalize()+data['Target'].get('First name').lower(),data['Target'].get('Current department number'))

    # Current living place + Current department number
    if data['Target'].get('Current living place') and data['Target'].get('Current department number'):
        target_wordlist += combine_with_department(data['Target'].get('Current living place').lower(),data['Target'].get('Current department number'))
        target_wordlist += combine_with_department(data['Target'].get('Current living place').capitalize(),data['Target'].get('Current department number'))


    # Place of birth + date of birth
    if data['Target'].get('Place of birth') and data['Target'].get('Date of birth (MMDDYYYY)'):
        target_wordlist += combine_with_date(data['Target'].get('Place of birth').lower(), data['Target'].get('Date of birth (MMDDYYYY)'))
        target_wordlist += combine_with_date(data['Target'].get('Place of birth').capitalize(), data['Target'].get('Date of birth (MMDDYYYY)'))

    # Place of birth only
    if data['Target'].get('Place of birth'):
        target_wordlist.append(data['Target'].get('Place of birth').lower())
        target_wordlist.append(data['Target'].get('Place of birth').capitalize())

    # Current living place only
    if data['Target'].get('Current living place'):
        target_wordlist.append(data['Target'].get('Current living place').lower())
        target_wordlist.append(data['Target'].get('Current living place').capitalize())

    # Date of birth only
    if data['Target'].get('Date of birth (MMDDYYYY)'):
        target_wordlist += combine_with_date('',data['Target'].get('Date of birth (MMDDYYYY)'))

    return target_wordlist




# Generates wordlist entries relative to the target's family
def generate_family_wordlist():
    family_wordlist = []

    # Partners firstname + Partners date of birth
    if data['Family'].get("Partner's first name") and data['Family'].get("Partner's date of birth (MMDDYYYY)"):
        family_wordlist += combine_with_date(data['Family'].get("Partner's first name").lower(),data['Family'].get("Partner's date of birth (MMDDYYYY)"))
        family_wordlist += combine_with_date(data['Family'].get("Partner's first name").capitalize(),data['Family'].get("Partner's date of birth (MMDDYYYY)"))

    # Kid's name + Kid's date of birth
    if data['Family'].get("Kid's name") and data['Family'].get("Kid's date of birth (MMDDYYYY)"):
        family_wordlist += combine_with_date(data['Family'].get("Kid's name").lower(),data['Family'].get("Kid's date of birth (MMDDYYYY)"))
        family_wordlist += combine_with_date(data['Family'].get("Kid's name").capitalize(),data['Family'].get("Kid's date of birth (MMDDYYYY)"))

    # Pet + Department number
    if data['Family'].get("Pet's name") and data['Target'].get('Current department number'):
        family_wordlist += combine_with_department(data['Family'].get("Pet's name").lower(),data['Target'].get('Current department number'))
        family_wordlist += combine_with_department(data['Family'].get("Pet's name").capitalize(),data['Target'].get('Current department number'))

    # Partner's name alone
    if data['Family'].get("Partner's first name"):
        family_wordlist.append(data['Family'].get("Partner's first name").lower())
        family_wordlist.append(data['Family'].get("Partner's first name").capitalize())

    # Partner's date of birth alone
    if data['Family'].get("Partner's date of birth (MMDDYYYY)"):
        family_wordlist += combine_with_date('',data['Family'].get("Partner's date of birth (MMDDYYYY)"))

    # Kid's name alone
    if data['Family'].get("Kid's name"):
        family_wordlist.append(data['Family'].get("Kid's name").lower())
        family_wordlist.append(data['Family'].get("Kid's name").capitalize())

    # Kid's date of birth alone
    if data['Family'].get("Kid's date of birth (MMDDYYYY)"):
        family_wordlist += combine_with_date('',data['Family'].get("Kid's date of birth (MMDDYYYY)"))

    # Pet's name alone
    if data['Family'].get("Pet's name"):
        family_wordlist.append(data['Family'].get("Pet's name").lower())
        family_wordlist.append(data['Family'].get("Pet's name").capitalize())


    return family_wordlist



# Generate wordlist entries relative to holidays
def generate_holidays_wordlist():
    holidays_wordlist = []

    # Memorable journey - City + Department number
    if data['Holidays'].get('Memorable journey - City') and data['Holidays'].get('Memorable journey - Department number'):
        holidays_wordlist += combine_with_department(data['Holidays'].get('Memorable journey - City').lower(),data['Holidays'].get('Memorable journey - Department number'))
        holidays_wordlist += combine_with_department(data['Holidays'].get('Memorable journey - City').capitalize(),data['Holidays'].get('Memorable journey - Department number'))

    # Usual place - City + Department number
    if data['Holidays'].get('Usual place - City') and data['Holidays'].get('Usual place - Department number'):
        holidays_wordlist += combine_with_department(data['Holidays'].get('Usual place - City').lower(),data['Holidays'].get('Usual place - Department number'))
        holidays_wordlist += combine_with_department(data['Holidays'].get('Usual place - City').capitalize(),data['Holidays'].get('Usual place - Department number'))

    # Usual place - City alone
    if data['Holidays'].get('Usual place - City'):
        holidays_wordlist.append(data['Holidays'].get('Usual place - City').lower())
        holidays_wordlist.append(data['Holidays'].get('Usual place - City').capitalize())

    # Memorable journey - City alone
    if data['Holidays'].get('Memorable journey - City'):
        holidays_wordlist.append(data['Holidays'].get('Memorable journey - City').lower())
        holidays_wordlist.append(data['Holidays'].get('Memorable journey - City').capitalize())

    return holidays_wordlist


# Generates worlist entries relative to areas of interest
def generate_areas_of_interest_wordlist():
    areas_of_interest_wordlist = []

    # Passion alone
    if data['Areas of interest'].get('Passion'):
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Passion').lower())
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Passion').capitalize())

    # Favorite sport alone
    if data['Areas of interest'].get('Favorite sport'):
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Favorite sport').lower())
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Favorite sport').capitalize())

    # Supported team alone
    if data['Areas of interest'].get('Supported team'):
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Supported team').lower())
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Supported team').capitalize())

    # Idol alone
    if data['Areas of interest'].get('Idol'):
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Idol').lower())
        areas_of_interest_wordlist.append(data['Areas of interest'].get('Idol').capitalize())


    # Passion + Current department number
    if data['Areas of interest'].get('Passion') and data['Target'].get('Current department number'):
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Passion').lower(),data['Target'].get('Current department number'))
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Passion').capitalize(),data['Target'].get('Current department number'))

    # Favorite sport + Current department number
    if data['Areas of interest'].get('Favorite sport') and data['Target'].get('Current department number'):
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Favorite sport').lower(),data['Target'].get('Current department number'))
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Favorite sport').capitalize(),data['Target'].get('Current department number'))

    # Supported team + Current department number
    if data['Areas of interest'].get('Supported team') and data['Target'].get('Current department number'):
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Supported team').lower(),data['Target'].get('Current department number'))
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Supported team').capitalize(),data['Target'].get('Current department number'))

    # Idol + Current department number
    if data['Areas of interest'].get('Idol') and data['Target'].get('Current department number'):
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Idol').lower(),data['Target'].get('Current department number'))
        areas_of_interest_wordlist += combine_with_department(data['Areas of interest'].get('Idol').capitalize(),data['Target'].get('Current department number'))


    return areas_of_interest_wordlist


# Generates wordlist entries relative to the target's company
def generate_company_wordlist():
    company_wordlist = []

    # Name + Arrival date
    if data['Company'].get('Name') and data['Company'].get('Arrival date (MMDDYYYY)'):
        company_wordlist += combine_with_date(data['Company'].get('Name').lower(),data['Company'].get('Arrival date (MMDDYYYY)'))
        company_wordlist += combine_with_date(data['Company'].get('Name').capitalize(),data['Company'].get('Arrival date (MMDDYYYY)'))
    # Name + Department number
    if data['Company'].get('Name') and data['Target'].get('Current department number'):
        company_wordlist += combine_with_department(data['Company'].get('Name').lower(),data['Target'].get('Current department number'))
        company_wordlist += combine_with_department(data['Company'].get('Name').capitalize(),data['Target'].get('Current department number'))
    # Name alone
    if data['Company'].get('Name'):
        company_wordlist.append(data['Company'].get('Name').lower())
        company_wordlist.append(data['Company'].get('Name').capitalize())

    # Arrival date alone
    if data['Company'].get('Arrival date (MMDDYYYY)'):
        company_wordlist.append(data['Company'].get('Arrival date (MMDDYYYY)'))

    return company_wordlist


# Generates the whole wordlist
def generate_wordlist():
    print("\n[+] Generating the wordlist...")
    target_wordlist = generate_target_wordlist()
    print("[-] \tTarget topic generated.")
    family_wordlist = generate_family_wordlist()
    print("[-] \tFamily topic generated.")
    holidays_wordlist = generate_holidays_wordlist()
    print("[-] \tHolidays topic generated.")
    areas_of_interest_wordlist = generate_areas_of_interest_wordlist()
    print("[-] \tAreas of interest topic generated.")
    company_wordlist = generate_company_wordlist()
    print("[-] \tCompany topic generated.")

    wordlist = target_wordlist + family_wordlist + holidays_wordlist + areas_of_interest_wordlist + company_wordlist # + ...

    if EXPORT_INFO:
        export_json_info(EXPORT_FILENAME)

    if WRITE_OUTPUT:
        save_wordlist(wordlist, OUTPUT_FILENAME)
    else:
        print("\n[+] Printing the wordlist on standard output:\n")
        for word in wordlist:
            print(word)




# Main function
if __name__ == "__main__":
    init_parser()
