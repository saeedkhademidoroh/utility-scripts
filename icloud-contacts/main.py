# Project-specific imports
from extract import extract_text
from generate import generate_icloud_vcf


# Run full pipeline on a single PDF
extract_path = extract_text("input/contacts.pdf")
generate_icloud_vcf(extract_path)

# Run only OCR extraction
# extract_path = extract_text("input/contacts.pdf")

# Run only VCF generation (assumes extract.txt exists)
# generate_icloud_vcf("input/extract.txt")


# Print confirmation message
print("\n✅ main.py successfully executed")
