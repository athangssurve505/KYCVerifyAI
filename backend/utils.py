import base64
import cv2
import numpy as np

def base64_to_image(b64):
    b64 = b64.split(",")[-1]
    img_bytes = base64.b64decode(b64)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)
