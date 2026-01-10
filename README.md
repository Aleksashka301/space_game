# Space game

Скрипт запускает анимацию мерцания звёзд, после появляется летящий космический корабль. Кораблём можно управлять 
стрелками на клавиатуре.

## Запуск скрипта

### Скачайте скрипт
```commandline
git clone https://github.com/Aleksashka301/space_game
```

### Установка скрипта
Перейдите в папку с проектом
```
cd space_game
```

Установите виртуальное окружение
```python
python -m venv myvenv
```

Активируйте виртуальное окружение

windows
```
myvenv\Scripts\activate
```
linux
```
source myvenv/bin/activate
```

Установите зависимости
```python
pip install -r requirements.txt
```

### Запуск скрипта
Запуск
```python
python main.py
```
После запуска скрипта, в консоли начнут появляться и мигать звёзды, после произойдёт выстрел и затем появиться корабль.
