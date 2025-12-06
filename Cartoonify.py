import numpy as n
import cv2 as c

def image_input():
    image = input("Please enter the path of the image you would like to access: ")

    img = c.imread(image)

    while True:
        if img is None:
            print(f"Could not access the image please try again")
            break
        else:
            print("Prcoessing image...")

        
        gray = c.cvtColor(img, c.COLOR_BGR2GRAY)
        gray = c.medianBlur(gray, 5)
        max_value = 255 #specifies maximum intensity
        block_size = 7 #specifies size of local neighborhood
        offset_C = 2 #used to bring balance

        adaptive = c.adaptiveThreshold(gray, max_value, c.ADAPTIVE_THRESH_MEAN_C, c.THRESH_BINARY, block_size, offset_C)
        #adaptive threshold mean handles varying illumination
        #thresh binary converts pixel intensity>max_value to white and remaining to black

        fil = c.bilateralFilter(gray, 12, 250, 250)

        cartoon = c.bitwise_and(adaptive, adaptive, mask = fil)

        c.imshow('filter', cartoon)
        c.waitKey(0)
        c.destroyAllWindows()
        break

image_input()