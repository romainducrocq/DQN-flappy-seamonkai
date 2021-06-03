from env import Env, View
from pyglet.gl import *  # """FIT TO VIEW IF NOT PYGLET"""


class Play(View):
    def __init__(self, *args, **kwargs):
        super(Play, self).__init__(*args, **kwargs)

        # """FIT TO ACTIONS"""
        self.action_keys = {
            pyglet.window.key.UP: self.env.seamonkey.actions['JUMP']
        }
        ######

    def setup(self):
        _ = self.env.reset()

    def loop(self):
        # """FIT TO ACTIONS"""
        action = self.env.seamonkey.actions['NOOP'] if self.key not in self.action_keys else self.action_keys[self.key]
        ######

        _, _, done, _ = self.env.step(action)
        if done:
            self.setup()


if __name__ == "__main__":

    # """FIT TO VIEW IF NOT PYGLET"""
    play = Play("PLAY", Env())
    pyglet.clock.schedule_interval(play.on_draw, 0.002)
    pyglet.app.run()
    ######
