import asyncio
import curses
import random


SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


async def blink(canvas, row, column, symbol='*'):
    await asyncio.sleep(random.choice(range(3)))
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        await asyncio.sleep(2)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        await asyncio.sleep(0.5)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0.3)


async def fire(canvas, start_row, start_column, rows_speed=-0.4, columns_speed=0):
    row, column = start_row, start_column
    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0.1)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0.9)

    canvas.addstr(round(row), round(column), ' ')
    await asyncio.sleep(0.8)

    row += rows_speed
    column += columns_speed
    symbol = '-' if columns_speed else '|'
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0.1)

        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def draw_frame(canvas, start_row, start_column, text, negative=True):
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def animate_frames(canvas, ship_pos, frame_files):
    await asyncio.sleep(6)
    while True:
        row = ship_pos['row']
        col = ship_pos['col']

        for frame_path in frame_files:
            with open(frame_path, 'r') as file:
                image = file.read()

            draw_frame(canvas, row, col, image, negative=False)
            canvas.refresh()
            await asyncio.sleep(0.3)

            draw_frame(canvas, row, col, image, negative=True)
            canvas.refresh()


def read_controls(canvas):
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


async def update_position(canvas, ship_pos, frame_files):
    with open(frame_files[0], 'r') as file:
        image = file.read()

    ship_height, ship_width = get_frame_size(image)
    screen_height, screen_width = canvas.getmaxyx()

    while True:
        row, col, _ = read_controls(canvas)
        new_row = ship_pos['row'] + row
        new_col = ship_pos['col'] + col

        if 1 <= new_row <= screen_height - ship_height - 1:
            ship_pos['row'] = new_row

        if 1 <= new_col <= screen_width - ship_width - 1:
            ship_pos['col'] = new_col

        await asyncio.sleep(0.1)


def get_frame_size(text):
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])

    return rows, columns


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
        'row': 0,
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
    coroutine_ship_move = update_position(canvas, ship_pos, frame_files)

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


