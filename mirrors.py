import requests
from bs4 import BeautifulSoup

url = 'http://mirrors.ubuntu.com/'

def get_HTML(url):
    response = requests.get(url)
    return response.text

def get_soup(url):
    html_of_page = get_HTML(url)
    return BeautifulSoup(html_of_page, 'html.parser')

def get_super_links(soup):
    a_tags = soup.find_all('a')
    all_links = [a.get('href') for a in a_tags]
    return [url + link for link in all_links]

def get_links(country_links):
    all_links = []
    for link in country_links:
        html_of_page = get_HTML(link)
        all_links += html_of_page.split("\n")
    return all_links

def get_list_of_mirrors():
    print("Retrieving list of Ubuntu mirror server URLs...")
    country_links = get_super_links(get_soup(url))
    links = get_links(country_links)
    links = list(dict.fromkeys(links))
    # print(links)
    print("List of mirror links successfully obtained")

# get_list_of_mirrors()
