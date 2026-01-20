from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from json import dump
import os


class DynamicForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        with self.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.control_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        self.control_layout.add_widget(
            Label(text="Number of Items:", font_size=22, color=(1, 1, 1, 1))
        )

        self.num_input = TextInput(
            text="1",
            multiline=False,
            size_hint_x=0.2,
            font_size=22,
        )
        self.num_input.bind(text=self.update_fields)
        self.control_layout.add_widget(self.num_input)

        self.add_widget(self.control_layout)

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.field_layout = GridLayout(cols=1, size_hint_y=None, spacing=15, padding=10)
        self.field_layout.bind(minimum_height=self.field_layout.setter("height"))
        self.scroll_view.add_widget(self.field_layout)

        self.add_widget(self.scroll_view)

        self.submit_btn = Button(
            text="Save Data",
            size_hint_y=None,
            height=60,
            font_size=24,
        )
        self.submit_btn.bind(on_press=self.save_data)
        self.add_widget(self.submit_btn)

        self.fields = []
        self.update_fields()

    def update_fields(self, *args):
        try:
            num_items = max(1, int(self.num_input.text))
        except ValueError:
            num_items = 1

        self.field_layout.clear_widgets()
        self.fields = []

        for i in range(num_items):
            item_box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=220,
                padding=15,
                spacing=10,
            )

            with item_box.canvas.before:
                Color(0.15, 0.15, 0.15, 1)
                item_box.rect = RoundedRectangle(
                    size=item_box.size, pos=item_box.pos, radius=[10]
                )
            item_box.bind(size=self.update_rect, pos=self.update_rect)

            name = TextInput(hint_text="Camera Name", multiline=False)
            desc = TextInput(hint_text="Description", multiline=True)
            link = TextInput(hint_text="Camera Stream URL", multiline=False)

            item_box.add_widget(name)
            item_box.add_widget(desc)
            item_box.add_widget(link)

            self.fields.append({"name": name, "desc": desc, "link": link})
            self.field_layout.add_widget(item_box)

    def show_popup(self, message):
        layout = BoxLayout(orientation="vertical", padding=20)
        layout.add_widget(Label(text=message))
        popup = Popup(title="Info", content=layout, size_hint=(None, None), size=(400, 200))
        popup.open()

    def save_data(self, instance):
        data = []
        for f in self.fields:
            if not f["name"].text or not f["link"].text:
                self.show_popup("All fields are required")
                return

            data.append(
                {
                    "name": f["name"].text.strip(),
                    "desc": f["desc"].text.strip(),
                    "link": f["link"].text.strip(),
                }
            )

        os.makedirs("data/raw", exist_ok=True)
        with open("data/raw/data.json", "w") as file:
            dump(data, file, indent=2)

        self.show_popup("Camera configuration saved to data/raw/data.json")

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class DynamicFormApp(App):
    def build(self):
        return DynamicForm()


if __name__ == "__main__":
    DynamicFormApp().run()
