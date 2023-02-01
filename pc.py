import arena
import path_finder
import threading
import time
import socket
#import pico
import paho.mqtt.client as mqtt
import sys
import os
import numpy as np

class Final():

    def __init__(self) -> None:
        self.client_name = "XORVEOTESI"
        self.is_path_ready = True
        self.mock_data_stats = [{'ID':9, 'POS':[[500,170],[500, 230],[600,230],[600,170]]}, {'ID':12, 'POS':[[300,160],[340, 160],[340,200],[300,200]]}]
        self.mock_data_config = {"PREDATOR":[-10, 10, "H", "S", [8, 9, 10, 11]], "PREY":[10, -10, "M", "H", [12, 13, 14, 15]], "TIMEOUT":15 }
        self.id = 8
        self.arena_dim = [600,450]
        self.roles = ['PREDATOR', 'PREY']
        self.cell_width = self.arena_dim[0]/8
        self.cell_height = self.arena_dim[1]/6
        self.flag = False
        self.points = 0
        self.speed = 'M'
        self.map = np.zeros((6,8), dtype=int)
        self.green_locations = []
        #self.pico = pico.Pico()
        self.pc2main = threading.Thread(target=self.mqqt_send)
        self.main2pc = threading.Thread(target=self.mqqt_recieve)
        self.pc2pico = threading.Thread(target=self.socket_send)
        self.pc2main.start()
        self.main2pc.start()
        self.pc2pico.start()
        self.pc2main.join()
        self.main2pc.join()
        self.pc2pico.join()

    def socket_send(self):
        
        addr = socket.getaddrinfo("192.168.8.141", 1236)[0][-1]
        ServerSideSocket = socket.socket()
        ServerSideSocket.bind(addr)
        ServerSideSocket.listen(5)
        conn, address = ServerSideSocket.accept()

        while True:
            if self.flag:
                data = conn.recv(1024).decode()
                conn.sendall(f"{0},{1000},{self.role}".encode())  # send data to the client
                time.sleep(0.2)
                break

    def mqqt_send(self):
        while True:
            if self.flag:
            #if "/robotsay":
                self.green_left = self.green_timeout - (time.time() - self.green_last)
                if self.green_left < 0:
                    self.green_left = 0

                list_send = f"[{self.id}, {self.role}, {self.speed}, {self.points}, (3,2), (3,3), {self.green_left}]"
                #print(list_send)
                #b = eval(f"[{self.id}, {self.role}, {self.speed}, {self.points}, (3,2), (3,3), {time.time() - self.green_last}]")
            break

    def on_log(self,client, userdata, level, buf):
        print("log: ",buf)
        
    def on_message(self,client, userdata, message, details = False):
        #print(f'{message.topic}:{message.payload.decode("utf-8")}')
        print("incoming")
        if message.topic =='arena':
            f = open("out.png", "wb")
            f.write(message.payload)
            print(message.topic)
            print("pict obtained")
            f.close()
        else:
            print(message.topic)
            print(message.payload)

    def waitwait(self):
        while True:
            try:
                time.sleep(4)
            except KeyboardInterrupt:
                print('\n no more listening \n bye')
                self.client.disconnect()
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

    def mqqt_recieve(self):
        broker_add = '144.122.143.29' # broker ip 
        stats_topic = 'stats' # topic to update aruco coords
        image_topic = 'arena' # topic to send arena image ONCE
        time_topic = 'tick' # topic to update remaining time in seconds
        game_status_topic = 'start' # topic to send game status
        config_topic = 'config' # topic to send game configuration parameters
        self.client = mqtt.Client(f"{self.client_name}") #create new instance
        self.client.on_log=self.on_log
        self.client.on_message=self.on_message        #attach function to callback
        
        while True:
            if "/arena":
                self.arena = arena.ArenaFinder()
                self.grid = self.arena()
                for color, cells in self.grid.items():
                    if color == "blue":
                        cell_value = 1
                    elif color == "yellow":
                        cell_value = 2
                    elif color == "red":
                        cell_value = -1
                    elif color == "green":
                        self.green_locations.append(cells)
                        cell_value = 3
                    for row, col in cells:
                        self.map[row][col] = cell_value
                print(self.grid)

            if "/config":
                for key in self.mock_data_config:
                    if key == "PREDATOR":
                        self.pred = [pred for pred in self.mock_data_config[key][4]]
                        self.yellow_point_pred = self.mock_data_config[key][0]
                        self.blue_point_pred = self.mock_data_config[key][1]
                        self.yellow_speed_pred = self.mock_data_config[key][2]
                        self.blue_speed_pred = self.mock_data_config[key][3]

                    elif key == "PREY":
                        self.prey = [prey for prey in self.mock_data_config[key][4]]
                        self.yellow_point_prey = self.mock_data_config[key][0]
                        self.blue_point_prey = self.mock_data_config[key][1]
                        self.yellow_speed_prey = self.mock_data_config[key][2]
                        self.blue_speed_prey = self.mock_data_config[key][3]

                    elif key == "TIMEOUT":
                        self.green_timeout = self.mock_data_config[key]
                        self.green_last = time.time()

                if self.id in self.pred:
                    self.ally = self.pred
                    self.enemy = self.prey
                    self.current_role = 0 # PREDATOR
                    self.role = self.roles[self.current_role]

                if self.id in self.prey:
                    self.ally = self.prey
                    self.enemy = self.pred
                    self.current_role = 1 # PREY
                    self.role = self.roles[self.current_role]

                #print(self.role)
                #print(self.enemy, self.ally)

            if "/tick":
                self.remaining_time = 90

            if "start":
                if "GO":
                    pass

                if "PAUSE":
                    pass

                if "STOP":
                    pass

            if "/stats":
                self.enemy_pos = []
                self.ally_pos = []
                for data in self.mock_data_stats:
                    cx = int((data["POS"][0][0] + data["POS"][2][0]) / 2)
                    cy = int((data["POS"][0][1] + data["POS"][2][1]) / 2)
                    pos = [[int(cy/self.cell_height),int(cx/self.cell_width)]]

                    if pos in self.grid["green"]:
                        temp = self.pred
                        self.pred = self.prey
                        self.prey = temp
                        self.current_role = not self.current_role
                        self.role = self.roles[self.current_role]

                    if data["ID"] == self.id:
                        if pos in self.grid["yellow"]:
                            if self.role == "PREDATOR":
                                self.speed = self.yellow_speed_pred
                                self.points += self.yellow_point_pred

                            elif self.role == "PREY":
                                self.speed = self.yellow_speed_prey
                                self.points += self.yellow_point_prey

                        if pos in self.grid["blue"]:
                            if self.role == "PREDATOR":
                                self.speed = self.blue_speed_pred
                                self.points += self.blue_point_pred

                            elif self.role == "PREY":
                                self.speed = self.blue_speed_prey
                                self.points += self.blue_point_prey

                    if data["ID"] in self.ally:
                        self.ally_pos.append([pos,data["ID"]])

                    if data["ID"] in self.enemy:
                        self.enemy_pos.append([pos,data["ID"]])


                #print(self.ally_pos)
                #print(self.enemy_pos)
                #print(self.role)
            self.flag = True
            #time.sleep(1)
            break

if __name__ == "__main__":
    final = Final()
    path_finder(final.map, final.ally_pos, final.enemy_pos, final.role)