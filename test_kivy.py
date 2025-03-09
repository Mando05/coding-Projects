import threading
import time
from rpy_flask import send_integers_to_rpi


from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import  ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import AsyncImage
import difflib 
import csv

CSV_FILE = 'plants.csv'

# Read the CSV file and store the data
def read_csv(file_path):
    plants_data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            plants_data.append({
                'name': row['name'],
                'description': row['description'],
                'image_url': row['image_url']
            })
    return plants_data

plant_data = read_csv('plants.csv')


class AddPlantScreen(Screen):
     
     def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.plant_name_label = Label(text="Adding: ")
        self.layout.add_widget(self.plant_name_label)

        self.fields = {}
        for field in ["Family", "Soil", "Water", "Sunlight", "Origin"]:
            self.layout.add_widget(Label(text=field + ":"))
            input_field = TextInput(multiline=False)
            self.layout.add_widget(input_field)
            self.fields[field.lower()] = input_field

        # Image upload button
        self.image_path = ""  # Store the selected image path
        self.image_button = Button(text="Upload Image")
        self.image_button.bind(on_press=self.open_file_chooser)
        self.layout.add_widget(self.image_button)

        save_button = Button(text="Save Plant")
        save_button.bind(on_press=self.save_plant)
        self.layout.add_widget(save_button)

        back_button = Button(text="Back")
        back_button.bind(on_press=lambda _: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

     def set_plant_name(self, plant_name):
        """Set the plant name when navigating to this screen"""
        self.plant_name_label.text = f"Adding: {plant_name}"
        self.plant_name = plant_name

     def open_file_chooser(self, instance):
        """Open a file chooser popup for image selection"""
        content = FileChooserIconView()
        popup = Popup(title="Select Image", content=content, size_hint=(0.9, 0.9))

        def select_image(selection):
            if selection:
                self.image_path = selection[0]
                self.image_button.text = "Image Selected"  # Update button text
            popup.dismiss()

        content.bind(on_submit=lambda _, selection, __: select_image(selection))
        popup.open()

     def save_plant(self, instance):
        """Save the new plant information"""
        plant_data[self.plant_name] = {
            "family": self.fields["family"].text,
            "soil": self.fields["soil"].text,
            "water": self.fields["water"].text,
            "sunlight": self.fields["sunlight"].text,
            "origin": self.fields["origin"].text,
            "image": self.image_path  # Save image path
        }
        self.manager.current = 'home'  # Go back home after saving


class PlantDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[20, 10, 20, 10], spacing=10)

        # Set background color to white
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Image display
        self.image = AsyncImage(size_hint_y=None, height=250)
        layout.add_widget(self.image)

        # Scrollable text area
        scroll_view = ScrollView(size_hint=(1, None), height=300)
        text_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=[10, 5], spacing=10)
        text_layout.bind(minimum_height=text_layout.setter('height'))

        # Label for plant information with black text
        self.info_label = Label(text="", halign="left", valign="top", size_hint_y=None, font_size=16,
                                text_size=(None, None), markup=True, color=(0, 0, 0, 1))  # Black color
        self.info_label.bind(texture_size=self._update_text_size)

        text_layout.add_widget(self.info_label)
        scroll_view.add_widget(text_layout)
        layout.add_widget(scroll_view)

        # Back Button
        back_button = Button(text="Back", size_hint_y=None, height=50)
        back_button.bind(on_press=lambda _: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def _update_rect(self, self_instance, size):
        self.rect.size = self_instance.size
        self.rect.pos = self_instance.pos

    def _update_text_size(self, instance, value):
        """Dynamically adjusts text size to fit within the screen width"""
        self.info_label.text_size = (self.width - 40, None)

    def display_plant(self, plant_name):
        plant = next((p for p in plant_data if p['name'] == plant_name), None)
        if plant:
            self.image.source = plant['image_url']
            description_text = " ".join(plant['description'].split()[:55])  # Limit description to 55 words
            self.info_label.text = f"[b]Description:[/b] {description_text}"


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=0)
        
        # Set background color
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Centered Search Bar
        float_layout = FloatLayout(size_hint=(1, 1))
        search_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 58), spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.search_input = TextInput(multiline=False, hint_text="Search plants/crops", size_hint_x=0.8, padding=(10, 10))
        search_button = Button(text="Search", size_hint_x=0.2, size_hint_y=None, height=58, width=108, background_color=(0.1, 0.6, 0.2, 1))
        search_button.bind(on_press=self.search_plant)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        float_layout.add_widget(search_layout)
        layout.add_widget(float_layout)

        # Scrollable Vertical List
        scroll_view = ScrollView()
        plant_list = GridLayout(cols = 1, size_hint_y=None, padding=[300, 80, 90, 55], spacing = 10,
             pos_hint={'center_x': 0.5})  # Center the content horizontally
        plant_list.bind(minimum_height=plant_list.setter('height'))
        # Center the scroll view within a FloatLayout
        float_layout = FloatLayout(size_hint=(1, None), height=600)  # Adjust height as needed

        for plant in plant_data:
            # Create a button for each plant card
            plant_card = Button(
                text=plant['name'],
                size_hint_x=None,  # Let the width be determined by the content
                width=400,  # Set a fixed width for the button
                size_hint_y=None,
                height=150,
                background_color=(0.2, 0.8, 0.4, 1),
                font_size=18,
                padding=(10, 10),
                background_normal='',
                background_down=''
            )
            # When clicked, show more information
            plant_card.bind(on_press=lambda _, name=plant['name']: self.show_plant_info(name))
            plant_list.add_widget(plant_card)

        scroll_view.add_widget(plant_list)
        float_layout.add_widget(scroll_view)
        layout.add_widget(float_layout)

        # Floating Add Button
        float_layout = FloatLayout()
        add_button = Button(
            text='+',
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={'right': 0.95, 'y': 0.05},
            background_color=(0.9, 0.2, 0.2, 1),
            font_size=24,
            background_normal='',
            background_down=''
        )
        add_button.bind(on_press=lambda _: setattr(self.manager, 'current', 'add_plant'))
        float_layout.add_widget(add_button)
        layout.add_widget(float_layout)

        self.add_widget(layout)

    def _update_rect(self, instance, _):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_plant_info(self, plant_name):
        self.manager.get_screen('plant_info').display_plant(plant_name)
        self.manager.current = 'plant_info'

    def search_plant(self, _):
        search_term = self.search_input.text.strip().lower()

        if not search_term:
            return  # Don't search if the input is empty

        # Get plant names from the dataset
        plant_names = [plant['name'].lower() for plant in plant_data]

        # Find the closest match
        closest_match = difflib.get_close_matches(search_term, plant_names, n=1, cutoff=0.6)

        if closest_match:
            # Find the actual plant object from the dataset
            plant_name = next((plant['name'] for plant in plant_data if plant['name'].lower() == closest_match[0]), None)
            if plant_name:
                self.show_plant_info(plant_name)
                return

        # If no match is found, prompt user to add the plant
        self.manager.get_screen('add_plant').set_plant_name(search_term)
        self.manager.current = 'add_plant'


class WaterCalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Land Size Input
        layout.add_widget(Label(text="Land Size (sq ft):"))
        self.land_size = TextInput(multiline=False)
        layout.add_widget(self.land_size)

        # Plant Name Input
        layout.add_widget(Label(text="Plant Name:"))
        self.plant_name = TextInput(multiline=False)
        layout.add_widget(self.plant_name)

        # Calculate Button
        calc_button = Button(text="Calculate Water Needs")
        calc_button.bind(on_press=self.calculate_water)
        layout.add_widget(calc_button)

        # Result Label
        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        # Placeholder Button - Prints "Hello" to terminal when clicked
        placeholder_button = Button(text="Set Automated Water", size_hint_y=None, height=50)
        placeholder_button.bind(on_press=lambda _: send_integers_to_rpi(1,1))
        layout.add_widget(placeholder_button)

        self.add_widget(layout)

    def calculate_water(self, _):
        size = self.land_size.text
        plant = self.plant_name.text
        if size.isdigit() and plant in plant_data:
            water_needed = int(size) * 0.2
            self.result_label.text = f"Estimated water: {water_needed} gallons"
        else:
            self.result_label.text = "Invalid input"


class CultiGro(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddPlantScreen(name='add_plant'))
        sm.add_widget(PlantDetailScreen(name='plant_info'))
        sm.add_widget(WaterCalcScreen(name='water_calc'))

        bottom_bar = BoxLayout(size_hint=(1, None), height=60)
        home_button = Button(text="Home")
        water_calc_button = Button(text="Water Calc")

        home_button.bind(on_press=lambda _: setattr(sm, 'current', 'home'))
        water_calc_button.bind(on_press=lambda _: setattr(sm, 'current', 'water_calc'))

        bottom_bar.add_widget(home_button)
        bottom_bar.add_widget(water_calc_button)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(sm)
        main_layout.add_widget(bottom_bar)

        return main_layout


if __name__ == '__main__':
    CultiGro().run()