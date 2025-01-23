import tkinter as tk
from tkinter import filedialog, simpledialog, font, colorchooser
import json
import time
import threading

class Teleprompter:
    def __init__(self, root):
        self.root = root
        self.root.title("Teleprompter")
        self.root.geometry("800x600")

        self.text = tk.Text(root, wrap=tk.WORD, font=("Arial", 20))
        self.text.pack(fill=tk.BOTH, expand=True)

        self.scrolling = False
        self.scroll_speed = 100  # milliseconds
        self.alignment = "left"
        self.scroll_step = 1  # pixels to scroll per step

        self.create_menu()
        self.load_settings()


    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Open Config", command=self.open_config)
        self.file_menu.add_command(label="Save Settings", command=self.save_settings)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Font", command=self.change_font)
        self.settings_menu.add_command(label="Font Size", command=self.change_font_size)
        self.settings_menu.add_command(label="Scroll Speed", command=self.change_scroll_speed)
        self.settings_menu.add_command(label="Alignment", command=self.change_alignment)

        self.menu_bar.add_command(label="Change Theme", command=self.change_theme)

        self.menu_bar.add_command(label="Start\Stop" , command=self.toggle_scrolling )


    def change_theme(self):
        theme = simpledialog.askstring("Theme", "Enter theme (light/dark):", initialvalue="light" if self.text.cget("bg") == "white" else "dark")
        if theme:
            if theme.lower() == "dark":
                self.root.config(bg="black")
                self.text.config(bg="black", fg="white")
            elif theme.lower() == "light":
                self.root.config(bg="white")
                self.text.config(bg="white", fg="black")
            self.save_settings()


    def toggle_scrolling(self):
        if self.scrolling:
            self.scrolling = False
        else:
            self.scrolling = True
            self.scroll_thread = threading.Thread(target=self.scroll_text)
            self.scroll_thread.start()


    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, content)


    def open_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.load_settings(file_path)


    def change_font(self):
        current_font = self.text.cget("font")
        font_name, font_size = current_font.split()
        font_name = simpledialog.askstring("Font", "Enter font name:", initialvalue=font_name)
        if font_name:
            self.text.config(font=(font_name, font_size))
            self.save_settings()


    def change_font_size(self):
        current_font = self.text.cget("font")
        font_name, font_size = current_font.split()
        font_size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=int(font_size))
        if font_size:
            self.text.config(font=(font_name, font_size))
            self.save_settings()


    def change_scroll_speed(self):
        scroll_speed = simpledialog.askinteger("Scroll Speed", "Enter scroll speed (ms):", initialvalue=self.scroll_speed)
        if scroll_speed:
            self.scroll_speed = scroll_speed
            self.save_settings()


    def change_alignment(self):
        alignment = simpledialog.askstring("Alignment", "Enter alignment (left/right/center):", initialvalue=self.alignment)
        if alignment:
            self.alignment = alignment.lower()
            if self.alignment == "left":
                self.text.tag_configure("align", justify=tk.LEFT)
            elif self.alignment == "right":
                self.text.tag_configure("align", justify=tk.RIGHT)
            elif self.alignment == "center":
                self.text.tag_configure("align", justify=tk.CENTER)
            self.text.tag_add("align", 1.0, tk.END)
            self.save_settings()


    def save_settings(self, file_path="settings.json"):
        current_font = self.text.cget("font")
        font_name, font_size = current_font.split()
        settings = {
            "font": font_name,
            "font_size": int(font_size),
            "scroll_speed": self.scroll_speed,
            "theme": "dark" if self.text.cget("bg") == "black" else "light",
            "alignment": self.alignment
        }
        with open(file_path, "w") as file:
            json.dump(settings, file)

    def load_settings(self, file_path="settings.json"):
        try:
            with open(file_path, "r") as file:
                settings = json.load(file)
                self.text.config(font=(settings["font"], settings["font_size"]))
                self.scroll_speed = settings["scroll_speed"]
                self.alignment = settings["alignment"]
                if settings["theme"] == "dark":
                    self.root.config(bg="black")
                    self.text.config(bg="black", fg="white")
                elif settings["theme"] == "light":
                    self.root.config(bg="white")
                    self.text.config(bg="white", fg="black")
                if self.alignment == "left":
                    self.text.tag_configure("align", justify=tk.LEFT)
                elif self.alignment == "right":
                    self.text.tag_configure("align", justify=tk.RIGHT)
                elif self.alignment == "center":
                    self.text.tag_configure("align", justify=tk.CENTER)
                self.text.tag_add("align", 1.0, tk.END)
        except FileNotFoundError:
            pass


    def scroll_text(self):
        while self.scrolling:
            self.text.yview_scroll(self.scroll_step, "pixels")
            time.sleep(self.scroll_speed / 1000)

if __name__ == "__main__":
    root = tk.Tk()
    app = Teleprompter(root)
    root.mainloop()
