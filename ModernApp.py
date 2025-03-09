from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

# Define KV string for improved UI
kv_string = """
#:kivy 2.0.0

<ModernScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: root.title
            size_hint_y: None
            height: '48sp'
            font_size: '24sp'
            bold: True
            color: '#333333'

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 10

                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1  # White background
                    Rectangle:
                        pos: self.pos
                        size: self.size

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: '48sp'
                    spacing: 10

                    Label:
                        text: root.label_text
                        size_hint_x: 0.3
                        color: '#555555'

                    TextInput:
                        id: input_field
                        multiline: False
                        background_color: '#f0f0f0'
                        foreground_color: '#333333'

                Button:
                    text: root.button_text
                    size_hint_y: None
                    height: '48sp'
                    background_color: '#4CAF50'  # Green
                    color: '#ffffff'
                    on_press: root.on_button_press()

                Image:
                    id: display_image
                    size_hint_y: None
                    height: '200sp'
                    allow_stretch: True
                    keep_ratio: True

                Button:
                    text: "Choose Image"
                    size_hint_y: None
                    height: '48sp'
                    background_color: '#2196F3'  # Blue
                    color: '#ffffff'
                    on_press: root.show_file_chooser()

<FileChooserPopup>:
    title: "Choose an Image"
    BoxLayout:
        orientation: 'vertical'
        FileChooserIconView:
            id: filechooser
            path: root.path
        BoxLayout:
            size_hint_y: None
            height: '48sp'
            Button:
                text: 'Cancel'
                on_press: root.dismiss()
            Button:
                text: 'Select'
                on_press: root.select(filechooser.selection)

"""

Builder.load_string(kv_string)

class ModernScreen(Screen):
    title = "Modern App"
    label_text = "Enter Text:"
    button_text = "Submit"

    def on_button_press(self):
        text = self.ids.input_field.text
        print(f"Submitted text: {text}")

    def show_file_chooser(self):
        popup = FileChooserPopup(path='/', select=self.load_image)
        popup.open()

    def load_image(self, selection):
        if selection:
            self.ids.display_image.source = selection[0]

class FileChooserPopup(Popup):
    def __init__(self, path, select, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.select = select

class ModernApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#e0e0e0') # Light grey background
        sm = ScreenManager()
        sm.add_widget(ModernScreen(name='main'))
        return sm

if __name__ == '__main__':
    ModernApp().run()