from email.policy import default
import gettext
import tkinter as tk
from pathlib import Path
from sys import platform
from tkinter.filedialog import askdirectory, askopenfilename

import ttkwidgets.autocomplete as ttkwa

import core

_ = gettext.gettext

class Application:
    def __init__(self, master:tk.Tk=None):

        master.title("Vers2Img")

        self.load_default()

        if platform == "linux":
            self.os_font = "Liberation Sans.ttf"
        elif platform == "win32" or platform == "cygwin":
            self.os_font = "Verdana.ttf"
        elif platform == "darwin":
            self.os_font = "Lucida Grande.ttf"
        self.ui_font  = (self.os_font, "8")

        # Title
        self.title_container = tk.Frame(master)
        self.title_container["pady"] = 10
        self.title_container.pack()

        self.title = tk.Label(self.title_container, text=_("Generate versicle images"))
        self.title["font"] = (self.os_font, "9", "bold")
        self.title.pack()

        # Version
        self.version_container = tk.Frame(master)
        self.version_container["padx"] = 20
        self.version_container["pady"] = 5
        self.version_container.pack()

        self.label_version = tk.Label(self.version_container,
            text=_("Version:"), font=self.ui_font, width=10)
        self.label_version.pack(side=tk.LEFT)

        versions = [version.stem.upper() for version in Path(f"{core.install_path}/assets/versions").iterdir() if version.name.endswith(".json")]
        if Path(f"{core.home_path}/versions").exists():
            versions.extend([version.stem.upper() for version in Path(f"{core.home_path}/versions").iterdir() if version.name.endswith(".json")])
        self.selected_version = tk.StringVar(self.version_container)
        self.selected_version.trace("w", self.load_bible)
        self.option_version = ttkwa.AutocompleteCombobox(self.version_container, completevalues=versions, textvariable=self.selected_version)
        self.option_version["width"] = 20
        self.option_version["font"] = self.ui_font
        self.option_version.pack(side=tk.LEFT)

        # Book
        self.book_container = tk.Frame(master)
        self.book_container["padx"] = 20
        self.book_container["pady"] = 5
        self.book_container.pack()

        self.label_book = tk.Label(self.book_container, text=_("Book:"),
            font=self.ui_font, width=10)
        self.label_book.pack(side=tk.LEFT)

        books = []
        self.selected_book = tk.StringVar(self.book_container)
        self.selected_book.trace("w", self.load_book)
        self.option_book = ttkwa.AutocompleteCombobox(self.book_container, completevalues=books, textvariable=self.selected_book)
        self.option_book["width"] = 20
        self.option_book["font"] = self.ui_font
        self.option_book.pack(side=tk.LEFT)

        # Chapter
        self.chapter_container = tk.Frame(master)
        self.chapter_container["padx"] = 20
        self.chapter_container["pady"] = 5
        self.chapter_container.pack()

        self.label_chapter = tk.Label(self.chapter_container, text=_("Chapter:"),
            font=self.ui_font, width=10)
        self.label_chapter.pack(side=tk.LEFT)

        chapters = []
        self.selected_chapter = tk.StringVar(self.chapter_container)
        self.selected_chapter.trace("w", self.load_chapter)
        self.option_chapter = ttkwa.AutocompleteCombobox(self.chapter_container, completevalues=chapters, textvariable=self.selected_chapter)
        self.option_chapter["width"] = 20
        self.option_chapter["font"] = self.ui_font
        self.option_chapter.pack(side=tk.LEFT)

        # Versicle
        self.versicle_container = tk.Frame(master)
        self.versicle_container["padx"] = 20
        self.versicle_container["pady"] = 5
        self.versicle_container.pack()

        self.label_min_versicle= tk.Label(self.versicle_container, text=_("Versicle from:"),
            font=self.ui_font, width=10)
        self.label_min_versicle.pack(side=tk.LEFT)

        versicles = []
        self.selected_min_versicle = tk.StringVar(self.versicle_container)
        self.selected_min_versicle.trace("w", self.versicle_min_options)
        self.option_min_versicle = ttkwa.AutocompleteCombobox(self.versicle_container, completevalues=versicles, textvariable=self.selected_min_versicle)
        self.option_min_versicle["width"] = 5
        self.option_min_versicle["font"] = self.ui_font
        self.option_min_versicle.pack(side=tk.LEFT)

        self.label_max_versicle = tk.Label(self.versicle_container, text=_("to:"),
            font=self.ui_font, width=3)
        self.label_max_versicle.pack(side=tk.LEFT)

        self.selected_max_versicle = tk.StringVar(self.versicle_container)
        self.selected_max_versicle.trace("w", self.versicle_max_options)
        self.option_max_versicle = ttkwa.AutocompleteCombobox(self.versicle_container, completevalues=versicles, textvariable=self.selected_max_versicle)
        self.option_max_versicle["width"] = 5
        self.option_max_versicle["font"] = self.ui_font
        self.option_max_versicle.pack(side=tk.LEFT)

        # Fonts
        fonts = [item.name for item in Path(f'{core.install_path}/assets/fonts/').iterdir() if item.name.endswith('.ttf')]
        if Path(f'{core.home_path}/fonts/').exists():
            fonts.extend([item.name for item in Path(f'{core.home_path}/fonts/').iterdir() if item.name.endswith('.ttf')])

        # Title Font
        self.title_font_container = tk.Frame(master)
        self.title_font_container["padx"] = 20
        self.title_font_container["pady"] = 5
        self.title_font_container.pack()

        self.title_font_label = tk.Label(self.title_font_container, text=_("Title Font:"),
            font=self.ui_font, width=10)
        self.title_font_label.pack(side=tk.LEFT)

        self.title_font = tk.StringVar(self.title_font_container)
        self.title_font.set(self.defaults["fonts"]["title"])
        self.option_title_font = ttkwa.AutocompleteCombobox(self.title_font_container, completevalues=fonts, textvariable=self.title_font)
        self.option_title_font["width"] = 20
        self.option_title_font["font"] = self.ui_font
        self.option_title_font.pack(side=tk.LEFT)

        self.title_size_label = tk.Label(self.title_font_container, text=_("Size:"),
            font=self.ui_font, width=10)
        self.title_size_label.pack(side=tk.LEFT)
        
        self.title_size = tk.Entry(self.title_font_container)
        self.title_size["width"] = 5
        self.title_size["font"] = self.ui_font
        self.title_size.delete(0, tk.END)
        self.title_size.insert(tk.INSERT, self.defaults["fonts"]["title_size"])
        self.title_size.pack(side=tk.LEFT)

        # Text Font
        self.text_font_container = tk.Frame(master)
        self.text_font_container["padx"] = 20
        self.text_font_container["pady"] = 5
        self.text_font_container.pack()

        self.text_font_label = tk.Label(self.text_font_container, text=_("Text Font:"),
            font=self.ui_font, width=10)
        self.text_font_label.pack(side=tk.LEFT)

        self.text_font = tk.StringVar(self.text_font_container)
        self.text_font.set(self.defaults["fonts"]["text"])
        self.option_text_font = ttkwa.AutocompleteCombobox(self.text_font_container, completevalues=fonts, textvariable=self.text_font)
        self.option_text_font["width"] = 20
        self.option_text_font["font"] = self.ui_font
        self.option_text_font.pack(side=tk.LEFT)

        self.text_size_label = tk.Label(self.text_font_container, text=_("Size:"),
            font=self.ui_font, width=10)
        self.text_size_label.pack(side=tk.LEFT)
        
        self.text_size = tk.Entry(self.text_font_container)
        self.text_size["width"] = 5
        self.text_size["font"] = self.ui_font
        self.text_size.delete(0, tk.END)
        self.text_size.insert(tk.INSERT, self.defaults["fonts"]["text_size"])
        self.text_size.pack(side=tk.LEFT)

        # Background
        self.background_container = tk.Frame(master)
        self.background_container["padx"] = 20
        self.background_container["pady"] = 5
        self.background_container.pack(ipadx=2)

        self.label_background= tk.Label(self.background_container, text=_("Background:"),
            font=self.ui_font, width=15)
        self.label_background.pack(side=tk.LEFT)

        self.selected_background = tk.Entry(self.background_container)
        self.selected_background["width"] = 20
        self.selected_background["font"] = self.ui_font
        self.selected_background.delete(0, tk.END)
        self.selected_background.insert(tk.INSERT, self.defaults["background"])
        self.selected_background.pack(side=tk.LEFT)

        self.button_search_background = tk.Button(self.background_container, text=_("Search"),
            font=self.ui_font, width=10)
        self.button_search_background["command"] = self.search_background
        self.button_search_background.pack(side=tk.RIGHT)

        # Destino
        self.destination_container = tk.Frame(master)
        self.destination_container["padx"] = 20
        self.destination_container["pady"] = 5
        self.destination_container.pack(ipadx=2)

        self.label_destination= tk.Label(self.destination_container, text=_("Destination Folder:"),
            font=self.ui_font, width=15)
        self.label_destination.pack(side=tk.LEFT)

        self.selected_destination = tk.Entry(self.destination_container)
        self.selected_destination["width"] = 20
        self.selected_destination["font"] = self.ui_font
        self.selected_destination.pack(side=tk.LEFT)

        self.button_search_destination = tk.Button(self.destination_container, text=_("Search"),
            font=self.ui_font, width=10)
        self.button_search_destination["command"] = self.search_destination
        self.button_search_destination.pack(side=tk.RIGHT)

        # Buttons
        self.button_container = tk.Frame(master)
        self.button_container["padx"] = 20
        self.button_container["pady"] = 10
        self.button_container.pack()

        self.button_save_default = tk.Button(self.button_container, text=_("Save Default"),
            font=self.ui_font, width=15)
        self.button_save_default["command"] = self.save_default
        self.button_save_default.pack (side=tk.LEFT)

        self.button_reset_default = tk.Button(self.button_container, text=_("Load Default"),
            font=self.ui_font, width=15)
        self.button_reset_default["command"] = self.reset_default
        self.button_reset_default.pack (side=tk.LEFT)

        self.button_generate = tk.Button(self.button_container, text=_("Generate Images"),
            font=self.ui_font, width=15)
        self.button_generate["command"] = self.render_images
        self.button_generate.pack(side=tk.LEFT)

        self.button_preview = tk.Button(self.button_container, text=_("Preview"),
            font=self.ui_font, width=15)
        self.button_preview["command"] = self.preview
        self.button_preview.pack(side=tk.LEFT)
        
        # Messages
        self.message_container = tk.Frame(master)
        self.message_container["pady"] = 15
        self.message_container.pack()

        self.lblmsg = tk.Label(self.message_container, text="")
        self.lblmsg["font"] = (self.os_font, "9", "italic")
        self.lblmsg.pack()

        self.selected_version.set(self.defaults["version"])

    def load_default(self):
        self.defaults = core.load_default()
    
    def reset_default(self):
        self.selected_version.set(self.defaults["version"])
        self.selected_background.delete(0, tk.END)
        self.selected_background.insert(tk.INSERT, self.defaults["background"])
        self.text_font.set(self.defaults['fonts']['text'])
        self.title_font.set(self.defaults['fonts']['title'])
        self.text_size.delete(0, tk.END)
        self.text_size.insert(tk.INSERT, self.defaults['fonts']['text_size'])
        self.title_size.delete(0, tk.END)
        self.title_size.insert(tk.INSERT, self.defaults['fonts']['title_size'])
        self.lblmsg["text"] = _("Default settings loaded")

    def save_default(self):
        self.defaults = core.save_default(
            background=self.selected_background.get(),
            version=self.selected_version.get(),
            title_font=self.title_font.get(),
            title_size=self.title_size.get(),
            text_font=self.text_font.get(),
            text_size=self.text_size.get()
        )
        self.lblmsg["text"] = _("Default satting saved")
    
    def load_bible(self, *args):
        version = self.selected_version.get()
        self.bible = core.load_bible(version)
        self.option_book["values"] = [book["name"] for book in self.bible]
        self.selected_book.set(self.bible[0]["name"])
 
    def load_book(self, *args):
        try:
            book = core.load_book(bible=self.bible, name=self.selected_book.get())
        except:
            return
        self.book = book
        self.option_chapter['values'] = list([i for i in range(1, len(self.book['chapters'])+1)])
        self.selected_chapter.set("1")

    def load_chapter(self, *args):
        self.option_min_versicle['values'] = self.option_max_versicle['values'] = list([i for i in range(1, len(self.book['chapters'][ int(self.selected_chapter.get()) - 1 ] ) + 1)])
        self.selected_min_versicle.set("1")
        self.selected_max_versicle.set("1")
    
    def versicle_min_options(self, *args):
        min_versicle = self.selected_min_versicle.get() or 1
        max_versicle = self.selected_max_versicle.get() or 1
        if int(min_versicle) > int(max_versicle):
            self.selected_max_versicle.set(min_versicle)
        
    def versicle_max_options(self, *args):
        min_versicle = self.selected_min_versicle.get() or 1
        max_versicle = self.selected_max_versicle.get() or 1
        if int(max_versicle) < int(min_versicle):
            self.selected_min_versicle.set(max_versicle)

    def search_background(self):
        self.selected_background.delete(0, tk.END)
        self.selected_background.insert(tk.INSERT, askopenfilename())

    def search_destination(self):
        self.selected_destination.delete(0, tk.END)
        self.selected_destination.insert(tk.INSERT, askdirectory())

    def preview(self):
        core.render_preview(
            title_font=self.title_font.get(),
            title_size=self.title_size.get(),
            text_font=self.text_font.get(),
            text_size=self.text_size.get(),
            background=self.selected_background.get()
        )

    def render_images(self):
        if self.selected_destination.get() is '' or not Path(self.selected_destination.get()).is_dir():
            self.lblmsg["text"] = _("Please select a valid destination folder")
            return
        core.render_text(
            book=self.book,
            chapter=self.selected_chapter.get(),
            versicle=f'{self.selected_min_versicle.get()}-{self.selected_max_versicle.get()}',
            title_font=self.title_font.get(),
            title_size=self.title_size.get(),
            text_font=self.text_font.get(),
            text_size=self.text_size.get(),
            output=self.selected_destination.get(),
            background=self.selected_background.get()
        )
        self.lblmsg["text"] = _("Images generated")

if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()
