from ursina import *

from config import *

app = Ursina()

from terrain import *

from ui import * 

terrain = Entity(model=None, collider=None)

gray_blocks = generate_chunks()

camera.rotation_x = 30
camera.rotation_y = 0
camera.position = (0, 20, -20)

window.fullscreen = True

def update():
    if mouse.right:
        camera.rotation_x -= mouse.delta[1] * 1
        camera.rotation_y += mouse.delta[0] * 1
    if held_keys['w']:
        camera.position += camera.forward * 10 * time.dt
    if held_keys['s']:
        camera.position -= camera.forward * 10 * time.dt
    if held_keys['a']:  
        camera.position -= camera.right * 10 * time.dt
    if held_keys['d']:
        camera.position += camera.right * 10 * time.dt
    if held_keys['space']:
        camera.position += Vec3(0, 10 * time.dt, 0)
    if held_keys['left control']:
        camera.position -= Vec3(0, 10 * time.dt, 0)
        
    global money
    money += money_per_second * time.dt
    update_money_text()

app.run()
