import numpy as np
import cv2

def generate_noisy_shapes(noise_level=40):
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    cv2.circle(img, (80, 128), 40, (255, 255, 255), -1)
    pts = np.array([[160, 80], [200, 180], [120, 180]], np.int32).reshape((-1,1,2))
    cv2.fillPoly(img, [pts], (255, 255, 255))
    noise = np.random.normal(0, noise_level, img.shape).astype(np.uint8)
    return cv2.add(img, noise)
