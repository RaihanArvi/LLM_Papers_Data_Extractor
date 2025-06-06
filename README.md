# Papers Data Extractor

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Website](https://img.shields.io/badge/Website-Raihan_Arvi-red)](https://www.raihanarvi.com)

A command-line tool to batch-extract structured information from a collection of scientific papers based on a user-defined protocol spreadsheet. The tool reads Markdown versions of papers (or converts PDFs to Markdown), consults a protocol file specifying which fields to extract, and outputs the results as a CSV file.

Author : Raihan (Ray) Arvi

## Requirements
- Python 3.7 or newer
- Python packages:
- openai
- pandas
- numpy
- pymupdf4llm (optional, for on-the-fly PDF→Markdown conversion)
- openpyxl (for reading .xlsx protocol files)

## Instalation
```
git clone https://github.com/yourusername/your-repo.git
```
```
pip install -r requirements.txt
```


## Usage
```
python extract_data.py [options]
```
**Options:**

| Flag                | Description                                               | Default              |
|---------------------|-----------------------------------------------------------|----------------------|
| `-i`, `--input_dir` | Path to folder containing markdown files.                 | `markdown_file`      |
| `-p`, `--protocol`  | Path to the protocol spreadsheet (.XLSX) defining fields. | `protocol.xlsx`      |
| `-o`, `--output`    | Path to save the extracted data .CSV.                     | `extracted_data.csv` |
| `-m`, `--model`     | OpenAI model to use.                                      | `gpt-4.1`            |

## Convert PDFs to Markdown Files (UTF-8)
```
python pdf_to_markdown.py [options]
```
| Flag                    | Description                          | Default         |
|-------------------------|--------------------------------------|-----------------|
| `-i`, `--input_folder`  | Path to folder containing PDF files. | `pdf_papers`    |
| `-o`, `--output_folder` | Path to save the markdown files.     | `markdown_file` |

## Output
Generates a CSV (.csv) with one row per paper and one column per protocol field.

## License
This project is licensed under the MIT License. See LICENSE for details.
