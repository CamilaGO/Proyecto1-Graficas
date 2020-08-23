from glFinal import *

r = Render(1000, 1000)
t = Texture('./texture.bmp')
r.light = V3(0, 0, 1)

r.active_texture = t
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
# r.load('./models/model.obj', translate=(400, 300, 300), scale=(200, 200, 200), rotate=(0, 0, 0))
r.load('./fox.obj', translate=(0, 0, 0), scale=(0.01, 0.01, 0.01), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.finish('out1.bmp')
