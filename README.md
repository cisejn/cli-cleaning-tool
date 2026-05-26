# csv-cleaner-cli

A simple but powerful Python CLI tool to clean and summarize messy CSV files

## Features

- Removes duplicate rows
- Drops fully empty rows
- Detects and reports missing values per column
- Trims whitespace from all string fields
- Prints a clean summary report to the terminal
- Optionally saves the report as a `.txt` file

## Requirements

- Python 3.10+
- pandas

## Installation

```bash
git clone https://github.com/cisejn/csv-cleaner-cli.git
cd csv-cleaner-cli
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage (outputs cleaned_sample.csv)
python cleaner.py sample.csv

# Specify output file
python cleaner.py sample.csv --output clean.csv

# Also save a text report
python cleaner.py sample.csv --output clean.csv --save-report
```

## Example Output
Saved to: cleaned_sample.csv

==================================================
CSV CLEANER REPORT #sample
==================================================
  Timestamp     : 2026-05-26 11:28:49 
  Output file   : cleaned_laptopData.csv 
--------------------------------------------------
  Original rows : 1303
  Columns       : 12  →  ['Unnamed: 0', 'Company', 'TypeName', 'Inches', 'ScreenResolution', 'Cpu', 'Ram', 'Memory', 'Gpu', 'OpSys', 'Weight', 'Price']
  Duplicates    : 0 rows removed
  Empty rows    : 30 rows removed
  Final rows    : 1273
--------------------------------------------------
  Missing values (before cleaning):
    • Unnamed: 0: 30 missing
    • Company: 30 missing
    • TypeName: 30 missing
    • Inches: 30 missing
    • ScreenResolution: 30 missing
    • Cpu: 30 missing
    • Ram: 30 missing
    • Memory: 30 missing
    • Gpu: 30 missing
    • OpSys: 30 missing
    • Weight: 30 missing
    • Price: 30 missing
==================================================
```

## Project Structure

```
csv-cleaner-cli/
├── cleaner.py        # Main script
├── requirements.txt
├── laptopData.csv        # Example dirty CSV for testing
├── .gitignore
└── README.md
```

## Future Ideas

- [ ] Excel `.xlsx` support
- [ ] Column type inference & validation
- [ ] HTML report output
- [ ] Auto-fix common date formats
