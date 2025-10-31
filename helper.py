from typing import List, Tuple

import cv2
import numpy as np


# convert the pixel value from camera to cm
def coordinate_in_cm(x, y, pixel_to_cm_ratio) -> Tuple[float, float]:
    return float(f"{(x*pixel_to_cm_ratio):.1f}"), float(f"{(y*pixel_to_cm_ratio):.1f}")


# This function checks if a new coordinate (x, y) is close to any of the existing coordinates in a list.
# If it finds a match (within a small allowed difference called "offset"), it returns:
#    - True, and the index (position) of the matching coordinate in the list.
# If not, it returns:
#    - False, and -1 to show no match was found.


def is_coordinates_exist(
    current_coordinates: List[
        Tuple[int, float, float]
    ],  # A list of coordinates, where each coordinate is a pair like (x, y)
    new_coordinate: Tuple[
        int, float, float
    ],  # A new coordinate (x, y) we want to check against the list
    offset: float = 1.0,  # Small allowed difference when comparing coordinates (default: 1)
) -> Tuple[bool, int]:  # Function will return a True/False and an index (integer)

    # Separate the new coordinate into x and y values
    shape, new_X, new_Y = new_coordinate

    # Go through each coordinate in the current list, one at a time
    for idx, (shape, current_X, current_Y) in enumerate(current_coordinates):
        # Check if both the x and y values are close enough (difference is smaller than the offset)
        if abs(current_X - new_X) <= offset and abs(current_Y - new_Y) <= offset:
            # If a match is found, return True and the index where it matched
            return True, idx

    # If no match is found in the entire list, return False and -1
    return False, -1


# This function creates and returns a new list of updated coordinates.
# It checks each new coordinate against the current list.
# If it exists (within a small offset), it replaces the old one.
# If it doesn't exist, it adds it to the new list.


def update_coordinates(
    current_object_coordinates: List[Tuple[int, float, float]],
    latest_object_coordinates: List[Tuple[int, float, float]],
    offset: float = 1.0,
) -> List[Tuple[int, float, float]]:
    """
    Updates and returns a list of unique coordinates by:
    - Replacing existing coordinates within a given offset.
    - Adding new ones if no similar coordinate exists.

    Ensures the final list has no coordinates within 'offset' distance of each other.
    """

    # Convert current set to list for ordered processing and editing
    updated_coordinates: List[Tuple[int, float, float]] = list(
        current_object_coordinates
    )

    for new_coord in latest_object_coordinates:
        _, new_X, new_Y = new_coord
        found = False

        # Check if there's a coordinate already close to the new one
        for idx, (shape, existing_X, existing_Y) in enumerate(updated_coordinates):
            if abs(existing_X - new_X) <= offset and abs(existing_Y - new_Y) <= offset:
                # Replace the existing coordinate
                updated_coordinates[idx] = new_coord
                found = True
                break

        if not found:
            updated_coordinates.append(new_coord)

    # Remove duplicates that are within the offset — ensure uniqueness
    final_coordinates: List[Tuple[float, float]] = []
    for coord in updated_coordinates:
        is_unique = True
        for unique_coord in final_coordinates:
            if (
                abs(coord[1] - unique_coord[1]) <= offset
                and abs(coord[2] - unique_coord[2]) <= offset
            ):
                is_unique = False
                break
        if is_unique:
            final_coordinates.append(coord)

    return final_coordinates


