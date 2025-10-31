import math

import cv2
import numpy as np

from helper import (
    coordinate_in_cm,
    is_contour_within_workspace_boundary,
    is_coordinates_exist,
)
from MyObjectDetector import *

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
parameters = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(dictionary, parameters)

# Load your Object Detector
detector = NewObjectDetector()


def detect_object(img, shape: str, color: str):
    # Get Aruco marker corner and id
    corners, __, _ = arucoDetector.detectMarkers(img)

    objects_coordinate = []

    if corners:

        # Draw polygon around the marker
        int_corners = np.int32(
            corners
        )  # convert to ints since polylines does not accept array
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
        top_left, top_right, bottom_right, bottom_left = corners[0][0]

        marker_actual_size = 10
        pixel_width = np.linalg.norm(top_right - top_left)

        # Pixel to cm ratio
        pixel_cm_ratio = marker_actual_size / pixel_width

        # use Script to extract contours
        contours = detector.My_detector(img, color)

        # workobject dimensions in pixels
        workobj_width = 36 / pixel_cm_ratio
        workobj_height = 36 / pixel_cm_ratio

        # Define workspace area, for example, the board area
        workobj_pixels = [
            (0, 0),
            (0, workobj_width),
            (workobj_height, workobj_width),
            (workobj_height, 0),
        ]
        workobj_polygon = np.array(workobj_pixels, dtype=np.int32)

        # Draw objects boundaries
        for cnt in contours:
            # checks if contour is within workspace, skip if not within area
            if not is_contour_within_workspace_boundary(cnt, workobj_polygon):
                continue

            if shape == "Rectangle" or shape == "All":  # If the object is Rectangle
                rx, ry = detect_rectangle(
                    img,
                    cnt,
                    pixel_cm_ratio,
                )
                # if shape is detected, return the center coordinate
                if rx and ry:
                    new_coordinate = (1, rx, ry)  # shape, x_coordinate, y_coordinate
                    is_exist, index = is_coordinates_exist(
                        objects_coordinate, new_coordinate
                    )
                    if is_exist:
                        objects_coordinate[index] = new_coordinate
                    else:
                        objects_coordinate.append(new_coordinate)

            if shape == "Triangle" or shape == "All":  # If the object is Triangle
                rx, ry = detect_triangle(img, cnt, pixel_cm_ratio)
                # if shape is detected, return the center coordinate
                if rx and ry:
                    new_coordinate = (2, rx, ry)  # shape, x_coordinate, y_coordinate
                    is_exist, index = is_coordinates_exist(
                        objects_coordinate, new_coordinate
                    )
                    if is_exist:
                        objects_coordinate[index] = new_coordinate
                    else:
                        objects_coordinate.append(new_coordinate)

            if shape == "Hexagonal" or shape == "All":  # If the object is Hexagonal
                rx, ry = detect_hexagonal(img, cnt, pixel_cm_ratio)
                # if shape is detected, return the center coordinate
                if rx and ry:
                    new_coordinate = (3, rx, ry)  # shape, x_coordinate, y_coordinate
                    is_exist, index = is_coordinates_exist(
                        objects_coordinate, new_coordinate
                    )
                    if is_exist:
                        objects_coordinate[index] = new_coordinate
                    else:
                        objects_coordinate.append(new_coordinate)

            if shape == "Star" or shape == "All":  # If the object is Star
                rx, ry = detect_star(img, cnt, pixel_cm_ratio)
                # if shape is detected, return the center coordinate
                if rx and ry:
                    new_coordinate = (4, rx, ry)  # shape, x_coordinate, y_coordinate
                    is_exist, index = is_coordinates_exist(
                        objects_coordinate, new_coordinate
                    )
                    if is_exist:
                        objects_coordinate[index] = new_coordinate
                    else:
                        objects_coordinate.append(new_coordinate)

            if shape == "Circle" or shape == "All":  # If the object is Circle
                rx, ry = detect_circle(img, cnt, pixel_cm_ratio)
                # if shape is detected, return the center coordinate
                if rx and ry:
                    new_coordinate = (5, rx, ry)  # shape, x_coordinate, y_coordinate
                    is_exist, index = is_coordinates_exist(
                        objects_coordinate, new_coordinate
                    )
                    if is_exist:
                        objects_coordinate[index] = new_coordinate
                    else:
                        objects_coordinate.append(new_coordinate)

    return objects_coordinate


