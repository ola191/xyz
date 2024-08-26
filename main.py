from asyncio import sleep
from threading import Thread

from ursina import *

from config import *


app = Ursina()

from ui import * 

terrain = Entity(model=None, collider=None)



def update_money_text():
    money_text.text = f'${int(money)}'

def update_district_info(district_id):
    global current_district_info
    if district_id in districts:
        district = districts[district_id]
        if district['value'] > 200:
            district['maxHeight'] = 2
        if district['value'] > 1000:
            district['maxHeight'] = 3
        if district['value'] > 3000:
            district['maxHeight'] = 4
        if district['value'] > 6000:
            district['maxHeight'] = 5
        if district['value'] > 10000:
            district['maxHeight'] = 6

        current_district_info = f"District ID: {district['id']}\nValue: {district['value']}\nMax Height: {district['maxHeight']}\nPeople: {district['people']}"
        district_info_text.text = current_district_info
    else:
        district_info_text.text = ""

def create_chunk(x_start, z_start):
    chunk_id = (x_start, z_start) 
    
    districts[chunk_id] = {
        'id': chunk_id,
        'value': 0,
        'maxHeight': 1,
        'people': 0
    }
    
    chunk = Entity(model=None, collider=None)
    
    for x in range(chunk_size):
        for z in range(chunk_size):
            pos = Vec3(x + x_start, base_height, z + z_start)
            block = Entity(model='cube', color=color.white, scale=block_size, position=pos, collider='box')

            block.parent = chunk
            block.chunk_id = chunk_id
    
    chunk.combine()
    chunk.collider = 'mesh'
    chunk.texture = 'white_cube'
    chunk.parent = terrain

def on_mouse_enter_block(block):
    def handler():
        global actualColor 
        actualColor = block.color
        if block.color != selected_color and block.color != selected_color_b and block.color != selected_color_c and block.color != selected_color_d and block.color != selected_color_e and block.color != selected_color_f:  # Tylko jeśli blok nie jest wybrany
            block.color = highlight_color
            update_district_info(block.chunk_id)
    return handler

def on_mouse_exit_block(block):
    def handler():
        if block.color != selected_color and block.color != selected_color_b and block.color != selected_color_c and block.color != selected_color_d and block.color != selected_color_e and block.color != selected_color_f:  # Przywróć kolor, jeśli blok nie jest wybrany
            block.color = block.original_color
        update_district_info(None)
    return handler

def update_district(x_start, z_start, color):
    chunk_id = (x_start, z_start)
    if chunk_id in districts:
        if color == default_color:
            districts[chunk_id]['value'] += 20
            districts[chunk_id]['people'] += 100
        elif color == selected_color:
            districts[chunk_id]['value'] += 50
            districts[chunk_id]['people'] += 150
        elif color == selected_color_b:
            districts[chunk_id]['value'] += 150
            districts[chunk_id]['people'] += 200
        elif color == selected_color_c:
            districts[chunk_id]['value'] += 350
            districts[chunk_id]['people'] += 250
        elif color == selected_color_d:
            districts[chunk_id]['value'] += 550
            districts[chunk_id]['people'] += 300
        elif color == selected_color_e:
            districts[chunk_id]['value'] += 750
            districts[chunk_id]['people'] += 350
        elif color == selected_color_f:
            districts[chunk_id]['value'] += 1000
            districts[chunk_id]['people'] += 400

        update_district_info(chunk_id)

def interpolate_color(start_color, end_color, factor):
    r = start_color.r + (end_color.r - start_color.r) * factor
    g = start_color.g + (end_color.g - start_color.g) * factor
    b = start_color.b + (end_color.b - start_color.b) * factor
    a = start_color.a + (end_color.a - start_color.a) * factor
    return Color(r, g, b, a)

def animate_scale_and_color(block, start_size, end_size, start_color, end_color, duration=0.5):
    def animation():
        steps = 20 
        step_duration = duration / steps
        for i in range(steps):
            factor = i / steps
            scale = start_size + (end_size - start_size) * factor
            color = interpolate_color(start_color, end_color, factor)
            block.scale = Vec3(block_size, scale, block_size)
            block.color = color
            time.sleep(step_duration)
        block.scale = Vec3(block_size, end_size, block_size)
        block.color = end_color
    Thread(target=animation).start()

