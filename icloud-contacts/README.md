
---

## 📁 `icloud-contacts/README.md`

```markdown
# icloud-contacts

Utilities for extracting contacts from PDFs and generating iCloud-compatible VCF files.

## Features

- Extract text from PDF files using OCR.
- Parse extracted text to identify contact names and phone numbers.
- Generate `.vcf` files compatible with iCloud.

## Usage

1. Place the PDF file containing contacts in the project directory.
2. Run `extract.py` to extract text from the PDF.
3. Run `generate.py` to create the VCF file from the extracted text.

## Dependencies

- Python 3.x
- pytesseract
- pdf2image

Install dependencies using pip:

```bash
pip install pytesseract pdf2image
