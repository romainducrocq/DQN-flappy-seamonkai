from .utils import \
    points_to_vertices, \
    RES, \
    FLOOR_Y
import random


class Pipe:
    def __init__(self):
        self.w = 120
        self.h_head = 90
        self.gap = 350

        self.y_lim = (
            -RES[1] + (self.gap // 2) + self.h_head + 1 + FLOOR_Y,
            RES[1] - (self.gap // 2) - self.h_head - 1
        )

        self.x = RES[0] + (self.w // 2)
        self.y = random.randint(*self.y_lim)

        self.speed = 2

        self.is_passed = False

    def move(self):
        self.x -= self.speed

    def points_up(self):
        return [
                (self.x + (self.w // 2), RES[1]),
                (self.x - (self.w // 2), RES[1]),
                (self.x - (self.w // 2), self.y + (self.gap // 2)),
                (self.x + (self.w // 2), self.y + (self.gap // 2))
            ]

    def points_down(self):
        return [
                (self.x + (self.w // 2), self.y - (self.gap // 2)),
                (self.x - (self.w // 2), self.y - (self.gap // 2)),
                (self.x - (self.w // 2), -RES[1]),
                (self.x + (self.w // 2), -RES[1])
            ]

    def points(self):
        return [
            self.points_up(),
            self.points_down()
        ]

    def vertices_up(self):
        return points_to_vertices(self.points_up())

    def vertices_down(self):
        return points_to_vertices(self.points_down())

    def middle_of_screen(self):
        return self.x == 0

    def out_of_screen(self):
        return self.x + (self.w // 2) < -RES[0]

    def passed(self, x):
        return self.x + (self.w // 2) < x

    @property
    def end_x_y(self):
        return self.x + (self.w // 2), self.y


class Pipes:
    def __init__(self):
        self.pipes = [Pipe()]
        self.next_pipe_i = 0

    def add_pipe(self):
        for pipe in self.pipes:
            if pipe.middle_of_screen():
                self.pipes.append(Pipe())
                break

    def move_pipes(self):
        for pipe in self.pipes:
            pipe.move()

    def remove_pipe(self):
        if self.pipes[0].out_of_screen():
            self.pipes.pop(0)

    def next_pipe(self, x):
        for e, pipe in enumerate(self.pipes):
            if not pipe.passed(x):
                self.next_pipe_i = e
                break

    def passed_pipe(self, x):
        for pipe in self.pipes:
            if pipe.passed(x) and not pipe.is_passed:
                pipe.is_passed = True
                return True
        return False

    @property
    def get_next_pipe(self):
        return self.pipes[self.next_pipe_i]
