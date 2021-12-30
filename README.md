# Work In Progress

## Python
- The python program should generate a json file with all the materials
- Progress can be tracked in the app.py file, named so because it's pleasant to the eye 
- ~~Currently rewriting and testing the whole thing using tabula as the main pdf tool, then it'll be restructured~~
- ~~Currently testing pdfplumber~~
- The project will use pdfplumber as the tool for extracting data from pdfs
- pdfblumber doesn't work properly with form data, will have to either go back or make a method that will extract data from form fields :( 

### Current Iteration: 
  - Restructure everything 
  - Add option for debug
  - Improve Comments & Readability
  - Add the option for argument

## Docker*
- Only used during development.
- Dockerfile frequently changed, saved and deleted locally to prevent golden images (the saving part)


## Azure Pipelines*
- The pipeline should run once a month and generate a new updated json file artifact

## Github Pages*
- The web page acts as a place to see the generated json artifact

### * Current Tasks 
- Try tabula and pdfplumber for table extraction
- Rewrite and Restructure initial the code
