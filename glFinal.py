import random
import numpy
from numpy import matrix, cos, sin, tan
from obj import Obj, Texture
from collections import namedtuple
import struct 

## UTILS
# implementacion de "vectores" para manejar menos variables en funciones y tener mejor orden de coordenadas
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def sum(v0, v1):
  # suma dos vectores de 3 elementos 
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  # resta dos vectores de 3 elementos
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  # multiplica un vector de 3 elementos por una constante
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  # reliza el producto punto de dos vectores de 3 elementos 
  # el resultado es un escalar
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v1, v2):
  return V3(
    v1.y * v2.z - v1.z * v2.y,
    v1.z * v2.x - v1.x * v2.z,
    v1.x * v2.y - v1.y * v2.x,
  )

def length(v0):
  # devuelve el tamaño (escalar) del vector
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  #calcula la normal de un vector de 3 elementos
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  # Se reciben *n vectores de 2 elementos para encontrar los x,y maximos y minimos
  # para poder hacer la boundingbox, es decir cubrir el poligono
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]

  return (max(xs), max(ys), min(xs), min(ys))

def barycentric(A, B, C, P):
  # Este algoritmo de numeros baricentricos sirve para llena un poligono
  # Parametros: 3 vectores de 2 elementos y un punto
  # Return: 3 coordinadas baricentricas del punto segun el triangulo formado a partir de los vectores
  cx, cy, cz = cross(
    V3(B.x - A.x, C.x - A.x, A.x - P.x), 
    V3(B.y - A.y, C.y - A.y, A.y - P.y)
  )

  if abs(cz) < 1:
    return -1, -1, -1   # no es un triangulo de verdad, no devuelve nada afuera

  # [cx cy cz] == [u v 1]

  u = cx/cz
  v = cy/cz
  w = 1 - (cx + cy)/cz

  return w, v, u

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([b, g, r])

# ===============================================================
# Render BMP file
# ===============================================================

BLACK = color(0,0,0)
WHITE = color(255,255,255)
RED = color(255, 0, 0)

