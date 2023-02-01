import heapq

class path_finder:

    def __init__(self, map, prey_pos, predator_pos, role):
        self.arena = map
        self.prey_locations = []
        self.predator_locations = []
        self.our_location = []
        self.our_role = role
        self.row, self.col = map.shape
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
        print("Shortest path length:", self.find_path((3,7)))

    def predator(self):
        pass

    def prey(self):
        pass

    def is_valid(self, x, y):
        if x >= 0 and x < self.row and y >= 0 and y < self.col:
            if self.arena[x][y] != -1:
                return True
        return False

    def find_path(self, goal):
        heap = [(0, (self.our_location[0], self.our_location[1]))]
        visited = set()
        while heap:
            (cost, curr) = heapq.heappop(heap)
            if curr in visited:
                continue
            visited.add(curr)
            if curr == goal:
                return cost
            neighbors = [(curr[0]+1, curr[1]), (curr[0]-1, curr[1]), (curr[0], curr[1]+1), (curr[0], curr[1]-1)]
            for neighbor in neighbors:
                if self.is_valid(*neighbor):
                    heapq.heappush(heap, (cost+1, neighbor))
        return -1