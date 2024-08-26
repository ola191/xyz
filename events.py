from config import *
from ursina import Vec3
from ui import *
from animation import *


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

def upgrade_block(block, cost, increase_money_per_second, end_color, next_level):
    global money, money_per_second

    if money >= cost:
        x_start = (int(block.position.x) // chunk_size) * chunk_size
        z_start = (int(block.position.z) // chunk_size) * chunk_size
        block_position_str = f"{str(Vec3(block.position.x, base_height + 1, block.position.z))}"

        if districts[(x_start, z_start)]['maxHeight'] >= next_level:
            start_size = block.scale.y
            end_size = block_size * (next_level + 1)
            start_color = block.color

            animate_scale_and_color(block, start_size, end_size, start_color, end_color)
            money -= cost
            money_per_second += increase_money_per_second
            update_money_text()
            actualColor = end_color
            update_district(x_start, z_start, end_color)
            blocks[block_position_str]["level"] = next_level

def on_right_click_block(block):
    def handler():
        level_upgrades = [
            (100, 1, selected_color, 1),
            (200, 1.2, selected_color_b, 2),
            (300, 1.6, selected_color_c, 3),
            (400, 2.2, selected_color_d, 4),
            (500, 3, selected_color_e, 5),
            (600, 5, selected_color_f, 6)
        ]

        block_position_str = f"{str(Vec3(block.position.x, base_height + 1, block.position.z))}"
        current_level = blocks[block_position_str]["level"]

        if current_level < len(level_upgrades):
            cost, increase_money_per_second, end_color, next_level = level_upgrades[current_level]
            upgrade_block(block, cost, increase_money_per_second, end_color, next_level)
        else:
            animation_limit(block, selected_color_f, color.red)
        
    return handler
