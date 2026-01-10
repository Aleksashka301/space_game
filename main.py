import asyncio
import curses
import random

from modules.stars_functions import blink
from modules.fire_functions import fire
from modules.ship_functions import animate_frames, update_position


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

    row, column = (10, 159)
    symbols = '+*.:'
    coroutines_stars = []
    frame_files = [
        'frames/rocket_frame_1.txt',
        'frames/rocket_frame_2.txt',
    ]
    ship_pos = {
        'row': 1,
        'col': 78
    }

    for star in range(60):
        coroutines_stars.append(
            blink(
                canvas,
                random.choice(range(1, row)),
                random.choice(range(1, column)),
                random.choice(symbols),
            )
        )

    coroutine_fire = fire(canvas, 10, 80)
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


