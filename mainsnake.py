import os
import random
import sqlite3
import sys

import pygame
import time
from tkinter import Tk
pygame.init()
maxim = []
yellow = (255, 255, 102) # счёт
black = (0, 0, 0) # цвет змеи
red = (213, 50, 80) # проигрышь
green = (0, 255, 0) # еда
blue = (50, 153, 213) # поле
white = (255, 0, 0) # препятствия

root = Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
root.destroy()

dis = None
value = None
clock = pygame.time.Clock()

def load_image(name='head.png', color=(255, 255, 255)):
    fullname = os.path.join('Игра', name)
    if not os.path.isfile(fullname):
        print(f'file "{fullname}" not found')
        sys.exit()
    image = pygame.image.load(fullname)
    if color is not None:
        image = image.convert()
        if color == -1:
            color = image.get_at((0, 0))
        image.set_colorkey(color)
    else:
        image = image.convert_alpha()  # картинка будет прозрачной (png)
    return image
#function to check if a point lies in rectangle
def isIn(firstCorner=(0,0),secondCorner=(0,0),point=(0,0)):

   #assign values to variables
   x1,y1=firstCorner[0],firstCorner[1]
   x2,y2=secondCorner[0],secondCorner[1]

   x,y=point[0],point[1]
   #A point lies inside or not the rectangle
   #if and only if its x-coordinate lies
   #between the x-coordinate of the given bottom-right
   #and top-left coordinates of the rectangle
   #and y-coordinate lies between the y-coordinate of
   #the given bottom-right and top-left coordinates.
   if (x >= x1 and x <= x2 and y >= y1 and y <= y2) :
       return True
   #alternate case if coordinates are in reverse order
   elif(x >= x2 and x <= x1 and y >= y2 and y <= y1):
       return True

   else:
       return False


"""
snake_block = int(dis_width / 60)
snake_speed = 1"""

font_style = None
score_font = None


def Your_score(score, *text):
    global value
    if not text:
        value = score_font.render("Съедено: " + str(score), True, yellow)
        dis.blit(value, [0, 0])
    else:
        value = score_font.render(f'{score}{text[0]}', True, yellow)
        dis.blit(value, [0, 0])



def our_snake(snake_block, snake_list, *color):
    for x in snake_list:
        if not color:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
        else:
            pygame.draw.rect(dis, pygame.Color(color[0]),[x[0], x[1], snake_block, snake_block])


def message(msg, color, coords):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / coords[0], dis_height / coords[1]])


