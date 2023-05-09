# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:36:22 2023

@author: fan.z
"""

# /usr/bin/env python
import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup

# Cybersecurity Alerts & Advisories
DELAY = 5  # seconds
WEBSITE = "https://www.cisa.gov"
#PAGES = 281  # get THIS NUMBER from the website
PAGES = 1
# read all user agents in
if os.path.exists('user-agents.txt'):
    USER_AGENTS = open('user-agents.txt', 'r', encoding='utf-8').readlines()
else:
    sys.exit(
        'user-agents.txt file not found, download the file here from https://github.com/fanzhefu/luna.thecat/tree/main/common-files')

# get the url of all the aticles
urls = []
print('scraping all the links ... ... ')
for page in range(PAGES):
    url_page = WEBSITE + \
               '/news-events/cybersecurity-advisories?page=' + str(page)
    random_user_agent = random.choice(USER_AGENTS).rstrip()
    headers = {'User-Agent': random_user_agent}
    page = requests.get(url_page, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    titles = soup.find_all(class_="c-teaser__title")

    #for i in range(len(titles)):
    #    urls.append(titles[i].find("a")['href'])
    for i, title in enumerate(titles):
        urls.append(title.find("a")['href'])
print('links scraping done !!!' + '\n')

# write all files out to alerts/
if not os.path.exists('alerts'):
    os.makedirs('alerts')
# loop through the urls and get the title, released date and alert code of the article,
# then save into a file, sleep delayed seconds between two connections to slow down this process.
count = 0
for url in urls:
    print(str(count) + ' of ' + str(len(urls)) + '\nreading from: ' + url + '')
    random_user_agent = random.choice(USER_AGENTS).rstrip()
    headers = {'User-Agent': random_user_agent}
    page = requests.get(WEBSITE + url, headers=headers)
    print('status_code: ', page.status_code)
    if page.status_code != 200:
        continue
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find_all(class_="c-page-title__title")[0].text.strip()
    article = soup.find_all(class_="l-page-section__content")
    content = article[0].text
    date_and_code = soup.find_all(class_="c-field__content")
    released = 'Released: ' + date_and_code[0].text
    alert_code = '' if len(
        date_and_code) == 1 else 'Alert Code: ' + date_and_code[1].text

    file_name = 'alerts/' + url.split('/')[-1] + '.txt'
    print('writing file: ' + file_name + '\n')
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(title + '\n' + released + alert_code + content)
    time.sleep(DELAY)  # slow down, otherwise your ip will be blocked
    count += 1

print('All done ... ... ')
