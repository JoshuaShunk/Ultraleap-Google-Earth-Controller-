import Leap
import mouse
import time 
import math
import keyboard
import pyautogui
from Leap import Gesture 

# BaseBehavior Class:
# This is a parent class that provides a blueprint for other behavior classes.
# All specific behavior classes should inherit from this class and override its methods as needed.
class BaseBehavior(object):
    
    # Class variables for screen dimensions
    screen_width = 1920  # Default screen width value
    screen_height = 1080 # Default screen height value
    start_time = time.time()
    exitingStreetView = False
    switchingPlanet = False
    currentPlanet = "Earth"
    planetSwitchTime = time.time()
    autoSwitchTime = time.time()

    def __init__(self, name):
        """Constructor for the BaseBehavior class.
        
        Args:
        - name (str): Name of the behavior.
        """
        self.name = name

    def execute(self, frame):
        """Method to execute the behavior. 
        This method should be overridden in derived classes to implement specific behavior.
        
        Args:
        - frame: The frame data from the UltraLeap device.
        
        Raises:
        - NotImplementedError: If the method is not overridden in the derived class.
        """
        raise NotImplementedError("This method should be overridden in derived classes.")
    
    # Common movement functions 

    def navigate_to(self, destination):
        """Navigate to a specific destination in Google Earth.
        
        This function simulates keypresses and mouse interactions to navigate to 
        a specified destination in Google Earth.
        
        Args:
        - destination (str): The name or address of the destination in Google Earth.
        
        Note: This function currently has hardcoded behavior to navigate to the 
        Arizona Science Center, this should be updated if other destinations are intended.
        """
        # Simulate Ctrl + F to focus on the search bar
        pyautogui.hotkey('/')
        time.sleep(0.5)  # Wait for a short duration to ensure the search bar is focused
        
        # Type the destination
        pyautogui.write(destination)
        time.sleep(0.5)  # Wait again before pressing Enter
        
        # Simulate Enter key to initiate the search
        pyautogui.press('enter')
        
        # Right-click after searching (Exit out of search to allow for keyboard controls)
        pyautogui.rightClick()

    def sigmoid(self, x):
        """Computes the sigmoid of the input value.
        
        The sigmoid function maps any input value to an output value between 0 and 1.
        
        Args:
        - x (float): Input value.
        
        Returns:
        - float: The sigmoid of the input value.
        """
        return 1 / (1 + math.exp(-x))

    def movement_speed(self, value):
        """Calculate movement speed based on input value.
        
        Args:
        - value (float): Input value.
        
        Returns:
        - float: The calculated movement speed.
        """
        return float(value) / 90.0

    def exponential_zoom(self, distance, zoom_in_threshold=120, zoom_out_threshold=140, scale_factor=15, power=4):
        """Calculate an exponential zoom factor based on the distance from a sensor using a sigmoid curve.
        
        Args:
        - distance (float): Current distance to the sensor.
        - zoom_in_threshold (float, optional): Maximum distance for zooming in. Default is 160.
        - zoom_out_threshold (float, optional): Minimum distance for starting to zoom out. Default is 300.
        - scale_factor (float, optional): Determines the sharpness of the sigmoid curve. Higher values give a sharper curve. Default is 10.
        - power (float, optional): Power to which the normalized distance is raised to slow down zoom near thresholds. Default is 3.
        
        Returns:
        - float: A zoom factor. Positive values indicate zooming in, while negative values indicate zooming out.
        """
        
         # For zooming in
        if distance <= zoom_in_threshold:
            normalized_distance = (float(distance) / zoom_in_threshold) ** power
            return (1 - self.sigmoid(scale_factor * (normalized_distance - 0.5))) * 1.5
        
        # For zooming out
        elif distance > zoom_out_threshold:
            normalized_distance = ((distance - zoom_out_threshold) / (zoom_in_threshold - zoom_out_threshold)) ** power
            #print(" " + str(self.exitingStreetView) + " + " + str(self.inStreetView()))
            if(self.inStreetView() and self.exitingStreetView == False): 
                self.exitStreetView()


            return (-self.sigmoid(scale_factor * (normalized_distance - 0.5))) * 1.5
        
        # No zooming for distances between the two thresholds
        return 0

    def inStreetView(self):
        """Check if Google Earth is in "Street View" mode based on the pixel color of the "Exit Street View" button.

        Returns:
        - bool: True if in Street View, False otherwise.
        """
        
        # Coordinates of the pixel to check (this needs to be adjusted to where the "Exit Street View" button is)
        x, y = 1893, 37  # Assuming top-right corner, but this might need fine-tuning

        # Capture the pixel color at the specified location
        pixel_color = pyautogui.screenshot().getpixel((x, y))
        #print(pixel_color)
        # Define the expected color of the "Exit Street View" button (assuming white, but this might need adjustment)
        # The values might need fine-tuning based on the exact color in your Google Earth version
        expected_color = (248, 248, 248) 

        # Compare the captured pixel color to the expected color
        return pixel_color == expected_color
    
    def exitStreetView(self):
        start_time = time.time()
        exitingStreetView = True
        pyautogui.press('esc')
    
    def _move_to_planets(self, offset=0):
        pyautogui.moveTo(85, 11)
        pyautogui.click()
        pyautogui.moveTo(207, 340 - offset)
        pyautogui.click()
        pyautogui.moveTo(400, 340 - offset)

    def _move_to_moon(self, offset=0):
        self._move_to_planets(offset)
        pyautogui.moveTo(411, 410 - offset)
        pyautogui.click()
        pyautogui.moveTo(self.screen_width / 2.0, self.screen_height / 2.0)

    def _move_to_mars(self, offset=0):
        self._move_to_planets(offset)
        pyautogui.moveTo(415, 387 - offset)
        pyautogui.click()
        pyautogui.moveTo(self.screen_width / 2.0, self.screen_height / 2.0)

    def _move_to_earth(self, offset=0):
        self._move_to_planets(offset)
        pyautogui.click()
        pyautogui.moveTo(self.screen_width / 2.0, self.screen_height / 2.0)

    def _switch_to_target_planet(self, target_planet):
        """Private method to switch to a given target planet with the required offset."""
        offset = 0 if self.currentPlanet == "Earth" else 20

        planet_actions = {
            "Moon": self._move_to_moon,
            "Mars": self._move_to_mars,
            "Earth": self._move_to_earth
        }

        if target_planet in planet_actions and self.currentPlanet != target_planet:
            planet_actions[target_planet](offset)
            self.currentPlanet = target_planet

    def switch_planets(self, target_planet):
        if round(time.time() - self.planetSwitchTime) > 7 and self.switchingPlanet:
            self.switchingPlanet = False

        if not self.switchingPlanet:
            self.switchingPlanet = True
            self.planetSwitchTime = time.time()
            self._switch_to_target_planet(target_planet)

    def rotate_planets(self):
        next_planet = {
            "Earth": "Mars",
            "Mars": "Moon",
            "Moon": "Earth"
        }

        target_planet = next_planet.get(self.currentPlanet, "Earth")  # Default to Earth if something goes wrong
        self._switch_to_target_planet(target_planet)
    
    def relase_keys(self):
        pyautogui.keyUp('up')
        pyautogui.keyUp('down')
        pyautogui.keyUp('left')
        pyautogui.keyUp('right')






