import os
from fontTools.ttLib import TTFont

def extract_font_metadata(font_path):
    font = TTFont(font_path)
    font_name = font["name"].getName(4, 3, 1, 0x409).toUnicode()
    font_style = font["name"].getName(2, 3, 1, 0x409).toUnicode()
    font_weight = font["OS/2"].usWeightClass

        # Extract font style from "head" table
    mac_style = font["head"].macStyle
    is_bold = bool(mac_style & 0x01)
    is_italic = bool(mac_style & 0x02)
    if is_bold and is_italic:
        font_style_head = "Bold Italic"
    elif is_bold:
        font_style_head = "Bold"
    elif is_italic:
        font_style_head = "Italic"
    else:
        font_style_head = "Regular"


    font_metadata = {
        "name": font_name,
        "style": font_style,
        "weight": font_weight,
        "style-head": font_style_head,        
        # Add other metadata attributes as needed
    }

    return font_metadata

target_folder = "fonts/"
font_files = [f for f in os.listdir(target_folder) if f.endswith((".ttf", ".otf"))]

font_metadata_list = []
for font_file in font_files:
    font_path = os.path.join(target_folder, font_file)
    font_metadata = extract_font_metadata(font_path)
    font_metadata_list.append(font_metadata)

for metadata in font_metadata_list:
    print(metadata)
