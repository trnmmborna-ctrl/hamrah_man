
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

import arabic_reshaper
from bidi.algorithm import get_display
import json
import os

Window.size = (360, 640)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(BASE_DIR, "Vazirmatn-Regular.ttf")
FILE = os.path.join(BASE_DIR, "tasks.json")


def fa(text):
    return get_display(
        arabic_reshaper.reshape(str(text))
    )


class MyApp(App):

    def build(self):
        self.tasks = []
        self.load_tasks()

        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text=fa("برنامه‌ریز من"),
            font_name=FONT,
            font_size=25,
            size_hint_y=None,
            height=60
        )

        root.add_widget(title)

        self.input = TextInput(
            hint_text=fa("کار امروزت را بنویس..."),
            font_name=FONT,
            multiline=False,
            size_hint_y=None,
            height=50,
            halign="right"
        )

        root.add_widget(self.input)

        add_button = Button(
            text=fa("اضافه کردن"),
            font_name=FONT,
            size_hint_y=None,
            height=50
        )

        add_button.bind(on_press=self.add_task)
        root.add_widget(add_button)

        self.count = Label(
            text="",
            font_name=FONT,
            size_hint_y=None,
            height=40
        )

        root.add_widget(self.count)

        self.list_box = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None
        )

        self.list_box.bind(
            minimum_height=self.list_box.setter("height")
        )

        from kivy.uix.scrollview import ScrollView

        scroll = ScrollView()
        scroll.add_widget(self.list_box)
        root.add_widget(scroll)

        self.show_tasks()

        return root

    def add_task(self, button):
        task = self.input.text.strip()

        if task == "":
            self.count.text = fa("اول یک کار بنویس!")
            return

        self.tasks.append({
            "name": task,
            "done": False
        })

        self.input.text = ""

        self.save_tasks()
        self.show_tasks()

    def finish_task(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]

        self.save_tasks()
        self.show_tasks()

    def delete_task(self, index):
        self.tasks.pop(index)

        self.save_tasks()
        self.show_tasks()

    def show_tasks(self):
        self.list_box.clear_widgets()

        remaining = sum(
            1 for task in self.tasks
            if not task["done"]
        )

        self.count.text = fa(
            f"کارهای باقی‌مانده: {remaining}"
        )

        for i, task in enumerate(self.tasks):

            row = BoxLayout(
                size_hint_y=None,
                height=55,
                spacing=5
            )

            name = task["name"]

            if task["done"]:
                name = "✓ " + name

            label = Label(
                text=fa(name),
                font_name=FONT,
                font_size=15,
                halign="right"
            )

            row.add_widget(label)

            finish = Button(
                text=fa("تغییر وضعیت"),
                font_name=FONT
            )

            finish.bind(
                on_press=lambda x, n=i:
                self.finish_task(n)
            )

            row.add_widget(finish)

            delete = Button(
                text=fa("حذف"),
                font_name=FONT
            )

            delete.bind(
                on_press=lambda x, n=i:
                self.delete_task(n)
            )

            row.add_widget(delete)

            self.list_box.add_widget(row)

    def save_tasks(self):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.tasks,
                f,
                ensure_ascii=False
            )

    def load_tasks(self):
        if os.path.exists(FILE):
            try:
                with open(FILE, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except (ValueError, OSError):
                self.tasks = []


MyApp().run()
