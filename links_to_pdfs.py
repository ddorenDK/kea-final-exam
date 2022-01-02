import requests
import os


temp_directory_location = "./temp_pdf"

# Location and name of the stored pdf
temp_pdf_location = "./temp_pdf/single_epd.pdf"


#1.2
# Downloads the pdf from a single URL
def link_to_pdf(url, debug = False):

    if not os.path.exists(temp_directory_location):
        # DEBUG
        if debug:
            print (f'>Method: link_to_pdf \nFound no temp_pdf directory \n>Creating folder at {temp_directory_location} \n')
        # -----
        os.makedirs(temp_directory_location)
    elif debug:
        print('>Method: link_to_pdf \n>Found existing temp_pdf directory \n')
    r = requests.get(url, allow_redirects=True)
    # DEBUG
    if debug:
        print(f'Extracted pdf from {url}')
    # -----
    with open(temp_pdf_location, 'wb') as f:
        f.write(r.content)

#1.2
# Downloads the pdfs from a list of URLs
def links_to_pdfs(urls, debug = False, temp_directory_location = "./temp_pdf"):

    if not os.path.exists(temp_directory_location):
        # DEBUG
        if debug:
            print (f'>Method: links_to_pdfs \nFound no temp_pdf directory \n>Creating folder at {temp_directory_location} \n')
        # -----
        os.makedirs(temp_directory_location)
    elif debug:
        print('>Method: links_to_pdfs \n>Found existing temp_pdf directory \n')
    for url in urls:
        # This will be the location of the url, the full download url is split by / and the last part is saved as the name of the pdf file using s.split('_')[-1]
        full_temp_pdf_location = temp_directory_location + '/' + url.split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        # DEBUG
        if debug:
            print(f'Extracted pdf from {url}')
            print(f'>Saving pdf to {full_temp_pdf_location}')
        # -----
        with open(full_temp_pdf_location, 'wb') as f:
            f.write(r.content)