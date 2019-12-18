# UNIVERSITY OF GUELPH COURSE SCRAPER
# This program creates a CSV file containing course, restrictions, and prerequisites for every course on webadvisor
# Use this for something cool! (email me if you do thornej@uoguelph.ca)
# Enjoy! :)

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("chromedriver.exe");

titles = []  # List to store name of the product
restricts = []  # List to store the restrictions
prereqs = []  # List to store the prerequisites
links = []  # List to store links to all the links to courses

driver.get("https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/index.shtml")
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

linkbar = soup.find('div', attrs={'class': 'subnav'})

# gets the links for all the courses
for link in linkbar.findAll('a', href=True):
    links.append(link['href'][1:])  # [1:] to get rid of leading period in link

# gets rid of the first link because its just in the index link
links.pop(0)

for link in links:
    driver.get("https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12" + link)

    # getting the data
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    #  loops through all courses on site
    for a in soup.findAll('div', attrs={'class': 'course'}):

        #  gets name of course
        name = a.find('tr', attrs={'class': 'title'})

        #  gets course restrictions
        if a.find('tr', attrs={'class': 'restrictions'}):
            restrictions = a.find('tr', attrs={'class': 'restrictions'})
            restricts.append(restrictions.text.strip().replace('\n', ' '))
        else:
            restricts.append("NONE")

        #  gets course prerequisites
        if a.find('tr', attrs={'class': 'prereqs'}):
            prerequisites = a.find('tr', attrs={'class': 'prereqs'})
            prereqs.append(prerequisites.text.strip().replace('\n', ' '))
        else:
            prereqs.append("NONE")

        titles.append(name.text.strip())

#  sends all data to a TSV 
df = pd.DataFrame({'Course Title': titles, 'Restrictions': restricts, 'Prerequisites': prereqs})
df.to_csv('courses.tsv', index=False, encoding='utf-8', sep="\t")

print("finished")