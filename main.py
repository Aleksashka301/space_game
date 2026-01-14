import curses
import random
import time

from modules.stars_functions import blink
from modules.fire_functions import fire
from modules.ship_functions import get_frame_size, ship_controller


KEY_CODES = {
    'SPACE_KEY_CODE': 32,
    'LEFT_KEY_CODE': 260,
    'RIGHT_KEY_CODE': 261,
    'UP_KEY_CODE': 259,
    'DOWN_KEY_CODE': 258,
}
TIC_TIMEOUT = 0.05
TICS_PER_SECOND = 10


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
        'row': round((row - ship_height) / 2),
        'col': round((column - ship_width) / 2),
    }

    number_stars = 100
    max_tics_offset = 31
    for star in range(number_stars):
        coroutines_stars.append(
            blink(
                canvas,
                random.choice(range(1, row)),
                random.choice(range(1, column)),
                random.choice(range(1, max_tics_offset)),
                TICS_PER_SECOND,
                random.choice(symbols),
            )
        )

    coroutine_fire = fire(canvas, row-1, column/2, TICS_PER_SECOND)
    coroutine_ship = ship_controller(canvas, ship_pos, frame_files, KEY_CODES)

    coroutines = []
    coroutines.extend(coroutines_stars)
    coroutines.append(coroutine_fire)
    coroutines.append(coroutine_ship)

    while coroutines:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        time.sleep(TIC_TIMEOUT)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)


