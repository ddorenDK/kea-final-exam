import os
import pdfplumber


# Tools: list to string
# using list comprehension 
# listToStr = ' '.join([str(elem) for elem in s]) 
def list_to_string(list):
    string_output = ''
    for item in list:
        string_output = string_output + ' ' + str(item)
    return string_output

#2.1
# Gets a pdf and returns a STRING with the rows containing GWP or GWP-total
def extract_gwp_from_pdfs(pdfs_location='./temp_pdf', debug=False):
    #TODO 
    # Make it work with form data, currently form data is seen as None
    # The solution can be found on those pages:
    # https://github.com/jsvine/pdfplumber/issues/120
    # https://github.com/jsvine/pdfplumber

    #list that will hold found gwps in a string format
    found_gwps = []
    for file in os.listdir(pdfs_location):
        #String that will contain information about one extracted epd from a pdf
        found_gwp = ''
        pdf_location = pdfs_location + '/' + file
        # DEBUG
        if debug:
            print(f'>>>Starting extraction from the pdf at {pdf_location}<<<')
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
            if rows is not None:
                for row in rows:
                    #now working with a sinlge list
                    if 'GWP-total' in row or 'GWP' in row:
                        if debug: 
                            print(f'Found a row containing GWP or GWP total on a table on the page {it}/{len(pdf.pages)}')
                            print(f'Row containing \'GWP\' or \'GWP-total\': {row}')
                        rowToSave = list_to_string(row)
                        found_gwp = found_gwp + rowToSave + ' | ' + file + ' /'
                        # print(rows[0])
                        found_gwps.append(found_gwp)
    return found_gwps

def string_to_json(gwp_list):
    #TODO 
    #Utter bullshit and crap
    #Make this actually work, !but fix the form data first!
    with open('epd_data.txt', 'w') as f:
        f.close()
    with open('epd_data.txt', 'a') as f:
            for gwp in gwp_list:
                print(f'>{gwp}')
                f.write(gwp)
                f.write("\r\n")