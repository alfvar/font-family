import os
from fontTools.ttLib import TTFont
import json


from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Set the font size and scale factor
font_size = 64
scale_factor = 1
font_dir = "fonts/"
output_dir = "font-data/"
shift_offset = 8 * scale_factor


# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)


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

# Loop through all font files in the directory and its subdirectories
for root, dirs, files in os.walk(font_dir):
    for filename in files:
        if filename.endswith(".ttf") or filename.endswith(".otf"):
            font_path = os.path.join(root, filename)

        # Extract font metadata
        font_metadata = extract_font_metadata(font_path)
        font_style_head = font_metadata["style-head"]

        print(font_metadata)

        # Save metadata as JSON
        metadata_filename = os.path.join(output_dir, f"{font_metadata['name'].replace(' ', '_')}_{font_metadata['style-head'].replace(' ', '_')}.json")
        with open(metadata_filename, 'w') as f:
            json.dump(font_metadata, f)


        # Load the font file for visual rendering
        font = ImageFont.truetype(font_path, font_size * scale_factor)

        num_characters = 128
        grid_size = 10

        # Define fixed cell size
        cell_width, cell_height = 96 * scale_factor, 96 * scale_factor
        margin = 8 * scale_factor

        image_width = cell_width * grid_size + margin * (grid_size + 1)
        image_height = cell_height * grid_size + margin * (grid_size + 1)

        img = Image.new("L", (image_width, image_height), 255)
        draw = ImageDraw.Draw(img)

        for i in range(35, num_characters):
            x = (i - 35) % grid_size  # Subtract the offset (35) from i
            y = (i - 35) // grid_size  # Subtract the offset (35) from i
            draw_x = margin + shift_offset + x * (cell_width + margin)
            draw_y = margin + y * (cell_height + margin)

            # Get the glyph bounding box
            left, top, right, bottom = font.getbbox(chr(i))

            # Calculate the centering offsets
            offset_x = (cell_width - (right - left) * scale_factor) // 2
            offset_y = (cell_height - (bottom - top) * scale_factor) // 2

            draw.text((draw_x + offset_x, draw_y + offset_y), chr(i), (0), font=font)

        filename_base, ext = os.path.splitext(font_path)
        output_filename = os.path.join(output_dir, f"{font_metadata['name'].replace(' ', '_')}_{font_metadata['style-head'].replace(' ', '_')}.png")
        img.save(output_filename)