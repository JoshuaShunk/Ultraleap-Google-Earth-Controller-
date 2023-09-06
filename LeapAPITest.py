
'''
Leap Motion Controller for Google Earth Navigation
This script allows the user to navigate Google Earth using hand gestures detected by the Leap Motion sensor.

Configuration:
- Tilt hand forward/backward: Move forward/backward in Google Earth
- Tilt hand left/right: Mwove left/right in Google Earth
- Move hand closer/farther from the sensor: Zoom in/out in Google Earth
'''

import sys



from ControllerConfig import ConfigurationManager
from behaviors import HandSlideBehavior, HandTiltBehavior



import Leap
import time 
import win32gui




#import pyautogui

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky' ]
    
    
    current_time = time.time()
    
    # Configuration and Constants
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    config_manager = ConfigurationManager()

    def on_init(self, controller):
        print("Initialized")

        # 1. Instantiate Behavior Objects

        # 2. Add Behavior Objects to ConfigurationManager
        self.config_manager = ConfigurationManager()
        hand_tilt = HandTiltBehavior()
        hand_slide = HandSlideBehavior()
        self.config_manager.add_config(hand_tilt)
        self.config_manager.add_config(hand_slide)
        self.config_manager.select_config("handSlide")



    def on_connect(self, controller):
        print ("Motion Sensor Connected!")

        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        
        
        

    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")

    def on_exit(self, controller):
        print("Exited")
    
    def on_frame(self, controller):

        frame = controller.frame()

        if(is_google_earth_active()):
            # Execute the behavior using the frame data
            self.config_manager.execute_selected_behavior(frame)


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





