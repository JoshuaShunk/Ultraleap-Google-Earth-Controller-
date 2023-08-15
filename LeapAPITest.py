
'''
Leap Motion Controller for Google Earth Navigation
This script allows the user to navigate Google Earth using hand gestures detected by the Leap Motion sensor.

Configuration:
- Tilt hand forward/backward: Move forward/backward in Google Earth
- Tilt hand left/right: Mwove left/right in Google Earth
- Move hand closer/farther from the sensor: Zoom in/out in Google Earth
'''
from Controllers.ControllerConfig import ConfigurationManager, ControllerConfig
from Controllers.behaviors import *
import Leap
import sys
import mouse
import time 
import math
import keyboard
import win32gui
import pyautogui


#import pyautogui

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture





class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky' ]
    
    
    current_time = time.time()
    
    # Configuration and Constants
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print("Initialized")

        # 1. Instantiate Behavior Objects
        hand_tilt = HandTiltBehavior()

        # 2. Add Behavior Objects to ConfigurationManager
        config_manager = ConfigurationManager()
        config_manager.add_config(hand_tilt)

        # 3. Select a Behavior
        config_manager.select_config("HandTilt")

    def on_connect(self, controller):
        print ("Motion Sensor Connected!")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        
        
        

    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")

    def on_exit(self, controller):
        print("Exited")
    
    def on_frame(self, controller):

        frame = controller.frame()

        if(is_google_earth_active()):

            # Execute the behavior using the frame data
            ConfigurationManager.get_selected_behavior().execute(frame)


def is_google_earth_active():
    """Check if the active window is Google Earth."""
    window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return "Google Earth Pro" in window_title

def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print("Press enter to quit")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()





