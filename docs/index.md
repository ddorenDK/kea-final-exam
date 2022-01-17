# Welcome to My Final Exam Project


## PDF Data Extraction Branches

### Camelot
[Camelot Branch](https://github.com/ddorenDK/kea-final-exam/tree/camelot)

Requirements:
- Python
- Ghostscript

Output:
- Each table is extracted into a pandas DataFrame, which seamlessly integrates into ETL and data analysis workflows. You can also export tables to multiple formats, which include CSV, JSON, Excel, HTML, Markdown, and Sqlite.

### Tabula
[Tabula Branch](https://github.com/ddorenDK/kea-final-exam/tree/tabula)

Requirements:
- Java 8+
- Python 3.6+

Output:
- Tabula extracts tables from a PDF into a DataFrame, or a JSON. It can also extract tables from a PDF and save the file as a CSV, a TSV, or a JSON

### PDFplumber
[pdfplumber Branch](https://github.com/ddorenDK/kea-final-exam/tree/pdfplumber)

Requirements:
- Python
- ImageMagick and ghostscript for visual debugging

## Stream vs Lattice PDF Data Extraction methods
[Link to the Information](https://camelot-py.readthedocs.io/en/master/user/how-it-works.html)

### Stream

Stream can be used to parse tables that have whitespaces between cells to simulate a table structure. It is built on top of PDFMiner’s functionality of grouping characters on a page into words and sentences, using margins.

### Lattice

Lattice is more deterministic in nature, and it does not rely on guesses. It can be used to parse tables that have demarcated lines between cells, and it can automatically parse multiple tables present on a page.

It starts by converting the PDF page to an image using ghostscript, and then processes it to get horizontal and vertical line segments by applying a set of morphological transformations (erosion and dilation) using OpenCV.
