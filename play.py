from env import Env, View, safe_dict, RES
from pyglet.gl import *


class Play(View):
    def __init__(self, *args, **kwargs):
        super(Play, self).__init__(*args, **kwargs)

        self.action_keys = {
            pyglet.window.key.SPACE: self.env.seamonkey.actions['JUMP']
        }

    def setup(self):
        _ = self.env.reset()
        """
        self.polygons_track = self.env.reset_render()
        """
        self.env.reset_render()

    def loop(self):
        action = safe_dict(self.action_keys, self.key, self.env.seamonkey.actions['NOOP'])
        _, _, done, _ = self.env.step(action)
        if done:
            self.setup()


if __name__ == "__main__":

    play = Play(RES[0], RES[1], "flappy seamonkai - PLAY", Env())
    pyglet.clock.schedule_interval(play.on_draw, 0.002)
    pyglet.app.run()
