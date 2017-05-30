#coding: utf-8
import random,time,pygame,sys
from pygame.locals import *
'''
俄罗斯方块
author: cxq
email: 80803716@qq.com
'''
#文件路径
bgm_path = "./bgm/tetris/"
image_path = "./image/tetris/"
font_path = "./font/"
#帧率
FPS = 60
#窗口大小
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
#每一个格子的边长（一个图形由多个格子组成，格子是一个正方形）
BOXSIZE = 20
#游戏区域叫做board，长宽都指的格子的数量，比如下面实际的大小是200*400
BOARDWIDTH = 10
BOARDHEIGHT = 20
#不是方块则为.，一行都不是.则表示此行被方块填满可以消除了
BLANK = '.'
#左右和向下移动的频率
MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1
#XMARGIN是屏幕最坐标到
XMARGIN = int((WINDOWWIDTH-BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) -5

#RGB
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = ( 0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = ( 0, 155, 0)
LIGHTGREEN = ( 20, 175, 20)
BLUE = ( 0, 0, 155)
LIGHTBLUE = ( 20, 20, 175)
YELLOW = (155,155, 0)
LIGHTYELLOW = (175, 175, 20)
#看名字，意义自明
BORDERCOLOR = BLUE
BGCOLOR = BLACK
BOARDCOLOR = WHITE
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE,GREEN,RED,YELLOW)
LIGHTCOLORS = (LIGHTBLUE,LIGHTGREEN,LIGHTRED,LIGHTYELLOW)
#断言，保证两种颜色成对出现
assert len(COLORS) == len(LIGHTCOLORS)
#任何一个图案都由5*5的方块组成
TEMPLATEHEIGHT = 5
TEMPLATEWIDTH = 5
#各个图案的样子，0表示方块
S_SHAPE_TEMPLATE = [['.....',
            '.....',
            '..00.',
            '.00..',
            '.....'],
            ['.....',
            '..O..',
            '..OO.',
            '...O.',
            '.....']]

Z_SHAPE_TEMPLATE = [['.....',
            '.....',
            '.OO..',
            '..OO.',
            '.....'],
            ['.....',
            '..O..',
            '.OO..',
            '.O...',
            '.....']]

I_SHAPE_TEMPLATE = [['..O..',
            '..O..',
            '..O..',
            '..O..',
            '.....'],
            ['.....',
            '.....',
            'OOOO.',
            '.....',
            '.....']]

O_SHAPE_TEMPLATE = [['.....',
            '.....',
            '.OO..',
            '.OO..',
            '.....']]

J_SHAPE_TEMPLATE = [['.....',
           '.O...',
           '.OOO.',
           '.....',
           '.....'],
          ['.....',
           '..OO.',
           '..O..',
           '..O..',
           '.....'],
          ['.....',
           '.....',
           '.OOO.',
           '...O.',
           '.....'],
          ['.....',
           '..O..',
           '..O..',
           '.OO..',
           '.....']]

L_SHAPE_TEMPLATE = [['.....',
           '...O.',
           '.OOO.',
           '.....',
           '.....'],
          ['.....',
           '..O..',
           '..O..',
           '..OO.',
           '.....'],
          ['.....',
           '.....',
           '.OOO.',
           '.O...',
           '.....'],
          ['.....',
           '.OO..',
           '..O..',
           '..O..',
           '.....']]

T_SHAPE_TEMPLATE = [['.....',
           '..O..',
           '.OOO.',
           '.....',
           '.....'],
          ['.....',
           '..O..',
           '..OO.',
           '..O..',
           '.....'],
          ['.....',
           '.....',
           '.OOO.',
           '..O..',
           '.....'],
          ['.....',
           '..O..',
           '.OO..',
           '..O..',
           '.....']]
PIECES = {'S':S_SHAPE_TEMPLATE,
        'Z':Z_SHAPE_TEMPLATE,
        'J': J_SHAPE_TEMPLATE,
        'L': L_SHAPE_TEMPLATE,
        'I': I_SHAPE_TEMPLATE,
        'O': O_SHAPE_TEMPLATE,
        'T': T_SHAPE_TEMPLATE}
def makeTextObjs(text, font, color):
    #获得文字对象和矩形
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def checkForKeyPress():
    #检查是否有按键事件
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            return event.key
    return None

def showTextScreen(text):
  #显示文字
  titleShadowSurf, titleShadowRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
  titleShadowRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)-50)

  titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
  titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 53)

  pressKeySurf, pressKeyRect = makeTextObjs(u'按ESC结束游戏/按任意键开始游戏', BASICFONT, TEXTCOLOR)
  pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 80)

  while True:
    #显示背景图，文字
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    DISPLAYSURF.blit(titleShadowSurf, titleShadowRect)
    DISPLAYSURF.blit(titleSurf, titleRect)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    #用光标图片替换原鼠标，记得要先隐藏原有光标
    (x,y) = pygame.mouse.get_pos()
    DISPLAYSURF.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
    press = checkForKeyPress()
    if press == K_ESCAPE:
        return False
    elif press != None:
        return True
    pygame.display.update()
    #每次循环都调用可以设置最高帧率
    FPSCLOCK.tick(FPS)

