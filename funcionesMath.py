from collections import namedtuple
import struct
import numpy
""" implementacion de "vectores" para manejar menos variables en funciones y tener mejor orden de coordenadas
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])"""

class V3(object):
  def __init__(self, x, y = None, z = None):
    if (type(x) == numpy.matrix):
      self.x, self.y, self.z = x.tolist()[0]
    else:
      self.x = x
      self.y = y
      self.z = z

  def __repr__(self):
    return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

class V2(object):
  def __init__(self, x, y = None):
    if (type(x) == numpy.matrix):
      self.x, self.y = x.tolist()[0]
    else:
      self.x = x
      self.y = y

  def __repr__(self):
    return "V2(%s, %s)" % (self.x, self.y)

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
  bc = cross(
    V3(B.x - A.x, C.x - A.x, A.x - P.x), 
    V3(B.y - A.y, C.y - A.y, A.y - P.y)
  )

  if abs(bc.z) < 1:
    return -1, -1, -1   # no es un triangulo de verdad, no devuelve nada afuera

  # [cx cy cz] == [u v 1]

  u = bc.x/bc.z
  v = bc.y/bc.z
  w = 1 - (bc.x + bc.y)/bc.z

  return w, v, u

"""def allbarycentric(A, B, C, bbox_min, bbox_max):
  barytransform = numpy.linalg.inv([[A.x, B.x, C.x], [A.y,B.y,C.y], [1, 1, 1]])
  grid = numpy.mgrid[bbox_min.x:bbox_max.x, bbox_min.y:bbox_max.y].reshape(2,-1)
  grid = numpy.vstack((grid, numpy.ones((1, grid.shape[1]))))
  barycoords = numpy.dot(barytransform, grid)
  # barycoords = barycoords[:,numpy.all(barycoords>=0, axis=0)]
  barycoords = numpy.transpose(barycoords)
  return barycoords"""

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([b, g, r])