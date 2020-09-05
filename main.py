import random

from gl import Raytracer, color
from object import Object, Texture
from sphere import Sphere, Material

r = Raytracer(500, 500)

brick = Material(diffuse = color(0.8, 0.25, 0.25))
stone = Material(diffuse = color(0.4, 0.4, 0.4 ))
grass = Material(diffuse = color(0.5, 1, 0))

snow = Material(diffuse = color(1, 0.96, 0.96))
orange = Material(diffuse = color(1, 0.65, 0))
coal = Material(diffuse = color(0.2, 0.2, 0.2))
dark = Material(diffuse = color(1, 1, 1))


##  snowman body
r.scene.append(Sphere([0, 2.5,  -7], 1, snow))
r.scene.append(Sphere([0, 0.5,  -6], 1.3, snow))
r.scene.append(Sphere([0, -2,  -8], 2, snow))

##  snowman eyes
r.scene.append(Sphere([0.25, 2.2, -5], 0.07, coal))
r.scene.append(Sphere([-0.25, 2.2, -5], 0.07, coal))

##  snowman nose
r.scene.append(Sphere([0, 1.9, -5], 0.2, orange))

##  snowman mouth
r.scene.append(Sphere([0.25, 1.6, -5], 0.07, stone))
r.scene.append(Sphere([-0.25, 1.6, -5], 0.07, stone))
r.scene.append(Sphere([0.1, 1.5, -5], 0.07, stone))
r.scene.append(Sphere([-0.1, 1.5, -5], 0.07, stone))

##  snowman buttons
r.scene.append(Sphere([0, 0.35, -3], 0.2, coal))
r.scene.append(Sphere([0, -0.15, -3], 0.25, coal))
r.scene.append(Sphere([0, -0.75, -3], 0.3, coal))

r.rtRender()

r.glFinish('snowman.bmp')