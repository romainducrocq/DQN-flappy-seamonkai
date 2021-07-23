# """CHANGE CUSTOM ENV IMPORT HERE""" ##################################################################################
from .custom_env import Pipes, SeaMonkey, RES
########################################################################################################################


class DqnEnv:

    def min_max_scale(self, x, feature):
        return (x - self.min_max[feature][0]) / (self.min_max[feature][1] - self.min_max[feature][0])

    def __init__(self, m, p=None):
        self.mode = {"train": False, "observe": False, "play": False, m: True}
        self.player = p if self.mode["play"] else None

        # """CHANGE ENV CONSTRUCT HERE""" ##############################################################################
        self.seamonkey = SeaMonkey()
        self.pipes = Pipes()
        ################################################################################################################

        # """CHANGE FEATURE SCALING HERE""" ############################################################################
        self.min_max = {
            "sonar_distance_x": (0., RES[0] + (self.pipes.pipes[0].w // 2)),
            "sonar_distance_y": (0., abs(self.seamonkey.y_lim[0]) + abs(self.pipes.pipes[0].y_lim[1])),
            "rel_h": (0., 1.),
            "rew": (0., 1.)
        }
        ################################################################################################################

        # """CHANGE ACTION AND OBSERVATION SPACE SIZES HERE""" #########################################################
        self.action_space_n = len(self.seamonkey.actions)
        self.observation_space_n = self.seamonkey.n_sonars + 1
        ################################################################################################################

    def obs(self):
        # """CHANGE OBSERVATION HERE""" ################################################################################
        x, y = self.pipes.get_next_pipe.end_x_y
        self.seamonkey.sonars(x, y)
        self.seamonkey.relative_height(y)

        obs = [
            self.min_max_scale(self.seamonkey.sonar_distances[0], "sonar_distance_x"),
            self.min_max_scale(self.seamonkey.sonar_distances[1], "sonar_distance_y"),
            self.min_max_scale(self.seamonkey.rel_h, "rel_h")
        ]
        ################################################################################################################
        return obs

    def rew(self):
        # """CHANGE REWARD HERE""" #####################################################################################
        rew = pow(1 - self.min_max_scale(self.seamonkey.sonar_distances[1], "sonar_distance_y"), 2) / 10

        if self.pipes.passed_pipe(self.seamonkey.back_x()):
            self.seamonkey.reward()
            rew = 1
        ################################################################################################################
        return rew

    def done(self):
        # """CHANGE DONE HERE""" #######################################################################################
        done = self.seamonkey.is_collision(self.pipes.get_next_pipe.points())
        ################################################################################################################
        return done

    def info(self):
        # """CHANGE INFO HERE""" #######################################################################################
        info = {
            "time": round(self.seamonkey.get_time(), 2),
            "score": self.seamonkey.score
        }
        ################################################################################################################
        return info

    def reset(self):
        # """CHANGE RESET HERE""" ######################################################################################
        self.seamonkey = SeaMonkey(lim_features=self.min_max)
        self.pipes = Pipes()
        ################################################################################################################

    def step(self, action):
        # """CHANGE STEP HERE""" #######################################################################################
        self.seamonkey.move(action)
        self.pipes.add_pipe()
        self.pipes.move_pipes()
        self.pipes.remove_pipe()
        self.pipes.next_pipe(self.seamonkey.back_x())
        ################################################################################################################

    def reset_render(self):
        # """CHANGE RESET RENDER HERE""" ###############################################################################
        pass
        ################################################################################################################

    def step_render(self):
        # """CHANGE STEP RENDER HERE""" ################################################################################
        self.seamonkey.rotate_theta()
        ################################################################################################################
