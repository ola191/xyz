from ursina import Text
from config import *

money_text = Text(
    text=f'${money}',
    position=(-0.85, 0.45),
    color=color.white,
    background=color.black,
    scale=2,
    anchor=('left', 'top')
)

district_info_text = Text(
    text=current_district_info,
    position=(-0.85, 0.35),
    color=color.white,
    background=color.black,
    scale=1.5,
    anchor=('left', 'top')
)

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