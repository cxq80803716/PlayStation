#coding: utf-8
import Tetris,game2048,FlappyBird,GreedySnake
import pygame,sys
from pygame.locals import *
bgm_path = "./bgm/tetris/"
main_menu_image_path = "./image/main-menu/"
select_game_menu_image_path = "./image/select-game-menu/"
font_path = "./font/"
FPS = 60
SIZE = (640,480)
TEXTCOLOR = (255,255,255)
TEXTSHADOWCOLOR = (185,185,185)

def terminate():
  pygame.quit()
  sys.exit()

def checkForPress(SelectGameRect,ExitRect):
    for event in pygame.event.get(): # get all the QUIT events
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate() # terminate if any QUIT events are present
        if event.type == MOUSEBUTTONDOWN:
            (x,y) = pygame.mouse.get_pos()
            (RectLeftx,RectTopy) = SelectGameRect.topleft
            (RectRightx,RectBottomy) = SelectGameRect.bottomright
            if x>= RectLeftx and x<= RectRightx and y>=RectTopy and y<= RectBottomy:
                return True
            (RectLeftx,RectTopy) = ExitRect.topleft
            (RectRightx,RectBottomy) = ExitRect.bottomright
            if x>= RectLeftx and x<= RectRightx and y>=RectTopy and y<= RectBottomy:
                terminate()
    return None

def makeTextObjs(text, font, color):
  surf = font.render(text, True, color)
  return surf, surf.get_rect()

def SelectGameMenu():
    global DISPLAYSURF
    game1= pygame.image.load(select_game_menu_image_path + 'game1.jpg')
    game2= pygame.image.load(select_game_menu_image_path + 'game2.jpg')
    game3= pygame.image.load(select_game_menu_image_path + 'game3.jpg')
    game4= pygame.image.load(select_game_menu_image_path + 'game4.jpg')
    icon = pygame.image.load(select_game_menu_image_path + 'icon.png')
    pygame.display.set_icon(icon)
    while True:
        DISPLAYSURF.blit(game1,(0,0))
        DISPLAYSURF.blit(game2,(SIZE[0]/2,0))
        DISPLAYSURF.blit(game3,(0,SIZE[1]/2))
        DISPLAYSURF.blit(game4,(SIZE[0]/2,SIZE[1]/2))
        (x,y) = pygame.mouse.get_pos()
        DISPLAYSURF.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))

        for event in pygame.event.get(): # get all the QUIT event
            if event.type == QUIT:
                terminate() # terminate if any QUIT events are present
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x <= SIZE[0]/2 and y <= SIZE[1] /2:
                    GreedySnake.main()
                elif x > SIZE[0]/2 and y <= SIZE[1] /2:
                    FlappyBird.main()
                elif x <= SIZE[0]/2 and y > SIZE[1] /2:
                    Tetris.main()
                elif x > SIZE[0]/2 and y > SIZE[1] /2:
                    game2048.main()
                pygame.display.set_caption('Play Station')
                DISPLAYSURF = pygame.display.set_mode(SIZE)
                icon = pygame.image.load(select_game_menu_image_path + 'icon.png')
                pygame.display.set_icon(icon)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def MainMenu():
    titleshadowSurf, titleshadowRect = makeTextObjs(u'小游戏平台', BIGFONT, TEXTSHADOWCOLOR)
    titleshadowRect.center = (int(SIZE[0] / 2), 100)

    titleSurf, titleRect = makeTextObjs(u'小游戏平台', BIGFONT, TEXTCOLOR)
    titleRect.center = (int(SIZE[0] / 2) -3, 97)

    SelectGameSurf, SelectGameRect = makeTextObjs(u'选择游戏', BASICFONT, TEXTCOLOR)
    SelectGameRect.center = (int(SIZE[0] / 2), int(SIZE[1] / 2) )

    ExitSurf, ExitRect = makeTextObjs(u'退出游戏', BASICFONT, TEXTCOLOR)
    ExitRect.center = (int(SIZE[0] / 2), int(SIZE[1] / 2) + 100)

    while True:
        DISPLAYSURF.blit(BACKGROUND,(0,0))
        DISPLAYSURF.blit(titleshadowSurf, titleshadowRect)
        DISPLAYSURF.blit(titleSurf, titleRect)
        DISPLAYSURF.blit(SelectGameSurf, SelectGameRect)
        DISPLAYSURF.blit(ExitSurf, ExitRect)
        (x,y) = pygame.mouse.get_pos()
        DISPLAYSURF.blit(MOUSEIMAGE,(x-MOUSEIMAGE.get_width()/2,y-MOUSEIMAGE.get_height()/2))

        if checkForPress(SelectGameRect,ExitRect):
            SelectGameMenu()
            icon = pygame.image.load(main_menu_image_path + 'icon.png')
            pygame.display.set_icon(icon)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def run():
    global DISPLAYSURF,BACKGROUND,BIGFONT,BASICFONT,FPSCLOCK,MOUSEIMAGE
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font(font_path + 'FreeSansBold.ttf', 40)
    BIGFONT = pygame.font.Font(font_path + 'FreeSansBold.ttf', 70)
    BACKGROUND = pygame.image.load(main_menu_image_path + 'background.jpg')
    MOUSEIMAGE = pygame.image.load(main_menu_image_path + 'guangbiao.png')
    DISPLAYSURF = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Play Station')
    pygame.mouse.set_visible(False)
    icon = pygame.image.load(main_menu_image_path + 'icon.png')
    pygame.display.set_icon(icon)

    MainMenu()

if __name__ == '__main__':
    run()
