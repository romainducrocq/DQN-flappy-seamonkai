import math

# """CHANGE VIEW RESOLUTION HERE"""
RES = (360, 640)
######

#########################
# """CHANGE UTILS HERE"""

FLOOR_Y = 100


def safe_dict(d, key, def_val):
    return def_val if d is None or key not in d else d[key]


def clip(min_clip, max_clip, x):
    return max(min_clip, min([max_clip, x])) if min_clip < max_clip else x


def euclidean_distance(point1, point2):
    return math.sqrt(pow(point2[0] - point1[0], 2) + pow(point2[1] - point1[1], 2))


def point_on_circle(theta, radius, x_orig, y_orig):
    return x_orig + math.cos(theta)*radius, y_orig + math.sin(theta)*radius


def points_to_vertices(points):
    return [
        [points[i-1], points[i]]
        for i in range(len(points))
    ]

#########################
