import Leap
import sys
import mouse
import time 
import math
import keyboard
import win32gui
import pyautogui

class BaseBehavior:
    
    # Class variables for screen dimensions
    screen_width = 1920  # Example value
    screen_height = 1080 # Example value

    def __init__(self, name):
        self.name = name

    def execute(self, frame):
        """Override this method in derived classes to implement specific behavior."""
        raise NotImplementedError("This method should be overridden in derived classes.")
    
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



class HandTiltBehavior(BaseBehavior):
    def __init__(self):
        super(HandTiltBehavior, self).__init__("handTilt")

    def execute(self, frame):

        X_DISTANCE = 10  # Adjust as needed
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        auto_navigate = False
        # Hand position-based motion thresholds
        X_CENTER = 0  # The X position when the hand is directly over the sensor
        Z_CENTER = 0  # The Z position when the hand is directly over the sensor
        DEAD_ZONE_RADIUS = 75  # Radius around the center where no motion is triggered

        x, y = mouse.get_position()
        if(len(frame.hands) == 0 and auto_navigate == False):
            auto_navigate = True
            self.navigate_to_arizona_science_center()
        elif(len(frame.hands) != 0): 
            auto_navigate = False
            if(x < X_DISTANCE 
            or x > self.screen_width - X_DISTANCE or 
            y < X_DISTANCE or 
            y > self.screen_height - X_DISTANCE):
                mouse.move(center_x, center_y)

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
                mouse.wheel(delta=self.exponential_zoom(hand.palm_position[1] ))
                self.control_movement(pitch, roll, yaw)

    # Supporting Functions

    def sigmoid(x):
        """Returns a value between 0 and 1 using the logistic function"""
        return 1 / (1 + math.exp(-x))

    def exponential_zoom(self, distance, zoom_in_threshold=160, zoom_out_threshold=250, scale_factor=15, power=4):
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
            return (1 - self.sigmoid(scale_factor * (normalized_distance - 0.5))) * 2
        
        # For zooming out
        elif distance > zoom_out_threshold:
            normalized_distance = ((distance - zoom_out_threshold) / (zoom_in_threshold - zoom_out_threshold)) ** power
            return (-self.sigmoid(scale_factor * (normalized_distance - 0.5))) * 2
        
        # No zooming for distances between the two thresholds
        return 0

    def movement_speed(value):
        return float(value) / 90.0

    def control_movement(self, pitch, roll, yaw):
        forward_backward_speed = self.movement_speed(pitch)
        left_right_speed = self.movement_speed(roll)
        turn_speed = self.movement_speed(yaw)
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


