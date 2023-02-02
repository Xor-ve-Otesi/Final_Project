import math

class DENEME:

    def __init__(self) -> None:
        self.mock_data_stats = [{'ID':9, 'POS':[[20,20],[20, 100],[100,100],[100,20]]}, {'ID':12, 'POS':[[300,160],[340, 160],[340,200],[300,200]]}]

        for data in self.mock_data_stats:
            cx = int((data["POS"][0][0] + data["POS"][2][0]) / 2)
            cy = int((data["POS"][0][1] + data["POS"][2][1]) / 2)
            pos = [1,1.5]


            cx_f = int((data["POS"][0][0] + data["POS"][1][0]) / 2)
            cy_f = int((data["POS"][0][1] + data["POS"][1][1]) / 2)
            front = [2, 1]

            print(pos, front)
            slope1 = self.slope(pos[0], pos[1], front[0], front[1])
            slope2 = self.slope(pos[0], pos[1], 2, 1.5)

            self.ang = self.angle(slope2, slope1)
            print(self.ang)


    def slope(self, x1, y1, x2, y2): # Line slope given two points:
        return (y2-y1)/(x2-x1)

    def angle(self, s1, s2): 
        return math.degrees(math.atan((s2-s1)/(1+(s2*s1))))


DENEME()