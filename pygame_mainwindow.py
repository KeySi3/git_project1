import os
import pathlib
import sys
from tkinter import Tk
from shutil import copy2, copyfile
import pygame_menu
import pygame
from yadisk import yadisk
from result_worker import result_shower
from mainsnake import main_snake
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QColorDialog
from pygame_authorisation import main_auth
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog
from PyQt5.QtGui import QColor
from color_exui import color_show
speed = 1
prep = False
size = 1
menu = None
work_name = 'None'
password = None
registra = None

def sorting_with_registratio(lst):
    global speed, menu
    if not regist:
        datas = lst
        if speed == 1:
            return lst
        elif speed == 2:
            return [lst[1], lst[2], lst[0]]
        else:
            return [lst[2], lst[0], lst[1]]
    with sqlite3.connect(f'{work_name}.sqlite3') as con:
        cur = con.cursor()
        datas = [list(i) for i in
                 list(cur.execute('''SELECT * FROM settings''').fetchall())][0]
    if datas[-3] == '1':
        return lst
    elif datas[-3] == '2':
        return [lst[1], lst[2], lst[0]]
    else:
        return [lst[2], lst[0], lst[1]]

def change_prep(*args):
    global prep
    prep = not prep

def change_speed(*args):
    global speed, menu
    speed = menu.get_widget('speed', False).get_value()[0][1]


def sorting_size(lst):
    global  size
    if not regist:
        if size == 1:
            return lst
        elif size == 2:
            return [lst[1], lst[2], lst[0]]
        else:
            return [lst[2], lst[0], lst[1]]

    with sqlite3.connect(f'{work_name}.sqlite3') as con:
        cur = con.cursor()
        datas = [list(i) for i in
                 list(cur.execute('''SELECT * FROM settings''').fetchall())][0]
    if datas[-1] == '1':
        return lst
    elif datas[-3] == '2':
        return [lst[1], lst[2], lst[0]]
    else:
        return [lst[2], lst[0], lst[1]]

def prepya(lst:list):
    if not regist:
        if prep:
            return lst[::-1]
        return lst
    with sqlite3.connect(f'{work_name}.sqlite3') as con:
        cur = con.cursor()
        datas = [list(i) for i in
                 list(cur.execute('''SELECT * FROM settings''').fetchall())][0]
    if datas[-2] == '1':
        return lst[::-1]
    return lst

def draw_text(text, font, color, surface, x, y):  ## выводит текст
    obj = font.render(text, 1, color)
    rect = obj.get_rect()
    rect.topleft = (x, y)
    surface.blit(obj, rect)

def add_file(file):
    y = yadisk.YaDisk(token="AgAAAABJRyuzAAa6pTvMKnWv4Eeos3P4GVqkqmU")
    if os.path.isfile(file):
        if not y.is_file(os.path.basename(file)):
            y.upload(file, os.path.basename(file))
            return True, 'ok'
        return False, 'file_already_in_disk'
    return False, 'no_such_file'

def change_size(p):
    global size
    size = p



def download_file(file):
    y = yadisk.YaDisk(token="AgAAAABJRyuzAAa6pTvMKnWv4Eeos3P4GVqkqmU")
    if os.path.isfile(file + '.sqlite3'):
        return False, 'file_already_exists'
    if y.is_file(file + '.sqlite3'):
        try:
            y.download(file + '.sqlite3', file + '.sqlite3')
        except Exception:
            return False, 'no_internet'
        return True, 'ok'
    return False, 'no_such_file'


def delete_file(file):
    y = yadisk.YaDisk(token="AgAAAABJRyuzAAa6pTvMKnWv4Eeos3P4GVqkqmU")
    if y.is_file(file):
        y.remove(file, permanently=True)
        return True, 'ok'
    return False, 'no_such_file'


