import keyboard, socket
import time
import threading

class Joyride():
    
    speed = 0

    def __init__(self) -> None:

        addr = socket.getaddrinfo("192.168.8.141", 1236)[0][-1]
        ServerSideSocket = socket.socket()
        ServerSideSocket.bind(addr)
        ServerSideSocket.listen(5)
        self.conn, address = ServerSideSocket.accept()

        self.pc2pico = threading.Thread(target=self.socket_send)
        self.pc2pico.start()

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
        self.pc2pico.join()

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

    def socket_send(self):
        while True:
            data = self.conn.recv(1024).decode()
            self.conn.sendall(f"{0},{1000},{1}".encode())  # send data to the client
            time.sleep(0.2)

if __name__ == "__main__":
    Joyride()