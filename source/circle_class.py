from pyglet import shapes,text
from random import randint
import math
import numpy as np
# self.circle = shapes.Circle(x=100, y=150, radius=100, color=(50, 225, 30), batch=Batch)

DIVS = 15



class _Circle(shapes.Circle):
    def __init__(self,x=100, y=150, radius=100, color=(50, 225, 30), batch=None):
        super().__init__(x=x, y=y, radius=radius, color=color, batch=batch)
        self.vel = np.array([randint(-100,100),randint(-100,100)])
        self.bucket = 0
        self.label = None
    def set_label(self,batch):
        self.label = text.Label(f'{self.bucket}',font_name='Times New Roman',font_size=20,x=self.x, y=self.y,anchor_x='center', anchor_y='center',batch=batch)

    # def collision(self,other):
    #     if self == other:
    #         return
    #     close_flag = False
    #     for i in (-1, 0, 1,-DIVS,-DIVS+1,-DIVS-1,DIVS,DIVS+1,DIVS-1):
    #         if self.bucket + i == other.bucket:
    #             close_flag = True
    #             break
    #     if not close_flag:
    #         return

    def overlaps(self, other):
        if self == other:
            return False
        close_flag = False
        for i in (-1,0, 1,-DIVS,-DIVS+1,-DIVS-1,DIVS,DIVS+1,DIVS-1):
            if self.bucket + i == other.bucket:
                close_flag = True
                break
        if close_flag:
            return np.hypot(*(np.array((self.x, self.y)) - np.array((other.x, other.y)))) < self.radius + other.radius

    def update(self,w,h,batch,dlt):
        self.x += self.vel[0]*dlt
        self.y += self.vel[1]*dlt
        self.vel[0] *= .95
        self.vel[1] *= .95
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vel[0] *= -1
        elif self.x + self.radius > w:
            self.x = w -self.radius
            self.vel[0] *= -1

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vel[1] *= -1
        elif self.y + self.radius > h:
            self.y = h -self.radius
            self.vel[1] *= -1

        self.bucket = int((self.x // (w//DIVS))+ (self.y // (h // DIVS))*DIVS)
        self.set_label(batch)




