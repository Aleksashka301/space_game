import asyncio
import curses

from modules.explosion import explode
from modules.frames import draw_frame, get_frame_size
from modules.obstacles import Obstacle


obstacles = []
obstacles_in_last_collisions = []


async def blink(canvas, row, column, offset_tics, tics_per_sec, symbol='*'):
    SEC_DIM = 3.6
    SEC_NORMAL = 0.4
    SEC_BOLD = 0.8

    tics_dim = int(tics_per_sec * SEC_DIM)
    tics_normal = int(tics_per_sec * SEC_NORMAL)
    tics_bold = int(tics_per_sec * SEC_BOLD)

    await sleep(offset_tics)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(tics_dim)

        canvas.addstr(row, column, symbol)
        await sleep(tics_normal)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(tics_bold)

        canvas.addstr(row, column, symbol)
        await sleep(tics_normal)


async def fire(canvas, start_row, start_column, tics_per_sec, rows_speed=-0.4, columns_speed=0):
    global obstacles_in_last_collisions
    FLASH_SECONDS = 0.2
    CORE_SECONDS = 0.4
    DISAPPEAR_SECONDS = 0.2
    FLIGHT_STEP_SECONDS = 0.2

    flash_tics = int(FLASH_SECONDS * tics_per_sec)
    core_tics = int(CORE_SECONDS * tics_per_sec)
    disappear_tics = int(DISAPPEAR_SECONDS * tics_per_sec)
    flight_step_tics = int(FLIGHT_STEP_SECONDS * tics_per_sec)

    row, column = start_row, start_column
    canvas.addstr(round(row), round(column), '*')
    await sleep(flash_tics)

    canvas.addstr(round(row), round(column), 'O')
    await sleep(core_tics)

    canvas.addstr(round(row), round(column), ' ')
    await sleep(disappear_tics)

    row += rows_speed
    column += columns_speed
    symbol = '-' if columns_speed else '|'
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await sleep(flight_step_tics)

        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed

        for collider in obstacles:
            if collider.has_collision(row, column):
                obstacles_in_last_collisions.append(collider)
                obstacles.remove(collider)
                return collider


async def fly_garbage(canvas, column, garbage_frame, speed=0.1):
    rows_number, columns_number = canvas.getmaxyx()
    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0
    garbage_height, garbage_width = get_frame_size(garbage_frame)
    collider = Obstacle(
        row=row,
        column=column,
        rows_size=garbage_height,
        columns_size=garbage_width
    )

    global obstacles
    obstacles.append(collider)

    while row < rows_number:
        if collider in obstacles_in_last_collisions:
            obstacles_in_last_collisions.remove(collider)
            await explode(canvas, row + int(garbage_height / 2), column + int(garbage_width / 2))
            return

        collider.row = row
        collider.column = column
        draw_frame(canvas, row, column, garbage_frame, negative=False)

        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

    if collider in obstacles:
        obstacles.remove(collider)


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)
