 #coding:utf-8
'''
贪吃蛇
author: yoghurt-lee
'''
import random ,pygame,sys
from pygame.locals import *
import time
image_path = './image/greedy-snake/'
show_picture = './image/greedy-snake/show.png'
background_picture = './image/greedy-snake/background.jpg'

FPS = 60
WIDTH = 640
HEIGHT = 480
CELLSIZE = 20
CELLWIDTH = int(WIDTH/CELLSIZE)
CELLHEIGHT = int(HEIGHT/CELLSIZE)

# 颜色数组
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
YELLOW = (255,255,0)
#背景颜色
BGCOLOR = BLACK
#贪吃蛇头部
HEAD = 0

RIGHT = [1,0]
LEFT = [-1,0]
UP = [0,-1]
DOWN = [0,1]
#初始化 ,屏幕,让动画基于时间运作
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
FPSCLOCK = pygame.time.Clock()
FONT = pygame.font.Font('./font/FZSTK.TTF',18)
BACKGROUND_PICTURE = pygame.image.load(background_picture).convert()
SHOW_PICTURE = pygame.image.load(show_picture).convert()
def main():
    global MOUSEIMAGE
    MOUSEIMAGE = pygame.image.load(image_path + 'guangbiao.png')
    pygame.display.set_caption('Greedy Snake')
    icon = pygame.image.load(image_path + 'icon.png')
    pygame.display.set_icon(icon)

    if showStartScreen():
        return

    while True:
        runGame()
        if gameOver():
            break


def gameOver():
    gameoverFont = pygame.font.Font('./font/cabin.ttf', 100)
    gameSurf = gameoverFont.render('Game Over',True,RED)
    gameRect = gameSurf.get_rect()
    gameRect.center = (WIDTH/2,HEIGHT/2)

    FONT1 = pygame.font.Font('./font/FZSTK.TTF', 30)
    pressKeySurf = FONT1.render(u'按ESC结束游戏/按R重新开始', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (WIDTH /2, HEIGHT - 60)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return 0
                elif event.key == K_ESCAPE:
                    return 1
        SCREEN.blit(BACKGROUND_PICTURE,(0,0))
        SCREEN.blit(gameSurf,gameRect)
        SCREEN.blit(pressKeySurf, pressKeyRect)
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
        pygame.display.update()

def runGame():
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5,CELLHEIGHT - 6)
    #最开始蛇长度为 3
    snake = [
        {'x':startx,'y': starty},
        {'x': startx - 1, 'y': starty},
        {'x': startx - 2, 'y': starty}
    ]
    direction = RIGHT
    apple = appleLocation()
    TIME = 0.1
    laststate = len(snake)
    while True:
        SCREEN.blit(BACKGROUND_PICTURE,(0,0))
        #draw_grid()
        if snakeDie(snake):
            return
        lastdirection = direction
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            elif event.type == KEYDOWN:
                key = event.key
                if lastdirection != RIGHT:
                    if (key ==K_a or key==K_LEFT) and direction!=RIGHT: #往左
                        direction = LEFT
                if lastdirection != LEFT:
                    if (key ==K_d or key==K_RIGHT) and direction!=LEFT: #往右
                        direction = RIGHT
                if lastdirection != DOWN:
                    if (key ==K_a or key==K_UP) and direction!=DOWN: #往上
                        direction = UP
                if lastdirection != UP:
                    if (key ==K_s or key==K_DOWN) and direction!=UP: #往下
                        direction = DOWN
                if key==K_ESCAPE:
                    exit()
        if snake[HEAD]['x']== apple['x'] and snake[HEAD]['y'] == apple['y']:
            apple = appleLocation()
        else:
            del snake[-1] #删除掉蛇的尾巴

        new_head = {'x':snake[HEAD]['x']+direction[0],'y':snake[HEAD]['y']+direction[1]}
        snake.insert(0,new_head)
        draw_snake(snake)
        draw_apple(apple)
        draw_score(10*(len(snake)-3))
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        nowstate = len(snake)
        if laststate!=nowstate:
            TIME-=0.005
            laststate = nowstate
        if TIME<0: TIME = 0
        time.sleep(TIME)

def draw_score(score):
    Font = pygame.font.Font('./font/cabin.ttf', 30)
    scoreSurf = Font.render('Score: %s' % (score), True, YELLOW)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WIDTH - 200, 10)
    SCREEN.blit(scoreSurf,scoreRect)

def draw_snake(snake):
    head = True
    for item in snake:
        x = item['x']*CELLSIZE
        y = item['y']*CELLSIZE
        snakeRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(SCREEN,DARKGREEN,snakeRect)
        if head:
            head = False
            innersankeRect = pygame.Rect(x+2,y+2,CELLSIZE-4,CELLSIZE-4)
            pygame.draw.rect(SCREEN,YELLOW,innersankeRect)
        else:
            innersankeRect = pygame.Rect(x+2,y+2,CELLSIZE-4,CELLSIZE-4)
            pygame.draw.rect(SCREEN,GREEN,innersankeRect)

def draw_apple(apple):
    x = apple['x']*CELLSIZE
    y = apple['y']*CELLSIZE
    appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(SCREEN,RED,appleRect)

def draw_grid():
    color = (40,40,40)
    for x in range(0,WIDTH,CELLSIZE):
        pygame.draw.line(SCREEN,color,(x,0),(x,HEIGHT))
    for y in range(0,HEIGHT,CELLSIZE):
        pygame.draw.line(SCREEN,color,(0,y),(WIDTH,y))

def snakeDie(snake):
    # 蛇撞墙或者撞到自己就挂了
    if snake[HEAD]['x'] == -1 or snake[HEAD]['x'] == CELLWIDTH or snake[HEAD]['y'] == -1 or snake[HEAD]['y'] == CELLHEIGHT:
        return True
    for item in snake[1:]:
        if snake[HEAD]['x'] == item['x'] and snake[HEAD]['y'] == item['y']:
            return True
    return False

def appleLocation():
    return {'x':random.randint(0,CELLWIDTH-1),'y':random.randint(0,CELLHEIGHT-1)}

def showStartScreen():
    titleFont = pygame.font.Font('./font/cabin.ttf', 55)
    titleSurf = titleFont.render('Greedy Snake!', True, RED)
    #参数一：显示的内容
    #参数二：是否开启抗锯齿，就是说True的话字体会比较平滑，不过相应的速度有一点点影响
    #参数三：字体颜色
    #参数四：字体背景颜色（可选）
    degrees = 0
    while True:
        SCREEN.blit(SHOW_PICTURE,(0,0))
        rotatedSurf = pygame.transform.rotate(titleSurf, degrees)
        rotatedRect = rotatedSurf.get_rect()
        rotatedRect.center = (WIDTH / 2, HEIGHT / 3)
        SCREEN.blit(rotatedSurf, rotatedRect)

        FONT1 = pygame.font.Font('./font/FZSTK.TTF', 30)
        pressKeySurf = FONT1.render(u'请按任意键开始游戏.', True, WHITE)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.center = (WIDTH /2, HEIGHT - 60)
        SCREEN.blit(pressKeySurf, pressKeyRect)

        flag = checkForKeyPress()
        if flag==2:
            return 1
        elif flag==3:
            return 0
        pygame.event.get()
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees += 3 #每次增加的角度


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        exit()
    keyUpEvents = pygame.event.get(KEYDOWN)
    if len(keyUpEvents) == 0:
        return 1
    if keyUpEvents[0].key == K_ESCAPE:
        return 2
    return 3

if __name__ == '__main__':
    main()