# HandTiltBehavior Class:
# This class defines the behavior when a hand is tilted.
# It inherits from the BaseBehavior class and provides specific implementations for hand tilting behavior.
class HandTiltBehavior(BaseBehavior):

    def __init__(self):
        """Constructor for the HandTiltBehavior class.
        Initializes the name of the behavior to "handTilt".
        """
        super(HandTiltBehavior, self).__init__("handTilt")

    def execute(self, frame):
        """Execute the hand tilting behavior based on the frame data from the UltraLeap device.
        
        Args:
        - frame: The frame data from the UltraLeap device.
        
        Note: The exact behavior executed is determined by the logic inside this method.
        """
        X_DISTANCE = 10  # Threshold for hand motion (adjust as needed)
        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        auto_navigate = False
        # Constants for hand position-based motion
        X_CENTER = 0  # The X position when the hand is directly over the sensor
        Z_CENTER = 0  # The Z position when the hand is directly over the sensor
        DEAD_ZONE_RADIUS = 75  # Radius around the center where no motion is triggered

        # Get current mouse position
        x, y = mouse.get_position()

        # If no hands are detected and auto navigation is not active, navigate to the Arizona Science Center
        if len(frame.hands) == 0 and not auto_navigate:
            auto_navigate = True
            self.navigate_to_arizona_science_center()

        # If hands are detected, turn off auto navigation
        elif len(frame.hands) != 0: 
            auto_navigate = False

            # If mouse position is near the edges of the screen, reset it to the center
            if (x < X_DISTANCE or x > self.screen_width - X_DISTANCE or 
                y < X_DISTANCE or y > self.screen_height - X_DISTANCE):
                mouse.move(center_x, center_y)

            # Iterate through each hand detected in the frame
            for hand in frame.hands:
                handType = "Left Hand" if hand.is_left else "Right Hand"
                normal = hand.palm_normal
                direction = hand.direction
            
                # Convert hand orientation (pitch, roll, yaw) from radians to degrees
                pitch = direction.pitch * Leap.RAD_TO_DEG
                roll = normal.roll * Leap.RAD_TO_DEG
                yaw = direction.yaw * Leap.RAD_TO_DEG

                # Adjust the mouse wheel based on the palm's vertical position to control zoom
                mouse.wheel(delta=self.exponential_zoom(hand.palm_position[1]))

                # Control movement based on hand orientation
                self.control_movement(pitch, roll, yaw)

    # Supporting Function(s)
 
    def control_movement(self, pitch, roll, yaw):
        """Control movement based on hand orientation.
        
        Args:
        - pitch (float): Pitch of the hand in degrees.
        - roll (float): Roll of the hand in degrees.
        - yaw (float): Yaw of the hand in degrees.
        """
        
        # Calculate movement speeds based on hand orientation
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