def load_image(name, color=None):
    fullname = os.path.join('Игра', name)
    if not os.path.isfile(fullname):
        print(f'file "{fullname}" not found')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def game():  ## загрузчик данных для игры
    global menu, prep
    if work_name != 'None':
        with sqlite3.connect(f'{work_name}.sqlite3') as con:
            cur = con.cursor()
            datas = [list(i) for i in list(cur.execute('''SELECT * FROM settings''').fetchall())]
            datas[0][1], datas[0][2], datas[0][3] = datas[0][1][3:-1], datas[0][2][3:-1], datas[0][3][3:-1]
            datas = datas[0]
            for i in range(len(datas)):
                if i == 1 or i == 2 or i == 3:
                    a = datas[i]
                    a = a.replace('(', '')
                    a = a.replace(')', '')
                    a = a.replace(',', '')
                    a = tuple([int(j) for j in a.split()])
                    datas[i] = a
        con.close()
        datas[-1], datas[-2], datas[-3] = int(datas[-1]), int(datas[-2]), int(datas[-3])
        print(datas)
        if menu != None:
            main_snake(count_color=datas[1],
                       food_color=datas[1],
                       lose_color=datas[1],
                       field_color=datas[3],
                       snake_color=datas[1],
                       prep=menu.get_widget('prep', False).get_value()[0][1],
                       speed=menu.get_widget('speed', False).get_value()[0][1],
                       size=menu.get_widget('size', False).get_value()[0][1],
                       prep_color=datas[2],
                       file=work_name + '.sqlite3',
                       fonttype=datas[0].lower())
        else:
            main_snake(count_color = datas[1],
            food_color = datas[1],
            lose_color = datas[1],
            field_color = datas[3],
            snake_color = datas[2],
            prep = datas[-2],
            speed = datas[-3],
            size = datas[-1],
            prep_color = datas[2],
            file = work_name + '.sqlite3',
            fonttype = datas[0].lower())

    else:
        try:
            main_snake(count_color=(255, 255, 255),
                       food_color=(0, 255, 255),
                       lose_color=(81, 81, 255),
                       snake_color=(0, 0, 0),
                       field_color=(0, 255, 0),
                       prep=menu.get_widget('prep', False).get_value()[0][1],
                       speed=menu.get_widget('speed', False).get_value()[0][1],
                       size=menu.get_widget('size', False).get_value()[0][1],
                       prep_color=(255, 0, 0),
                       file='None',
                       fonttype='arial')
        except Exception:
            main_snake(count_color=(255, 255, 255),
                       food_color=(0, 255, 255),
                       lose_color=(81, 81, 255),
                       snake_color=(0, 0, 0),
                       field_color=(0, 255, 0),
                       prep=prep,
                       speed=speed,
                       size=size,
                       prep_color=(255, 0, 0),
                       file='None',
                       fonttype='arial')
    root = Tk()
    root.withdraw()
    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((int(WIDTH / 2.66), int(HEIGHT / 2.16)))
    pygame.display.set_caption('Змейка')
    font = pygame.font.SysFont('Arial', 15)
    color = (186, 214, 177)
    regist = False
    flag = False
    menu1(regist)
    menu.set_title(f'Привет, {work_name}!') # устанавлвает название меню

def help_get_datas():
    if work_name != 'None':
        with sqlite3.connect(f'{work_name}.sqlite3') as con:
            cur = con.cursor()
            params = [int(i) for i in list((cur.execute("""SELECT * FROM datas""").fetchall())[0])]
            result_shower(params[1], params[0], params[2], params[3])
    else:
        error()

def make_copy():
    if not os.path.isdir('Змейка'):
        os.mkdir('Змейка')
    if work_name != 'None':
        copy2(work_name + '.sqlite3', 'Змейка')
    else:
        error()

def options1():
    global menu
    menu = pygame_menu.Menu(width=int(WIDTH / 2.66), height=int(HEIGHT / 2.16), title='Настойки', theme=pygame_menu.themes.THEME_GREEN)
    menu.add_label('Статистика аккаунта:', max_char=-1, font_size=40)
    menu.add_button('Посмотреть', help_get_datas)
    menu.add_label('Сложность игры:', max_char=-1, font_size=40)
    menu.add_selector('Скорость змейки ', sorting_with_registratio([('Медленная', 1), ('Стандартная', 2), ('Высокая', 3)]), selector_id='speed',onchange=change_speed)
    menu.add_selector('Размер карты ',
                      sorting_size([('Маленький', 1), ('Стандартный', 2), ('Большой', 3)]), selector_id='size')
    menu.add_selector('Препятствия ',
                      prepya([('Нет', 0), ('Есть', 1)]),
                      selector_id='prep', onchange=change_prep)
    """menu.add_label('Внешний вид:', max_char=-1, font_size=40)
    menu.add_button('Цвет поля', chose_color) #1
    menu.add_button('Цвет змейки', chose_color1)
    menu.add_button('Цвет текста', chose_color2)
    menu.add_selector('Тип шрифта ',
                      [('Arial', 1), ('Times', 2), ('Calibri', 3)])"""
    menu.add_button('Сохранить копию аккаунта на это устройство', make_copy)
    # onchange=error



    run = True
    while run:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)
        # image = load_image('Locker1.png')
        # screen.blit(image, (100, 100))
        pygame.display.update()

    menu1(regist)

