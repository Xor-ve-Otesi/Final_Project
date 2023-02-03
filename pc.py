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
import math
import ast

class Final():

    def __init__(self) -> None:
        self.client_name = "XORVEOTESI"
        self.is_path_ready = True
        self.mock_data_stats = [{'ID':9, 'POS':[[500,170],[500, 230],[600,230],[600,170]]}, {'ID':12, 'POS':[[300,160],[340, 160],[340,200],[300,200]]}]
        self.mock_data_config = {"PREDATOR":[-10, 10, "H", "S", [8, 9, 10, 11]], "PREY":[10, -10, "M", "H", [12, 13, 14, 15]], "TIMEOUT":15 }
        self.id = 9
        self.arena_dim = [640,480]
        self.roles = ['PREDATOR', 'PREY']
        self.cell_width = self.arena_dim[0]/8
        self.cell_height = self.arena_dim[1]/6
        self.flag = False
        self.points = 0
        self.speed = 'M'
        self.green_available = False
        self.map = np.zeros((6,8), dtype=int)
        self.green_locations = []
        #self.pico = pico.Pico()
        self.green_last = time.time()
        self.arena_mock = True
        self.config_mock = True
        self.is_start = False
        self.motor1_speed = 0
        self.motor2_speed = 0
        self.goal_reached = True
        broker_add = '192.168.1.102'

        self.client = mqtt.Client(f"{self.client_name}")
        self.client.on_message=self.on_message

        self.client.connect(broker_add) #connect to broker
        self.client.loop_start() #start the loop
        self.client.subscribe([("arena",0),("tick",0),("config",0), ("stats",0)])

        self.pc2main = threading.Thread(target=self.mqqt_send)
        self.path2pc = threading.Thread(target=self.path_pc)
        #self.main2pc = threading.Thread(target=self.mqqt_recieve)
        #self.pc2pico = threading.Thread(target=self.socket_send)
        self.pc2main.start()
        self.path2pc.start()
        #self.main2pc.start()
        #self.pc2pico.start()
        self.pc2main.join()
        self.path2pc.join()
        #self.main2pc.join()
        #self.pc2pico.join()

    def path_pc(self):
        while True:
            if not self.goal_reached:
                current_loc = self.find.our_location
                target_top = [0,1]
                target_bottom = [2,1]
                target_left = [1,0]
                target_right = [1,2]

                target = self.find.path[1]
                target_loc = [int((target[1]+0.5)*self.cell_width),int((target[0]+0.5)*self.cell_height)]
                
                self.direction = 0
                self.turn_direction = 0

                for data in self.mock_data_stats:
                    cx = int((data["POS"][0][0] + data["POS"][2][0]) / 2)
                    cy = int((data["POS"][0][1] + data["POS"][2][1]) / 2)
                    pos = [int((current_loc[1]+0.5)*self.cell_width),int((current_loc[0]+0.5)*self.cell_height)]

                    cx_f = int((data["POS"][0][0] + data["POS"][1][0]) / 2)
                    cy_f = int((data["POS"][0][1] + data["POS"][1][1]) / 2)
                    front = [cx_f, cy_f]
                    front = [360,160]

                    self.angle  = self.ang([[pos[0], pos[1]], [front[0], front[1]]],[[pos[0], pos[1]], [target_loc[0], target_loc[1]]])

                    print(pos,front,target_loc)


                    if (current_loc[0] - target[0]) ==1 and  (current_loc[1] - target[1])==0:
                        self.direction = "top"

                    elif (current_loc[0] - target[0]) ==-1 and  (current_loc[1] - target[1])==0:
                        self.direction = "bottom"

                    elif (current_loc[0] - target[0]) ==0 and  (current_loc[1] - target[1])==1:
                        self.direction = "left"

                    elif (current_loc[0] - target[0]) ==0 and  (current_loc[1] - target[1])== -1:
                        self.direction = "right"
                    
                    else:
                        print("invalid target")

                    if self.direction == "top":
                        if front[0]>=target_loc[0]:
                            self.turn_direction = "left"
                        else:
                            self.turn_direction = "right"

                    if self.direction == "bottom":
                        if front[0]>=target_loc[0]:
                            self.turn_direction = "right"
                        else:
                            self.turn_direction = "left"

                    if self.direction == "left":
                        if front[1]>=target_loc[1]:
                            self.turn_direction = "right"
                        else:
                            self.turn_direction = "left"

                    if self.direction == "right":
                        if front[1]>=target_loc[1]:
                            self.turn_direction = "left"
                        else:
                            self.turn_direction = "right"

                    print(self.direction,self.turn_direction,self.angle)
                    self.goal_reached = True


    def dot(self,vA, vB):
        return vA[0]*vB[0]+vA[1]*vB[1]

    def ang(self,lineA, lineB):
        vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
        vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
        dot_prod = self.dot(vA, vB)
        magA = self.dot(vA, vA)**0.5
        magB = self.dot(vB, vB)**0.5
        cos_ = dot_prod/magA/magB
        angle = math.acos(dot_prod/magB/magA)
        ang_deg = math.degrees(angle)%360
        
        if ang_deg-180>=0:
            return 360 - ang_deg
        else: 
            
            return ang_deg

    def socket_send(self):
        
        addr = socket.getaddrinfo("192.168.1.102", 1235)[0][-1]
        ServerSideSocket = socket.socket()
        ServerSideSocket.bind(addr)
        ServerSideSocket.listen(5)
        conn, address = ServerSideSocket.accept()

        while True:
            if self.flag:

                if self.speed == "S" and self.is_start:
                    self.motor1_speed = 100
                    self.motor2_speed = 100
                
                elif self.speed == "M" and self.is_start:
                    self.motor1_speed = 100
                    self.motor2_speed = 100
                
                elif self.speed == "H" and self.is_start:
                    self.motor1_speed = 100
                    self.motor2_speed = 100
                
                else:
                    self.motor1_speed = 0
                    self.motor2_speed = 0
                
                data = conn.recv(1024).decode()
                conn.sendall(f"{0},{self.motor1_speed},{self.motor2_speed},{self.role}".encode())  # send data to the client
                time.sleep(0.2)

    def mqqt_send(self):
        while True:
            if self.flag:

                list_send = f"[{self.id}, {self.role}, {self.speed}, {self.points}, (3,2), (3,3), {self.green_left}]"
                self.client.publish("robotsay", list_send)
                #print(list_send)
            time.sleep(0.2)                

    def slope(self, x1, y1, x2, y2):
        return (y2-y1)/(x2-x1)

    def angle(self, s1, s2): 
        return math.degrees(math.atan((s2-s1)/(1+(s2*s1))))


    def on_message(self,client, userdata, message, details = False):
        
        if message.topic =='arena':
            print("arena")
            self.arena_mock = False
            f = open("arena.png", "wb")
            f.write(message.payload)
            f.close()
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


        if self.arena_mock:
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

        if self.arena_mock:
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

            if self.id in self.pred:
                self.ally = self.pred
                self.enemy = self.prey
                self.current_role = 0
                self.role = self.roles[self.current_role]

            if self.id in self.prey:
                self.ally = self.prey
                self.enemy = self.pred
                self.current_role = 1
                self.role = self.roles[self.current_role]


        if message.topic =='config':
            self.config = ast.literal_eval(message.payload.decode())
            #print(self.mock_data_config)
            print(self.config)
            for key in self.config:
                if key == "PREDATOR":
                    self.pred = [pred for pred in self.config[key][4]]
                    self.yellow_point_pred = self.config[key][0]
                    self.blue_point_pred = self.config[key][1]
                    self.yellow_speed_pred = self.config[key][2]
                    self.blue_speed_pred = self.config[key][3]

                elif key == "PREY":
                    self.prey = [prey for prey in self.config[key][4]]
                    self.yellow_point_prey = self.config[key][0]
                    self.blue_point_prey = self.config[key][1]
                    self.yellow_speed_prey = self.config[key][2]
                    self.blue_speed_prey = self.config[key][3]

                elif key == "TIMEOUT":
                    self.green_timeout = self.config[key]

            if self.id in self.pred:
                self.ally = self.pred.copy()
                self.enemy = self.prey.copy()
                self.current_role = 0
                self.role = self.roles[self.current_role]

            if self.id in self.prey:
                self.ally = self.prey.copy()
                self.enemy = self.pred.copy()
                self.current_role = 1
                self.role = self.roles[self.current_role]
            print(self.ally, self.enemy)

        if message.topic =='tick':
            self.remaining_time = message.payload

        if message.topic =='start':

            if "GO":
                self.is_start = True

            if "PAUSE":
                self.is_start = False

            if "STOP":
                self.is_start = False

        if message.topic =='stats':

            self.pred_pos = []
            self.prey_pos = []
            self.green_left = self.green_timeout - (time.time() - self.green_last)
            if self.green_left < 0:
                self.green_left = 0
                self.green_available = True
            #print(eval(message.payload.decode()))
            for data in eval(message.payload.decode()):
                cx = int((data["POS"][0][0] + data["POS"][2][0]) / 2)
                cy = int((data["POS"][0][1] + data["POS"][2][1]) / 2)
                pos = [[int(cy/self.cell_height),int(cx/self.cell_width)]]

                if pos in self.grid["green"] and self.green_available:
                    self.green_available = False
                    self.green_last = time.time()
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

                if data["ID"] in self.pred:
                    self.pred_pos.append([pos, data["ID"]])

                if data["ID"] in self.prey:
                    self.prey_pos.append([pos, data["ID"]])

                if self.goal_reached:
                    self.find = path_finder(self.map, self.prey_pos, self.pred_pos, self.role)
                    self.goal = self.find.path[1]
                    self.current = self.find.our_location
                    self.goal_reached = False
                    
            #print(self.enemy_pos)
            #print(self.ally_pos)

            self.flag = True


if __name__ == "__main__":
    final = Final()
