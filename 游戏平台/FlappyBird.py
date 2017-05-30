#coding: utf-8
'''
FlappyBird
author: cxq
email: 80803716@qq.com
'''
from pygame.locals import *
import pygame,random,time,sys
#背景音乐，背景图片，字体文件夹路径
bgm_path = "./bgm/flappy-bird/"
image_path = "./image/flappy-bird/"
font_path = "./font/"
#最大帧数
FPS = 60
#每隔2s生成新的水管
PIPETIME = 2 #s
#每次按SPACE小鸟上升的时间
BIRDFLYTIME = 1 #s
#小鸟上升速度，下降速度，水管移动的速度(x方向与y方向)
BirdFlySpeed = [0,15] #px/s
BirdFallSpeed = [0,15] #px/s
PipeMoveSpeed = [-200,0] #px/s
#游戏窗口大小
WINDOWWIDTH = 284 * 2
WINDOWHEIGHT = 512
#上下水管之间的高度
PASSHEIGHT = 135
#文本颜色和文本阴影颜色
TEXTCOLOR = (255, 255, 255)
TEXTSHADOWCOLOR = (185, 185, 185)
#获得文字对象以及对应的矩阵
def makeTextObjs(text, font, color):
  surf = font.render(text, True, color)
  return surf, surf.get_rect()
#程序终止
def terminate():
  pygame.quit()
  sys.exit()
#检查是否有按键事件，如果有则返回按下的键
def checkForKeyPress():
  for event in pygame.event.get():
    if event.type == QUIT :
        pygame.quit()
        sys.exit()
    if event.type == KEYDOWN:
        return event.key
  return None

#在窗口上显示文字（开始或者游戏结束页面）
def showTextScreen(text):
    #准备画上要显示的文字
    titleShadowSurf, titleShadowRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleShadowRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 100)

    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 103)

    pressKeySurf, pressKeyRect = makeTextObjs(u'按ESC结束游戏/按R开始游戏', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) )

    while True:
        #由于更换了鼠标光标，故每次都应更新背景，以免上一次的光标仍存在
        DISPLAYSURF.blit(BACKGROUND,(0,0))
        DISPLAYSURF.blit(BACKGROUND,(284,0))
        DISPLAYSURF.blit(titleShadowSurf, titleShadowRect)
        DISPLAYSURF.blit(titleSurf, titleRect)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
        #在鼠标的位置画上光标图
        (x,y) = pygame.mouse.get_pos()
        DISPLAYSURF.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
        #检测是否有按键事件
        press = checkForKeyPress()
        #如果用户按下esc则返回选择游戏界面，按下R则重新开始游戏
        if press == K_ESCAPE:
            return False
        elif press == K_r:
            return True
        #更新画布
        pygame.display.update()
        #每次循环都调用可以设置最高帧率，以免占用过多CPU
        FPSCLOCK.tick(FPS)
#检测小鸟是否在水管所形成的的矩形中（所谓的矩形就是上下两根水管所在的一个小竖矩形，从屏幕最上到屏幕最下）
def check_in_pipe(bird,pipe):
    if bird.x+bird.images[0].get_width()/2 < pipe.x - pipe.images[0].get_width()/2:
        return False
    if bird.x-bird.images[0].get_width()/2 > pipe.x + pipe.images[0].get_width()/2:
        return False
    return True
#小鸟是否在一个合法的位置（不能撞到边界或者水管）
def isValidPosition(pipes,bird):
    x=bird.x
    y=bird.y
    #是否撞到边界
    if(y-bird.images[0].get_height()/2 < 0 or y+bird.images[0].get_height()/2 > WINDOWHEIGHT):
        return False
    #是否撞到某一根水管
    for pipe in pipes:
        if check_in_pipe(bird,pipe):
            if y-bird.images[0].get_height()/2 < pipe.topy + pipe.images[0].get_height()/2:
                return False
            elif y + bird.images[0].get_height()/2 > pipe.bottomy - pipe.images[0].get_height()/2:
                return False
    return True

