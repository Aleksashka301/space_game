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


def get_frame_size(text):
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])

    return rows, columns


async def ship_controller(canvas, ship_pos, frame_files, key_codes):
    for _ in range(100):
        await asyncio.sleep(0)

    with open(frame_files[0], 'r') as file:
        image = file.read()
    ship_height, ship_width = get_frame_size(image)

    while True:
        rows_dir, cols_dir, _ = read_controls(canvas, key_codes)
        screen_height, screen_width = canvas.getmaxyx()
        new_row = ship_pos['row'] + rows_dir
        new_col = ship_pos['col'] + cols_dir

        if 1 <= new_row <= screen_height - ship_height - 1:
            ship_pos['row'] = new_row

        if 1 <= new_col <= screen_width - ship_width - 1:
            ship_pos['col'] = new_col

        for frame in frame_files:
            with open(frame, 'r') as file:
                frame = file.read()

            draw_frame(canvas, ship_pos['row'], ship_pos['col'], frame, negative=False)
            canvas.refresh()
            for _ in range(3):
                await asyncio.sleep(0)

            draw_frame(canvas, ship_pos['row'], ship_pos['col'], frame, negative=True)
            canvas.refresh()
