from PIL import Image, ImageFont, ImageDraw
import json
import math
import argparse
import sys


def text_wrap(text, font, max_widthidth):
    lines = []
    if font.getsize(text)[0] <= max_widthidth:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_widthidth:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines


# Read/Interpret Input
parser = argparse.ArgumentParser(
    description='Gerar imagens com versicleículos para o culto')
parser.add_argument("reference",
    action="store", help="Abreviação da referência do texto. Ex: 1Ts_1_1-3")
parser.add_argument("--versicleion",
	dest="versicleion", action="store", default="nvi", help="versicleão da Biblia a ser usada. Disponíveis: AA, ACF, NVI. Default: NVI")
parser.add_argument("--output",
    dest="output", action="store", default=".", help="Seleciona caminho de saída. Default: .")
args = parser.parse_args()

if (len(args.reference.split("_")) != 3):
    print("Entrada de referência fora do padrão")
    sys.exit()

# Settings
color = (255, 247, 213)
min_width = 320
max_width = 1600
min_height = 210
max_height = ref_height = 870

# Load Content
scriptina = ImageFont.truetype("assets/fonts/SCRIPTIN.ttf", 70)
bitter70 = ImageFont.truetype("assets/fonts/Bitter-Regular.ttf", 70)
bitter50 = ImageFont.truetype("assets/fonts/Bitter-Regular.ttf", 50)
with open("assets/versicleions/{}.json".format(args.versicleion.lower()), encoding='utf-8-sig') as file:
    bible = json.load(file)

# Prepare Text
book_ab, chapter, versicle = args.reference.split("_")
try:
    book = next(book for book in bible if book["abbrev"] == book_ab.lower())
except:
    answer = input("Abreviatura inválida. Deseja ver a lista de abreviaturas? (s/N) ")
    if (answer == "S" or answer == "s"):
        for book in bible:
            print("{}: {}".format(book["abbrev"], book["name"]))
    sys.exit()

# Render Text
versicle = versicle.split("-")
v_in = v_out = int(versicle[0])
if (len(versicle) == 2):
    v_out = int(versicle[1])
for v in range(v_in, v_out + 1):
    image = Image.open("assets/background.jpg")
    ref_text = "{} {}:{}".format(book["name"], chapter, v)
    versicle_text = book["chapters"][int(chapter) - 1][int(v) - 1]
    image_w, image_h = image.size
    image_editable = ImageDraw.Draw(image)

    # Reference
    line_width = scriptina.getsize(ref_text)[0]
    ref_x = math.floor((image_w - line_width) / 2)
    image_editable.text((ref_x, ref_height), ref_text, color, font=scriptina, align="center")

    # Versicle
    bitter = bitter70
    text_length = max_width - min_width
    lines = text_wrap(versicle_text, bitter, text_length)
    line_height = bitter.getsize("hg")[1]
    versicle_height = (len(lines) * line_height)
    if (versicle_height > max_height - min_height):
        bitter = bitter50
        lines = text_wrap(versicle_text, bitter, text_length)
        line_height = bitter.getsize("hg")[1]
        versicle_height = (len(lines) * line_height)
    versicle_y_min = math.floor((image_h - versicle_height) / 2)
    versicle_y = versicle_y_min
    for line in lines:
        line_width = bitter.getsize(line)[0]
        versicle_x = math.floor((image_w - line_width) / 2)
        image_editable.text((versicle_x, versicle_y), line, color, font=bitter, align="center")
        versicle_y = versicle_y + line_height

    # Export Image
    image.save("{}/{}-{}-{}.jpg".format(args.output, book["abbrev"], chapter, v))
