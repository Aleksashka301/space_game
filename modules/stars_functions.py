import asyncio
import curses


async def blink(canvas, row, column, offset_tics, tics_per_sec, symbol='*'):
    SEC_DIM = 3.6
    SEC_NORMAL = 0.4
    SEC_BOLD = 0.8

    tics_dim = int(tics_per_sec * SEC_DIM)
    tics_normal = int(tics_per_sec * SEC_NORMAL)
    tics_bold = int(tics_per_sec * SEC_BOLD)

    for _ in range(offset_tics):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(tics_dim):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(tics_normal):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(tics_bold):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(tics_normal):
            await asyncio.sleep(0)
