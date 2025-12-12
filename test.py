import numpy as n
import cv2 as c

def cartoonify(img,intensity):
    
    
            
    gray = c.cvtColor(img, c.COLOR_BGR2GRAY)
    gray = c.medianBlur(gray, 5)
    max_value = 55+intensity*100 #specifies maximum intensity
    block_size = 11 #specifies size of local neighborhood
    offset_C = 5 #used to bring balance

    adaptive = c.adaptiveThreshold(gray, max_value, c.ADAPTIVE_THRESH_MEAN_C, c.THRESH_BINARY, block_size, offset_C)
            #adaptive threshold mean handles varying illumination
            #thresh binary converts pixel intensity>max_value to white and remaining to black

    fil = c.bilateralFilter(gray, 12, 250, 250)

    cartoon = c.bitwise_and(adaptive, adaptive, mask = fil)
    return cartoon

def sketch_filter(img,intensity):
    image = img 

    g = c.cvtColor(image, c.COLOR_BGR2GRAY)
    g = c.medianBlur(g, 5)

    max_val = 255+intensity*100
    e = c.adaptiveThreshold(g, max_val, c.ADAPTIVE_THRESH_MEAN_C,
                            c.THRESH_BINARY, 9, 9)

    d = c.bilateralFilter(image, 9, 350, 350) 
    
    sketch = c.bitwise_and(d,d, mask=e)
    return sketch

def Black_White(img, intensity):
    gray = c.cvtColor(img, c.COLOR_BGR2GRAY)
    
    thresh_val = 137 - int(intensity * 30)
    
    trash_val, result = c.threshold(gray, thresh_val, 255, c.THRESH_BINARY) 
    
    return result
            

    
