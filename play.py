from utils import RES
from view import View
from pyglet.gl import *


class Play(View):
    def __init__(self, *args, **kwargs):
        super(Play, self).__init__(*args, **kwargs)

        """
        
        self.action_keys = {
            pyglet.window.key.UP: self.env.car.actions['UP'],
            pyglet.window.key.RIGHT: self.env.car.actions['RIGHT'],
            pyglet.window.key.DOWN: self.env.car.actions['DOWN'],
            pyglet.window.key.LEFT: self.env.car.actions['LEFT']
        }
        
        """

    def setup(self):
        pass

    def loop(self):
        pass


if __name__ == "__main__":
    play = Play(RES[0], RES[1], "FlappAI BirDQN - PLAY", None)
    pyglet.clock.schedule_interval(play.on_draw, 0.002)
    pyglet.app.run()
