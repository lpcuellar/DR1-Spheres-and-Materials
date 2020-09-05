import numpy as np

from gl import color
from mathGl import MathGl


white = color(1, 1, 1)

class Material(object):
    def __init__(self, diffuse = white):
        self.diffuse = diffuse

class Intersect(object):
    def __init__(self, distance):
        self.distance = distance

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

        self.mathGl = MathGl()

    def ray_intersect(self, orig, dir):
        L = self.mathGl.subtract(self.center, orig)
        tca = self.mathGl.dot(L, dir)
        
        l = self.mathGl.norm(L)

        d = (l**2 - tca**2) **0.5

        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None
        
        return Intersect(distance = t0)