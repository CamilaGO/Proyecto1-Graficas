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



r = Render(1000, 1000)
r.light = V3(0, 0, 1)

#Backgroun
#t = Texture('./back.bmp')
#r.buffer = t.pixels
#r.active_texture = t
#r.active_shader = gourad
#r.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
#r.load('./sphere.obj', translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 1))
#r.draw_arrays('TRIANGLES')
#r.finish('out2.bmp')

#item 1
#arbol
"""t = Texture('./cafe.bmp')
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load1('./tree.obj', translate=(0, -1, 0), scale=(0.05,0.05,0.05), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('mi_arbol.bmp')"""

#item 1
#arbol
t = Texture('./texts/snake_skin.bmp')
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load1('./models/sphere.obj', translate=(0, 0, 0), scale=(1,1,1), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('out2.bmp')