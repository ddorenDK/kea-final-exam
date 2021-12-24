import json
import os
import shutil
from bs4 import BeautifulSoup
import requests
import pdfplumber


#Place to test and update methods



database_url = 'https://www.epddanmark.dk/epd-databasen/'
base_url = 'https://www.epddanmark.dk'
# Directory Name and Location that will store pdfs
temp_directory_location = "./temp_pdf"

# Location and name of the stored pdf
temp_pdf_location = "./temp_pdf/single_epd.pdf"




##################################################################   SITE TO LINKS   #################################################################################
# 1

def get_epd_urls(base_url, database_url, debug = False, limit = -1):
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

########################################################################################################################################################################
##################################################################   LINKS TO PDFS   ###################################################################################

#2.1
# Downloads the pdf from a single URL
def link_to_pdf(url, debug = False):

    if not os.path.exists(temp_directory_location):
        # DEBUG
        if debug:
            print (f'>Method: link_to_pdf \nFound no temp_pdf directory \n>Creating folder at {temp_directory_location} \n')
        # -----
        os.makedirs(temp_directory_location)
    else:
        # DEBUG
        if debug:
            print (f'>Method: link_to_pdf \n>Found existing temp_pdf directory \n')
        # -----
            
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
    else:
        # DEBUG
        if debug:
            print (f'>Method: links_to_pdfs \n>Found existing temp_pdf directory \n')
        # -----

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



########################################################################################################################################################################
##################################################################   FILTER   ##########################################################################################

#3.1
# Gets a pdf and returns a STRING with the rows containing GWP or GWP-total
def extract_gwp_from_pdf(pdf_location, debug=False):
    found_rows = ''
    # DEBUG
    if debug:
        print(f'>Starting extraction from the pdf at {pdf_location}')
    # -----
    pdf = pdfplumber.open(pdf_location)
    # DEBUG
    if debug:
        print(f'>Pages in the epd pdf file: {len(pdf.pages)}')
        # Variable used for iteration
        it = 1
    # -----
    for page in pdf.pages:
        # DEBUG
        if debug:
            print(f'>Started checking for tables in page nr {it}/{len(pdf.pages)}')
            it += 1
        # -----
        #rows will be a list of lists
        rows = page.extract_table()
        if not rows is None:
            for row in rows:
                #now working with a sinlge list
                if 'GWP-total' in row or 'GWP' in row:
                    if debug: 
                        print(f'Found a row containing GWP or GWP total on a table on the page {it}/{len(pdf.pages)}')
                        print(f'Row containing \'GWP\' or \'GWP-total\': {row}')
                    rowToSave = list_to_string(row)
                    found_rows = found_rows + rowToSave + ' | '
                    print(rows[0])
    return found_rows


########################################################################################################################################################################
##################################################################   FLUSHING   ########################################################################################

#Removes all the contents of the temp_json folder, !use only after the python object has been created!
def flush_temp_json():
    filelist = [ f for f in os.listdir('./temp_json') if f.endswith(".json") ]
    for f in filelist:
        os.remove(os.path.join('./temp_json', f))

def flush_temp_pdf():
    filelist = [ f for f in os.listdir('./temp_pdf') if f.endswith(".pdf") ]
    for f in filelist:
        os.remove(os.path.join('./temp_pdf', f)) 

def flush_all():
    try:
        flush_temp_json()
    except (FileNotFoundError) as e: 
        print(f'>WARNING \n>Could not flush temp_json, directory not found')
        print(f'Error : {e}')
    try: 
        flush_temp_pdf()
    except (FileNotFoundError) as e: 
        print(f'>WARNING \n>Could not flush temp_pdf, directory not found')
        print(f'Error : {e}')

########################################################################################################################################################################
################################################################   TOOLS   #############################################################################################

# using list comprehension 
# listToStr = ' '.join([str(elem) for elem in s]) 
def list_to_string(list):
    string_output = ''
    for item in list:
        string_output = string_output + ' ' + str(item)
    return string_output


########################################################################################################################################################################
############################################################   SAVE THE TABLE   ########################################################################################

def move_table_to_saved(table, debug = False):
    if debug:
        print(f'>Method: move_table_to_saved \n>Saving {table}')
    if not os.path.exists("./saved_tables"):
        os.makedirs("./saved_tables")

    shutil.move(table, "./saved_tables")

########################################################################################################################################################################
#################################################################   TESTING   ##########################################################################################

# 1.1
# # # Get a list with urls to pdfs
pdf_links_list = get_epd_urls(base_url, database_url, limit = 10)

# # # # 2.1
# # # # # Download the pdf from the urls
# link_to_pdf(pdf_links_list[0], debug = True)

# # # 1.2
# # # Download all pdfs from list of urls
links_to_pdfs(pdf_links_list, debug = True)

# Extract the tables from a pdf
# pdf_to_tables("./temp_pdf/single_epd.pdf")

# extracted_tables = get_list_json_tables(debug=True)

# exact_table = find_exact_table(extracted_tables)

# move_table_to_saved(exact_table, debug=True)

# flush_all()




