import cv2
import numpy as np

def ascii_art(img, width=120, theme='light', return_string=False):
    if isinstance(img, str):
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image")

    if img.ndim == 3 and img.shape[2] == 4:
        img = img[:, :, :3]

    if img.dtype != np.uint8:
        img = img.astype(np.uint8)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    font = cv2.FONT_HERSHEY_PLAIN
    (cw, ch), base = cv2.getTextSize("M", font, 1.0, 1)

    char_h = ch + base       
    char_w = cw
    char_ratio = char_h / char_w

    out_w = int(width)
    out_h = int((h / w) * out_w / char_ratio)
    out_h = max(1, out_h)

    resized = cv2.resize(gray, (out_w, out_h), interpolation=cv2.INTER_AREA)

    chars = "@%#*+=-:. "
    scale = (len(chars) - 1) / 255

    lines = [
        ''.join(chars[int(px * scale)] for px in row)
        for row in resized
    ]

    if return_string:
        return "\n".join(lines)
    
    pad = 10
    img_w = out_w * char_w + pad * 2
    img_h = out_h * char_h + pad * 2

    bg = 0 if theme == 'dark' else 255
    fg = (220, 220, 220) if theme == 'dark' else (0, 0, 0)

    output = np.full((img_h, img_w, 3), bg, dtype=np.uint8)
    
    y = pad + ch
    for line in lines:
        x = pad
        for c in line:
            cv2.putText(output, c, (x, y), font, 1.0, fg, 1, cv2.LINE_AA)
            x += char_w
        y += char_h

    return output
