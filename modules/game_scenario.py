from modules.frames import get_frame_size, draw_frame
import modules.global_var as global_var


PHRASES = {
    1957: "Первый искусственный спутник",
    1961: "Полёт Гагарина в космос",
    1969: "Армстронг высадился на луне",
    1971: "Первая орбитальная космическая станция 'Салют-1'",
    1981: "Полёт шатла 'Колумбия'",
    1998: "Начало строительства 'МКС'",
    2011: "Космический зонд Messenger отправляется к Меркурию",
    2020: "Получена плазменая пушка для уничтожения космического мусора",
}


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 80
    elif year < 1981:
        return 60
    elif year < 1995:
        return 40
    elif year < 2010:
        return 30
    elif year < 2020:
        return 20
    else:
        return 10


def show_gameover(canvas, screen_height, screen_width):
    with open('frames/text/game_over.txt', 'r') as file:
        text_gameover =  file.read()

    text_height, text_width = get_frame_size(text_gameover)
    row = (screen_height - text_height) // 2
    column = (screen_width - text_width) // 2

    draw_frame(canvas, row, column, text_gameover, negative=False)



