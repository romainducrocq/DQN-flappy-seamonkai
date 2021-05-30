from .utils import \
    RES, \
    FLOOR_Y
from pyglet.gl import *
import math
import time


def points_to_pyglet_vertex(points, color):
    return pyglet.graphics.vertex_list(len(points),
                                       ('v3f/stream', [item for sublist in
                                                       map(lambda p: [p[0], p[1], 0], points)
                                                       for item in sublist]),
                                       ('c3B', color_polygon(len(points), color))
                                       )


def color_polygon(n, color):
    colors = []
    for i in range(n):
        colors.extend(color)
    return colors


def draw_polygons(polygons, color):
    [points_to_pyglet_vertex(polygon, color).draw(gl.GL_TRIANGLE_FAN) for polygon in polygons]


def draw_vertices(vertices, color):
    [points_to_pyglet_vertex(vertex, color).draw(gl.GL_LINES) for vertex in vertices]


def draw_label_top_left(text, x, y, y_offset=0, margin=50, font_size=40, color=(0, 0, 0, 255)):
    pyglet.text.Label(text, x=x+margin, y=y-y_offset*(font_size+margin)-margin, font_size=font_size, color=color).draw()


def load_sprite(path, anchor_x=0.5, anchor_y=0.5):
    img = pyglet.image.load(path)
    img.anchor_x = int(img.width * anchor_x)
    img.anchor_y = int(img.height * anchor_y)
    return pyglet.sprite.Sprite(img, 0, 0)


class View(pyglet.window.Window):

    def __init__(self, width, height, name, env):
        super(View, self).__init__(width, height, name, resizable=True)
        glClearColor(1, 1, 1, 1)
        self.width = width
        self.height = height
        self.name = name
        self.zoom = 1
        self.key = None

        self.env = env

        self.ai_view = False
        self.ai_view_timer = time.time()

        self.debug = False
        self.debug_colors = ([255, 0, 0], [0, 0, 255])

        self.background_sprite = load_sprite("./env/img/background.png")
        self.foreground_sprite = load_sprite("./env/img/foreground.png")
        self.seamonkey_sprite = load_sprite("./env/img/seamonkey.png", anchor_x=2/3)
        self.pipe_head_sprite = load_sprite("./env/img/pipe_head.png")
        self.pipe_body_sprite = load_sprite("./env/img/pipe_body_full.png")

        self.setup()

    def on_draw(self, dt=0.002):
        self.clear()

        self.loop()

        self.background_sprite.draw()

        self.seamonkey_sprite.update(x=self.env.seamonkey.x, y=self.env.seamonkey.y, scale_x=1, scale_y=1, rotation=math.degrees(self.env.seamonkey.theta))
        self.seamonkey_sprite.draw()

        for pipe in self.env.pipes.pipes:
            self.pipe_body_sprite.update(x=pipe.x, y=pipe.y - ((pipe.gap // 2) + 2 * RES[0]), scale_x=1, scale_y=1, rotation=0)
            self.pipe_body_sprite.draw()

            self.pipe_head_sprite.update(x=pipe.x, y=pipe.y - ((pipe.gap + pipe.h_head) // 2), scale_x=1, scale_y=1, rotation=0)
            self.pipe_head_sprite.draw()

            self.pipe_body_sprite.update(x=pipe.x, y=pipe.y + ((pipe.gap // 2) + 2 * RES[0]), scale_x=1, scale_y=1, rotation=180)
            self.pipe_body_sprite.draw()

            self.pipe_head_sprite.update(x=pipe.x, y=pipe.y + ((pipe.gap + pipe.h_head) // 2), scale_x=1, scale_y=1, rotation=180)
            self.pipe_head_sprite.draw()

        self.foreground_sprite.draw()

        if self.key == pyglet.window.key.SPACE and (time.time() - self.ai_view_timer) > 0.2:
            self.ai_view = not self.ai_view
            self.ai_view_timer = time.time()
        if self.ai_view:
            draw_vertices(
                self.env.seamonkey.sonar_vertices,
                self.debug_colors[0]
            )

        if self.debug:
            draw_vertices([
                [(-RES[0], -RES[1] + FLOOR_Y), (RES[0], -RES[1] + FLOOR_Y)]
            ],
                self.debug_colors[0]
            )

            draw_vertices(
                self.env.seamonkey.vertices() +
                self.env.seamonkey.vertex_theta(),
                self.debug_colors[0]
            )

            for e, pipe in enumerate(self.env.pipes.pipes):
                draw_vertices(
                    pipe.vertices_up(),
                    self.debug_colors[int(e == self.env.pipes.next_pipe_i)]
                )

                draw_vertices(
                    pipe.vertices_down(),
                    self.debug_colors[int(e == self.env.pipes.next_pipe_i)]
                )

        draw_label_top_left("Time: " + str(round(self.env.seamonkey.get_time(), 2)), -RES[0], RES[1], y_offset=1)
        draw_label_top_left("Score: " + str(self.env.seamonkey.score), -RES[0], RES[1], y_offset=2)

    def on_resize(self, width, height):
        glMatrixMode(gl.GL_MODELVIEW)
        glLoadIdentity()
        glOrtho(-width, width, -height, height, -1, 1)
        glViewport(0, 0, width, height)
        glOrtho(-self.zoom, self.zoom, -self.zoom, self.zoom, -1, 1)

    def on_key_press(self, symbol, modifiers):
        self.key = symbol

    def on_key_release(self, symbol, modifiers):
        if self.key == symbol:
            self.key = None

    def setup(self):
        raise NotImplementedError

    def loop(self):
        raise NotImplementedError
