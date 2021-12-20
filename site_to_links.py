import requests
from bs4 import BeautifulSoup


def get_epd_urls(base_url, database_url, debug = False):
    # arg 1 = base_url of the site used in the creation of the output links
    # arg 2 = url with the location of the pdfs
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
    # DEBUG 
    if debug:
        print (f'>get_epd_urls Method \n>URL provided {database_url} \n>URLS extracted: {len(url_list)}')
    # ----- 
    return url_list



