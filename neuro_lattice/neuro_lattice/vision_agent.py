import cv2
import numpy as np

class VisionAgent:
    def __init__(self, denoise=True):
        self.denoise = denoise

    def detect_shapes(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.denoise:
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shapes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 300: 
                continue
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
            sides = len(approx)
            circularity = (4 * np.pi * area) / (perimeter ** 2 + 1e-5)
            if 0.7 < circularity <= 1.2 and area > 1000:
                shapes.append('circle')
            elif sides == 3:
                shapes.append('triangle')
        return list(set(shapes)) if shapes else ["unknown"]
