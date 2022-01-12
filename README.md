# Work In Progress
[![Build Status](https://dev.azure.com/dori1411/kea-cs-final-project/_apis/build/status/ddorenDK.kea-final-exam?branchName=pipelines)](https://dev.azure.com/dori1411/kea-cs-final-project/_build/latest?definitionId=1&branchName=pipelines)

![Status Badge](https://dev.azure.com/dori1411/kea-cs-final-project/_apis/build/status/ddorenDK.kea-final-exam?branchName=main)

## Python
- The python program should generate a json file with all the material data
- The project will use pdfplumber as the tool for extracting data from pdfs
- pdfblumber doesn't work properly with form data, will have to either go back or make a method that will extract data from form fields properly, as currently it is extracted as     'None' :( 

## Docker
- Currently Only used during development.
- If the project switches to using tabula or camelot, the dockerfile will have an use in the Azure Pipeline

## Azure Pipelines
- The pipeline should run once a week and generate a new updated json file
- FAILS because: ##[error]No hosted parallelism has been purchased or granted. To request a free parallelism grant, please fill out the following form https://aka.ms/azpipelines-parallelism-request

## Github Pages
- The web page acts as a place to see the generated json artifact
- Work in progress

### * Current Tasks 
- Fix the form data reading with the pdfplumber
- Get an Azure subscription
