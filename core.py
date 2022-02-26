import gettext
import json
import math
import os
import sys
from pathlib import Path
from tkinter import image_names
from typing import Dict

from PIL import Image, ImageDraw, ImageFont

# Settings
color = (255, 247, 213)
min_width = 320
max_width = 1600
min_height = 210
max_height = ref_height = 870

install_path = os.path.dirname(os.path.realpath(__file__))
home_path = Path(Path.home() / ".vers2img")

# TODO does it work properly?
#language = locale.getdefaultlocale()[0]
#os.environ['LANG'] = language
_ = gettext.gettext

def load_bible(version):
    if Path(f'{install_path}/assets/versions/{version}.json').exists():
        with Path(f'{install_path}/assets/versions/{version}.json').open(encoding="utf-8-sig") as f:
            bible = json.load(f)   
    elif Path(f'{home_path}/versions/{version}.json').exists():
        with Path(f'{home_path}/versions/{version}.json').open(encoding="utf-8-sig") as f:
            bible = json.load(f)
    return bible

def load_book(bible, name):
    book = next(book for book in bible if book["name"] == name)
    return book

def load_default():
    if not Path(home_path).exists():
        for folder in ["versions", "fonts", "background"]:
            Path(f"{home_path}/{folder}").mkdir(parents=True, exist_ok=True)
    default_file = Path(f'{home_path}/default.json')
    if not default_file.exists():
        defaults = {
            "background": Path(f"{install_path}/assets/background.jpg").__str__(),
            "version": "NVI",
            "fonts": {
                "title": "SCRIPTIN.ttf",
                "title_size": 70,
                "text": "Bitter-Regular.ttf",
                "text_size": 70
            }
        }
        with Path(default_file).open('w') as f:
            json.dump(defaults, f, indent=4)
        defaults = defaults
    else:
        with default_file.open() as f:
            defaults =  json.load(f)
    return defaults

def save_default(defaults, background=None, version=None, title_font=None, title_size=None, text_font=None, text_size=None):
    default_file = Path(f'{home_path}/default.json')
    if background is not None:
        defaults["background"] = background
    if version is not None:
        defaults["version"] = version
    if title_font is not None:
        defaults["fonts"]["title_font"] = title_font
    if title_size is not None:
        defaults["fonts"]["title_size"] = title_size
    if text_font is not None:
        defaults["fonts"]["text_font"] = text_font
    if text_size is not None:
        defaults["fonts"]["text_size"] = text_size
    with Path(default_file).open('w') as f:
        json.dump(defaults, f, indent=4)
    return defaults

def text_wrap(text, font, max_width):
    lines = []
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

def prepare_text(bible:Dict, reference:str):
    book_ab, chapter, versicles = reference.split("_")
    try:
        book = next(book for book in bible if book["abbrev"] == book_ab.lower())
    except:
        answer = input(_("Abbreviature invalid. Do you want to see the abbreaviature list? (y/N) "))
        answer.lower()
        if (answer == "s" or answer == "y"):
            for book in bible:
                print("{}: {}".format(book["abbrev"], book["name"]))
        sys.exit()
    return book, chapter, versicles

def _setup_font(title_font, title_size, text_font, text_size):
    if Path(f'{install_path}/assets/fonts/{title_font}').is_file():
        title_font = f'{install_path}/assets/fonts/{title_font}'
    elif Path(f'{home_path}/fonts/{title_font}').is_file():
        title_font = f'{home_path}/fonts/{title_font}'
    else:
        raise FileNotFoundError(_('Font: {} was not found.').format(title_font))
    if Path(f'{install_path}/assets/fonts/{text_font}').is_file():
        text_font = f'{install_path}/assets/fonts/{text_font}'
    elif Path(f'{home_path}/fonts/{text_font}').is_file():
        text_font = f'{home_path}/fonts/{text_font}'
    else:
        raise FileNotFoundError(_('Font: {} was not found.').format(text_font))  
    title_font = ImageFont.truetype(title_font, int(title_size))
    text_font_large = ImageFont.truetype(text_font, int(text_size))
    text_font_small = ImageFont.truetype(text_font, int(math.floor(int(text_size)*0.7)))

    return title_font, text_font_large, text_font_small

def _get_image(background):
    if background is not None and not Path(background).is_file():
        raise FileNotFoundError(_('Image: {} was not found.').format(background))  
    image = Image.open(background)
    image_w, image_h = image.size
    editable_image = ImageDraw.Draw(image)
    return image, editable_image, image_w, image_h

def _add_title(title, title_font, editable_image, image_w):
    line_width = title_font.getsize(title)[0]
    title_x = math.floor((image_w - line_width) / 2)
    editable_image.text((title_x, ref_height), title, color, font=title_font, align="center")

def _add_text(text, text_font_large, text_font_small, editable_image, image_w, image_h):
    text_font = text_font_large
    text_length = max_width - min_width
    lines = text_wrap(text, text_font, text_length)
    line_height = text_font.getsize("hg")[1]
    versicle_height = (len(lines) * line_height)
    if (versicle_height > max_height - min_height):
        text_font = text_font_small
        lines = text_wrap(text, text_font, text_length)
        line_height = text_font.getsize("hg")[1]
        versicle_height = (len(lines) * line_height)
    versicle_y_min = math.floor((image_h - versicle_height) / 2)
    versicle_y = versicle_y_min
    for line in lines:
        line_width = text_font.getsize(line)[0]
        versicle_x = math.floor((image_w - line_width) / 2)
        editable_image.text((versicle_x, versicle_y), line, color, font=text_font, align="center")
        versicle_y = versicle_y + line_height

def render_text(book, chapter, versicle:str, title_font, title_size, text_font, text_size, output, background):
    title_font, text_font_large, text_font_small = _setup_font(title_font, title_size, text_font, text_size)
    versicle = versicle.split("-")
    v_in = v_out = int(versicle[0])
    if (len(versicle) == 2):
        v_out = int(versicle[1])
    for v in range(v_in, v_out + 1):
        # SetUp
        image, editable_image, image_w, image_h = _get_image(background)
        ref_text = "{} {}:{}".format(book["name"], chapter, v)
        versicle_text = book["chapters"][int(chapter) - 1][int(v) - 1]
        # Reference
        _add_title(ref_text, title_font, editable_image, image_w)
        # Versicle
        _add_text(versicle_text, text_font_large, text_font_small, editable_image, image_w, image_h)
        # Export Image
        image.save("{}/{}-{}-{}.jpg".format(output, book["abbrev"], chapter, v))

def render_preview(title_font, title_size, text_font, text_size, background):
    # SetUp
    title = 'Lorem 1:1'
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    title_font, text_font_large, text_font_small = _setup_font(title_font, title_size, text_font, text_size)
    image, editable_image, image_w, image_h = _get_image(background)
    # Title
    _add_title(title, title_font, editable_image, image_w)
    # Text
    _add_text(text, text_font_large, text_font_small, editable_image, image_w, image_h)
    # Show
    image.show()
