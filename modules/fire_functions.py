import asyncio
import curses


async def fire(canvas, start_row, start_column, tics_per_sec, rows_speed=-0.4, columns_speed=0):
    FLASH_SECONDS = 0.2
    CORE_SECONDS = 1.6
    DISAPPEAR_SECONDS = 0.2
    FLIGHT_STEP_SECONDS = 0.2

    flash_tics = int(FLASH_SECONDS * tics_per_sec)
    core_tics = int(CORE_SECONDS * tics_per_sec)
    disappear_tics = int(DISAPPEAR_SECONDS * tics_per_sec)
    flight_step_tics = int(FLIGHT_STEP_SECONDS * tics_per_sec)

    row, column = start_row, start_column
    canvas.addstr(round(row), round(column), '*')
    for _ in range(flash_tics):
        await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    for _ in range(core_tics):
        await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), ' ')
    for _ in range(disappear_tics):
        await asyncio.sleep(0)

    row += rows_speed
    column += columns_speed
    symbol = '-' if columns_speed else '|'
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        for _ in range(flight_step_tics):
            await asyncio.sleep(0)

        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed
