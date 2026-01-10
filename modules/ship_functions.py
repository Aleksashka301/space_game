import asyncio


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
    await asyncio.sleep(10)
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


def read_controls(canvas, key_codes):
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == key_codes['UP_KEY_CODE']:
            rows_direction = -1

        if pressed_key_code == key_codes['DOWN_KEY_CODE']:
            rows_direction = 1

        if pressed_key_code == key_codes['RIGHT_KEY_CODE']:
            columns_direction = 1

        if pressed_key_code == key_codes['LEFT_KEY_CODE']:
            columns_direction = -1

        if pressed_key_code == key_codes['SPACE_KEY_CODE']:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


async def update_position(canvas, ship_pos, frame_files, key_codes):
    with open(frame_files[0], 'r') as file:
        image = file.read()

    ship_height, ship_width = get_frame_size(image)
    screen_height, screen_width = canvas.getmaxyx()

    while True:
        row, col, _ = read_controls(canvas, key_codes)
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