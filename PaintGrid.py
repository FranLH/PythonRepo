import pygame
import math


pygame.init()
WindowSize = 600
window = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("PaintGrid")

ColDecimals = 2
BrushMult = 0.2
GridSize = 100
LineWidth = 0
TileSize = (WindowSize/GridSize)-LineWidth/2
grayRange = 1/TileSize*BrushMult

s = [1,0]
t = [0,1]
Pictures = []
def SeparateDataAns(dans):
    ans = []
    data = []
    for i in dans:
        ans.append(i[1])
        data.append(i[0])
    print(data)
    print(ans)
def DrawGrid():
    global Canvas
    Canvas = []
    window.fill((0, 0, 0))
    for y in range(GridSize):
        Canvas.append([])
        for x in range(GridSize):
            Canvas[y].append(0)
            pygame.draw.rect(window, (255,255,255), (TileSize*x+LineWidth,TileSize*y+LineWidth,TileSize-LineWidth, TileSize-LineWidth))
    pygame.display.flip()

def Paint(pos,color):
    x, y = round((pos[0]-TileSize/2)/TileSize), round((pos[1]-TileSize/2)/TileSize)
    pygame.draw.rect(window, color, (TileSize*x+LineWidth,TileSize*y+LineWidth,TileSize-LineWidth, TileSize-LineWidth))
    if color == (0,0,0):
        Canvas[y][x] = 1
    else:
        Canvas[y][x] = 0
def GrayscalePaint(pos,color):
    if color != 255:
        #x, y = round((pos[0]-TileSize/2)/TileSize), round((pos[1]-TileSize/2)/TileSize)
        for y in range(GridSize):
            for x in range(GridSize):
                col = round(math.dist([pos[0],pos[1]], [TileSize*x+LineWidth+TileSize/2, TileSize*y+LineWidth+TileSize/2])*grayRange,ColDecimals)

                if col < 1-Canvas[y][x]:
                    if col <= 1:
                        Canvas[y][x] = round(1-col,ColDecimals)
                    col = col * 255
                    col = (col,col,col)
                    pygame.draw.rect(window, col, (TileSize*x+LineWidth,TileSize*y+LineWidth,TileSize-LineWidth, TileSize-LineWidth))
    
running = True
DrawGrid()
pygame.display.flip()

time = 0
while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save = []
                    for i in Canvas:
                        save.extend(i)
                    Pictures.append([save,s])
                elif event.key == pygame.K_t:
                    save = []
                    for i in Canvas:
                        save.extend(i)
                    Pictures.append([save,t])
                elif event.key == pygame.K_q:
                    SeparateDataAns(Pictures)
                elif event.key == pygame.K_e:
                    DrawGrid()
                if event.key == pygame.K_p:
                    print(Pictures)
        if pygame.mouse.get_pressed()[0] == True:
            GrayscalePaint(pygame.mouse.get_pos(),0)
        if pygame.mouse.get_pressed()[2] == True:
            Paint(pygame.mouse.get_pos(),(255,255,255))
        pygame.display.flip()     
    except:
        pass
pygame.display.quit()