from .utils import \
    RES, \
    point_on_circle
import math
import time


class SeaMonkey:
    def __init__(self):
        self.x = -RES[0] / 2
        self.y = 0
        self.r = 40
        self.speed = 0
        self.theta = 0
        self.n_points = 50

        self.fall = 1
        self.jump = -80

        self.min_speed = 0
        self.max_speed = 100

        self.score = 0

        self.actions = {'NOOP': 0, 'JUMP': 1}

        self.is_collision = False

        self.debug_color = [255, 0, 0]

        self.start_time = time.time()

    def move(self, action):
        if action == self.actions['JUMP']:
            self.speed += self.jump

        self.speed += self.fall

    def points(self):
        return [
            point_on_circle(i / self.n_points * math.pi * 2, self.r, self.x, self.y)
            for i in range(self.n_points)
        ]

    def vertices(self):
        points = self.points()
        return [
            [points[i-1], points[i]]
            for i in range(self.n_points)
        ]
