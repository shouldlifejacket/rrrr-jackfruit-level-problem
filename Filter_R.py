import cv2
import numpy as np
from PIL import Image, ImageFilter

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

def sepia_filter(img,intensity):
        
    
    sepia_matrix = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.693, 1.469, 0.289]
    ])
 
    sepia_img = cv2.transform(img, sepia_matrix)
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    intensity = np.clip(intensity, 0.0, 1.0)
   
    return cv2.addWeighted(img, 1 - intensity, sepia_img, intensity, 0)

def negative_filter(img,intensity):
    
    negative_img = 255 - img
    intensity = np.clip(intensity, 0.0, 1.0)
    return cv2.addWeighted(img, 1 - intensity, negative_img, intensity, 0)


def film_filter(img,intensity):
    
    
    film_matrix =np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]])
 
    film_img = cv2.transform(img, film_matrix)
    film_img = np.clip(film_img, 0, 255).astype(np.uint8)
    intensity = np.clip(intensity, 0.0, 1.0)
    
    return cv2.addWeighted(img, 1 - intensity, film_img, intensity, 0)

def oil_paint_effect_fast(img, radius=3, intensity_levels=32):
    
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
    
    
    
    return output_bgr



