from PIL import Image, ImageFont, ImageDraw
import os

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def image_to_ascii(img, new_width=150):
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.45)   # GOOD results

    img = img.resize((new_width, new_height)).convert("L")
    pixels = img.getdata()

    ascii_str = "".join(ASCII_CHARS[p // 25] for p in pixels)
    ascii_lines = [ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)]

    return "\n".join(ascii_lines)


def save_ascii_as_image(ascii_text, output_path):
    try:
        font = ImageFont.truetype("cour.ttf", size=12)
    except:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\cour.ttf", size=12)

    lines = ascii_text.split("\n")

    char_width, char_height = font.getbbox("A")[2:]
    
    img_width = char_width * max(len(line) for line in lines)
    img_height = char_height * len(lines)

    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    y = 0
    for line in lines:
        draw.text((0, y), line, fill="black", font=font)
        y += char_height

    img.save(output_path)


def convert_image_to_ascii_image(input_path):
    img = Image.open(input_path)

    ascii_art = image_to_ascii(img)

    base, ext = os.path.splitext(input_path)
    output_path = base + "_ascii.png"

    save_ascii_as_image(ascii_art, output_path)

    print("Saved:", output_path)


# Test:
convert_image_to_ascii_image("image10.jpg")
