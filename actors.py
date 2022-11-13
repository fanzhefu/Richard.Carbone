import requests
from bs4 import BeautifulSoup
import html5lib

URL = "https://malpedia.caad.fkie.fraunhofer.de"
ACTORS = 'actors'

page = requests.get(URL+'/'+ACTORS)
soup = BeautifulSoup(page.content, "html5lib")   

names = [name.text for name in soup.find_all(class_="common_name")]
akas = [ aka['title'] if (aka := row.find(class_='fa fa-info-circle')) != None else 'aka: N/A' for row in soup.find_all(class_="clickable-row")]
synonyms = [ (synonym:= row.find(class_='synonyms')).text  for row in soup.find_all(class_="clickable-row")]

actors =list( zip(names, akas, synonyms) )

links = [URL+link['data-href'] for link in soup.find_all( class_="clickable-row")]


# go through each page to extract the description 
i = 0
for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html5lib")   
    print(actors[i])
    i += 1
    print(soup.body.find_all(class_="col-xl-12")[1].select("p")[0].text.strip())
