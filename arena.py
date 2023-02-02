import cv2
import numpy as np

"""
https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-self.hsv-boundaries-for-color-detection-withcv
"""

class ArenaFinder():

    def __init__(self) -> None:
        try:
            self.arena_raw = cv2.imread("arena.png")
            self.hsv = cv2.cvtColor(self.arena_raw, cv2.COLOR_BGR2HSV)
        except:
            self.arena_raw = cv2.imread("arena.jpeg")
            self.hsv = cv2.cvtColor(self.arena_raw, cv2.COLOR_BGR2HSV)

        self.kernel_3 = np.ones((3, 3), np.uint8)
        self.kernel_5 = np.ones((5, 5), np.uint8)
        self.kernel_7 = np.ones((7, 7), np.uint8)
        self.grid = {"blue":[],"green":[],"yellow":[],"red":[]}
        self.grid_loc = {"blue":[],"green":[],"yellow":[],"red":[]}
        self.color_bgr = {"blue":(255,0,0),"green":(0,255,9),"yellow":(0,255,255),"red":(0,0,255)}
        self.color_segmentation(np.array([80, 138, 0]), np.array([163, 255, 184]), "blue")
        self.color_segmentation(np.array([40, 138, 0]), np.array([90, 255, 184]), "green")
        self.color_segmentation(np.array([14, 138, 0]), np.array([31, 255, 184]), "yellow")
        self.color_segmentation(np.array([0, 138, 0]), np.array([20, 255, 184]), "red", np.array([150, 138, 0]), np.array([179, 255, 184]))
        
        cell_height = self.arena_raw.shape[0]/6
        cell_width = self.arena_raw.shape[1]/8
        for key in self.grid:
            for loc in self.grid[key]:
                self.grid_loc[key].append([int(loc[1]/cell_width),int(loc[0]/cell_height)])

        #print(self.grid)
        #print("**************")
        #print(self.grid_loc)
        #cv2.imshow("Original", self.arena_raw)
        #cv2.waitKey(0)


    def color_segmentation(self, lower_bound, upper_bound, color, lower_bound2 = [], upper_bound2 = []):

        if len(lower_bound2):
            mask_1 = cv2.inRange(self.hsv, lower_bound, upper_bound)
            mask_2 = cv2.inRange(self.hsv, lower_bound2, upper_bound2)
            mask = mask_1 + mask_2

        else:
            mask = cv2.inRange(self.hsv, lower_bound, upper_bound)

        result = cv2.bitwise_and(self.arena_raw , self.arena_raw , mask=mask)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        erode = cv2.erode(gray, self.kernel_3,iterations=1)
        dil = cv2.dilate(erode, self.kernel_5, iterations=2)
        erode = cv2.erode(dil, self.kernel_5, iterations=3)

        #cv2.imshow(f"result {color}", erode)
        ret,thresh_img = cv2.threshold(erode, 0, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0
        for cnt in contours:
            if cv2.contourArea(cnt) > 2000:
                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cv2.putText(self.arena_raw, color, (cx-20, cy),cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.color_bgr[color], 2)
                    cv2.drawContours(self.arena_raw, contours, i, self.color_bgr[color], 3)
                    self.grid[color].append([cx,cy])
            i += 1


    def __call__(self):
        return self.grid_loc

if __name__ == "__main__":
    ArenaFinder()