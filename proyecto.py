from glFinal import *
from shaders import *
from obj import *

# ===============================================================
# Paula Camila Gonzalez Ortega - 18398
# ===============================================================

r = Render(1400, 980)
r.light = V3(0, 1, 1)

print("Espere un momento, se esta renderizando su bmp")
#Backgroun
t = Texture('./texts/mybg.bmp')
r.buffer = t.pixels
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
r.finish('mybmp.bmp')

#item 1
#sol
t = Texture('./texts/sunt.bmp')
r.active_texture = t
r.active_shader = myshader
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/sphere.obj', translate=(-0.8, 0.6, 0), scale=(0.35,0.5,0.5), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('mybmp.bmp')

#item 2
#arbol
t = Texture('./texts/cafe.bmp')
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/tree.obj', translate=(-0.5, -0.5, 0), scale=(0.03,0.03,0.03), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('mybmp.bmp')

#item 3
#cactus
t = Texture('./texts/cactus.bmp')
r.active_texture = t
r.active_shader = flat
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
#r.load1('./models/cactus1.obj', translate=(-0.8, -0.98, 0), scale=(0.1,0.15,0.15), rotate=(0.2, 1.25, -0.1))
r.load('./models/cactus1.obj', translate=(-0.8, -0.98, 0), scale=(0.1,0.15,0.15), rotate=(-0.02, -1.6, -0.1))
r.draw_arrays('TRIANGLES')
r.finish('mybmp.bmp')

#item 4
#fox
t = Texture('./texts/ft.bmp')
r.active_texture = t
#r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/fox.obj', translate=(-0.1, -0.9, 0), scale=(0.005,0.005,0.005), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('mybmp.bmp')


#item 5
#ave 1
t = Texture('./texts/cafe.bmp')
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/raven.obj', translate=(0, 0, 0), scale=(0.2,0.2,0.2), rotate=(0, -1, 0))
r.draw_arrays('TRIANGLES')
r.finish('mybmp.bmp')
#ave 2
t = Texture('./texts/negro.bmp')
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/raven.obj', translate=(-0.5, 0.5, 0), scale=(0.2,0.2,0.2), rotate=(0.5, -1, 0))
r.draw_arrays('TRIANGLES')
r.finish('mybmp.bmp')
