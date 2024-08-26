from ursina import Text
from config import money, color, current_district_info

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