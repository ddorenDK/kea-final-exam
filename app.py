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

    # used to provide unique file names for the pdfs
    iteration = 1

    for url in urls:
        full_temp_pdf_location = temp_directory_location + '/' + 'epd_' + str(iteration) + '.pdf'
        r = requests.get(url, allow_redirects=True)
        # DEBUG
        if debug:
            print(f'Extracted pdf from {url}')
            print(f'>Saving pdf to {full_temp_pdf_location}')
        # -----
        with open(full_temp_pdf_location, 'wb') as f:
            f.write(r.content)

        iteration = iteration + 1

########################################################################################################################################################################
##################################################################   PDFS TO TABLES   ##################################################################################

#2.2
#Extracts all tables in a json format from a given pdf file at the temp_pdf_location.
#Exports the found tables to the temp_json directory
def pdf_to_tables(temp_pdf_location, debug = False):
    if not os.path.exists("./temp_json"):
        # DEBUG
        if debug:
            print (f'>Method: pdf_to_tables \n>Found no temp_json folder \n>Creating folder at ./temp_json \n')
        # -----
        os.makedirs("./temp_json")
    else:
        # DEBUG
        if debug:
            print (f'>Method: pdf_to_tables \n>Found existing temp_json folder \n')
        # -----

    #tables = camelot.read_pdf(temp_pdf_location, flavor='lattice', pages='all')
    df = tabula.read_pdf(temp_pdf_location, pages='all')
    # print(f'Found {tables.__len__()} tables in {temp_pdf_location}')
    # tables.export('temp_json/table.json', f='json')


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
############################################################   SAVE THE TABLE   ########################################################################################

def move_table_to_saved(table, debug = False):
    if debug:
        print(f'>Method: move_table_to_saved \n>Saving {table}')
    if not os.path.exists("./saved_tables"):
        os.makedirs("./saved_tables")

    shutil.move(table, "./saved_tables")

########################################################################################################################################################################
############################################################   SAVE THE TABLE   ########################################################################################

# 1.1
# # # Get a list with urls to pdfs
# pdf_links_list = get_epd_urls(base_url, database_url)

# # # # 2.1
# # # # # Download the pdf from the urls
# link_to_pdf(pdf_links_list[0], debug = True)

# # # 1.2
# # # Download all pdfs from list of urls
# links_to_pdfs(pdf_links_list)

# pdf = pdfplumber.open("./temp_pdf/single_epd.pdf")

# for page in pdf.pages:
#     print("///////////////////////////////////////////////////////")
#     table = page.extract_tables()
#     for lists in table:
#         temp_epd = ""
#         for list in lists:
#             print(f'list = {list}')
#         # print(f'result after loop: {temp_epd}')

def list_to_string(list):
    string_output = ''
    for item in list:
        string_output = string_output + ' ' + str(item)
    return string_output


# list = ['GWP-total', None, '1.95E+00', '8.54E-02', '4.69E-02', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', '7.89E-06', '8.51E-03', '2.53E-04', '0', '2.08E-02']
# if 'GWP-total' in list:
#     print('True')
#     saved_list = save_list(list)
# else:
#     print('False')

# print(saved_list)

debug = True
#Extract a row of data with the first entry GWP or GWP-total
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

toPrint = extract_gwp_from_pdf("./temp_pdf/single_epd.pdf", True)
print(toPrint)

# list1 = ['Water use', None, '0', None, 'm3', None, None]
# list2 = ['GWP-luluc', None, '1.05E-03', '6.88E-04', '5.83E-07', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', '1.14E-08', '6.86E-05', '3.65E-07', '0', '-7.20E-06']
# list3 = ['GWP-total', None, '1.95E+00', '8.54E-02', '4.69E-02', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', 'MNR', '7.89E-06', '8.51E-03', '2.53E-04', '0', '2.08E-02']

# if 'GWP-total' in list1 :
#     print('list1 True')

# if 'GWP-total' in list2 :
#     print('list2 True')

# if 'GWP-total' in list3 :
#     print (list3)
#     print('list3 True')
































# Extract the tables from a pdf
# pdf_to_tables("./temp_pdf/single_epd.pdf")

# extracted_tables = get_list_json_tables(debug=True)

# exact_table = find_exact_table(extracted_tables)

# move_table_to_saved(exact_table, debug=True)

# flush_all()

# dfs = tabula.read_pdf("./temp_pdf/single_epd.pdf", pages='all')

# tabula.convert_into("./temp_pdf/single_epd.pdf", "output.json", output_format="json", pages='all', lattice=True)
# tabula.io.build_options(pages=all, guess=False, area=None, relative_area=False, lattice=True, stream=False, password=None, silent=None, columns=None, format=json, batch=True, output_path="./tabula_output", options='')
# tabula.io.convert_into_by_batch("./temp_pdf", output_format='json', pages='all', lattice = True, guess=False)



