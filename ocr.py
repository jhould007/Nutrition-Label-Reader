from PIL import Image, ExifTags
import pytesseract
import re
import cv2

# Set path to Tesseract .exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to read a nutrition label using OCR
def read_label(file_path):
    try:
        image = Image.open(file_path) # Load the image
        image = convert_to_grayscale(file_path)
        
         # Correct orientation based on EXIF data
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            
            exif = image._getexif()
            if exif is not None:
                orientation = exif.get(orientation, None)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        except AttributeError:
            # If no EXIF data is present or the image lacks rotation info, continue without changes
            pass
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        
    try:
        full_text = pytesseract.image_to_string(image) # Perform OCR
        return extract_ingredients(full_text)
    except Exception as e:
        print(f"Error performing OCR on on image: {e}")
    

# Function to extract the ingredient list from a nutrition label
def extract_ingredients(text):
    # Get first 200 characters of text
    start_of_label = text[:300]
    
    # Define the regular expression pattern
    pattern = r"INGREDIENTS.*?\."  # Matches 'INGREDIENTS' followed by any characters and ends with a period

    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)  # re.DOTALL allows '.' to match newline characters as well

    # If a match is found, return it
    if match:
        return match.group(0)  # Return the matched portion of the text
    else:
        return start_of_label # Return first 200 characters if match is not found
    
# Function to convert an image to grayscale
def convert_to_grayscale(image_path):
    image = cv2.imread(image_path)  # Load image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    return gray_image