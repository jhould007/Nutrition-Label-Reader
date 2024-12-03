from PIL import Image
import pytesseract
import re

# Set path to Tesseract .exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to read a nutrition label using OCR
def read_label(file_path):
    image = Image.open(file_path) # Load the image
    full_text = pytesseract.image_to_string(image) # Perform OCR
    return extract_ingredients(full_text)

def extract_ingredients(text):
    # Define the regular expression pattern
    pattern = r"Ingredients.*?\."  # Matches 'Ingredients' followed by any characters and ends with a period

    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)  # re.DOTALL allows '.' to match newline characters as well

    # If a match is found, return it
    if match:
        return match.group(0)  # Return the matched portion of the text
    else:
        return "Ingredients not found."

#print(read_label("Images/SkittleIngredientList.png"))