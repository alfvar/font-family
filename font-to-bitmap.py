import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os

# Set the font size and scale factor
font_size = 64
scale_factor = 2
font_dir = "fonts/"

# Loop through all font files in the directory
for filename in os.listdir(font_dir):
    if filename.endswith(".ttf") or filename.endswith(".otf"):
        font_path = os.path.join(font_dir, filename)

        # Load the font file
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

        img.save(os.path.splitext(font_path)[0] + ".png")
