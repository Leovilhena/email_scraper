#!/usr/bin/env python3
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlsplit, urljoin


def urlBuilder(url):
    """Builds our url, if not well written"""

    if url.startswith('//',0,2):
        url = url.replace('//','')

    # Splits url for checking, useful to add more features later
    split_url = urlsplit(url)

    # if not given which protocol, put http as standard
    if not split_url.scheme:
        return 'http://' + url
    else:
        return url


def seleniumRequest(url):
    """Make a request through selenium and PhantomJS headless browser"""

    # Path for browser, you can have a different one. Remember to install it with NodesJS
    driver = webdriver.PhantomJS(executable_path='/usr/local/bin/PhantomJS')
    # Simple GET request
    driver.get(url)
    try:
        # Try to wait until get all page and JS scripts loaded.
        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, 'loadedButton')))
    finally:
        # Get all rendered HTML
        pageSource = driver.page_source
        # Close browser
        driver.close()

        return pageSource


def makeRequest(url):
    """Requests given url """

    # Sanity check
    if not url:
        return
    # Headers for request mobile version
    headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1",
                "Accept-Language":"en-US,en;q=0.5"}
    try:
        print('\nCrawling ...')
        # Our main request
        html  = requests.get(url, headers=headers)
        # Check for OK status and return html body
        if html.status_code == requests.codes.ok:
            print('Page fetched!')
            print(url)
            return html.text

    except requests.exceptions.RequestException as e:
        print('Connection problems:')
        print(e)
        return None
