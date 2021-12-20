import requests
import os

# Directory Name and Location that will store pdfs
temp_directory_location = "./temp_pdf"

# Location and name of the stored pdf
temp_pdf_location = "./temp_pdf/single_epd.pdf"

# Downloads the pdf from a single URL
def link_to_pdf(url):

    if not os.path.exists(temp_directory_location):
         os.makedirs(temp_directory_location)
            
    r = requests.get(url, allow_redirects=True)
    with open(temp_pdf_location, 'wb') as f:
        f.write(r.content)

#TESTING
# link_to_pdf("https://www.epddanmark.dk/media/qqcf2ybh/md-18009-en-vola.pdf")