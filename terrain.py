from ursina import Entity, Vec3, color
from config import block_size, chunk_size, base_height, default_color, gray_interval, districts, blocks
from events import on_mouse_enter_block, on_mouse_exit_block, on_right_click_block

terrain = Entity(model=None, collider=None)

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