def process_coordinates_with_offset(
    coordinates: List[Tuple[int, float, float]],
) -> List[Tuple[int, float, float]]:
    """
    Adjusts coordinates by applying an offset and converts them from centimeters to millimeters.

    Offset applied:
        - Subtract 1 from X
        - Subtract 0.5 from Y

    Conversion:
        - Multiply both X and Y by 10 to convert from cm to mm

    Parameters:
        coordinates: List of (x, y) tuples in centimeters

    Returns:
        A new list of (x, y) tuples in millimeters after offset and conversion
    """

    # Create a list to store the new converted coordinates
    converted_coordinates = []

    # Go through each (x, y) in the list
    for shape, objX, objY in coordinates:
        # Step 1: Apply the offset
        objX -= 0.8  # Shift X by -0.8 cm
        objY -= 0.9  # Shift Y by -0.9 cm

        # Step 2: Convert to millimeters (1 cm = 10 mm)
        objX = float(f"{(objX):.1f}") * 10
        objY = float(f"{(objY):.1f}") * 10

        # Add the new coordinate to the result list
        converted_coordinates.append((shape, objX, objY))

    # Return the final list
    return converted_coordinates


def extract_shape_and_color(text: str) -> Tuple[str, str]:
    """
    Extracts the shape and color index from a formatted string like 'shape:  6, color: 6'.

    Parameters:
        text (str): The input string containing shape and color.

    Returns:
        Tuple[int, int]: A tuple containing (shape_index, color_index)
    """

    shapes = ["Rectangle", "Triangle", "Hexagonal", "Star", "Circle", "All"]
    colors = ["Red", "Blue", "Green", "White", "Black", "All"]

    try:
        # Split the string by comma into two parts
        parts = text.split(",")

        # Extract shape index
        shape_index = int(parts[0].split(":")[1].strip())

        # Extract color index
        color_index = int(parts[1].split(":")[1].strip())

        return shapes[shape_index - 1], colors[color_index - 1]
    except (IndexError, ValueError):
        raise ValueError("Input string format is incorrect.")


def is_color_match(image, center, target_color):
    """
    Check if the region around the center pixel matches the specified color.

    Args:
        image (np.ndarray): Input BGR image (from cv2.imread).
        center (tuple): (x, y) pixel coordinate to check.
        target_color (str): One of ["Red", "Blue", "Green", "White", "Black", "All"].

    Returns:
        bool: True if the target color is detected near the center, otherwise False.
    """
    # Normalize color name
    target_color = target_color.strip().capitalize()

    # Validate color
    valid_colors = ["Red", "Blue", "Green", "White", "Black", "All"]
    if target_color not in valid_colors:
        raise ValueError(
            f"Unsupported color '{target_color}'. Must be one of {valid_colors}"
        )

    # Shortcut for "All"
    if target_color == "All":
        return True

    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV color ranges
    color_ranges = {
        "Red": [
            (np.array([0, 100, 100]), np.array([10, 255, 255])),
            (np.array([160, 100, 100]), np.array([179, 255, 255])),
        ],
        "Green": [(np.array([40, 50, 50]), np.array([80, 255, 255]))],
        "Blue": [(np.array([100, 100, 100]), np.array([130, 255, 255]))],
        "White": [(np.array([0, 0, 180]), np.array([180, 40, 255]))],
        "Black": [(np.array([0, 0, 0]), np.array([180, 255, 60]))],
    }

    # Patch around the center
    x, y = center
    h, w = hsv.shape[:2]
    x1, x2 = max(0, x - 5), min(w, x + 6)
    y1, y2 = max(0, y - 5), min(h, y + 6)
    patch = hsv[y1:y2, x1:x2]

    # Create mask for selected color
    mask = np.zeros(patch.shape[:2], dtype=np.uint8)
    for lower, upper in color_ranges[target_color]:
        mask |= cv2.inRange(patch, lower, upper)

    # Check match ratio
    ratio = cv2.countNonZero(mask) / mask.size
    return ratio > 0.3


# Checks if contour is within workspace
def is_contour_within_workspace_boundary(cnt, workobj_polygon):
    inside = True

    for point in cnt:
        x, y = point.ravel()  # Flattens [[x, y]] to (x, y)
        dist = cv2.pointPolygonTest(workobj_polygon, (float(x), float(y)), False)
        if dist < 0:  # Point is outside the polygon
            inside = False
            break

    return inside
