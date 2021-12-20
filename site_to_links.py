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
    #Debug option
    if debug is True:
        print ("############### GET # EPD # URLS ##############")
        # Debug Mode On; get_epd_urls; Printing The Urls
        print (f'> Urls found: {len(url_list)}')
        print ("> Printing the URL List:")
        print (url_list)
        print ("###############################################")
    return url_list



