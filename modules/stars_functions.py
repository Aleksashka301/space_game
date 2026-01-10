import asyncio
import curses
import random


async def blink(canvas, row, column, symbol='*'):
    await asyncio.sleep(random.choice(range(3)))
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        await asyncio.sleep(1.8)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0.2)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        await asyncio.sleep(0.4)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0.2)
