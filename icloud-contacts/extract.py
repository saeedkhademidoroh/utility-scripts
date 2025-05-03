# Import standard libraries
import os  # Used for handling file paths

# Import third-party libraries
import pytesseract
from pdf2image import convert_from_path


# Function to extract text from a PDF using OCR
def extract_text(pdf_path):
    """
    Extract text from a PDF file using OCR and save it to 'extract.txt'.

    Steps:
    1. Convert PDF pages to images using pdf2image.
    2. Apply Tesseract OCR on each image.
    3. Save extracted text to 'extract.txt' in the same directory.

    Args:
        pdf_path (str): The file path of the input PDF.

    Returns:
        str: The full path to the saved extracted text file.
    """
    pdf_dir = os.path.dirname(pdf_path)
    text_file_path = os.path.join(pdf_dir, "extract.txt")

    print("🔄 Converting PDF to images...")
    images = convert_from_path(pdf_path)

    print("🔍 Running OCR on extracted images...")
    ocr_text = "\n".join(pytesseract.image_to_string(img) for img in images)

    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(ocr_text)

    print(f"✅ Extracted text saved to: {text_file_path}")
    return text_file_path

# Print confirmation message
print("\n✅ extract.py successfully executed")
