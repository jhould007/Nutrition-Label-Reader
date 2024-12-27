import ocr
import azure
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from plyer import filechooser

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
        btn_open.bind(on_press=self.open_file_chooser)  # Bind the button to the method

        # Add the button to the AnchorLayout
        button_layout.add_widget(btn_open)

        # Add the AnchorLayout (with button) to the main layout
        main_layout.add_widget(button_layout)

        # Add padding between the button and the bottom of the window
        main_layout.add_widget(Widget(size_hint_y=None, height=20))

        return main_layout

    def open_file_chooser(self, instance):
        # Open the native file chooser
        filechooser.open_file(on_selection=self.file_selected)

    def file_selected(self, selection):
        print(f"Selection: {selection}")  # Debug print to check the selection
        if selection:
            file_path = selection[0]
            self.label.text = f"Selected file: {file_path}"  # Show selected file path in the label
            print(f"Selected file: {file_path}")  # Debug print to check the selected file path
            self.process_image(file_path)
        else:
            print("No file selected")  # Debug print to check if no file was selected

    def process_image(self, file_path):
        # Call the OCR function with the selected file path
        full_text = ocr.read_label(file_path)

        # Extract ingredients from the full OCR text
        ingredients = ocr.extract_ingredients(full_text)
        print(f"Extracted Ingredients: {ingredients}")  # Print the extracted ingredients
        self.ocr_results.text = ingredients # Update the TextInput with the extracted ingredients

        # Call the Azure OpenAI function with the extracted ingredients
        azure_output = azure.get_openai_insights(file_path)
        print(f"Azure OpenAI Output: {azure_output}")  # Print the Azure OpenAI output (or update the UI with the results)
        self.azure_output.text = azure_output  # Update the TextInput with the Azure OpenAI output

if __name__ == '__main__':
    MyApp().run()