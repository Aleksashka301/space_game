import asyncio
import curses
import random

from modules.stars_functions import blink
from modules.fire_functions import fire
from modules.ship_functions import animate_frames, update_position, get_frame_size


KEY_CODES = {
    'SPACE_KEY_CODE': 32,
    'LEFT_KEY_CODE': 260,
    'RIGHT_KEY_CODE': 261,
    'UP_KEY_CODE': 259,
    'DOWN_KEY_CODE': 258,
}


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.box()

    frame_files = [
        'frames/rocket_frame_1.txt',
        'frames/rocket_frame_2.txt',
    ]

    with open(frame_files[0], 'r') as file:
        image = file.read()

    row, column = canvas.getmaxyx()
    ship_height, ship_width = get_frame_size(image)
    symbols = '+*.:'
    coroutines_stars = []
    ship_pos = {
        'row': (row - ship_height) / 2,
        'col': (column - ship_width) / 2,
    }

    for star in range(100):
        coroutines_stars.append(
            blink(
                canvas,
                random.choice(range(1, row)),
                random.choice(range(1, column)),
                random.choice(symbols),
            )
        )

    coroutine_fire = fire(canvas, row-1, column/2)
    coroutine_ship = animate_frames(canvas, ship_pos, frame_files)
    coroutine_ship_move = update_position(canvas, ship_pos, frame_files, KEY_CODES)

    async def start_game():
        await asyncio.gather(
            *coroutines_stars,
            coroutine_fire,
            coroutine_ship,
            coroutine_ship_move,
        )

    asyncio.run(start_game())


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)


