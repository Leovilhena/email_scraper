import os
import csv

def openFile(path):
    try:
        with open(path,'r') as address_list:
            link_list = list(set(link.replace("\n", "") for link in address_list if link))
            return link_list

    except:
        print('Error while opening the file!')
        return None

def exportCSV(emails):
    if not emails:
        return

    try:
        print('Please write file name (with no extension)')
        output_file = input('If you write the same file name, new emails will be appended to the file: ')

        with open(output_file + '.csv', 'a+') as out_stream:
            out_writer = csv.writer(out_stream)
            for line in emails:
                out_writer.writerow([line])

        print('File sucessfully exported %s.csv' % output_file)
        return

    except:
        print('An error has occured')
        return None





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

    elif u_input == 'o':
        path = input('Type file name: ')
        link_list = openFile(path)
        if link_list:
            for link in link_list:
                # UNDER_CONSTRUCTION
                return False
        else:
            return True
    elif u_input == 'h':
        print('\nJust type a website address to get contacts (english)')
    #    print('Type O to open a file')
        print('Press Q to quit')
        return True

    return False
