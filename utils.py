import math


RES = (360, 640)


def point_on_circle(theta, radius, x_orig, y_orig):
    return x_orig + math.cos(theta)*radius, y_orig + math.sin(theta)*radius
