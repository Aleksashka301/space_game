import curses
import random
import time

from modules.animations import blink
from modules.controls import ship_controller
from modules.frames import get_frame_size
from modules.global_var import KEY_CODES, TIC_TIMEOUT, TICS_PER_SECOND
from modules.objects import fill_orbit_with_garbage


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.box()

    frames_ship = [
        'frames/ship/rocket_frame_1.txt',
        'frames/ship/rocket_frame_2.txt',
    ]
    frames_garbage = [
        'frames/garbage/trash_large.txt',
        'frames/garbage/trash_small.txt',
        'frames/garbage/trash_xl.txt',
    ]

    with open(frames_ship[0], 'r') as file:
        ship_image = file.read()

    row, column = canvas.getmaxyx()
    ship_height, ship_width = get_frame_size(ship_image)
    symbols = '+*.:'
    coroutines_stars = []
    ship_pos = {
        'row': (row - ship_height) // 2,
        'col': (column - ship_width) // 2,
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

    coroutines = []
    coroutines.extend(coroutines_stars)
    coroutines.append(ship_controller(canvas, ship_pos, frames_ship, KEY_CODES, coroutines))
    coroutines.append(fill_orbit_with_garbage(canvas, frames_garbage, column, coroutines))

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