def chose_color():
    if regist:
        return color_show()

    else:
        error()


def chose_color1():
    if regist:
        return color_show()

    else:
        error()


def chose_color2():
    if regist:
        return color_show()

    else:
        error()


def error(color=(186, 214, 177)):
    root = Tk()
    root.withdraw()
    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    message = "Эта функция доступна только для зарегистрированных пользователей" \
              "                Press Esc"
    menu = pygame_menu.Menu(width=int(screen.get_width() / 2.4), height=int(screen.get_height() / 1.25), title='Ошибка', theme=pygame_menu.themes.THEME_DARK)
    menu.add_label(message, max_char=-1, font_size=20)
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        if regist:
            sys.exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)
        pygame.display.update()


def registration():
    global registra, work_name , regist, speed, size, prep

    if not regist:
        if work_name == 'None':
            a = (main_auth())
            work_name = a
        if work_name != 'None':
            regist = True
            registra.set_title(f'Привет, {work_name}!')

            with sqlite3.connect(f'{work_name}.sqlite3') as con:
                cur = con.cursor()
                datas = [list(i) for i in list(
                    cur.execute('''SELECT * FROM settings''').fetchall())]
                datas[0][1], datas[0][2], datas[0][3] = datas[0][1][3:-1], \
                                                        datas[0][2][3:-1], \
                                                        datas[0][3][3:-1]
                datas = datas[0]
                for i in range(len(datas)):
                    if i == 1 or i == 2 or i == 3:
                        a = datas[i]
                        a = a.replace('(', '')
                        a = a.replace(')', '')
                        a = a.replace(',', '')
                        a = tuple([int(j) for j in a.split()])
                        datas[i] = a
            datas[-1], datas[-2], datas[-3] = int(datas[-1]), int(
                datas[-2]), int(datas[-3])
            speed = datas[-3]
            prep = datas[-2]
            size = datas[-1]


def change_diff():
    pass


def change_color():
    pass


def menu1(regist):
    global work_name, registra
    root = Tk()
    root.withdraw()
    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    if work_name == 'None':
        menu = pygame_menu.Menu(width=int(WIDTH / 2.66), height=int(HEIGHT / 2.16), title='Привет, незнакомец!', theme=pygame_menu.themes.THEME_GREEN)
    else:
        menu = pygame_menu.Menu(width=int(WIDTH / 2.66), height=int(HEIGHT / 2.16), title=f'Привет, {work_name}!', theme=pygame_menu.themes.THEME_GREEN)
    menu.add_button('Играть', game)
    menu.add_button('Авторизация', registration)
    menu.add_button('Настройки', options1)
    menu.add_button('Выйти', pygame_menu.events.EXIT)
    registra = menu
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                try:
                    with sqlite3.connect(f'{work_name}.sqlite3') as con:
                        cur = con.cursor()
                        datas = [list(i) for i in
                                 list(cur.execute(
                                     '''SELECT * FROM settings''').fetchall())][
                            0]
                        cur.execute("""DELETE FROM settings""")
                        con.commit()
                        datas = datas[:-3]
                        datas.extend([speed, int(prep), size])
                        font = datas[0]
                        background = datas[1]
                        text = datas[2]
                        button_color = datas[3]
                        cur.execute(
                            """INSERT INTO  settings VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
                                font, background, text, button_color, speed,
                                int(prep), size))
                        con.commit()
                    con.close()

                    (delete_file(f'{work_name}.sqlite3'))
                    (add_file(f'{work_name}.sqlite3'))
                    file = pathlib.Path(f'{work_name}.sqlite3')
                    file.unlink()
                    sys.exit()
                except Exception as e:

                    print(e.args)
                    sys.exit()
        if regist:
            pass
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()

    root = Tk()
    root.withdraw()
    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((int(WIDTH / 2.66), int(HEIGHT / 2.16)))
    pygame.display.set_caption('Змейка')
    gameIcon = pygame.image.load('icon.png')
    pygame.display.set_icon(gameIcon)
    font = pygame.font.SysFont('Arial', 15)
    color = (186, 214, 177)
    regist = False
    flag = False
    menu1(regist)
    pygame.quit()