
'''
Leap Motion Controller for Google Earth Navigation
This script allows the user to navigate Google Earth using hand gestures detected by the Leap Motion sensor.

Configuration:
- Tilt hand forward/backward: Move forward/backward in Google Earth
- Tilt hand left/right: Mwove left/right in Google Earth
- Move hand closer/farther from the sensor: Zoom in/out in Google Earth
'''
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
    screen_width = 1920
    screen_height = 1080
    X_DISTANCE = 10  # Adjust as needed
    center_x, center_y = screen_width / 2, screen_height / 2
    auto_navigate = False
    # Hand position-based motion thresholds
    X_CENTER = 0  # The X position when the hand is directly over the sensor
    Z_CENTER = 0  # The Z position when the hand is directly over the sensor
    DEAD_ZONE_RADIUS = 75  # Radius around the center where no motion is triggered


    # Define the minimum distance from the border
      # Adjust as needed

    # Get the center of the screen
    

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print ("Motion Sensor Connected!")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        
        
        

    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")

    def on_exit(self, controller):
        print("Exited")
    
    def on_frame(self, controller):

        frame = controller.frame()

        

        x, y = mouse.get_position()
        if(is_google_earth_active()):

            if(len(frame.hands) == 0 and self.auto_navigate == False):
                self.auto_navigate = True
                navigate_to_arizona_science_center()
            elif(len(frame.hands) != 0): 
                self.auto_navigate = False
                if(x < self.X_DISTANCE 
                or x > self.screen_width - self.X_DISTANCE or 
                y < self.X_DISTANCE or 
                y > self.screen_height - self.X_DISTANCE):
                    mouse.move(self.center_x, self. center_y)

                for hand in frame.hands:
                    handType = "Left Hand" if hand.is_left else "Right Hand"
                    
                    normal = hand.palm_normal
                    direction = hand.direction
                
                    sys.stdout.write("\r" + "X Position: " + str(hand.palm_position[0]) + " Y Position: " + str(hand.palm_position[2]))
                    sys.stdout.flush()
                    #sys.stdout.write("\n" + "Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) + " Yaw: " + str(direction.yaw * Leap.RAD_TO_DEG))
                    pitch = direction.pitch * Leap.RAD_TO_DEG
                    roll = normal.roll * Leap.RAD_TO_DEG
                    yaw = direction.yaw * Leap.RAD_TO_DEG
                    mouse.wheel(delta=exponential_zoom(hand.palm_position[1] ))
                    control_movement(pitch, roll, yaw)



def sigmoid(x):
    """Returns a value between 0 and 1 using the logistic function"""
    return 1 / (1 + math.exp(-x))

def exponential_zoom(distance, zoom_in_threshold=160, zoom_out_threshold=250, scale_factor=15, power=4):
    """
    Calculate an exponential zoom factor based on the distance from a sensor using a sigmoid curve.

    Parameters:
    - distance: Current distance to the sensor.
    - zoom_in_threshold: Maximum distance for zooming in. (default: 160)
    - zoom_out_threshold: Minimum distance for starting to zoom out. (default: 300)
    - scale_factor: Determines the sharpness of the sigmoid curve. Higher values give a sharper curve. (default: 10)
    - power: Power to which the normalized distance is raised to slow down zoom near thresholds (default: 3)

    Returns:
    - A zoom factor. Positive values for zooming in, negative values for zooming out.
    """
    
    # For zooming in
    if distance <= zoom_in_threshold:
        normalized_distance = (float(distance) / zoom_in_threshold) ** power
        return (1 - sigmoid(scale_factor * (normalized_distance - 0.5))) * 2
    
    # For zooming out
    elif distance > zoom_out_threshold:
        normalized_distance = ((distance - zoom_out_threshold) / (zoom_in_threshold - zoom_out_threshold)) ** power
        return (-sigmoid(scale_factor * (normalized_distance - 0.5))) * 2
    
    # No zooming for distances between the two thresholds
    return 0

def movement_speed(value):
    return float(value) / 90.0

def control_movement(pitch, roll, yaw):
    forward_backward_speed = movement_speed(pitch)
    left_right_speed = movement_speed(roll)
    turn_speed = movement_speed(yaw)
    threshold = 0.1

    # Forward and Backward movement based on pitch (using arrow keys)
    if forward_backward_speed < -threshold:  # Negative pitch indicates forward movement
        keyboard.press('up')
        time.sleep(-forward_backward_speed)
        keyboard.release('up')
    elif forward_backward_speed > threshold:  # Positive pitch indicates backward movement
        keyboard.press('down')
        time.sleep(forward_backward_speed)
        keyboard.release('down')

    # Left and Right movement based on roll (using arrow keys)
    if left_right_speed > threshold:  # Positive roll indicates left movement
        keyboard.press('left')
        time.sleep(left_right_speed)
        keyboard.release('left')
    elif left_right_speed < -threshold:  # Negative roll indicates right movement
        keyboard.press('right')
        time.sleep(-left_right_speed)
        keyboard.release('right')
    
    # Turning left and right based on yaw (using mouse movement)
    if turn_speed < -threshold:  # Negative yaw indicates turning left
        mouse.press(button='middle')
        mouse.move(-100 * turn_speed, 0)
        mouse.release(button='middle')
    elif turn_speed > threshold:  # Positive yaw indicates turning right
        mouse.press(button='middle')
        mouse.move(100 * turn_speed, 0)
        mouse.release(button='middle')

def is_google_earth_active():
    """Check if the active window is Google Earth."""
    window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return "Google Earth Pro" in window_title

def navigate_to_arizona_science_center():
    """Navigate to the Arizona Science Center in Google Earth."""
    # Simulate Ctrl + F to focus on the search bar
    pyautogui.hotkey('/')
    time.sleep(0.5)  # Wait for a short duration to ensure the search bar is focused
    
    # Type the destination
    pyautogui.write('Arizona Science Center')
    time.sleep(0.5)  # Wait again before pressing Enter
    
    # Simulate Enter key to initiate the search
    pyautogui.press('enter')



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