def calculateLevelAndFallFreq(score):
  #计算分数，每10分增加下落频率
  level = int(score / 10) + 1
  fallFreq = 0.27 - (level * 0.02)
  return level, fallFreq

def getNewPiece():
  # 获得一个新的随机方块
  shape = random.choice(list(PIECES.keys()))
  newPiece = {'shape': shape,
        'rotation': random.randint(0, len(PIECES[shape]) - 1),
        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
        'y': -2, #起始位置
        'color': random.randint(0, len(COLORS)-1)}
  return newPiece


def addToBoard(board, piece):
  # 将所有方块画在board上
  for x in range(TEMPLATEWIDTH):
    for y in range(TEMPLATEHEIGHT):
      if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
        board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
  # 获得一个新的board
  board = []
  for i in range(BOARDWIDTH):
    board.append([BLANK] * BOARDHEIGHT)
  return board


def isOnBoard(x, y):
  #是否在board里
  return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
  #是否在一个合法的位置
  for x in range(TEMPLATEWIDTH):
    for y in range(TEMPLATEHEIGHT):
      isAboveBoard = (y + piece['y'] + adjY) < 0
      if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
        continue
      if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
        return False
      if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
        return False
  return True

def isCompleteLine(board, y):
  #是否一行都填满了方格
  for x in range(BOARDWIDTH):
    if board[x][y] == BLANK:
      return False
  return True


def removeCompleteLines(board):
  #一行被填满时移除
  numLinesRemoved = 0
  y = BOARDHEIGHT - 1
  while y >= 0:
    if isCompleteLine(board, y):
      for pullDownY in range(y, 0, -1):
        for x in range(BOARDWIDTH):
          board[x][pullDownY] = board[x][pullDownY-1]
      # Set very top line to blank.
      for x in range(BOARDWIDTH):
        board[x][0] = BLANK
      numLinesRemoved += 1
    else:
      y -= 1
  return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
  # 把相对坐标转换成真正的坐标（board中的1是20像素）
  return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
  #画方块
  if color == BLANK:
    return
  if pixelx == None and pixely == None:
    pixelx, pixely = convertToPixelCoords(boxx, boxy)
  pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
  pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
  DISPLAYSURF.blit(GAMEBACKGROUND,(0,0))
  pygame.draw.line(DISPLAYSURF,BOARDCOLOR,(XMARGIN,TOPMARGIN),(XMARGIN + BOXSIZE*BOARDWIDTH,TOPMARGIN),5)
  pygame.draw.line(DISPLAYSURF,BOARDCOLOR,(XMARGIN,TOPMARGIN),(XMARGIN,TOPMARGIN + BOXSIZE*BOARDHEIGHT),5)
  pygame.draw.line(DISPLAYSURF,BOARDCOLOR,(XMARGIN + BOXSIZE*BOARDWIDTH,TOPMARGIN),(XMARGIN + BOXSIZE*BOARDWIDTH,TOPMARGIN + BOXSIZE*BOARDHEIGHT),5)
  pygame.draw.line(DISPLAYSURF,BOARDCOLOR,(XMARGIN,TOPMARGIN + BOXSIZE*BOARDHEIGHT),(XMARGIN + BOXSIZE*BOARDWIDTH,TOPMARGIN + BOXSIZE*BOARDHEIGHT),5)
  #画board
  for x in range(BOARDWIDTH):
    for y in range(BOARDHEIGHT):
      drawBox(x, y, board[x][y])

