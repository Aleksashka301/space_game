import asyncio

from modules.animations import fire, obstacles
from modules.frames import draw_frame, get_frame_size
from modules.game_scenario import show_gameover
import modules.objects as year
from modules.physics import update_speed


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


async def ship_controller(canvas, ship_pos, frame_files, key_codes, coroutines):
    frames = []

    for frame_file in frame_files:
        with open(frame_file, 'r') as file:
            frames.append(file.read())

    ship_height, ship_width = get_frame_size(frames[0])
    frame_index = 0
    animation_counter = 0

    row_speed = 0.0
    col_speed = 0.0

    while True:
        old_row, old_col = ship_pos['row'], ship_pos['col']
        rows_dir, cols_dir, shot = read_controls(canvas, key_codes)

        if year.year >= 2020 and shot:
            coroutines.append(run_spaceship(canvas, old_col, ship_width, ship_pos))

        row_speed, col_speed = update_speed(
            row_speed=row_speed,
            column_speed=col_speed,
            rows_direction=rows_dir,
            columns_direction=cols_dir,
        )
        screen_height, screen_width = canvas.getmaxyx()
        new_row = old_row + row_speed
        new_col = old_col + col_speed

        draw_frame(canvas, old_row, old_col, frames[frame_index], negative=True)

        if 1 <= new_row <= screen_height - ship_height - 1:
            ship_pos['row'] = new_row

        if 1 <= new_col <= screen_width - ship_width - 1:
            ship_pos['col'] = new_col

        for collider in obstacles:
            if collider.has_collision(
                    ship_pos['row'], ship_pos['col'], obj_size_rows=ship_height, obj_size_columns=ship_width
            ):
                return show_gameover(canvas, screen_height, screen_width)

        animation_counter += 1
        tics_frame_change = 6
        if animation_counter >= tics_frame_change:
            draw_frame(canvas, ship_pos['row'], ship_pos['col'], frames[frame_index], negative=True)

            frame_index = (frame_index + 1) % len(frames)
            animation_counter = 0

        draw_frame(canvas, ship_pos['row'], ship_pos['col'], frames[frame_index], negative=False)
        await asyncio.sleep(0)


async def run_spaceship(canvas, old_col, ship_width, ship_pos):
    fire_col = old_col + (ship_width // 2)
    await fire(canvas, ship_pos['row'], fire_col, 10)
