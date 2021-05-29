from .seamonkey import SeaMonkey
from .pipe import Pipes
from .utils import \
    RES
import gym
from gym import spaces
import numpy as np


class CustomEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, train=False):
        super(CustomEnv, self).__init__()

        self.train = train

        self.steps = 0
        self.total_reward = 0.

        self.seamonkey = SeaMonkey()
        self.pipes = Pipes()

        self.MAX_FEATURES = {
            "sonar_distance_x": RES[0] + (self.pipes.pipes[0].w // 2),
            "sonar_distance_y": abs(self.seamonkey.y_lim[0]) + abs(self.pipes.pipes[0].y_lim[1])
        }

        self.action_space = spaces.Discrete(len(self.seamonkey.actions))
        self.observation_space = spaces.Box(low=0., high=1., shape=(self.seamonkey.n_sonars+1,), dtype=np.float32)

    def _obs(self):
        x, y = self.pipes.get_next_pipe.end_x_y
        self.seamonkey.sonars(x, y)
        self.seamonkey.relative_height(y)

        obs = np.array(
            [
                self.seamonkey.sonar_distances[0] / self.MAX_FEATURES["sonar_distance_x"],
                self.seamonkey.sonar_distances[1] / self.MAX_FEATURES["sonar_distance_y"],
                self.seamonkey.rel_h / 1.
            ], dtype=np.float32)

        print(obs)
        return obs

    def _rew(self):
        rew = 0.
        if self.pipes.passed_pipe(self.seamonkey.back_x()):
            self.seamonkey.reward()
            rew += 1
        self.total_reward += rew
        return rew

    def _done(self):
        done = self.seamonkey.is_collision(self.pipes.get_next_pipe.points())
        return done

    def _info(self):
        info = {
            "l": self.steps,
            "r": self.total_reward
        }
        return info

    def reset(self):
        self.seamonkey = SeaMonkey(self.MAX_FEATURES)
        self.pipes = Pipes()

        return self._obs()

    def step(self, action):
        self.seamonkey.move(action)
        self.pipes.add_pipe()
        self.pipes.move_pipes()
        self.pipes.remove_pipe()
        self.pipes.next_pipe(self.seamonkey.back_x())

        if not self.train:
            self.seamonkey.rotate_theta()

        self.steps += 1

        return self._obs(), self._rew(), self._done(), self._info()

    def render(self, mode='human'):
        pass