# Draw the triangle shape
def detect_triangle(img, cnt, pixel_cm_ratio):
    # Approximate the contour
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

    # Check if the contour has 3 vertices (triangle)
    if len(approx) == 3:
        # Calculate the area of the triangle
        area = cv2.contourArea(cnt) * (pixel_cm_ratio**2)

        if 11 < area < 13:
            # Calculate the center of the triangle
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])

                center_x, center_y = coordinate_in_cm(x, y, pixel_cm_ratio)

                cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
                cv2.polylines(img, [approx], True, (0, 225, 0), 3)

                return center_y, center_x

    return None, None


# Draw the hexagonal shape
def detect_hexagonal(img, cnt, pixel_cm_ratio):
    # Approximate the contour
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

    # Check if the contour has 6 vertices (hexagonal)
    if len(approx) == 6:
        # Calculate the area of the hexagonal
        area = cv2.contourArea(cnt) * (pixel_cm_ratio**2)

        if 23 < area < 26:
            # Calculate the center of the hexagonal
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])

                center_x, center_y = coordinate_in_cm(x, y, pixel_cm_ratio)

                cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
                cv2.polylines(img, [approx], True, (0, 225, 0), 3)

                return center_y, center_x

    return None, None


# Draw the star shape
def detect_star(img, cnt, pixel_cm_ratio):
    # Approximate the contour
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

    # Check if the contour has 10 vertices (star)

    if 9 <= len(approx) <= 11:

        # Calculate the area of the star
        area = cv2.contourArea(cnt) * (pixel_cm_ratio**2)

        if 9 < area < 15:
            # Calculate the center of the star
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])

                center_x, center_y = coordinate_in_cm(x, y, pixel_cm_ratio)

                cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
                cv2.polylines(img, [approx], True, (0, 225, 0), 3)

                return center_y, center_x

    return None, None


# Draw the circle shape
def detect_circle(img, cnt, pixel_cm_ratio):

    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

    if peri == 0:
        return None, None

    circle = cv2.minEnclosingCircle(cnt)
    (x, y), radius = circle
    correct_per = 2 * math.pi * radius

    # Keep only shapes close to a perfect circle
    if len(approx) == 8 and 620 < correct_per < 680:  # adjust area threshold as needed
        circle = cv2.minEnclosingCircle(cnt)
        (x, y), radius = circle

        center_x, center_y = coordinate_in_cm(x, y, pixel_cm_ratio)

        # Draw circle outline
        cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
        cv2.circle(
            img, (int(x), int(y)), int(radius), (0, 255, 0), 2
        )  # Green circle around object

        return center_y, center_x

    return None, None


# Draw the rectangular shape
def detect_rectangle(img, cnt, pixel_cm_ratio):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

    # Get bounding rectangel of objects found
    rect = cv2.minAreaRect(cnt)
    (x, y), (w, h), angle = rect

    box = cv2.boxPoints(rect)
    # Get Width and Height of the Objects by applying the Ratio pixel to cm
    object_width = w * pixel_cm_ratio
    object_height = h * pixel_cm_ratio

    box = np.int32(box)
    # sort out qualifed shapes and keep center coords
    if (
        len(approx) == 4
        and object_width > 4.45
        and object_width < 5.2
        and object_height > 4.45
        and object_height < 5.2
    ):
        center_x, center_y = coordinate_in_cm(x, y, pixel_cm_ratio)

        cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
        cv2.polylines(img, [box], True, (0, 225, 0), 3)
        return center_y, center_x

    return None, None
