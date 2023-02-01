import heapq
import numpy as np

class path_finder:

    def __init__(self, map, prey_pos, predator_pos, role):
        self.arena = map
        self.prey_locations = []
        self.predator_locations = []
        self.our_location = []
        self.our_role = role
        self.row, self.col = map.shape
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.goal = (-1, -1)
        self.path = []
        for pos in prey_pos:
            self.prey_locations.append(pos[0][0])
            if pos[1] == 8:
                self.our_location = pos[0][0]
        for pos in predator_pos:
            self.predator_locations.append(pos[0][0])
            if pos[1] == 8:
                self.our_location = pos[0][0]
        print("Prey Locations:", self.prey_locations)
        print("Predator Locations:", self.predator_locations)
        print("Our Location:", self.our_location)
        print("Our Role:", self.our_role)
        print("Arena:\n", self.arena)
        self.objective()

    def is_valid(self, x, y):
        if x >= 0 and x < self.row and y >= 0 and y < self.col:
            if self.arena[x][y] != -1:
                if self.our_role == "PREY":
                    for i in self.prey_locations:
                        if x == i[0] and y == i[1]:
                            return False
                    for i in self.predator_locations:
                        if x == i[0] and y == i[1]:
                            return False
                elif self.our_role == "PREDATOR":
                    if self.arena[x][y] == 3:
                        return False
                    for i in self.predator_locations:
                        if x == i[0] and y == i[1]:
                            return False
                return True
        return False

    def find_path(self, goal):
        heap = [(0, (self.our_location[0], self.our_location[1]), [])]
        visited = set()
        while heap:
            (cost, curr, self.path) = heapq.heappop(heap)
            if curr in visited:
                continue
            visited.add(curr)
            self.path = self.path + [curr]
            if curr == goal:
                return cost, self.path
            for direction in self.directions:
                x, y = curr
                x += direction[0]
                y += direction[1]
                if self.is_valid(x, y):
                    heapq.heappush(heap, (cost+1, (x, y), self.path))
        return -1, []

    def get_min_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def objective(self):

        if self.our_role == "PREY":
            min_distance = float('inf')
            for i in range(self.map.shape[0]):
                for j in range(self.map.shape[1]):
                    if self.map[i][j] == 3:
                        distance = self.find_path((i, j))
                        if distance < min_distance:
                            min_distance = distance
                            self.goal = (i, j)
            self.path = self.find_path(self.goal())

        elif self.our_role == "PREDATOR":
            prey_distances = []
            for prey in self.prey_locations:
                distance, path = self.find_path(tuple(prey))
                prey_distances.append((distance, prey))
            closest_prey = min(prey_distances, key=lambda x: x[0])[1]
            print("Going after prey at", closest_prey)
            self.goal = (closest_prey[0], closest_prey[1])
            length, self.path = self.find_path(self.goal)

arena = np.array([  [ 0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  3,  0,  0,  0],
                    [ 0,  1,  0, -1,  0,  2,  0,  3],
                    [ 0,  0,  0,  0,  2,  0,  0,  0],
                    [ 0,  0,  1,  0,  0, -1,  0, -1],
                    [-1,  0,  0,  0,  0,  0,  0,  0]])

#find = path_finder(arena, [[[[2, 6]], 9], [[[0, 0]], 8]], [[[[2, 4]], 12], [[[3, 4]], 10]], "PREY")
find = path_finder(arena, [[[[2, 6]], 9], [[[0, 0]], 12]], [[[[2, 4]], 8], [[[3, 4]], 10]], "PREDATOR")
print("Path:", find.path)