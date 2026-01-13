import asyncio
import curses


async def blink(canvas, row, column, offset_tics, symbol='*'):
    for _ in range(offset_tics):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(36):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(4):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(8):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(4):
            await asyncio.sleep(0)
