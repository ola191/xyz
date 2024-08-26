from ursina import Color, Vec3
import time
from threading import Thread

from config import block_size

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
        original_y = block.position.y 
        current_height = block.scale.y

        for i in range(steps):
            factor = i / steps
            scale = start_size + (end_size - start_size) * factor
            color = interpolate_color(start_color, end_color, factor)
            block.scale = Vec3(block_size, scale, block_size)
            
            block.position = Vec3(block.position.x, original_y + (scale - current_height) / 2, block.position.z)
            block.color = color
            time.sleep(step_duration)

        block.scale = Vec3(block_size, end_size, block_size)
        block.position = Vec3(block.position.x, original_y + (end_size - current_height) / 2, block.position.z)
        block.color = end_color
    Thread(target=animation).start()


def animation_limit(block, start_color, warning_color, duration=0.75, blink_count=2):
    def animation():
        step_duration = duration / (blink_count * 2)
        original_color = block.color

        for _ in range(blink_count):
            block.color = warning_color
            time.sleep(step_duration)
            block.color = start_color
            time.sleep(step_duration)

        block.color = original_color
    Thread(target=animation).start()