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
# Get A list of all files generated at the input directory
def get_list_json_tables(debug = False):
    #List of all the files generated by camelot
    tableList = []
    for root, dirs, files in os.walk("./temp_json"):
        for file in files:
            toAppend = os.path.join("./temp_json",file).replace('\\', '/')
            tableList.append(toAppend)
    if debug:
        print(f'>Table Filtration Begins \n>Method: get_list_json_tables \n>Tables in the list: {len(tableList)} \n')

    return tableList

#3.2
#Find the exact table and returns its location
def find_exact_table(tableList, debug=False):
    for table in tableList:
        jsonFile = json.load(open(table))
        
        #TODO
        #Replace this if with a nicer thing, maybe add a list of all the needed values; this problem will solve itself with improved accuraty (using GhostScraper)
        if 'ENVIRONMENTAL IMPACTS PER KG' in str(jsonFile) or 'RESOURCE USE PER DECLARED UNIT' in str(jsonFile) or 'Miljøpåvirkninger, 15 cm tyk væg' in str(jsonFile):
            if debug: 
                print(f'>Method: find_exact_table \n>Found Table at {table} !\n')
            #TODO, get the exact table location by splitting the table after page - <> and table - <> 
            #will greatly improve accuracy
            #table_location = table.split("word",1)
            return table


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
# # Get a list with urls to pdfs
pdf_links_list = get_epd_urls(base_url, database_url)

# # # 2.1
# # # # Download the pdf from the urls
# link_to_pdf(pdf_links_list[0], debug = True)

# # # 1.2
# # # Download all pdfs from list of urls
links_to_pdfs(pdf_links_list)

# pdf = pdfplumber.open("./temp_pdf/single_epd.pdf")

# for page in pdf.pages:
#     table = page.extract_table()
#     print(table) 























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



