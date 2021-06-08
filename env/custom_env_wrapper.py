# """CHANGE CUSTOM ENV IMPORT HERE""" ##################################################################################
from .custom_env import Pipes, SeaMonkey, RES
########################################################################################################################

import gym
from gym import spaces
import numpy as np

import os
from csv import DictWriter


class CustomEnvWrapper(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, m, p=None):
        super(CustomEnvWrapper, self).__init__()

        self.mode = {"train": False, "observe": False, "play": False, m: True}
        self.player = p if self.mode["play"] else None

        self.steps = 0
        self.total_reward = 0.

        # """CHANGE ENV CONSTRUCT HERE""" ##############################################################################
        self.seamonkey = SeaMonkey()
        self.pipes = Pipes()
        ################################################################################################################

        # """CHANGE FEATURE SCALING HERE""" ############################################################################
        self.lim_features = {
            "sonar_distance_x": (0., RES[0] + (self.pipes.pipes[0].w // 2)),
            "sonar_distance_y": (0., abs(self.seamonkey.y_lim[0]) + abs(self.pipes.pipes[0].y_lim[1])),
            "rel_h": (0., 1.)
        }
        ################################################################################################################

        # """CHANGE ACTION AND OBSERVATION SPACES HERE""" ##############################################################
        action_space_n = len(self.seamonkey.actions)
        observation_space_n = self.seamonkey.n_sonars + 1
        ################################################################################################################

        if "reward" not in self.lim_features:
            self.lim_features["reward"] = (0., 1.)

        self.action_space = spaces.Discrete(action_space_n)
        self.observation_space = spaces.Box(low=0., high=1., shape=(observation_space_n,), dtype=np.float32)

        self.log_info_buffer = []

    def scale(self, x, feature):
        return (x - self.lim_features[feature][0]) / (self.lim_features[feature][1] - self.lim_features[feature][0])

    def _obs(self):
        obs = []

        # """CHANGE OBSERVATION HERE""" ################################################################################
        x, y = self.pipes.get_next_pipe.end_x_y
        self.seamonkey.sonars(x, y)
        self.seamonkey.relative_height(y)

        obs += [
            self.scale(self.seamonkey.sonar_distances[0], "sonar_distance_x"),
            self.scale(self.seamonkey.sonar_distances[1], "sonar_distance_y"),
            self.scale(self.seamonkey.rel_h, "rel_h")
        ]
        ################################################################################################################

        return np.array(obs, dtype=np.float32)

    def _rew(self):
        rew = 0.

        # """CHANGE REWARD HERE""" #####################################################################################
        rew += pow(1 - (self.seamonkey.sonar_distances[1] / self.lim_features["sonar_distance_y"][1]), 2) / 10

        if self.pipes.passed_pipe(self.seamonkey.back_x()):
            self.seamonkey.reward()
            rew = 1
        ################################################################################################################

        rew = self.scale(rew, "reward")
        self.total_reward += rew
        return rew

    def _done(self):
        done = False

        # """CHANGE DONE HERE""" #######################################################################################
        if self.seamonkey.is_collision(self.pipes.get_next_pipe.points()):
            done = True
        ################################################################################################################

        return done

    def _info(self):
        info = {
            "l": self.steps,
            "r": self.total_reward
        }

        if not self.mode["train"]:

            # """CHANGE INFO HERE""" ###################################################################################
            info["time"] = round(self.seamonkey.get_time(), 2)
            info["score"] = self.seamonkey.score
            ############################################################################################################

        return info

    def reset(self):
        self.steps = 0
        self.total_reward = 0.

        # """CHANGE RESET HERE""" ######################################################################################
        self.seamonkey = SeaMonkey(lim_features=self.lim_features)
        self.pipes = Pipes()
        ################################################################################################################

        if not self.mode["train"]:
            self.reset_render()

        return self._obs()

    def step(self, action):
        # """CHANGE STEP HERE""" #######################################################################################
        self.seamonkey.move(action)
        self.pipes.add_pipe()
        self.pipes.move_pipes()
        self.pipes.remove_pipe()
        self.pipes.next_pipe(self.seamonkey.back_x())
        ################################################################################################################

        if not self.mode["train"]:
            self.step_render()

        self.steps += 1

        return self._obs(), self._rew(), self._done(), self._info()

    def reset_render(self):
        # """CHANGE RESET RENDER HERE""" ###############################################################################
        pass
        ################################################################################################################

    def step_render(self):
        # """CHANGE STEP RENDER HERE""" ################################################################################
        self.seamonkey.rotate_theta()
        ################################################################################################################

    def render(self, mode='human'):
        pass

    def log_info_writer(self, info, done, log, log_step, log_path):
        if log and (done or (log_step > 0 and info["l"] % log_step == 0)):
            if "TimeLimit.truncated" not in info:
                info["TimeLimit.truncated"] = False
            info["done"] = done

            self.log_info_buffer.append(info)

            if done:
                file_exists = os.path.isfile(log_path + ".csv")

                with open(log_path + ".csv", 'a') as f:
                    csv_writer = DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=[k for k in info])
                    if not file_exists:
                        csv_writer.writeheader()
                    for log_info in self.log_info_buffer:
                        csv_writer.writerow(log_info)
                    f.close()

                self.log_info_buffer = []
