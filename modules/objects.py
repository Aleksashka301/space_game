import random

from modules.animations import fly_garbage, sleep
from modules.game_scenario import PHRASES, get_garbage_delay_tics


year = 1957


async def fill_orbit_with_garbage(canvas, frames_garbage, columns, coroutines):
    global year
    tics_year = 15
    frames = []

    for frame_file in frames_garbage:
        with open(frame_file, 'r') as file:
            frames.append(file.read())

    while True:
        update_info(canvas)
        if not get_garbage_delay_tics(year):
            year += 1
            await sleep(tics_year)
        else:
            garbage = fly_garbage(
                    canvas,
                    random.randint(1, columns),
                    random.choice(frames),
            )
            coroutines.append(garbage)

            year += 1
            await sleep(get_garbage_delay_tics(year))
        update_info(canvas)


def update_info(canvas):
    _, screen_width = canvas.getmaxyx()
    info_window = canvas.derwin(1, screen_width, 0, 0)

    if year in PHRASES:
        info_window.clear()
        info_window.addstr(0, 0, f'Год {year} - "{PHRASES[year]}"!')
        info_window.refresh()