def gameLoop(prep, size, file):
    flag = True
    pause = False
    previous = ''
    game_over = False
    game_close = False
    foodx = round(random.randrange(5, dis_width - snake_block - 5) / 10.0) * 10
    foody = round(random.randrange(5,
                                   dis_height - snake_block - 5) / 10.0) * 10




    x1 = int(dis_width / 2)
    y1 = int(dis_height / 2)

    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    os.chdir('data')
    pygame.mixer.music.load('snake.mp3')
    os.chdir('..')
    pygame.mixer.music.play()
    while not game_over:
        while game_close == True:
            maxim.append(Length_of_snake - 1)
            dis.fill(blue)
            pygame.mixer.music.stop()
            Your_score('Рекорд: ', max(maxim))

            message("Игра закончена.", red, (3, 4))
            message(f"Всего съедено яблок: {Length_of_snake - 1}.", red, (3.5, 2.7))
            message(" Для начала новой игры нажмите C, для выхода в основное меню - Q.", red, (500, 2))
            #Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if file != 'None':
                            with sqlite3.connect(file) as con:
                                cur = con.cursor()
                                params = [int(i) for i in list((cur.execute(
                                    """SELECT * FROM datas""").fetchall())[0])]

                                params[0] = params[0] + 1 #
                                params[1] = params[1] + Length_of_snake - 1
                                if Length_of_snake - 1 > params[2]:
                                    params[2] = Length_of_snake - 1
                                params[3] = int(params[1] / params[0])
                                cur.execute("""DELETE FROM datas""")
                                con.commit()
                                cur.execute(
                                    """INSERT INTO datas VALUES ('{}', '{}', '{}', '{}')""".format(
                                        *params))
                                con.commit()
                            con.close()
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(prep, size, file)
                elif event.type == pygame.QUIT:
                    sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN and snake_speed and not pause:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                    if pause:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.type == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0
            elif event.type == pygame.KEYDOWN and snake_speed and pause:
                if event.key == pygame.K_SPACE:
                    pause = not pause
        if not pause:

            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)
            if not prep:
                prep_list = []

            elif prep and flag:
                flag = False
                prep_list = []
                for i in range(20):
                    a = random.choice([1, 2, 3])
                    x = round(random.randrange(5,
                                               dis_width - snake_block - 5) / 10.0) * 10
                    y = round(random.randrange(5,
                                               dis_height - value.get_height()) / 10.0) * 10
                    if x > value.get_width() or y > value.get_height():
                        prep_list.append((x, y))
            our_snake(snake_block, prep_list, white)

            if (x1 <= snake_block or x1 >= dis_width - snake_block):
                game_close = True
            if (y1 >= dis_height - snake_block or (y1 <= snake_block and x1 >= value.get_width())):
                game_close = True
            if (x1 <= value.get_width() and y1 <= value.get_height()):
                game_close = True
            if (x1, y1) in prep_list:
                game_close = True

            if True:
                lst = [(dis_width - snake_block, snake_block * i) for i in
                       range(dis_height // snake_block)]
                our_snake(snake_block, lst, white)
                lst = [(i * snake_block, dis_height - snake_block) for i in
                       range(dis_width // snake_block)]
                our_snake(snake_block, lst, white)

                lst = [(0, dis_height - snake_block * i) for i in
                       range(1 +
                           (int(dis_height - value.get_height())) // snake_block)]
                our_snake(snake_block, lst, white)

                lst = [(dis_width - snake_block * i, 0) for i in
                       range(1 +
                           (int(dis_width - value.get_width())) // snake_block)]
                our_snake(snake_block, lst, white)

                lst = [((snake_block * i), value.get_height() - 0.01 * size) for i in range(1 + (value.get_width() // snake_block))]
                our_snake(snake_block, lst, white)

                lst = [(value.get_width(), snake_block * i) for i
                       in range(2 + (value.get_height() // snake_block))]
                our_snake(snake_block, lst, white)
                if size == 1:
                    our_snake(snake_block, [(lst[-1][0], lst[-1][1] + snake_block // 1.3)], blue)
                elif size == 3:
                    our_snake(snake_block, [(lst[-1][0], lst[-1][1] + snake_block // 1.5)], blue)
                else:
                    our_snake(snake_block,
                              [(lst[-1][0], lst[-1][1] + snake_block // 12)],
                              blue)


            pygame.display.update()
            for i in prep_list:
                if abs(x1 - i[0]) <= 3 and abs(y1 - i[1]) <= 3:
                    game_close = True
                    break

            if abs(x1 - foodx) <= 3 and abs(y1 - foody) <= 3:
                foodx = round(random.randrange(5,
                                               dis_width - snake_block - 5) / 10.0) * 10
                foody = round(random.randrange(5,
                                               dis_height - snake_block - 5) / 10.0) * 10
                while ((foodx < value.get_width() + snake_block * 2 + 5) and (foodx < value.get_height() + snake_block * 2 + 5)) or (foodx, foody) in prep_list:
                    foodx = round(random.randrange(5, dis_width - snake_block - 5) / 10.0) * 10
                    foody = round(random.randrange(5,
                                                   dis_height - snake_block - 5) / 10.0) * 10
                Length_of_snake += 1
                pygame.display.update()

            clock.tick(8 * snake_speed)
        else:
            message('Пауза', red, (2.15, 2.5))
            pygame.display.update()




def main_snake(count_color: tuple, food_color: tuple, lose_color: tuple, snake_color: tuple, field_color: tuple, prep: bool, speed: int, size: int, prep_color: tuple, file: str, fonttype:str):
    global yellow, black, red, green, blue, white, dis, dis_width, dis_height, snake_block, snake_speed, font_style, score_font
    yellow = count_color
    black = snake_color
    red = lose_color
    green = food_color
    blue = field_color
    if speed == 1:
        snake_speed = 1.5
    elif speed == 2:
        snake_speed = 2
    elif speed == 3:
        snake_speed = 2.5
    else:
        snake_speed = 0

    if prep:
        white = prep_color
    if size != 1:
        dis_width = int((size / 1.5) * int(WIDTH / 2.66))
        dis_height = int((size / 1.5) * (int(HEIGHT / 2.16)))
    else:
        dis_width = int(WIDTH / 2.66)
        dis_height = (int(HEIGHT / 2.16))

    dis = pygame.display.set_mode((dis_width, dis_height))
    font_style = pygame.font.SysFont(fonttype, int(dis_height * 0.055))
    score_font = pygame.font.SysFont(fonttype, int(dis_height * 0.0675))
    snake_block = int(WIDTH / 192)
    pygame.display.set_caption('Змейка')
    gameLoop(prep, size, file)

if __name__ == '__main__':

    main_snake(count_color=(255, 255, 255),
               food_color=(0, 255, 255),
               lose_color=(81, 81, 255),
               snake_color=(0, 0, 0),
               field_color=(0, 255, 0),
               prep=True,
               speed=3,
               size=3,
           prep_color=(255, 0, 0),
            file='None')
#gameLoop(True)