class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.glClear()
    self.light = V3(0,0,1)
    self.active_texture = None
    self.active_vertex_array = []
    #array del tamaño del buffer lleno de -infinitos

  def glClear(self):
    self.buffer = [
      [BLACK for x in range(self.width)] 
      for y in range(self.height)
    ]
    self.zbuffer = [
      [-float('inf') for x in range(self.width)] 
      for y in range(self.height)
    ]

  def finish(self, filename):
    f = open(filename, 'wb')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Pixel data (width x height x 3 pixels)
    for x in range(self.height):
      for y in range(self.width):
        f.write(self.buffer[x][y])

    f.close()

  def set_color(self, color):
    self.current_color = color

  def glColor(self, r=1, g=1, b=1):
    red = round(r*255)
    green = round(g*255)
    blue = round(g*255)
    self.current_color = color(red, green, blue)

  def point(self, x, y):
    try:
      self.buffer[y][x] = self.current_color
    except:
      # si esta "out of index"
      pass
    
  def glLine(self, x0, y0, x1, y1):
    # Funciones para aplicar la ecuacion de la recta y dibujar lineas con valores mayores de -1 a 1
    x1, y1 = x0, y0
    x2, y2 = x1, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx

    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            self.point(y, x)
        else:
            self.point(x, y)
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += dx * 2


  def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)

    if self.active_texture:
      tA = next(self.active_vertex_array)
      tB = next(self.active_vertex_array)
      tC = next(self.active_vertex_array)

    nA = next(self.active_vertex_array)
    nB = next(self.active_vertex_array)
    nC = next(self.active_vertex_array)

    xmax, ymax, xmin, ymin = bbox(A, B, C)

    normal = norm(cross(sub(B, A), sub(C, A)))
    intensity = dot(normal, self.light)
    if intensity < 0:
      return

    for x in range(round(xmin), round(xmax) + 1):
      for y in range(round(ymin), round(ymax) + 1):
        P = V2(x, y)
        w, v, u = barycentric(A, B, C, P)
        if w < 0 or v < 0 or u < 0:  # 0 es valido y estan el la orilla
          #el punto esta afuera y no se dibuja
          continue
          #se calcula la profunidad en z de cada punto

        if self.active_texture:
          tx = tA.x * w + tB.x * v + tC.x * u
          ty = tA.y * w + tB.y * v + tC.y * u

          self.current_color = self.active_texture.get_color(tx, ty, intensity)
        
        z = A.z * w + B.z * v + C.z * u
        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y)
          self.zbuffer[x][y] = z
        """try:
          if z > self.zbuffer[x][y]:
            self.point(x,y)
            self.zbuffer[x][y] = z
        except:
          pass"""
    
  def transform(self, vertex):
    augmented_vertex = [
      vertex.x,
      vertex.y,
      vertex.z,
      1
    ]
    tranformed_vertex = self.Viewport @ self.Projection @ self.View @ self.Model @ augmented_vertex

    tranformed_vertex = tranformed_vertex.tolist()[0]

    tranformed_vertex = [
      (tranformed_vertex[0]/tranformed_vertex[3]),
      (tranformed_vertex[1]/tranformed_vertex[3]),
      (tranformed_vertex[2]/tranformed_vertex[3])
    ]
    print(V3(*tranformed_vertex))
    return V3(*tranformed_vertex)
      
  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    self.loadModelMatrix(translate, scale, rotate)
    model = Obj(filename)
    vertex_buffer_object = []
    
    for face in model.faces:
      for facepart in face:
          vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
          vertex_buffer_object.append(vertex)

      if self.active_texture:
        for facepart in face:
          tvertex = V3(*model.tvertices[facepart[1]-1])
          vertex_buffer_object.append(tvertex)

    self.active_vertex_array = iter(vertex_buffer_object)

  def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)

    translation_matrix = matrix([
      [1, 0, 0, translate.x],
      [0, 1, 0, translate.y],
      [0, 0, 1, translate.z],
      [0, 0, 0, 1],
    ])


    a = rotate.x
    rotation_matrix_x = matrix([
      [1, 0, 0, 0],
      [0, cos(a), -sin(a), 0],
      [0, sin(a),  cos(a), 0],
      [0, 0, 0, 1]
    ])

    a = rotate.y
    rotation_matrix_y = matrix([
      [cos(a), 0,  sin(a), 0],
      [     0, 1,       0, 0],
      [-sin(a), 0,  cos(a), 0],
      [     0, 0,       0, 1]
    ])

    a = rotate.z
    rotation_matrix_z = matrix([
      [cos(a), -sin(a), 0, 0],
      [sin(a),  cos(a), 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1]
    ])

    rotation_matrix = rotation_matrix_x @ rotation_matrix_y @ rotation_matrix_z

    scale_matrix = matrix([
      [scale.x, 0, 0, 0],
      [0, scale.y, 0, 0],
      [0, 0, scale.z, 0],
      [0, 0, 0, 1],
    ])

    self.Model = translation_matrix @ rotation_matrix @ scale_matrix

  def loadViewMatrix(self, x, y, z, center):
    M = matrix([
      [x.x, x.y, x.z,  0],
      [y.x, y.y, y.z, 0],
      [z.x, z.y, z.z, 0],
      [0,     0,   0, 1]
    ])

    O = matrix([
      [1, 0, 0, -center.x],
      [0, 1, 0, -center.y],
      [0, 0, 1, -center.z],
      [0, 0, 0, 1]
    ])

    self.View = M @ O

  def loadProjectionMatrix(self, coeff):
    self.Projection =  matrix([
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, coeff, 1]
    ])

  def loadViewportMatrix(self, x = 0, y = 0):
    self.Viewport =  matrix([
      [self.width/2, 0, 0, x + self.width/2],
      [0, self.height/2, 0, y + self.height/2],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ])

  def lookAt(self, eye, center, up):
    z = norm(sub(eye, center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))
    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix(-1 / length(sub(eye, center)))
    self.loadViewportMatrix()

  def draw_arrays(self, polygon):
    if polygon == 'TRIANGLES':
      try:
        while True:
          self.triangle()
      except StopIteration:
        print('Done.')



  