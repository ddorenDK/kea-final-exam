from get_epd_urls import get_epd_urls
from links_to_pdfs import links_to_pdfs
from pdfs_to_object import extract_gwp_from_pdf
import argparse


def main():

    # Argument Parser
    parser = argparse.ArgumentParser(description = "Extracts epd information from edpdanmark and outputs a json file with the data")
    parser.add_argument("--debug", default=False, help = "Debug Mode; True/False") 
    args = parser.parse_args()
    
    database_url = 'https://www.epddanmark.dk/epd-databasen/'
    base_url = 'https://www.epddanmark.dk'

    # 1.1
    # # # Get a list with urls to pdfs
    pdf_links_list = get_epd_urls(base_url, database_url, limit = 10, debug = args.debug)

    # 1.2
    links_to_pdfs(pdf_links_list, debug = args.debug)

    # 2
    extracted_gwps = extract_gwp_from_pdf(debug = args.debug)

    
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()