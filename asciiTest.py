import cv2
import numpy as np

def image_to_ascii(img):
    
    
    # If a file path (string) was passed instead of an image
    if isinstance(img, str):
        img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
        if img is None:
            return "wrong image format"


    # If 4 channels (RGBA), drop alpha
    if img.ndim == 3 and img.shape[2] == 4:
        img = img[:, :, :3]

    # If grayscale 16-bit, convert to 8-bit
    if img.dtype == np.uint16:
        img = (img / 256).astype('uint8')

    # Convert to grayscale (now safe for any PNG)
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    height, width = gray.shape
    output_width = 100
    aspect_ratio = height / width
    output_height = int(output_width * aspect_ratio * 0.5)

    resized = cv2.resize(gray, (output_width, output_height))

    ascii_chars = "@%#*+=-:. "

    ascii_art = []
    for row in resized:
        ascii_row = ""
        for pixel in row:
            char_index = int(pixel / 255 * (len(ascii_chars) - 1))
            ascii_row += ascii_chars[char_index]
        ascii_art.append(ascii_row)

    return "\n".join(ascii_art)
