##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  DR1: SPHERES AND MATERIALS
##  LUIS PEDRO CUÉLLAR - 18220
##


import struct
import numpy as np
from numpy import cos, sin, tan

from object import Object
from mathGl import MathGl


##  char --> 1 byte
def char(var):
    return struct.pack('=c', var.encode('ascii'))

##  word --> 2 bytes
def word(var):
    return struct.pack('=h', var)

##  dword --> 4 bytes
def dword(var):
    return struct.pack('=l', var)

##  function that puts the rgb value of a color into bytes
def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Raytracer(object):
    def __init__(self, width, height, background = None):
        self.glInit(width, height, background)

    ##  initiates the image with the width, height and background color
    def glInit(self, width, height, background):
        background = color(0, 0, 0) if background == None else background
        self.bg_color = background
        self.current_color = color(1, 1, 1)

        self.camera_position = [0, 0, 0]
        self.fov = 60
        self.scene = []

        self.mathGl = MathGl()
        self.glCreateWindow(width, height)

    ##  creates the window with the given
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear(self.bg_color)
        self.glViewPort(0, 0, width, height)

    ##  colors the image with the background color
    def glClear(self, bg_color):
        self.bg_color = bg_color
        self.pixels = [ [ self.bg_color for x in range(self.width)] for y in range(self.height) ]
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glBackground(self, texture):
        self.pixels = [ [ texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in range(self.height) ]

    ##  defines an area inside the window in which it can be drawn points and lines
    def glViewPort(self, x, y, width, height):
         self.vp_x = x
         self.vp_y = y
         self.vp_width = width
         self.vp_height = height

    ##   changes de background color of the image
    def glClearColor(self, r, g, b):
        self.bg_color = color(r, g, b)

        self.glClear(self.bg_color)

   
    ##  draws a point in the image with the given NDC coordinates
    def glVertex(self, x, y, color = None):
        ver_x = (x + 1) * (self.vp_width / 2) + self.vp_x
        ver_y = (y + 1) * (self.vp_height / 2) + self.vp_y

        if (ver_x >= self.width) or (ver_x < 0) or (ver_y >= self.height) or (ver_y < 0) :
            return
        
        try:
            self.pixels[round(ver_y)][round(ver_x)] = color or self.current_color
        except: 
            pass

    ##  draws a pint in the image with pixel coordinates
    def glVertex_coordinates(self, x, y, color = None):
        if (x < self.vp_x) or (x >= self.vp_x + self.vp_width) or (y < self.vp_y) or (y >= self.vp_y + self.vp_height) :
            return
        if (x >= self.width) or (x < 0) or (y >= self.height) or (y < 0):
            return
        try:
            self.pixels[y][x] = color or self.current_color
        except:
            pass

    ##  changes the color of the points that can be drawn
    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    ##  this function is used to write the image into the file, and saves it
    def glFinish(self, filename):
        file = open(filename, 'wb')

        ##  file header --> 14 bytes
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))

        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        ##  image header --> 40 bytes
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        ##  pixels --> 3 bytes each

        for x in range(self.height) :
            for y in range(self.width) :
                file.write(self.pixels[x][y])

        file.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth, depth, depth))

        archivo.close()
    
    def rtRender(self):
        for y in range(self.height):
            for x in range(self.width):
                px = 2 * ((x + 0.5) / self.width) - 1
                py = 2 * ((y + 0.5) / self.height) - 1

                tangente = tan((self.fov * np.pi / 180) / 2)
                r = tangente * self.width / self.height

                px *= r
                py *= tangente

                direction = [px, py, -1]
                nomr_direction = self.mathGl.norm(direction)
                direction = self.mathGl.divMatrix(direction, nomr_direction)

                material = None

                for obj in self.scene:
                    intersect = obj.ray_intersect(self.camera_position, direction)
                    if intersect is not None:
                        if intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = intersect.distance
                            material = obj.material
                
                if material is not None:
                    self.glVertex_coordinates(x, y, material.diffuse)