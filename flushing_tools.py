import os

#Removes all the contents of the temp_json folder, !use only after the python object has been created!
def flush_temp_json():
    filelist = [ f for f in os.listdir('./temp_json') if f.endswith(".json") ]
    for f in filelist:
        os.remove(os.path.join('./temp_json', f))

#Removes all the contents of the temp_pdf folder, !use only after the python object has been created!
def flush_temp_pdf():
    filelist = [ f for f in os.listdir('./temp_pdf') if f.endswith(".pdf") ]
    for f in filelist:
        os.remove(os.path.join('./temp_pdf', f)) 

#Removes all the contents of both temp_pdf and temp_json folder, !use only after the python object has been created!
def flush_all():
    try:
        flush_temp_json()
    except FileNotFoundError as e:
        print('>WARNING \n>Could not flush temp_json, directory not found')
        print(f'Error : {e}')
    try: 
        flush_temp_pdf()
    except FileNotFoundError as e:
        print('>WARNING \n>Could not flush temp_pdf, directory not found')
        print(f'Error : {e}')

