import os
from fontTools.ttLib import TTFont
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Set the font size and scale factor
font_size = 64
scale_factor = 2
font_dir = "fonts/"
output_dir = "output/"


# Get font metadata
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
    }
    return font_metadata

# Loop through all font files in the directory
for filename in os.listdir(font_dir):
    if filename.endswith(".ttf") or filename.endswith(".otf"):
        font_path = os.path.join(font_dir, filename)

        # Extract font metadata
        font_metadata = extract_font_metadata(font_path)
        font_style_head = font_metadata["style-head"]

        print(font_metadata)

        # Load the font file for visual rendering
        font = ImageFont.truetype(font_path, font_size * scale_factor)

        num_characters = 256
        grid_size = 16

        left, top, right, bottom = font.getbbox("A")  # Assumes all glyphs have similar size
        cell_width, cell_height = (right - left) * scale_factor, (bottom - top) * scale_factor
        margin = 8 * scale_factor

        image_width = cell_width * grid_size + margin * (grid_size + 1)
        image_height = cell_height * grid_size + margin * (grid_size + 1)

        img = Image.new("RGBA", (image_width, image_height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        for i in range(num_characters):
            x = i % grid_size
            y = i // grid_size
            draw_x = margin + x * (cell_width + margin)
            draw_y = margin + y * (cell_height + margin)
            draw.text((draw_x, draw_y), chr(i), (0, 0, 0), font=font)

        filename_base, ext = os.path.splitext(font_path)
        img.save(f"{filename_base}_{font_style_head}.png")