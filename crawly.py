#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urljoin
from utils import openFile, logger, printResults, helper
from requests_handler import urlBuilder, makeRequest

# My second email crawler

# Functionalities to be added soon:
# - Fix UNDER_CONSTRUCTION
# - Identify language and improve for Portuguese and Polish
# - Save info in a database
# - Add Selenium Request for JS websites
#
# DONE IS BETTER THAN PERFECT!
#


def getEmails(url_input):
    """Get all links from page and look for contact page and emails for contact"""

    # Variables in scope
    global contact_pages
    global emails

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

    # Iteration on BeautifulSoup object: Gets 'href' attrs from 'a' tags
    for a in bsObj.findAll('a',attrs={'href':[regex_contact_about, regex_email]}):
        # Get text from tag
        a = a.get('href')

        # if it's an email add to emails set
        if regex_email.search(a):
            emails.add(a.replace('mailto:',''))
        # if it's a link check if internal or external
        elif regex_contact_about.search(a):
            # Internal link
            if regex_internal_link.search(a):
                # Fix url
                url = urljoin(my_url,a)
                if url not in contact_pages:
                    contact_pages.add(url)
                    getEmails(url)
            # External link
            else:
                if a not in contact_pages:
                    contact_pages.add(a)
                    getEmails(a)
    return


# Welcome prints
print('Type H for help')
print('Type Q to exit')
#print('Type O to open a file')

# Variables declaration
contact_pages = set()
emails = set()

# Infinite loop for running
def main():
    while(True):

        # Getting url from input
        try:
            url_input = input('\nWebsite url: ')
        except:
            print('An error has occurred')
            exit(1)

        # Checking input for other options
        if helper(url_input):
            continue
        else:

            # Call of our function to get emails
            getEmails(url_input)

            # Print results
            printResults(emails)

            # UNDER_CONSTRUCTION Compiling all results
            #final_results ={'url':my_url,'title':title, 'topics':about, 'emails': emails,'meta':[meta['content'] for meta in metas]}

            # UNDER_CONSTRUCTION Saving/logging activities
            #logger(final_results)


if __name__ == '__main__':
    main()
