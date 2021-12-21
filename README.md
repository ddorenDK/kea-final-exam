# Work In Progress

## Python
- The python script should generate a json file with all the materials
### Current Iteration: 
  - Restructure everything 
  - Add option for debug
  - Improve Comments & Readability
  - Add the option for arguments

## ~~Docker*~~
- ~~The Docker Container should have camelot properly installed to be able to extract the data faster (by removing the number of false tables extracted) and more accurate (by providing better tables)~~
- ~~The Pipeline will be responsible for the python script run in docker~~

## Azure Pipelines*
- The pipeline should run once a month and generate a new updated json file artifact

## Github Pages*
- The web page acts as a place to see the generated json artifact

### * Still Working on it  

Try using tabula instead of camelot
Requires java and python
Since all this runs on ubuntu in the pipeline shouldn't be a problem 
