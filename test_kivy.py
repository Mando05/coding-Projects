from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image

# Sample plant and crop data
plant_data = {
    "Aloe Vera": {"image": "images/alo vera.jpg", "soil": "Sandy, well-draining", "water": "Infrequent", "sunlight": "Full to partial", "origin": "Arabian Peninsula"},
    "Tomato": {"image": "", "soil": "Loamy, well-drained", "water": "Regular", "sunlight": "Full", "origin": "South America"},
    "Cactus": {"image": "image/Cactus.jpg", "soil": "Sandy, well-drained", "water": "Very infrequent", "sunlight": "Full", "origin": "Americas"},
    "Lettuce": {"image": "", "soil": "Loamy, well-drained", "water": "Regular", "sunlight": "Partial", "origin": "Mediterranean"},
}
def display_plant(self, plant_name):
    plant = plant_data[plant_name]
    self.info_label.text = f"Soil: {plant['soil']}\nWater: {plant['water']}"
    self.image.source = plant['image/alo vera.jpg']

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Search Bar
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.search_input = TextInput(multiline=False, hint_text="Search plants/crops")
        search_button = Button(text="Search")
        search_button.bind(on_press=self.search_plant)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        layout.add_widget(search_layout)

        scroll_view = ScrollView()
        plant_list = BoxLayout(orientation='vertical', size_hint_y=None)
        plant_list.bind(minimum_height=plant_list.setter('height'))

        for plant_name in plant_data:
            plant_button = Button(text=plant_name, size_hint_y=None, height=50)
            plant_button.bind(on_press=lambda instance, name=plant_name: self.show_plant_info(name))
            plant_list.add_widget(plant_button)

        scroll_view.add_widget(plant_list)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def search_plant(self, instance):
        search_term = self.search_input.text.lower()
        for plant_name in plant_data:
            if search_term in plant_name.lower():
                self.show_plant_info(plant_name)
                return  

    def show_plant_info(self, plant_name):
        self.manager.current = 'plant_info'
        self.manager.get_screen('plant_info').display_plant(plant_name)

class PlantInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.image = Image()
        layout.add_widget(self.image)

        self.info_label = Label(text="")
        layout.add_widget(self.info_label)

        back_button = Button(text="Back", size_hint_y=None, height=50)
        back_button.bind(on_press=lambda _: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def display_plant(self, plant_name):
        plant = plant_data[plant_name]
        self.info_label.text = f"Soil: {plant['soil']}\nWater: {plant['water']}"

class CropScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        crop_label = Label(text="Tomato\nLettuce")
        layout.add_widget(crop_label)

        back_button = Button(text="Back", size_hint_y=None, height=50)
        back_button.bind(on_press=lambda _: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

class WaterCalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text="Land Size (sq ft):"))
        self.land_size = TextInput(multiline=False)
        layout.add_widget(self.land_size)

        layout.add_widget(Label(text="Plant Name:"))
        self.plant_name = TextInput(multiline=False)
        layout.add_widget(self.plant_name)

        calc_button = Button(text="Calculate Water Needs")
        calc_button.bind(on_press=self.calculate_water)
        layout.add_widget(calc_button)

        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        back_button = Button(text="Back", size_hint_y=None, height=50)
        back_button.bind(on_press=lambda _: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def calculate_water(self, instance):
        size = self.land_size.text
        plant = self.plant_name.text
        if size.isdigit() and plant in plant_data:
            water_needed = int(size) * 0.2
            self.result_label.text = f"Estimated water: {water_needed} gallons"
        else:
            self.result_label.text = "Invalid input"

class CultivateGro(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(PlantInfoScreen(name='plant_info'))
        sm.add_widget(CropScreen(name='crop'))
        sm.add_widget(WaterCalcScreen(name='water_calc'))

        bottom_bar = BoxLayout(size_hint=(1, None), height=60)
        home_button = Button(text="Home")
        crop_button = Button(text="Crops")
        water_calc_button = Button(text="Water Calc")

        home_button.bind(on_press=lambda _: setattr(sm, 'current', 'home'))
        crop_button.bind(on_press=lambda _: setattr(sm, 'current', 'crop'))
        water_calc_button.bind(on_press=lambda _: setattr(sm, 'current', 'water_calc'))

        bottom_bar.add_widget(home_button)
        bottom_bar.add_widget(crop_button)
        bottom_bar.add_widget(water_calc_button)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(sm)
        main_layout.add_widget(bottom_bar)

        return main_layout  # <<<<<< THIS MAKES THE APP SHOW UP!

if __name__ == "__main__":
    CultivateGro().run()

