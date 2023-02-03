import keyboard, socket
import time
import threading

class Joyride():
    
    speed = 0

    def __init__(self) -> None:


        # Register the function to handle arrow key events
        keyboard.on_press_key("up", self.handle_arrow_keys, suppress=True)
        keyboard.on_press_key("down", self.handle_arrow_keys, suppress=True)
        keyboard.on_press_key("left", self.handle_arrow_keys, suppress=True)
        keyboard.on_press_key("right", self.handle_arrow_keys, suppress=True)
        keyboard.on_press_key("q", self.handle_speed, suppress=True)
        keyboard.on_press_key("w", self.handle_speed, suppress=True)
        keyboard.on_press_key("e", self.handle_speed, suppress=True)

        # Start listening for key events
        keyboard.wait("ESC")        

    # Function to handle arrow key events
    def handle_arrow_keys(self,e):
        if e.name == 'up':
            print("Up arrow key pressed")
        elif e.name == 'down':
            print("Down arrow key pressed")
        elif e.name == 'left':
            print("Left arrow key pressed")
        elif e.name == 'right':
            print("Right arrow key pressed")

    def handle_speed(self,e):
        global speed
        if e.name == 'q':
            print("Speed: Low")
            speed = 0
        elif e.name == 'w':
            print("Speed: Medium")
            speed = 0            
        elif e.name == 'e':
            print("Speed: Low")
            speed = 0


if __name__ == "__main__":
    Joyride()