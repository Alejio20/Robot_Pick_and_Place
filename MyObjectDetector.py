import cv2
import numpy as np


class NewObjectDetector:
    def __init__(self):
        pass

    def My_detector(self, img, filter_color):

        # Convert Image to grayscale
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_ranges = {
            "Red": (
                (np.array([0, 100, 100]), np.array([10, 255, 255])),
                (np.array([170, 100, 100]), np.array([180, 255, 255])),
            ),
            "Blue": ((np.array([100, 50, 50]), np.array([140, 255, 255])),),
            "Green": ((np.array([50, 100, 50]), np.array([90, 255, 255])),),
            "White": ((np.array([0, 0, 200]), np.array([0, 0, 255])),),
            "Black": ((np.array([0, 0, 0]), np.array([180, 255, 70])),),
        }

        # Create masks for each color
        masks = {}
        for color, ranges in color_ranges.items():
            if color == "Red":
                mask1 = cv2.inRange(hsv, ranges[0][0], ranges[0][1])
                mask2 = cv2.inRange(hsv, ranges[1][0], ranges[1][1])
                masks[color] = cv2.bitwise_or(mask1, mask2)
            else:
                masks[color] = cv2.inRange(hsv, ranges[0][0], ranges[0][1])

        objects_contours = []

        for color, mask in masks.items():
            if filter_color != "All" and color != filter_color:
                continue  # Skip colors that don't match the filter

            # Apply a slight blur to the mask to reduce noise before finding contours.
            blurred_mask = cv2.GaussianBlur(mask, (3, 3), 0)
            contours, _ = cv2.findContours(
                blurred_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for cnt in contours:
                area = cv2.contourArea(cnt)
                # Filter out the smallest stuff
                if area > 500:
                    objects_contours.append(cnt)

        return objects_contours
