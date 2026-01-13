import asyncio
import curses


async def fire(canvas, start_row, start_column, rows_speed=-0.4, columns_speed=0):
    row, column = start_row, start_column
    canvas.addstr(round(row), round(column), '*')
    for _ in range(2):
        await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    for _ in range(16):
        await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), ' ')
    for _ in range(2):
        await asyncio.sleep(0)

    row += rows_speed
    column += columns_speed
    symbol = '-' if columns_speed else '|'
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        for _ in range(2):
            await asyncio.sleep(0)

        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed
