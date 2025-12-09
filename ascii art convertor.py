import cv2
import numpy 

def image_to_ascii(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "wrong image format "
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
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


if __name__ == "__main__":
    ascii_result = image_to_ascii('apple.png')
    print(ascii_result)
    
    with open('ascii_art.txt', 'w') as f:
        f.write(ascii_result)
