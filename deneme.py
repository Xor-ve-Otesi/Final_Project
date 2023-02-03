import math
from path_finder import path_finder
import numpy as np

arena = np.array([  [ 0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  3,  0,  0,  0],
                    [ 0,  1,  0, -1,  0,  2,  0,  3],
                    [ 0,  0,  0,  0,  2,  0,  0,  0],
                    [ 0,  0,  1,  0,  0, -1,  0, -1],
                    [-1,  0,  0,  0,  0,  0,  0,  0]])

class DENEME:

    def __init__(self) -> None:
        self.mock_data_stats = [{'ID':9, 'POS':[[0,0],[0, 80],[80,80],[80,0]]}, {'ID':12, 'POS':[[300,160],[340, 160],[340,200],[300,200]]}]
        self.cell_width = 80
        self.cell_height = 80
        find = path_finder(arena, [[[[2, 6]], 9], [[[0, 0]], 12]], [[[[2, 4]], 8], [[[3, 4]], 10]], "PREDATOR")
        print("Path:", find.path)
        current_loc = find.our_location
        target_top = [0,1]
        target_bottom = [2,1]
        target_left = [1,0]
        target_right = [1,2]

        target = find.path[1]
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


DENEME()