#小鸟对象
class Bird(object):
    def __init__(self,x,y,speed,bird_images):
        #小鸟中心坐标
        self.x = x
        self.y = y
        self.images = bird_images #小鸟照片，分为两张，相互切换来展示飞行的效果
        self.fall_speed = speed#小鸟下降的速度
        self.destination = [self.x,self.y] #每次按下SPACE给小鸟设定一个目标地点，小鸟会往这个目标移动
#水管对象
class Pipe(object):
    def __init__(self,pipe_x,toppipe_mid_y,pipe_image):
        #这里同时生成一组水管，所谓的一组指的是上下两根水管
        #两根水管都用的同一个x坐标，toppipe_mid_y是上面水管的中点y坐标
        self.x = pipe_x
        self.topy = toppipe_mid_y
        #下面水管的中心y坐标是上面水管+上面水管的一半高度+水管中间高度+下面水管的一半高度
        #我用的图片上下水管高度均相同
        self.bottomy = toppipe_mid_y + pipe_image[0].get_height() + PASSHEIGHT
        #这个图片保存着上下水管两张图片，区别在于一个水管头在下，一个在上
        self.images = pipe_image
#把所有内容画上去
def DrawTheWorld(bird,pipes,score):
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    DISPLAYSURF.blit(BACKGROUND,(284,0))
    DISPLAYSURF.blit(bird.images[random.randint(0,1)],(bird.x - bird.images[0].get_width()/2,bird.y - bird.images[0].get_height()/2))
    for pipe in pipes:
        DISPLAYSURF.blit(pipe.images[0],(pipe.x - pipe.images[0].get_width()/2,pipe.topy - pipe.images[0].get_height()/2))
        DISPLAYSURF.blit(pipe.images[1],(pipe.x - pipe.images[0].get_width()/2,pipe.bottomy - pipe.images[0].get_height()/2))
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.center = (WINDOWWIDTH/2, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def runGame():
    #加载需要的图片
    bird_wing_up_image = pygame.image.load(image_path + 'bird_wing_up.png')
    bird_wing_down_image = pygame.image.load(image_path + 'bird_wing_down.png')
    top_pipe_image = pygame.image.load(image_path + 'toppipe.png')
    down_pipe_image = pygame.image.load(image_path + 'downpipe.png')
    bird = Bird(50,WINDOWHEIGHT/2,BirdFallSpeed,[bird_wing_up_image,bird_wing_down_image])
    #最后一次生成水管的时间，水管最后一次移动的时间，小鸟最后一次起飞的时间（也就是用户按下SPACE时）
    #最后一次小鸟掉落的时间，这四个参数用来控制时间，不同电脑帧率不同，为了让不同电脑都看到一样的效果
    #则需要每次更新距离都根据经过的时间来计算（好的电脑刷新一次所需时间比较短）
    LastPipeTime = time.time()
    LastPipeMoveTime = time.time()
    LastBirdFlyTime = time.time()
    LastBirdDwonTime = time.time()
    #当前存在的所有水管
    pipes = []
    score = 0
    #一个标记变量，标记当前小鸟是否在水管之间
    IsInPipe = False
    #如果小鸟在水管之间，记录一下是哪根水管
    NowInPipe = None
    #小鸟是否飞行状态（用户按下SPACE后的1s内）
    IsBirdFly = False
    while True: #game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                #用户按下ESC则返回游戏大厅，因为下面游戏结束返回的是分数，分数最少为0
                if event.key == K_ESCAPE:
                    return -1
                #用户按下r重新开始
                elif event.key == K_r:
                    return score
                #p暂停，记得暂停结束时更新一下四个时间
                elif event.key == K_p:
                    #Pausing the game
                    showTextScreen('Paused')
                    LastPipeTime = time.time()
                    LastBirdFlyTime = time.time()
                    LastBirdDwonTime = time.time()
                    LastPipeMoveTime = time.time()
            #鼠标左键单击或者用户按下空格，上键，回车时小鸟起飞
            if event.type == MOUSEBUTTONDOWN or (event.type
            == KEYDOWN and event.key in (K_SPACE,K_UP,K_RETURN)):
                #起飞时播放音效
                pygame.mixer_music.load(WINGBGM)
                pygame.mixer.music.play()
                #小鸟处于飞行状态
                IsBirdFly = True
                LastBirdFlyTime = time.time()
                bird.destination = [bird.x,bird.y-80.0]
        #如果小鸟处于飞行状态则向上移动
        if IsBirdFly:
            if bird.y <= bird.destination[1]+1.0:
                #已飞行了指定时间
                IsBirdFly = False
                LastBirdDwonTime = time.time()
            else:
                #小鸟向目标移动
                direction = [bird.destination[0] - bird.x,bird.destination[1] - bird.y]
                bird.x += (time.time() - LastBirdFlyTime) * direction[0] * BirdFlySpeed[0]
                bird.y += (time.time() - LastBirdFlyTime) * direction[1] * BirdFlySpeed[1]
                LastBirdFlyTime = time.time()
        #不处于飞行状态则掉落
        else:
            bird.x += (time.time() - LastBirdDwonTime) * bird.fall_speed[0]
            bird.y += (time.time() - LastBirdDwonTime) * bird.fall_speed[1]
        #水管移动
        for pipe in pipes:
            pipe.x += (time.time() - LastPipeMoveTime) * PipeMoveSpeed[0]
        LastPipeMoveTime = time.time()
        #检查上一次生成水管至今知否已过了水管生成间隔时间
        if time.time() - LastPipeTime > PIPETIME:
            pipe = Pipe(WINDOWWIDTH + top_pipe_image.get_width()/2, random.randint(-200,200),[top_pipe_image,down_pipe_image])
            pipes.append(pipe)
            LastPipeTime = time.time()
        #如果水管已经移动到最左端，从lsit中删除该组水管
        if len(pipes) > 0 and pipes[0].x + pipe.images[0].get_width()/2 < 0:
            del pipes[0]
        #水管位置是否合法
        if not isValidPosition(pipes,bird):
            pygame.mixer_music.load(HITBGM)
            pygame.mixer.music.play()
            return score
        #检查小鸟此时是否在两根水管之间
        if not IsInPipe:
            for pipe in pipes:
                if check_in_pipe(bird,pipe):
                    IsInPipe = True
                    NowInPipe = pipe
                    break
        #小鸟之前在水管之间，现在离开了水管，则更改标记并且分数+1
        if IsInPipe and not check_in_pipe(bird,NowInPipe):
            IsInPipe = False
            score +=1
            NowInPipe = None
        #draw the world
        DrawTheWorld(bird,pipes,score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def main():
    global FPSCLOCK,DISPLAYSURF,BACKGROUND,GAMEBACKGROUND,BASICFONT,BIGFONT,MOUSEIMAGE
    global HITBGM,WINGBGM
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    #小鸟飞行和撞击音效
    HITBGM = bgm_path + 'sfx_hit.ogg'
    WINGBGM = bgm_path + 'sfx_wing.ogg'
    BACKGROUND = pygame.image.load(image_path + 'background.png')
    MOUSEIMAGE = pygame.image.load(image_path + 'guangbiao.png')
    #窗口图标
    icon = pygame.image.load(image_path + 'icon.png')
    pygame.display.set_icon(icon)
    #小字体和大字体
    BASICFONT = pygame.font.Font(font_path + 'FZSTK.TTF', 30)
    BIGFONT = pygame.font.Font(font_path + 'FreeSansBold.ttf', 50)
    #标题
    pygame.display.set_caption('Flappy Bird')
    if showTextScreen('Flappy Bird') == False:
        return
    while True:
        GAMEBACKGROUND = pygame.image.load(image_path + 'background.png')
        score = runGame()
        if score == -1:
            return
        if showTextScreen('Game Over!Score: %i' % score) == False:
            return

if __name__ == '__main__':
    main()
