import random, sys, time, pygame
from pygame.locals import *


###  贪吃蛇小游戏   ###

# 屏幕刷新率（在这里相当于贪吃蛇的速度）
FPS = 5
# 屏幕宽度
WINDOWWIDTH = 640
# 屏幕高度
WINDOWHEIGHT = 480
# 小方格的大小
CELLSIZE = 20

# 断言，屏幕的宽和高必须能被方块大小整除
assert WINDOWWIDTH % CELLSIZE == 0, "窗口宽度太小了"
assert WINDOWHEIGHT % CELLSIZE == 0, "窗口高度太小了"

# 横向和纵向的方格数
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# 定义常用颜色
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
BGCOLOR = BLACK

# 定义贪吃蛇的动作
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# 贪吃蛇的头（后面会经常用到）
HEAD = 0

def main():

    # 定义全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    # 初始化pygame
    pygame.init()
    # 获得pygame时钟
    FPSCLOCK = pygame.time.Clock()
    # 设置屏幕宽高
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # 设置基本字体
    BASICFONT = pygame.font.Font('main.ttf', 18)
    # 设置窗口的标题
    pygame.display.set_caption('贪吃蛇小游戏')

    # 显示游戏开始画面
    showStartScreen()

    while True:

        # 这里一直循环于游戏运行时和显示游戏结束画面之间，运行游戏里有一个循环，显示游戏结束画面也有一个循环，两个循环都有相应的return，这样就可以达到切换这两个模块的效果

        # 运行游戏
        runGame()

        # 显示游戏结束画面
        showGameOverScreen()

# 绘制所有的方格
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        # 绘制垂直线
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        # 绘制水平线
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

# 随机生成一个苹果的坐标位置
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

# 根据coord绘制苹果
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

# 根据wormCoords列表绘制贪吃蛇
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

# 显示分数
def drawScore(score):
    scoreSurf = BASICFONT.render('得分: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

# 退出游戏
def terminate():
    pygame.quit()
    sys.exit()

# 提示按键消息
def drawPressKeyMsg():
    
    pressKeySurf = BASICFONT.render('按任意键开始游戏！', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 4)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

# 检测按键事件
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

# 显示游戏开始画面
def showStartScreen():
    pass

# 游戏运行时
def runGame():
    pass

# 显示游戏结束画面
def showGameOverScreen():
    pass






# 显示游戏开始画面
def showStartScreen():

    DISPLAYSURF.fill(BGCOLOR)
    titleFont = pygame.font.Font('main.ttf', 100)
    titleSurf = titleFont.render('准备好了吗？', True, GREEN)
    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(titleSurf, titleRect)

    drawPressKeyMsg()

    pygame.display.update()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return




# 游戏运行画面
def runGame():
    # 随机初始化设置一个点作为贪吃蛇的起点
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)

    # 以这个点为起点，建立一个长度为3格的贪吃蛇（列表）
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    direction = RIGHT # 初始化一个运动的方向

    # 随机一个苹果的位置
    apple = getRandomLocation()

    # 游戏主循环
    while True:
        # 事件处理
        for event in pygame.event.get():
            # 退出事件
            if event.type == QUIT:
                terminate()
            # 按键事件
            elif event.type == KEYDOWN:
                #如果按下的是左键或a键，且当前的方向不是向右，就改变方向，以此类推
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # 检查贪吃蛇是否撞到撞到边界，即检查蛇头的坐标
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            # game over
            return

        # 检查贪吃蛇是否撞到自己，即检查蛇头的坐标是否等于蛇身的坐标
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                # game over
                return

        # 检查贪吃蛇是否吃到苹果，若没吃到，则删除尾端，蛇身前进一格
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # 不移除蛇的最后一个尾巴格
            # 重新随机生成一个苹果
            apple = getRandomLocation()
        else:
            # 移除蛇的最后一个尾巴格
            del wormCoords[-1]

        # 根据方向，添加一个新的蛇头，以这种方式来移动贪吃蛇
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        # 插入新的蛇头在数组的最前面
        wormCoords.insert(0, newHead)

        # 绘制背景
        DISPLAYSURF.fill(BGCOLOR)

        # 绘制所有的方格
        drawGrid()

        # 绘制贪吃蛇
        drawWorm(wormCoords)

        # 绘制苹果
        drawApple(apple)

        # 绘制分数（分数为贪吃蛇列表当前的长度-3）
        drawScore(len(wormCoords) - 3)

        # 更新屏幕
        pygame.display.update()

        # 设置帧率
        FPSCLOCK.tick(FPS)


# 显示游戏结束画面
def showGameOverScreen():
    gameOverFont = pygame.font.Font('main.ttf', 50)
    gameSurf = gameOverFont.render('游戏', True, WHITE)
    overSurf = gameOverFont.render('结束', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2-gameRect.height-10)
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return



if __name__ == '__main__':
    main()