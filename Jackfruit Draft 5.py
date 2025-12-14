import cv2
import numpy as np
from PIL import Image

def resize_image(input_path, output_path, new_width, new_height):
    img = Image.open(input_path)
    img = img.resize((new_width, new_height), Image.LANCZOS)  # high-quality downscale
    img.save(output_path)
    return output_path
    
def show_histogram(img_path):
    import matplotlib.pyplot as plt
    
    img = cv2.imread(img_path)
    colors = ('b', 'g', 'r')

    plt.figure(figsize=(8, 5))
    plt.title("Color Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    for i, col in enumerate(colors):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)

    plt.show()

def sepia_filter(img_path, output_path):
    img = cv2.imread(img_path)
    
    sepia_matrix = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.693, 1.469, 0.289]
    ])
 
    sepia_img = cv2.transform(img, sepia_matrix)
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, sepia_img)
    return sepia_img

def film_filter(img_path, output_path):
    img = cv2.imread(img_path)
    
    film_matrix =np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]])
 
    film_img = cv2.transform(img, film_matrix)
    film_img = np.clip(film_img, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, film_img)
    return film_img

def negative_filter(img_path, output_path):
    img = cv2.imread(img_path)
    negative_img = 255 - img
    cv2.imwrite(output_path, negative_img)
    return negative_img

def oil_paint_filter(img_path, output_path, radius=3, intensity_levels=32):

    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    factor = 256 // intensity_levels
    img_posterized = (img_rgb // factor) * factor

    height, width, _ = img_posterized.shape
    output = np.zeros_like(img_posterized)

    padded = cv2.copyMakeBorder(img_posterized, radius, radius, radius, radius, cv2.BORDER_REFLECT)

    for y in range(height):
        for x in range(width):
            window = padded[y:y+2*radius+1, x:x+2*radius+1].reshape(-1, 3)
            colors, counts = np.unique(window, axis=0, return_counts=True)
            output[y, x] = colors[np.argmax(counts)]

    output_bgr = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, output_bgr)
    return output

# Test Run
if __name__ == "__main__":
    image = resize_image("image4.jpeg", "small.jpg", 400, 400)
    show_histogram(image)
    sepia_filter(image, "final_output_sepia.jpg")
    film_filter(image, "final_output_film.jpg")
    negative_filter(image, "final_output_negative.jpg")
    oil_paint_filter(image, "final_output_oilpaint.jpg")

