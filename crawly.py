#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urljoin
from difflib import SequenceMatcher
from utils import openFile, exportCSV, printResults, helper
from requests_handler import urlBuilder, makeRequest

# My second email crawler

# Functionalities to be added soon:
# - Fix UNDER_CONSTRUCTION
# - Identify language and improve for Portuguese and Polish
# - Save info in a database
# - Add Selenium Request for JS websites
# - Go to external website and find contacts related to base website (based on emails domains outside base scoupe)
# - Divide getEmails function into different functions
# - Add log wrapper
# - Add sequenceMatcher control through command line
#
# DONE IS BETTER THAN PERFECT!
#

def similar(url, link):
    """Check for ratio similarities between two strings"""
    # You can tweak this percentage if you're not getting so much emails or errors
    # Sometimes domains can have different addresses
    if SequenceMatcher(None, url, link).ratio() > 0.6:
        return True
    else:
        return False

def getEmails(url_input, contact_pages, emails):
    """Get all links from page and look for contact page and emails for contact"""

    # Builds url
    my_url = urlBuilder(url_input)

    # Makes a GET request
    url_text = makeRequest(my_url)

    # Sanity check
    if not url_text:
        return

    # Creates a BeautifulSoup Object for scraping
    try:
        bsObj = BeautifulSoup(url_text, "lxml")
    except AttributeError as e:
        print('Error: Lack of ingredients')

    # Sanity check
    if not bsObj:
        return

    # Compiling REGEX
    regex_contact_about = re.compile(r"[./a-z0-9-]+(contact)|(about)[./a-z0-9-]+", re.I)
    regex_email = re.compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", re.I)
    regex_internal_link = re.compile(r"(^/[a-z0-9]+/).+")

    # Get emails from paragraphs
    for p in bsObj.findAll('p'):
        emails.update(regex_email.findall(p.get_text()))

    # Iteration on BeautifulSoup object: Gets 'href' attrs from 'a' tags
    for a in bsObj.findAll('a',attrs={'href':[regex_contact_about, regex_email]}):
        # Get text from tag
        a = a.get('href')

        # if it's an email add to emails set
        email = regex_email.search(a, re.I)
        if email:
            emails.add(email[0])

        # if it's a link check if internal or external
        elif regex_contact_about.search(a):
            # Internal link
            if regex_internal_link.search(a):
                # Url fix
                url = urljoin(my_url,a)
                # Check if not contacted this page before and if we are in the same domain
                if url not in contact_pages and similar(url,a):
                    # Add to do not crawl again list
                    contact_pages.add(url)
                    # Function recursion
                    getEmails(url, contact_pages, emails)
            # External link
            else:
                # Check if not contacted this page before and if we are in the same domain
                if a not in contact_pages and similar(my_url,a):
                    # Add to do not crawl again list
                    contact_pages.add(a)
                    # Function recursion
                    getEmails(a, contact_pages, emails)
    return emails


# Welcome prints
print('Type Q to exit')
print('Type O to open a file')


# Infinite loop for running
def main():
    while(True):
        contact_pages = set()
        emails = set()

        # Getting url from input
        try:
            url_input = input('\nWebsite url: ')
        except:
            print('An error has occurred')
            exit(1)

        # Checking input for other options
        if helper(url_input):
            path = input('Type file name: ')
            link_list = openFile(path)
            if link_list:
                for link in link_list:
                    getEmails(link, contact_pages,emails)
                printResults(emails)
            else:
                continue

        else:
            # Call of our function to get emails
            getEmails(url_input, contact_pages,emails)

            # Print results
            printResults(emails)

            if emails:
                export = input('\nDo you want to export these emails? (y/n): ')
                if export.lower() == 'y' or export.lower() == 'yes':
                    exportCSV(emails)



if __name__ == '__main__':
    main()
