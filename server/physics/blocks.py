import math
from copy import deepcopy

class Block:
    def normalize(self, point, angle, border):
        # print(angle)
        if "n" in border:
            start_point = [0, point[0]]
            angle += 0.5 * math.pi
        if "e" in border:
            start_point = [0, point[1]]
        if "s" in border:
            start_point = [0, 1 - point[0]]
            angle += 1.5 * math.pi
        if "w" in border:
            start_point = [0, 1 - point[1]]
            angle += math.pi

        angle = (angle + (2*math.pi))%(2*math.pi)

        return start_point, angle
    
    def denormalize(self, start_point, end_point, angle, border):
        if "n" in border:
            start_point = [start_point[1], 1]
            end_point = [end_point[1], 1 - end_point[0]]
            angle -= 0.5 * math.pi
        if "e" in border:
            start_point = start_point
            end_point = end_point
        if "s" in border:
            start_point = [1 - start_point[1], 0]
            end_point = [1 - end_point[1], end_point[0]]
            angle -= 1.5 * math.pi
        if "w" in border:
            start_point = [1, 1 - start_point[1]]
            end_point = [1 - end_point[0], 1 - end_point[1]]
            angle -= math.pi
        
        angle = (angle + (2*math.pi))%(2*math.pi)

        return start_point, end_point, angle


class Empty(Block):
    def __init__(self):
        pass

    def get_laser_path(self, point, angle, strength, border):
        lines = []

        # normalize
        start_point, angle = self.normalize(point, angle, border)

        # get output
        if angle < (math.pi / 2):
            new_y = start_point[1] + math.tan(angle)
            new_x = 1
            if new_y > 1:
                new_y = 1
                new_x = (1-start_point[1]) / math.tan(angle)
        else:
            new_y = start_point[1] + math.tan(angle)
            new_x = 1
            if new_y < 0:
                new_y = 0
                new_x = start_point[1] / -math.tan(angle)
        end_point = [new_x, new_y]
        # print(end_point)


        # denormalize output
        start_point, end_point, angle = self.denormalize(start_point, end_point, angle, border)

        # get output border
        border = []
        if end_point[0] == 0:
            border.append("w")
        if end_point[1] == 0:
            border.append("n")
        if end_point[0] == 1:
            border.append("e")
        if end_point[1] == 1:
            border.append("s")

       
        lines = [start_point, end_point]
        return ([lines], deepcopy(end_point), angle, strength, border)

class Wall(Block):
    def __init__(self):
        pass

    def get_laser_path(self, point, angle, strength, border):
        exit_border = []
        print(angle)
        if "n" in border:
            angle *= -1
            end_point = [point[0], 1]
            exit_border.append("s")
        if "e" in border:
            angle = 0
            end_point = [0, point[1]]
            exit_border.append("w")
        if "s" in border:
            angle *= -1
            end_point = [point[0], 0]
            exit_border.append("n")
        if "w" in border:
            angle *= -1
            end_point = [1, point[1]]
            exit_border.append("e")

        angle = (angle + (2*math.pi))%(2*math.pi)
        print(angle)

        lines = []
        return (lines, end_point, angle, strength, exit_border)

class Emitter:
    def __init__(self, angle=0, strength=10):
        self.angle = angle
        self.strength = strength

    def update_state(self, new_state):
        self.angle = new_state[0]
        self.strength = new_state[1]

    def create_laser_path(self):
        lines = [[0.5, 0.5]]

        dy = 0.5 * math.tan(self.angle)
        dx = 0.5 * math.tan((math.pi / 2) - self.angle)

        exit_border = []
        self.angle = ((self.angle + (math.pi * 2)) % (math.pi * 2))
        if ((math.pi / 4) * 7) <= self.angle or self.angle <= (math.pi / 4):
            exit_border.append("e")
            end_point = [1, dy + 0.5]
        if (math.pi / 4) <= self.angle <= ((math.pi / 4) * 3):
            exit_border.append("s")
            end_point = [dx + 0.5, 1]
        if ((math.pi / 4) * 3) <= self.angle <= ((math.pi / 4) * 5):
            exit_border.append("w")
            end_point = [0, 0.5 - dy]
        if ((math.pi / 4) * 5) <= self.angle <= ((math.pi / 4) * 7):
            exit_border.append("n")
            end_point = [0.5 - dx, 0]


        lines.append(deepcopy(end_point))

        return ([lines], end_point, self.angle, self.strength, exit_border)
    
    def get_laser_path(self, point, angle, strength, border):
        lines =[]
        return (lines, end_point, end_angle, end_strength, exit_border)




class Receiver:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_laser_path(self, point, angle, strength, border):
        # some code
        return (lines, end_point, end_angle, end_strength, exit_border)

class Wood:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_laser_path(self, point, angle, strength, border):
        # some code
        return (lines, end_point, end_angle, end_strength, exit_border)

class Mirror:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_laser_path(self, point, angle, strength, border):
        # some code
        return (lines, end_point, end_angle, end_strength, exit_border)

class Glass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_laser_path(self, point, angle, strength, border):
        # some code
        return (lines, end_point, end_angle, end_strength, exit_border)
