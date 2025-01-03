from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
import cv2
import numpy as np
import pytesseract
from PIL import Image
import ocr
import re
import azure

# Set path to Tesseract .exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
            text="The captured image will appear here.",
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
        self.azure_output = TextInput(text="", size_hint=(1, None), height=350, readonly=True)
        main_layout.add_widget(self.azure_output)

        # Create an AnchorLayout for positioning the button at the bottom center
        button_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')

        # Create the Camera widget
        self.camera = Camera(play=True, resolution=(640, 480), size_hint=(1, 0.6))
        main_layout.add_widget(self.camera)

        # Create the button to capture the image
        btn_capture = Button(text="Capture Image", size_hint=(None, None), size=(150, 40))
        btn_capture.bind(on_press=self.capture_image)  # Bind the button to the method

        # Add the button to the AnchorLayout
        button_layout.add_widget(btn_capture)

        # Add the AnchorLayout (with button) to the main layout
        main_layout.add_widget(button_layout)

        return main_layout

    def capture_image(self, instance):
        # Capture the image from the camera
        texture = self.camera.texture
        size = texture.size
        pixels = texture.pixels

        # Convert the captured image to a format suitable for OpenCV
        image = np.frombuffer(pixels, np.uint8).reshape(size[1], size[0], 4)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        # Save the captured image
        image_path = "captured_image.png"
        cv2.imwrite(image_path, image)

        self.label.text = f"Captured image saved to: {image_path}"  # Show captured image path in the label
        print(f"Captured image saved to: {image_path}")  # Debug print to check the captured image path

        # Process the captured image
        self.process_image(image_path)

    def process_image(self, file_path):
        # Preprocess the image
        processed_image = ocr.preprocess_image(file_path)
        
        # Convert the processed image to PIL format for Tesseract
        processed_image_pil = Image.fromarray(processed_image)
        
        # Perform OCR on the preprocessed image
        full_text = pytesseract.image_to_string(processed_image_pil)
        print(f"OCR Results: {full_text}")  # Print the OCR results (or update the UI with the results)
        self.ocr_results.text = full_text  # Update the TextInput with the OCR results

        # Extract ingredients from the full OCR text
        ingredients = ocr.extract_ingredients(full_text)
        print(f"Extracted Ingredients: {ingredients}")  # Print the extracted ingredients

        # Call the Azure OpenAI function with the extracted ingredients
        azure_output = azure.get_openai_insights(ingredients)
        print(f"Azure OpenAI Output: {azure_output}")  # Print the Azure OpenAI output (or update the UI with the results)
        self.azure_output.text = azure_output  # Update the TextInput with the Azure OpenAI output

if __name__ == '__main__':
    MyApp().run()