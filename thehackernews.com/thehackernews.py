# /usr/bin/env python
import os
import sys
import time
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup


WEBSITE = 'https://thehackernews.com'
DELAY = 5  # 5 seconds btw connectiona

# read all user agents in
if os.path.exists('user-agents.txt'):
    USER_AGENTS = open('user-agents.txt', 'r',  encoding='utf-8').readlines()
else:
    sys.exit('user-agents.txt file not found, download the file here from https://github.com/fanzhefu/luna.thecat/tree/main/common-files')
    
    
updated_max = datetime.now()
first_day = datetime.strptime('Sep 19, 2012', '%b %d, %Y')
url = WEBSITE + '/search/label/Cyber%20Attack'
urls = []
loop = True
print('scraping all the links ... ... ')
while loop:
    random_user_agent = random.choice(USER_AGENTS).rstrip()
    headers = {'User-Agent': random_user_agent}    
    page = requests.get(url, headers)
    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.find_all(class_="story-link")
    dates = soup.find_all(class_="h-datetime")

    for l in links:
        link = l.get_attribute_list('href')[0]
        if 'wing-newsfeed-3' not in link:
            urls.append(link)

    for d in dates:
        dt = datetime.strptime(d.text[1:], '%b %d, %Y')
        if dt < updated_max:
            updated_max = dt

    url = WEBSITE + '/search/label/Cyber%20Attack?updated-max=' + \
        updated_max.strftime("%Y-%m-%d") + \
        'T20:29:00%2B05:30&max-results=20&by-date=false'
    if updated_max == first_day:
        loop = False
print('links scraping done !!!' + '\n')
# write all files out to results/
if not os.path.exists('results'):
    os.makedirs('results')

i = 1
for url in urls:
    print( str(i)+' of '+str(len(urls))+' reading from: ' + url + '')
    random_user_agent = random.choice(USER_AGENTS).rstrip()
    headers = {'User-Agent': random_user_agent}
    page = requests.get(url, headers=headers)
    print('    status_code: ', page.status_code)
    if page.status_code != 200: continue
    soup = BeautifulSoup(page.text, "html.parser")
    
    title = soup.find_all(class_='story-title')[0].text
    author = soup.find_all(class_='author')[1].text
    released = soup.find_all(class_='author')[0].text
    content = soup.find_all(class_='articlebody clear cf')[0].text

    file_name = 'results/' + url.split('/')[-1]
    print('writing to file: ' + file_name + '\n')
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(title + '\n' + author + '\n' + released + '\n' + content)
    time.sleep(DELAY)  # slow down, otherwise your ip will be blocked
    i +=1
    
print('All done, find the results under results folder ')
