# General imports
import ocr
import azure
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from os.path import expanduser

# Kivy and Tkinter imports
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
import tkinter as tk
from tkinter import filedialog

# Load Azure OpenAI endpoint URL and API key
load_dotenv("azure.env")
endpoint_url = os.getenv("AZURE_OPENAI_ENDPOINT_URL")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

if not(endpoint_url and api_key):
    raise ValueError("There is a problem with your endpoint URL or API key. Check your .env file.")

# Set up Azure OpenAI info
endpoint = os.getenv("ENDPOINT_URL", endpoint_url)
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", api_key)

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

class MyApp(App):
    def build(self):
        # Set window size
        Window.size = (700, 800)
        
        # Set app title
        self.title = "Nutrition Label Reader"

        # Create a main layout to hold everything
        main_layout = BoxLayout(orientation='vertical')

        # Create a label to display the selected file path
        self.label = Label(
            text="The selected file will appear here.",
            size_hint=(1, None),
            height=40,
            text_size=(Window.width - 20, None),  # Set text_size to wrap text within the window width
            halign='center'  # Center align the text
        )
        main_layout.add_widget(self.label)
        
        # Display OCR results
        ocr_label = Label(text="OCR results", size_hint=(1, None), height=40)
        main_layout.add_widget(ocr_label)
        self.ocr_results = TextInput(text="", size_hint=(1, None), height=200, readonly=True)
        main_layout.add_widget(self.ocr_results)
        
        # Add vertical padding
        main_layout.add_widget(Widget(size_hint_y=None, height=20))
        
        # Display Azure OpenAI Output
        azure_label = Label(text="Azure OpenAI Output", size_hint=(1, None), height=40)
        main_layout.add_widget(azure_label)
        self.azure_output = TextInput(text="", size_hint=(1, None), height=200, readonly=True)
        main_layout.add_widget(self.azure_output)

        # Create an AnchorLayout for positioning the button at the bottom center
        button_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')

        # Create the button to trigger the native file picker
        btn_open = Button(text="Select Image", size_hint=(None, None), size=(150, 40))
        btn_open.bind(on_press=self.open_file_picker)  # Bind the button to the method

        # Add the button to the AnchorLayout
        button_layout.add_widget(btn_open)

        # Add the AnchorLayout (with button) to the main layout
        main_layout.add_widget(button_layout)
        
        # Add padding between the button and the bottom of the window
        main_layout.add_widget(Widget(size_hint_y=None, height=10))

        return main_layout
    
    def open_file_picker(self, instance):
        # Set up Tkinter's root window, which is required to open the file dialog
        root = tk.Tk()
        root.withdraw()  # Hide the Tkinter root window

        # Open the file picker (native file dialog) and filter for image types
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*"))
        )

        if file_path:
            self.label.text = f"Selected file: {file_path}"  # Show selected file path in the label
            print(f"Selected file: {file_path}")  # You can process the file here
            self.process_image(file_path)
            
        return file_path
    
    def process_image(self, file_path):
        # Call the OCR function with the selected file path
        ocr_results = ocr.read_label(file_path)
        print(f"OCR Results: {ocr_results}")  # Print the OCR results (or update the UI with the results)
        self.ocr_results.text = ocr_results  # Update the TextInput with the OCR results
        
        azure_output = azure.get_openai_insights(ocr_results)
        print(f"Azure OpenAI Output: {azure_output}")  # Print the Azure OpenAI output (or update the UI with the results)
        self.azure_output.text = azure_output  # Update the TextInput with the Azure OpenAI output
        
if __name__ == '__main__':
    MyApp().run()