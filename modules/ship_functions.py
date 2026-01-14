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
    frames = []

    for frame_file in frame_files:
        with open(frame_file, 'r') as file:
            frames.append(file.read())

    ship_height, ship_width = get_frame_size(frames[0])
    frame_index = 0
    animation_counter = 0

    while True:
        old_row, old_col = ship_pos['row'], ship_pos['col']
        rows_dir, cols_dir, _ = read_controls(canvas, key_codes)
        screen_height, screen_width = canvas.getmaxyx()
        new_row = old_row + rows_dir
        new_col = old_col + cols_dir
        tics_frame_change = 6

        draw_frame(canvas, old_row, old_col, frames[frame_index], negative=True)

        if 1 <= new_row <= screen_height - ship_height - 1:
            ship_pos['row'] = new_row

        if 1 <= new_col <= screen_width - ship_width - 1:
            ship_pos['col'] = new_col

        animation_counter += 1
        if animation_counter >= tics_frame_change:
            draw_frame(canvas, ship_pos['row'], ship_pos['col'], frames[frame_index], negative=True)

            frame_index = (frame_index + 1) % len(frames)
            animation_counter = 0

        draw_frame(canvas, ship_pos['row'], ship_pos['col'], frames[frame_index], negative=False)
        await asyncio.sleep(0)