def drawStatus(score, level):
  # 画分数
  scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
  scoreRect = scoreSurf.get_rect()
  scoreRect.topleft = (WINDOWWIDTH - 150, 20)
  DISPLAYSURF.blit(scoreSurf, scoreRect)

  #画等级
  levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
  levelRect = levelSurf.get_rect()
  levelRect.topleft = (WINDOWWIDTH - 150, 50)
  DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
  shapeToDraw = PIECES[piece['shape']][piece['rotation']]
  if pixelx == None and pixely == None:
    #转换成真正坐标
    pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

  # 画上一个图形里的所有方块
  for x in range(TEMPLATEWIDTH):
    for y in range(TEMPLATEHEIGHT):
      if shapeToDraw[y][x] != BLANK:
        drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
  # 写上next
  nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
  nextRect = nextSurf.get_rect()
  nextRect.topleft = (WINDOWWIDTH - 150, 80)
  DISPLAYSURF.blit(nextSurf, nextRect)
  # 画下一个图形
  drawPiece(piece, pixelx=WINDOWWIDTH-150, pixely=100)

def runGame():
    global GAMEBACKGROUND
    #获得一个board
    board = getBlankBoard()
    lastMoveDownTime = time.time() # 最后一次加速下落的时间
    lastFallTime = time.time() # 最后一次自然掉落的时间
    lastMoveSidewaysTime = time.time() # 最后一次左右移动的时间
    #是否按下了下，左，右键
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    level,fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: #游戏循环
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() #重置最后一次下落时间

        if not isValidPosition(board,fallingPiece):
            return # 如果刚创建出来的方块不在一个合法位置，游戏结束

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_p :
                    #暂停游戏
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif event.key == K_LEFT or event.key == K_a :
                    movingLeft = False
                elif event.key == K_RIGHT or event.key == K_d:
                    movingRight = False
                elif event.key == K_DOWN or event.key == K_s:
                    movingDown = False

            elif event.type == KEYDOWN:
                # 移动图形
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # 旋转图形
                elif event.key == K_UP or event.key == K_w :
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['x'] -= 1
                        if not isValidPosition(board, fallingPiece):
                            fallingPiece['x'] +=2
                            if not isValidPosition(board, fallingPiece):
                                fallingPiece['x'] -=1
                                fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])

                elif (event.key == K_q): # 另一个方向旋转图形
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['x'] -= 1
                        if not isValidPosition(board, fallingPiece):
                            fallingPiece['x'] +=2
                            if not isValidPosition(board, fallingPiece):
                                fallingPiece['x'] -=1
                                fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # 更快下落
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()
                #直接到底
                elif event.key == K_SPACE :
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1,BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece,adjY = i):
                            break
                    fallingPiece['y'] += i-1

                # 用户长按左键或者右键
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()
        #用户长按下键
        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            if isValidPosition(board,fallingPiece,adjY= 1):
                fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        if time.time() - lastFallTime > fallFreq:
          # 自然下落
          if not isValidPosition(board, fallingPiece, adjY=1):
            addToBoard(board, fallingPiece)
            score += removeCompleteLines(board)
            level, fallFreq = calculateLevelAndFallFreq(score)
            fallingPiece = None
          else:
            fallingPiece['y'] += 1
            lastFallTime = time.time()
        #1/2000概率换背景图片
        if random.randint(1,2000) == 1:
            GAMEBACKGROUND = pygame.image.load(image_path + 'game_bg' + str(random.randint(1,7))+ '.jpg').convert()
        # 画上所有
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score,level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        (x,y) = pygame.mouse.get_pos()
        DISPLAYSURF.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT,BIGFONT,BACKGROUND,GAMEBACKGROUND,MOUSEIMAGE
    pygame.init()
    #初始化各变量
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BACKGROUND = pygame.image.load(image_path + 'background.jpg').convert()
    MOUSEIMAGE = pygame.image.load(image_path + 'guangbiao.png')
    icon = pygame.image.load(image_path + 'icon.jpg')
    pygame.display.set_icon(icon)

    BASICFONT = pygame.font.Font(font_path + 'FZSTK.TTF', 30)
    BIGFONT = pygame.font.Font(font_path + 'FreeSansBold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    if showTextScreen('Tetromino') == False:
        return
    while True:
        GAMEBACKGROUND = pygame.image.load(image_path + 'game_bg' + str(random.randint(1,7))+ '.jpg').convert()
        bgm = bgm_path + 'tetris' + str(random.randint(0,6)) + '.ogg'
        pygame.mixer_music.load(bgm)
        pygame.mixer.music.play(-1,0.0)
        if runGame() == False:
            pygame.mixer.music.stop()
            return
        pygame.mixer.music.stop()
        if showTextScreen('Game Over') == False:
            return

if __name__ == '__main__':
    main()
