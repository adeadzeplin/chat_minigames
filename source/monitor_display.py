from pyglet import window, graphics, shapes, text,gl
import pyglet
from source.circle_class import _Circle, DIVS
import numpy as np
from itertools import combinations
import random






class Pachinko(window.Window):
    def __init__(self, queue_dict):
        super().__init__(width=1280, height=720,caption='PACHINKO')
        # self.minimize()
        # self.config = gl.Config(double_buffer=True)
        # self.window = window.Window(1280, 720,config=self.config,caption='PACHINKO')
        self.queue_dict = queue_dict

        self.game_objects = {}
        self.object_batch = graphics.Batch()
        self.text_batch = graphics.Batch()
        self.spawn_circles()

    def spawn_circles(self):
        for _ in range(0,20):
            self.game_objects[f'{random.randint(1,100000000)}'] = _Circle(random.randint(100,900),random.randint(100,620),30,
                                            (random.randint(0,255),random.randint(0,255),random.randint(0,255)),
                                            self.object_batch)

    def on_key_release(self,symbol, modifiers):
        self.game_objects = {}
        self.object_batch = graphics.Batch()
        self.text_batch = graphics.Batch()
        self.spawn_circles()

    # game_logic here
    def update(self, dlt):
        # print('update', dlt)
        self.check_ques()
        self.update_circles(dlt)
        self.check_collision()
        # self.circle.x += dlt*5
        # self.circle.y += dlt*5
    def update_circles(self,dlt):
        self.text_batch = graphics.Batch()

        for _ in self.game_objects:
            self.game_objects[_].update(self.width,self.height,self.text_batch,dlt)

    def check_collision(self):
    #     checked = []
    #     for a in self.game_objects:
    #         if a not in checked:
    #             checked.append(a)
    #             for b in self.game_objects:
    #                 if a != b:
    #                     self.game_objects[a].collision(self.game_objects[b])
    # # https://scipython.com/blog/two-dimensional-collisions/
    # # collision detection code found here
    # def handle_collisions(self):
        def change_velocities(p1, p2):
            m1, m2 = p1.radius**2, p2.radius**2
            M = m1 + m2
            r1, r2 = np.array([p1.x,p1.y]), np.array([p2.x,p2.y])
            d = np.linalg.norm(r1 - r2)**2
            v1, v2 = p1.vel, p2.vel
            u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
            u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
            p1.vel = u1
            p2.vel = u2
        pairs = combinations(self.game_objects,2)
        for i,j in pairs:
            if self.game_objects[i].overlaps(self.game_objects[j]):
                change_velocities(self.game_objects[i], self.game_objects[j])


    def on_draw(self):
        self.clear()
        self.object_batch.draw()
        self.text_batch.draw()
        for _ in range(0,DIVS):
            graphics.draw(2, gl.GL_LINES,
                             ('v2i', (_ * self.width//DIVS, 0, _ * self.width//DIVS, self.height)))
            graphics.draw(2, gl.GL_LINES,
                          ('v2i', (0, _ * self.height//DIVS, self.width, _ * self.height//DIVS)))


    def check_ques(self):
        while True:
            try:
                data = self.queue_dict['queueue'].get(0)
                print(data)
            except:
                break


