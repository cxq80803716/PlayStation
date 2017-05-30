#coding:utf-8
import pygame,random,sys
from sys import exit
from pygame.locals import *
path = sys.argv[0]
image_path = './image/2048/'
background_picture = './image/2048/background.jpg'
pygame.init()

WIDTH = 480
HEIGHT = 580
SCORE_HIGHT = HEIGHT-WIDTH
CELLSIZE = 120
SIZE = 4
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
BACKGROND_PICTURE = pygame.image.load(background_picture).convert()

array = [[0 for i in range(SIZE)] for i in range(SIZE)]

BLOCK = [pygame.Surface((CELLSIZE, CELLSIZE)) for i in range(15)]
color = [
    (192,192,192),
    (211,211,211),
    (0,255,0),
    (255,105,180),
    (0,0,255),
    (255,255,0),
    (0,0,139),
    (119,136,153),
    (0,206,209),
    (0,128,128),
    (173,255,47),
    (255,250,205),
    (255,215,0),
    (255,250,240),
    (255,239,205)
]
for i in range(15):
    BLOCK[i].fill(color[i])
TIMES = SIZE*SIZE #还有多少个空地方 最开始有16个空
SCORE = 0
def main():
    while True:
        if runGame()==1:
            return
        if GAMEOVER():
            return

def runGame():
    global array,TIMES,SCORE,SCREEN,MOUSEIMAGE
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('2048')
    MOUSEIMAGE = pygame.image.load(image_path + 'guangbiao.png')
    icon = pygame.image.load(image_path + 'icon.jpg')
    pygame.display.set_icon(icon)
    array = [[0 for i in range(SIZE)] for i in range(SIZE)]
    TIMES = SIZE*SIZE #还有多少个空地方 最开始有16个空
    SCORE = 0
    create()
    create()
    showPanel()
    while True:
        SCREEN.blit(BACKGROND_PICTURE,(0,0))
        if gameOver():
            return
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 1
                else:
                    moveKey(event)
        showPanel()

def GAMEOVER():
    global SCORE
    gameoverFont = pygame.font.Font('./font/cabin.ttf', 100)
    gameSurf = gameoverFont.render('Game Over',True,(255,0,0))
    gameRect = gameSurf.get_rect()
    gameRect.center = (WIDTH/2,HEIGHT/2)

    Margin = pygame.Surface((WIDTH, CELLSIZE))
    Margin.fill((255,255,255))
    FONT1 = pygame.font.Font('./font/FZSTK.TTF', 30)
    pressKeySurf = FONT1.render(u'按ESC结束游戏/按R重新开始', True, (0,0,0))
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (WIDTH /2, HEIGHT - 60)

    while True:
        SCREEN.blit(BACKGROND_PICTURE,(0,0))
        SCREEN.blit(gameSurf,gameRect)
        SCREEN.blit(Margin,(0, HEIGHT-CELLSIZE))
        SCREEN.blit(pressKeySurf, pressKeyRect)
        (x,y) = pygame.mouse.get_pos()
        SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return 0
                elif event.key == K_ESCAPE:
                    return 1

        pygame.display.update()