def on_right_click_block(block):
    def handler():
        global money, money_per_second, blocks
        
        x_start = (int(block.position.x) // chunk_size) * chunk_size
        z_start = (int(block.position.z) // chunk_size) * chunk_size
        block_position_str = f"{str(Vec3(block.position.x, base_height + 1, block.position.z))}"
        print(block_position_str)
        print(blocks)
        if block_position_str in blocks:

            if blocks[block_position_str]["level"] == 0:
                if money >= 100:
                    if districts[(x_start, z_start)]['maxHeight'] >= 1:
                        
                        block.model = 'models/house/house_packed.obj'
                        block.texture = 'models/house/house_packed_full.png'
                        
                        block.position = Vec3(block.position.x, block.position.y -0.5, block.position.z)
                        money -= 100
                        money_per_second += 1
                        update_money_text()
                        actualColor = selected_color
                        update_district(x_start, z_start, selected_color)
                        blocks[block_position_str]["level"] = 1

            elif blocks[block_position_str]["level"] == 1:
                if money >= 200:
                    if districts[(x_start, z_start)]['maxHeight'] >= 2:
                        
                        block.model = 'models/bigHouse/bighouse_packed.obj'
                        block.texture = 'models/bigHouse/bighouse_packed_full.png'
                        block.scale = Vec3(block_size, block_size, block_size)
                        block.position = Vec3(block.position.x, block.position.y, block.position.z)
                        
                        print("lvl next")
                        money -= 200
                        money_per_second += 1.2
                        update_money_text()
                        actualColor = selected_color_b
                        update_district(x_start, z_start, selected_color_b)
                        blocks[block_position_str]["level"] = 2

            elif blocks[block_position_str]["level"] == 2:
                if money >= 300:
                    if districts[(x_start, z_start)]['maxHeight'] >= 3:
                        end_color = selected_color_c
                        start_size = block_size * 3
                        end_size = block_size * 4
                        animate_scale_and_color(block, start_size, end_size, selected_color_b, end_color)
                        money -= 300
                        money_per_second += 1.6
                        update_money_text()
                        actualColor = selected_color_c
                        update_district(x_start, z_start, selected_color_c)
                        blocks[block_position_str]["level"] = 3

            elif blocks[block_position_str]["level"] == 3:
                if money >= 400:
                    if districts[(x_start, z_start)]['maxHeight'] >= 4:
                        end_color = selected_color_d
                        start_size = block_size * 4
                        end_size = block_size * 5
                        animate_scale_and_color(block, start_size, end_size, selected_color_c, end_color)
                        money -= 400
                        money_per_second += 2.2
                        update_money_text()
                        actualColor = selected_color_d
                        update_district(x_start, z_start, selected_color_d)
                        blocks[block_position_str]["level"] = 4

            elif blocks[block_position_str]["level"] == 4:
                if money >= 500:
                    if districts[(x_start, z_start)]['maxHeight'] >= 5:
                        end_color = selected_color_e
                        start_size = block_size * 5
                        end_size = block_size * 6
                        animate_scale_and_color(block, start_size, end_size, selected_color_d, end_color)
                        money -= 500
                        money_per_second += 3
                        update_money_text()
                        actualColor = selected_color_e
                        update_district(x_start, z_start, selected_color_e)
                        blocks[block_position_str]["level"] = 5

            elif blocks[block_position_str]["level"] == 5:
                if money >= 600:
                    if districts[(x_start, z_start)]['maxHeight'] >= 6:
                        end_color = selected_color_f
                        start_size = block_size * 6
                        end_size = block_size * 7
                        animate_scale_and_color(block, start_size, end_size, selected_color_e, end_color)
                        money -= 600
                        money_per_second += 5
                        update_money_text()
                        actualColor = selected_color_f
                        update_district(x_start, z_start, selected_color_f)

    return handler

def create_gray_blocks(x_start, z_start):
    gray_blocks = []
    center = chunk_size // 2 
    for dx in range(-1, 2): 
        for dz in range(-1, 2): 
            pos = Vec3(center + dx * gray_interval + x_start, base_height + 1, center + dz * gray_interval + z_start)
            block = Entity(model='cube', color=default_color, scale=block_size, position=pos, collider='box')
            
            global blocks
            blocks[f"{pos}"] = {
                'level': 0,
            }

            block.on_mouse_enter = on_mouse_enter_block(block)
            block.on_mouse_exit = on_mouse_exit_block(block)
            block.on_click = on_right_click_block(block) 
            block.original_color = default_color 
            block.chunk_id = (x_start, z_start)
            gray_blocks.append(block)  

    return gray_blocks

def generate_chunks():
    num_chunks = 3 
    gray_blocks = []
    
    for x in range(num_chunks):
        for z in range(num_chunks):
            create_chunk(x * chunk_size, z * chunk_size)
            gray_blocks.extend(create_gray_blocks(x * chunk_size, z * chunk_size))
    
    return gray_blocks

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
