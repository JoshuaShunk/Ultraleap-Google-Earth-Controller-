# Google Earth Controller using Leap Motion

## Introduction

After the discontinuation of the official Google Earth UltraLeap controller, there was a need for a new solution to navigate Google Earth using hand gestures. This project aims to fill that void by providing a Python-based controller that leverages the capabilities of the Leap Motion sensor to interact with Google Earth Pro Desktop.

## Project Structure

- **LeapAPITest.py**: The main Python script that interfaces with the Leap Motion API to capture hand gestures and translate them into movements within Google Earth.
- **runscript.bat**: A batch script to conveniently run the main Python script.
- **Leap.py**: Contains the necessary functions and classes for the Leap Motion API.
- **Leap.dll**: Dynamic Link Library for the Leap Motion SDK. It contains compiled code that the main script relies upon.
- **Leap.lib**: A static library file associated with the Leap Motion SDK.
- **Leap.pyc**: Compiled Python file for the Leap Motion functions and classes.
- **LeapPython.pyd**: A Python extension module for the Leap Motion SDK, allowing the main script to interface with the Leap Motion hardware.

## Requirements

- Python 2.7
- [Google Earth Pro Desktop](https://www.google.com/earth/download/gep/agree.html)
- Leap Motion sensor and its SDK

## Setup and Usage

1. Ensure you have Python 2.7 installed and added to your system's PATH.
2. Install Google Earth Pro Desktop.
3. Connect your Leap Motion sensor to your computer.
4. Navigate to the project directory in your terminal or command prompt.
5. Run the `runscript.bat` file:

```
runscript.bat
```

6. Once the script is running, open Google Earth Pro Desktop. You should now be able to navigate within Google Earth using various hand gestures detected by the Leap Motion sensor.

## Hand Gestures

- **Move Left/Right**: Rotate your hand left or right.
- **Move Forward/Backward**: Tilt your hand forward (for moving forward) or backward (for moving backward).
- **Zoom In/Out**: Move your hand closer to the sensor to zoom in and farther away to zoom out.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
