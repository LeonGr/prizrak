import requests
import re
from bs4 import BeautifulSoup

url = 'http://mirrors.ubuntu.com/'

def getHTML(url):
    response = requests.get(url)
    return response.content

def getSoup(url):
    htmlOfPage = getHTML(url)
    return BeautifulSoup(htmlOfPage, 'html.parser')

def getSupLinks(soup):
    aTags = soup.find_all('a')
    allLinks = [a.get('href') for a in aTags]
    return [url + link for link in allLinks]

def getLinks(countryLinks):
    allLinks = []
    for link in countryLinks:
        htmlOfPage = getHTML(link)
        reLinks = re.findall(r'http.*?\\n', str(htmlOfPage))
        for link in reLinks:
            if (link[-2:] == "\\n"):
                link = link[:-2]
            allLinks.append(link)
    return allLinks

def getListOfMirrors():
    countryLinks = getSupLinks(getSoup(url))
    links = getLinks(countryLinks)
    links = list(dict.fromkeys(links))
    print(links)

getListOfMirrors()
