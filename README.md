
# Google Earth Controller using Leap Motion

## Introduction

After the discontinuation of the official Google Earth UltraLeap controller, there was a need for a new solution to navigate Google Earth using hand gestures. This project aims to fill that void by providing a Python-based controller that leverages the capabilities of the Leap Motion sensor to interact with Google Earth Pro Desktop.

## Project Structure

- **LeapAPITest.py**: The main Python script that interfaces with the Leap Motion API to capture hand gestures and translate them into movements within Google Earth.
- **Controllers/ControllerConfig.py**: Stores and manages the different controller configurations.
- **Controllers/behaviors.py**: Contains the different behaviors that define how hand gestures are interpreted and used to control Google Earth.
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
6. Once the script is running, open Google Earth Pro Desktop. You should now be able to navigate within Google Earth using the behavior you've selected, as detected by the Leap Motion sensor.
7. Selecting a Behavior: Inside the `on_init` function of the `LeapMotionListener` class in `LeapAPITest.py`, you can select a behavior by first creating an instance of the behavior, adding it to the `ConfigurationManager`, and then selecting it. Here's an example:
```python
def on_init(self, controller):
    # Instantiate the desired behavior object (e.g., HandTiltBehavior)
    hand_tilt = HandTiltBehavior()
    
    # Add the behavior object to the ConfigurationManager
    config_manager = ConfigurationManager()
    config_manager.add_config(hand_tilt)
    
    # Select the desired behavior by its name
    config_manager.select_config("HandTilt")
```
## Hand Gestures

The current behavior is "HandTilt". Here's how to use it:
- **Move Left/Right**: Rotate your hand left or right.
- **Move Forward/Backward**: Tilt your hand forward (for moving forward) or backward (for moving backward).
- **Zoom In/Out**: Move your hand closer to the sensor to zoom in and farther away to zoom out.

In the future, there will be a list of different behaviors and information on how to use each one.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request. 

To add a new behavior:
1. Define a new behavior class in `Controllers/behaviors.py` that inherits from `BaseBehavior`.
2. Implement the behavior logic in the `execute` method of the new class.
3. Add the new behavior to `ControllerConfig.py` and make sure it's available for selection in `LeapAPITest.py`.
