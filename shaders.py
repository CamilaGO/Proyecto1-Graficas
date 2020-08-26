from glFinal import *
from funcionesMath import *

def gourad(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tx, ty = kwargs['texture_coords']
  print('mi tx y ty', tx, ty)
  tcolor = render.active_texture.get_color(tx, ty)
  # normals
  nA, nB, nC = kwargs['varying_normals']

  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + u*iB + v*iC
  #intensity = 1
  r, g, b = tcolor[2] * intensity, tcolor[1] * intensity, tcolor[0] * intensity
  if r < 0:
    r = 0
  if r > 256:
    r = 255

  if b < 0:
    b = 0
  if b > 256:
    b = 255

  if g < 0:
    g = 0
  if g > 256:
    g = 255

  return color(
      int(r),
      int(g),
      int(b)
    )


import random

def fragment(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tx, ty = kwargs['texture_coords']

  # tcolor = render.active_texture.get_color(tx, ty)
  grey = int(ty * 256)
  tcolor = color(grey, 100, 100)
  #tcolor = kwargs['texture_color']
  # normals
  nA, nB, nC = kwargs['varying_normals']

  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + u*iB + v*iC

  if (intensity>0.85):
    intensity = 1
  elif (intensity>0.60):
    intensity = 0.80
  elif (intensity>0.45):
    intensity = 0.60
  elif (intensity>0.30):
    intensity = 0.45
  elif (intensity>0.15):
    intensity = 0.30
  else:
    intensity = 0

    return color(
        int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
        int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
        int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
      )



r = Render(1400, 980)
r.light = V3(0, 1, 1)

#Backgroun
t = Texture('./texts/mybg.bmp')
r.buffer = t.pixels
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
#r.load('./sphere.obj', translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 1))
#r.draw_arrays('TRIANGLES')
r.finish('out4.bmp')

#item 1
#arbol
t = Texture('./texts/cafe.bmp')
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load1('./models/tree.obj', translate=(-0.5, -0.5, 0), scale=(0.03,0.03,0.03), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('out3.bmp')

#item 2
#cactus
t = Texture('./texts/cactus.bmp')
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
#r.load1('./models/cactus1.obj', translate=(-0.8, -0.98, 0), scale=(0.1,0.15,0.15), rotate=(0.2, 1.25, -0.1))
r.load1('./models/cactus1.obj', translate=(-0.8, -0.98, 0), scale=(0.1,0.15,0.15), rotate=(-0.02, -1.6, -0.1))
r.draw_arrays('TRIANGLES')
r.finish('out3.bmp')

#item 3
#fox
t = Texture('./texts/ft.bmp')
r.active_texture = t
#r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load1('./models/fox.obj', translate=(-0.1, -0.9, 0), scale=(0.005,0.005,0.005), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('out4.bmp')