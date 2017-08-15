import datetime
import json
import os

def openFile(path):
    try:
        with open(path,'r') as address_list:
            link_list = list(set(link.replace("\n", "") for link in address_list if link))
            return link_list

    except:
        print('Error while opening the file!')
        return None

def logger(results, loaded={}):
    # Now time as key for dictionary
    date = str(datetime.datetime.now())

    # Check for file in disk
    if os.path.isfile('emails_list.json'):
        # Open file and load, if not a JSON create a dict for it
        with open('emails_list.json', 'r') as log:
            loaded = json.load(log)

    # Open file and save as a JSON
    with open('emails_list.json', 'w+') as log:
        loaded[date] = results
        json.dump(loaded, log, indent=2)


def printResults(emails):
    """Just print our results """

    # Print for emails
    if not emails:
        print('\nNo email found :(\n')
    else:
        print('\nContact emails:')
        for email in emails:
            print(email)


def helper(u_input):
    """Our instructions and program options"""

    # Change user input to lower
    u_input = u_input.lower()

    # Check for program options
    if u_input == 'q':
        exit(0)
    # UNDER_CONSTRUCTION
    #elif u_input == 'o':
    #    path = input('Type file name: ')
    #    link_list = openFile(path)
    #    if link_list:
    #        for link in link_list:
    #            print('\n' + link)
                # under_construction
    #            return False
        #else:
        #    return True
    elif u_input == 'h':
        print('\nJust type a website address to get contacts (english)')
    #    print('Type O to open a file')
        print('Press Q to quit')
        return True

    return False
