import requests
from bs4 import BeautifulSoup

#Creates a list with download links for each epd available on epddanmark site
def get_epd_urls(base_url, database_url):
    url_list = []
    page = requests.get(database_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll('div', {'class': 'small-12 medium-12 large-12 columns'})
    for r in results:
        a_list = r.findAll('a')
        if len(a_list) > 0:
            href = a_list[1]['href']
            if not href.startswith('/media'):
                continue
            url_list.append(base_url + href)
    return url_list


