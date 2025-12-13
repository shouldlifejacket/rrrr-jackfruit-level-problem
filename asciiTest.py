from PIL import Image, ImageFont, ImageDraw

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def image_to_ascii(img, new_width=150):
    width, height = img.size
    try:
        font = ImageFont.truetype("cour.ttf", size=12)
    except:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\cour.ttf", size=12)
    bbox = font.getbbox("A")
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]
    char_aspect = char_width / char_height
    new_height = int((height / width) * new_width / char_aspect)
    img = img.resize((new_width, new_height)).convert("L")
    pixels = img.getdata()

    ascii_str = "".join(
        ASCII_CHARS[int(p / 255 * (len(ASCII_CHARS) - 1))]
        for p in pixels
    )

    ascii_lines = [
        ascii_str[i:i + new_width].ljust(new_width, ASCII_CHARS[-1])
        for i in range(0, len(ascii_str), new_width)
    ]
    img_width = char_width * new_width
    img_height = char_height * new_height
    ascii_img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(ascii_img)
    y = 0
    for line in ascii_lines:
        draw.text((0, y), line, fill="black", font=font)
        y += char_height

    return ascii_img
