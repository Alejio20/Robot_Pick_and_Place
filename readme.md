# Pick and Place Project

## Project Goal

This project aims to implement a machine vision system that enables an ABB robot to autonomously identify, pick, and place selected objects using a camera. The robot is guided by visual input to locate the target object and move it to a designated location, demonstrating the integration of computer vision and robotic control.

![Demo of Project](./demo.gif)

### What Was Implemented

- **Object Detection:** A camera is used to capture images of the workspace. The system processes these images to detect and identify objects using custom detection algorithms.
- **Camera Calibration:** Calibration routines ensure accurate mapping between camera coordinates and robot workspace coordinates.
- **Robot Communication:** The project includes modules for communicating with the ABB robot, sending commands to move, pick, and place objects based on vision input.
- **Selection and Placement Logic:** The user can select an object, and the system computes the optimal path for the robot to pick and place the object in the appropriate location.
- **Helper Functions:** Utility scripts support image processing, coordinate transformation, and communication protocols.

### Files Overview

- `camera.py`: Handles camera operations and calibration.
- `detect_object.py` / `MyObjectDetector.py`: Implements object detection logic.
- `main.py`: Main entry point for running the pick and place workflow.
- `helper.py`: Contains supporting functions for image and data processing.
- `Comm.mod`, `ServerCommuncation.sys`: Modules for robot communication.
- `Final Project 2025.pdf`: Contains detailed project requirements and background.

### How It Works

1. The camera captures the workspace and detects objects.
2. The user selects an object to pick.
3. The system calculates the object's position and sends commands to the ABB robot.
4. The robot moves to the object, picks it up, and places it in the designated location.

### References

See `Final Project 2025.pdf` for full project details and requirements.
