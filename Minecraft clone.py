import math
import ctypes
import pyglet

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl

import shader
import matrix

vertex_positions = [
    -0.5,
    0.5,
    0.0,
    -0.5,
    -0.5,
    0.0,
    0.5,
    -0.5,
    0.0,
    0.5,
    0.5,
    0.0,
]

indices = [
    0,
    1,
    2,
    0,
    2,
    3,
]


class Window(pyglet.window.Window):
    def __init__(self, **args):
        super().__init__(**args)

        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        self.vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(vertex_positions)),
            (gl.GLfloat * len(vertex_positions))(*vertex_positions),
            gl.GL_STATIC_DRAW,
        )

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLuint * len(indices)),
            (gl.GLuint * len(indices))(*indices),
            gl.GL_STATIC_DRAW,
        )

        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")  # get the shader matrix uniform location
        self.shader.use()

        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()

        self.x = 0
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)  # call update function every 60th of a second

    def update(self, delta_time):
        self.x += delta_time

    def on_draw(self):

        self.p_matrix.load_identity()
        self.p_matrix.perspective(90, float(self.width) / self.height, 0.1, 500)

        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -1)
        self.mv_matrix.rotate_2d(self.x + 6.28 / 4, math.sin(self.x / 3 * 2) / 2)

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()

        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        gl.glViewport(0, 0, width, height)


class Game:
    def __init__(self):
        self.config = gl.Config(double_buffer=True, major_version=3, minor_version=3)
        self.window = Window(
            config=self.config, width=800, height=600, caption="Minecraft clone", resizable=True, vsync=False
        )

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.run()
