from .utils import \
    clip, \
    euclidean_distance, \
    point_on_circle, \
    points_to_vertices, \
    safe_dict, \
    RES, \
    FLOOR_Y
import math
import time
import numpy as np


class SeaMonkey:
    def __init__(self, max_features=None):
        self.x = -RES[0] / 2
        self.y = 0
        self.r = 40
        self.speed = 0
        self.n_points = 40

        self.y_lim = (
            -RES[1] + self.r + FLOOR_Y,
            RES[1] - self.r
        )

        self.fall = -0.8
        self.jump = 4
        self.d_a = 0.9

        self.score = 0

        self.actions = {'NOOP': 0, 'JUMP': 1}

        self.n_sonars = 2
        self.sonar_vertices = [[]] * self.n_sonars
        self.sonar_distances = [0.] * self.n_sonars
        self.rel_h = 0

        self.max_sonar_distances = [
            safe_dict(max_features, "sonar_distance_x", 1.),
            safe_dict(max_features, "sonar_distance_y", 1.),
        ]

        self.theta = 0
        self.y_prev = 0

        self.start_time = time.time()

    def move(self, action):
        if action == self.actions['JUMP']:
            self.speed += self.jump

        self.speed += self.fall
        self.speed *= self.d_a
        self.y = clip(*self.y_lim, self.y + self.speed)

    def points(self):
        return [
            point_on_circle(i / self.n_points * math.pi * 2, self.r, self.x, self.y)
            for i in range(self.n_points)
        ]

    def vertices(self):
        return points_to_vertices(self.points())

    def back_x(self):
        return self.x - self.r

    def is_collision(self, rectangles):
        points = self.points()
        for rectangle in rectangles:
            for point in points:
                if rectangle[3][1] <= point[1] <= rectangle[0][1] and rectangle[1][0] <= point[0] <= rectangle[0][0]:
                    return True
        return False

    def reward(self):
        self.score += 1

    def sonars(self, x, y):
        self.sonar_vertices[0] = [(self.x - self.r, self.y), (clip(self.x - self.r, self.x - self.r + self.max_sonar_distances[0], x), self.y)]
        self.sonar_vertices[1] = [(self.x - self.r, self.y), (self.x - self.r, clip(self.y - self.max_sonar_distances[1], self.y + self.max_sonar_distances[1], y))]

        self.sonar_distances[0] = euclidean_distance(self.sonar_vertices[0][0], self.sonar_vertices[0][1])
        self.sonar_distances[1] = euclidean_distance(self.sonar_vertices[1][0], self.sonar_vertices[1][1])

    def relative_height(self, y):
        self.rel_h = int(self.y >= y)

    def rotate_theta(self):
        self.theta = np.interp(self.y - self.y_prev, [-self.jump, self.jump], [-math.pi/4, math.pi/4])
        self.y_prev = self.y

    def vertex_theta(self):
        return [
            [(self.x, self.y), point_on_circle(self.theta, self.r, self.x, self.y)]
        ]

    def get_time(self):
        return time.time() - self.start_time
