from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk  # Import Pillow modules for image handling
import ocr
import azure
import os  
from openai import AzureOpenAI  

# Set up Azure OpenAI info   
endpoint = os.getenv("ENDPOINT_URL", "https://mywestusregion.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "f13de0a9e7e14570958e7fece7338171")
    
# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",  
)  

# Initialize window
window = Tk()
window.title("Nutrition Label Reader")
window.geometry("700x900")

# Create main label
top_label = Label(window, text="Click the upload button and upload an image to get started.", fg="black", font=("Arial", 16),
                  wraplength=500, anchor="center")
top_label.pack(side="top", fill="both", expand=True, padx=10, pady=30)

def display_image(file_path):
    # Open the image using PIL
    img = Image.open(file_path)
    
    # Resize the image to fit the window, keeping the aspect ratio
    img = img.resize((400, 400))  # Adjust size as needed

    # Convert the image to a Tkinter-compatible format
    img_tk = ImageTk.PhotoImage(img)
    
    # Create a label to display the image
    image_label = Label(window, image=img_tk)
    image_label.image = img_tk  # Keep a reference to the image object
    image_label.pack(pady=20)  # Add some padding around the image
    
# Define variable to store OCR and OpenAI results
ocr_results = ""
openai_response = ""

# Function to update the contents of a text object
def update_text_object(object, new_content):
    object.config(state="normal")  # Enable editing
    object.delete("1.0", "end")    # Clear existing content
    object.insert("1.0", new_content)     # Insert new content
    object.config(state="disabled")  # Disable editing to prevent user changes
    
# Function to open the file dialog and pick a file
def open_file_picker():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=(("Image Files", "*.png;*.jpg"), ("All Files", "*.*")), # Allow only PNG and JPG files
        initialdir="C:/Users/jdh10/Downloads/NLR_images"
    )
    if file_path:
        print(f"File selected: {file_path}") 
        #display_image(file_path)
        ocr_results = ocr.read_label(file_path)
        update_text_object(ocr_result_text, ocr_results)
        openai_response = azure.get_openai_insights(file_path)
        update_text_object(openai_response_text, openai_response)
        
# Create upload file button
upload_button = Button(window, text="Upload Image", fg="black", command=open_file_picker)

# Place the button in the window
upload_button.pack(side="bottom", pady=50)

# Create label to show OCR results
ocr_label_title = Label(window, text="OCR Result", fg="black", font=("Arial", 16), anchor="center")
ocr_label_title.pack(side="top", fill="both", expand=True, padx=10)
ocr_result_text = Text(
    window,
    bg="#caebee",
    font=("Arial", 10),
    wrap="word",  # Word wrapping for better readability
    height=10,    # Approximate height in lines
    width=65,     # Approximate width in characters
    padx=10,      # Internal padding
    pady=10,      # Internal padding
)
ocr_result_text.pack(fill="both", expand=True, padx=10, pady=3)
ocr_result_text.config(state="disabled")

# Get insights from OpenAI
openai_response_label_title = Label(window, text="OpenAI Response", fg="black", font=("Arial", 16), anchor="center")
openai_response_label_title.pack(side="top", fill="both", expand=True, padx=10)
openai_response_text = Text(
    window,
    bg="#cef1c5",
    font=("Arial", 10),
    wrap="word",
    height=10,
    width=65,
    padx=10,
    pady=10, 
)
openai_response_text.pack(fill="both", expand=True, padx=10, pady=3)
openai_response_text.config(state="disabled")

# Start main activity
window.mainloop()

"""
    ocr_result_label = Label(window, text="", bg="#b9f0f4", font=("Arial", 10), wraplength=650, justify="center")
    ocr_result_label.pack(pady=10)  
    
    openai_response_label = Label(window, text="", bg="#b3f1a1", font=("Arial", 8), wraplength=650, justify="center", padx=10, pady=10)
    openai_response_label.pack(pady=10)
    """