def moveKey(e):
    global SCORE,TIMES #引用全局变量,如果要修改全局变量的值必须这么弄,不然SCORE会被认为是局部变量
    flag = False #标志整个图是否发生了变化,如果发生了变化就调用 create()
    if e.key == K_UP or e.key == K_w:
        for y in range(1,SIZE):
            for x in range(0,SIZE):
                if array[x][y] == 0: continue
                dispos = -1 # 标记位置 ,如果这个dispos一直为-1 ,那么证明y以上的所有位置都不会被y代替的位置,否则y1的位置将被y位置的元素代替
                for y1 in range(y-1,-1,-1):
                    if array[x][y1]!=0:
                        if array[x][y] == array[x][y1]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x][y1]
                            array[x][y1]*=2
                            array[x][y] = 0
                            TIMES+=1 #空位增加了
                        break #直接退出循环,该层已经不可能再往上走了
                    else:
                        dispos = y1
                if dispos is not -1:
                    flag = True
                    array[x][dispos] = array[x][y]
                    array[x][y] = 0
    if e.key == K_DOWN or e.key == K_s:
        for y in range(SIZE-1,-1,-1):
            for x in range(0,4):
                if array[x][y] == 0: continue
                dispos = -1
                for y1 in range(y+1,SIZE):
                    if array[x][y1]!=0:
                        if array[x][y] == array[x][y1]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x][y1]
                            array[x][y1]*=2
                            array[x][y] = 0
                            TIMES+=1 #空位增加了
                        break #直接退出循环,该层已经不可能再往上走了
                    else:
                        dispos = y1
                if dispos is not -1:
                    flag = True
                    array[x][dispos] = array[x][y]
                    array[x][y] = 0
    if e.key == K_a or e.key == K_LEFT:
        for y in range(0,SIZE):
            for x in range(1,SIZE):
                if array[x][y] == 0:continue
                dispos = -1
                for x1 in range(x-1,-1,-1):
                    if array[x1][y] !=0:
                        if array[x1][y]== array[x][y]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x1][y]
                            array[x1][y]*=2
                            array[x][y] = 0
                            TIMES+=1
                        break
                    else:
                        dispos = x1
                if dispos is not -1:
                    flag = True
                    array[dispos][y] = array[x][y]
                    array[x][y] = 0

    if e.key == K_d or e.key == K_RIGHT:
        for y in range(0,SIZE):
            for x in range(SIZE-1,-1,-1):
                if array[x][y] == 0:continue
                dispos = -1
                for x1 in range(x+1,SIZE):
                    if array[x1][y] !=0:
                        if array[x1][y]== array[x][y]:
                            flag = True
                            dispos = -1
                            SCORE += 2*array[x1][y]
                            array[x1][y]*=2
                            array[x][y] = 0
                            TIMES+=1
                        break
                    else:
                        dispos = x1
                if dispos is not -1:
                    flag = True
                    array[dispos][y] = array[x][y]
                    array[x][y] = 0
    if flag:
        create()
def create():
    flag = False # 直到某个空位置产生一个新的数 flag 才变成 0
    if TIMES>0:
        while not flag:
            x = random.randint(0,3)
            y = random.randint(0,3)
            #print x,y
            if array[x][y] == 0:
                if random.randint(0,3) == 0: #1/4的几率生成 4
                    array[x][y] = 4
                else:
                    array[x][y] = 2
                flag = True

def gameOver():
        for r in range(SIZE):
            for c in range(SIZE):
                if array[r][c] == 0:
                    return False
        for r in range(SIZE):
            for c in range(SIZE-1):
                if array[r][c] == array[r][c + 1]:
                    return False
        for r in range(SIZE-1):
            for c in range(SIZE):
                if array[r][c] == array[r + 1][c]:
                    return False
        return True

def showPanel():
    for i in range(SIZE):
        for j in range(SIZE):
            WHITE=(255,255,255)
            outerRect = pygame.Rect(CELLSIZE * i,CELLSIZE * j+100,CELLSIZE,CELLSIZE)
            pygame.draw.rect(SCREEN,WHITE,outerRect)
            innerRect = pygame.Rect(CELLSIZE * i+5,CELLSIZE * j+100+5,CELLSIZE-10,CELLSIZE-10)
            if array[i][j] != 0:
                t = array[i][j]
                num=0
                while t!=1:
                    num+=1
                    t/=2
                '''
                SCREEN.blit(BLOCK[num%14],(CELLSIZE * i, CELLSIZE * j+100))
                '''
                pygame.draw.rect(SCREEN,color[num%14],innerRect)
                Font = pygame.font.Font('./font/cabin.ttf', 80)
                map_text = Font.render(str(array[i][j]), True, (106, 90, 205))
                text_rect = map_text.get_rect()
                text_rect.center = (CELLSIZE * i + CELLSIZE / 2, CELLSIZE * j + CELLSIZE / 2+100)
                SCREEN.blit(map_text, text_rect)
            else:
                '''
                SCREEN.blit(BLOCK[0],(CELLSIZE * i, CELLSIZE * j+100))
                '''
                pygame.draw.rect(SCREEN,color[0],innerRect)
            #draw_grid()
    Font = pygame.font.Font('./font/cabin.ttf', 45)
    score_text = Font.render("Score: %s"%str(SCORE),True,(255,255,0))
    text_rect = map_text.get_rect()
    text_rect.center = (250, 70)
    SCREEN.blit(score_text, text_rect)
    (x,y) = pygame.mouse.get_pos()
    SCREEN.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
    pygame.display.update()

def draw_grid():
    color = (40,40,40)
    for x in range(0,WIDTH,CELLSIZE):
        pygame.draw.line(SCREEN,color,(x,100),(x,HEIGHT))
    for y in range(0,HEIGHT,CELLSIZE):
        pygame.draw.line(SCREEN,color,(0,y+100),(WIDTH,y+100))

if __name__ == '__main__':
    main()