# HandSlideBehavior Class:
# This class defines the behavior when a hand slides.
# It inherits from the BaseBehavior class and provides specific implementations for hand sliding behavior.
class HandSlideBehavior(BaseBehavior):

    def __init__(self):
        """Constructor for the HandSlideBehavior class.
        Initializes the name of the behavior to "handSlide" and other related properties.
        """
        self.auto_navigate = False
        self.timeout = 30
        self.last_hand_detected_time = None
        self.alt = False
        BaseBehavior.currentPlanet = "Earth"
        super(HandSlideBehavior, self).__init__("handSlide")

        

    def execute(self, frame):
        """Execute the hand sliding behavior based on the frame data from the UltraLeap device.
        
        Args:
        - frame: The frame data from the UltraLeap device.
        
        Note: The exact behavior executed is determined by the logic inside this method.
        """
  
        if(round(time.time() - BaseBehavior.start_time) > 30 and BaseBehavior.exitingStreetView == True):
            #print("Exited Street View")
            BaseBehavior.exitingStreetView = False


        if(BaseBehavior.exitingStreetView != True and BaseBehavior.switchingPlanet != True):

            if(keyboard.is_pressed('m')):
                self.switch_planets("Mars")
            if(keyboard.is_pressed('l')):
                self.switch_planets("Moon")
            if(keyboard.is_pressed('e')):
                self.switch_planets("Earth")


            if frame.hands:
                self.last_hand_detected_time = time.time()    
                self.auto_navigate = False

                hand = frame.hands[0]

                hand_x = hand.palm_position[0]  # Left and right
                hand_z = hand.palm_position[2]  # Forward and backward

                # Constants for hand position-based motion
                dead_zone = 20  # A zone in the center where there's no movement
                outer_limits = 200

                # Check the dead zone for hand_x (left and right movement)

                # Check for slide
                
                if all(-outer_limits < coord < outer_limits for coord in [hand_x, hand_z]):

                    if self.alt:
                        # Using the exponential_zoom function for zooming
                        zoomStrength = self.exponential_zoom(hand.palm_position[1])
                        mouse.wheel(delta=zoomStrength)
                        self.alt = False 

                    else:
                        if -outer_limits < hand_x < -dead_zone:
                            keyboard.release('right')  # Ensure right arrow key is not pressed
                            keyboard.press('left')     # Press left arrow key for left movement
                        elif dead_zone < hand_x < outer_limits:
                            keyboard.release('left')   # Ensure left arrow key is not pressed
                            keyboard.press('right')    # Press right arrow key for right movement
                        else:
                            keyboard.release('left')
                            keyboard.release('right')

                        if -outer_limits < hand_z < -dead_zone:
                            keyboard.release('down')  # Ensure down is not pressed
                            keyboard.press('up')      # Keep up pressed
                        elif dead_zone < hand_z < outer_limits:
                            keyboard.release('up')  # Ensure up is not pressed
                            keyboard.press('down')  # Keep down pressed
                        else:
                            # In the dead zone: release any keys and do not trigger any movement
                            keyboard.release('up')
                            keyboard.release('down')
                        self.alt = True
                else:
                    self.relase_keys()
            # If no hands are detected and auto navigation is not active, and 30 seconds have passed since the last hand was detected
            
            
            elif self.auto_navigate == False and self.last_hand_detected_time and round(time.time() - self.last_hand_detected_time) == 30 and BaseBehavior.currentPlanet == "Earth":
                self.navigate_to("Arizona Science Center")
                self.auto_navigate = True
     
            elif(self.last_hand_detected_time and int(round(time.time() - self.last_hand_detected_time)) != 0 and int(round(time.time() - self.last_hand_detected_time)) % 120 == 0):
                self.rotate_planets()

            if not frame.hands:
                self.relase_keys()
                return

        # If none of the above conditions are met, release all movement keys
        else:
            self.relase_keys()
            return
