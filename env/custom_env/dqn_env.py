# """CHANGE DQN ENV TEMPLATE HERE""" ###################################################################################

from .pipe import Pipes
from .seamonkey import SeaMonkey
from .utils import RES


class DqnEnv:

    def min_max_scale(self, x, feature):
        return (x - self.min_max[feature][0]) / (self.min_max[feature][1] - self.min_max[feature][0])

    def __init__(self):
        self.seamonkey = SeaMonkey()
        self.pipes = Pipes()

        self.min_max = {
            "sonar_distance_x": (0., RES[0] + (self.pipes.pipes[0].w // 2)),
            "sonar_distance_y": (0., abs(self.seamonkey.y_lim[0]) + abs(self.pipes.pipes[0].y_lim[1])),
            "rel_h": (0., 1.),
            "rew": (0., 1.)
        }

        self.action_space_n = len(self.seamonkey.actions)
        self.observation_space_n = self.seamonkey.n_sonars + 1

    def obs(self):
        x, y = self.pipes.get_next_pipe.end_x_y
        self.seamonkey.sonars(x, y)
        self.seamonkey.relative_height(y)

        return [
            self.min_max_scale(self.seamonkey.sonar_distances[0], "sonar_distance_x"),
            self.min_max_scale(self.seamonkey.sonar_distances[1], "sonar_distance_y"),
            self.min_max_scale(self.seamonkey.rel_h, "rel_h")
        ]

    def rew(self):
        rew = pow(1 - self.min_max_scale(self.seamonkey.sonar_distances[1], "sonar_distance_y"), 2) / 10

        if self.pipes.passed_pipe(self.seamonkey.back_x()):
            self.seamonkey.reward()
            rew = 1

        return self.min_max_scale(rew, "rew")

    def done(self):
        return self.seamonkey.is_collision(self.pipes.get_next_pipe.points())

    def info(self):
        return {
            "time": round(self.seamonkey.get_time(), 2),
            "score": self.seamonkey.score
        }

    def reset(self):
        self.seamonkey = SeaMonkey(lim_features=self.min_max)
        self.pipes = Pipes()

    def step(self, action):
        self.seamonkey.move(action)
        self.pipes.add_pipe()
        self.pipes.move_pipes()
        self.pipes.remove_pipe()
        self.pipes.next_pipe(self.seamonkey.back_x())

    def reset_render(self):
        pass

    def step_render(self):
        self.seamonkey.rotate_theta()

########################################################################################################################
