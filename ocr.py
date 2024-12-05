from PIL import Image
import pytesseract
import re

# Set path to Tesseract .exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to read a nutrition label using OCR
def read_label(file_path):
    try:
        image = Image.open(file_path) # Load the image
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        
    try:
        full_text = pytesseract.image_to_string(image) # Perform OCR
    except Exception as e:
        print(f"Error performing OCR on on image: {e}")
    
    return extract_ingredients(full_text)

def extract_ingredients(text):
    # Get first 200 characters of text
    start_of_label = text[:300]
    
    # Define the regular expression pattern
    pattern = r"Ingredients.*?\."  # Matches 'Ingredients' followed by any characters and ends with a period

    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)  # re.DOTALL allows '.' to match newline characters as well

    # If a match is found, return it
    if match:
        return match.group(0)  # Return the matched portion of the text
    else:
        return start_of_label