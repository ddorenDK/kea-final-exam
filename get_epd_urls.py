import requests
from bs4 import BeautifulSoup


def get_epd_urls(base_url, database_url, debug = False, limit = 30):
    # arg 1 = base_url of the site used in the creation of the output links
    # arg 2 = url with the location of the pdfs
    it = 1
    url_list = []
    page = requests.get(database_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll('div', {'class': 'small-12 medium-12 large-12 columns'})
    # DEBUG
    if debug:
        print(f'>Starting Method get_epd_urls\n>Files to be extracted{limit}')
    for r in results:
        if it > limit and limit > 0:
            break
        a_list = r.findAll('a')
        if len(a_list) > 0:
            href = a_list[1]['href']
            if not href.startswith('/media'):
                continue
            url_list.append(base_url + href)
            it += 1
    # DEBUG 
    if debug:
        print (f'>Method get_epd_urls \n>URL provided {database_url} \n>URLS extracted: {len(url_list)} \n')
    # ----- 
    return url_list