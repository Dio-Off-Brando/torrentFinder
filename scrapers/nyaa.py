import requests
from bs4 import BeautifulSoup

# shenanigans to import file from parent folder
import sys
sys.path.append('../')
import utils



url = "https://nyaa.si/?f=0&c=1_0&q={query}&p={page}"


def search(query):
    page=1
    results = []
    query = query.replace(' ', '%20')
    #basic bs4 init stuff
    r = requests.get(url.format(query=query, page=page))

    soup = BeautifulSoup(r.text, 'html.parser')
    torrents = soup.find_all('table')[0]


    #cleaning list of table elements
    list_of_torrrents = torrents.find_all('tr')
    list_of_torrrents.pop(0)
    
    for tr in list_of_torrrents:
        entry = {}

        entry["title"] = tr.find_all("td")[1].a['title']
        entry['magnet'] = {}
        entry["magnet"]['link'] = tr.find_all('td')[2].find_all('a')[1]['href']
        entry['magnet']['seeds'] = tr.find_all('td')[5].string
        entry['magnet']['quality'] = utils.guess_quality(entry['title'])
        entry["source"] = "nyaa"
        results.append(entry)
    


    return results 
