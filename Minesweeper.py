import pygame
import random
import copy
import math




class Game:
    def __init__(self,size,mines):
        self.size, self.mines = size, mines
        self.Tiles = []
        self.Uncovered = []
        for i in range(size):
            self.Tiles.append([])
            for j in range(size):
                self.Tiles[i].append(0)
    def PickRandomValidTile(self, FirstClick):
        tilex = random.randint(0,self.size-1)
        tiley = random.randint(0,self.size-1)
        if [tilex,tiley] != FirstClick and self.Tiles[tilex][tiley]!=9:
            self.Tiles[tilex][tiley] = 9
        else:
            print("WRONG")
            self.PickRandomValidTile(FirstClick)
    def GetCellValue(self,x,y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return(self.Tiles[x][y])
        else:
            return(None)
    def CountMines(self, x, y):
        mines = 0
        if self.GetCellValue(x-1,y-1) == 9:
            #print("lol")
            mines+=1
        if self.GetCellValue(x,y-1) == 9:
            mines+=1
        if self.GetCellValue(x+1,y-1) == 9:
            mines+=1
        if self.GetCellValue(x-1,y) == 9:
            mines+=1
        if self.GetCellValue(x+1,y) == 9:
            mines+=1
        if self.GetCellValue(x-1,y+1) == 9:
            mines+=1
        if self.GetCellValue(x,y+1) == 9:
            mines+=1
        if self.GetCellValue(x+1,y+1) == 9:
            mines+=1
        return(mines)
    def Print(self):
        rotated = copy.deepcopy(self.Tiles)
        for i in range(self.size):
            for j in range(self.size):
                rotated[j][i] = self.Tiles[i][j]
        for row in range(self.size-1,-1,-1):
            print(rotated[row])
    def Start(self, FirstClick):

        for mine in range(self.mines):
            self.PickRandomValidTile(FirstClick)
        for i in range(self.size):
            for j in range(self.size):
                if self.Tiles[i][j] != 9:
                    self.Tiles[i][j] = self.CountMines(i,j)
                    #print(self.Tiles[i][j])
        self.Uncover(FirstClick[0], FirstClick[1])
    def RenderAll(self):
        
        window.fill((0,0,0))
        TileSize = WindowSize[0]/self.size
        font = pygame.font.SysFont("arial", int(TileSize/1.25), False, False)
        text = []
        for i in range(self.size):
            for j in range(self.size):
                if self.Tiles[i][j] == 9:
                    color = (255,0,255,0)
                else:
                    color = [self.Tiles[i][j]*28] * 3
                x = i*TileSize
                y = WindowSize[0]-TileSize-(j*TileSize)
                pygame.draw.rect(window,color,((x,y),(TileSize,TileSize)))

                text.append((font.render(str(self.Tiles[i][j]), True, (255,255,255)),(x+TileSize/4,y)))
        print(text)
        window.blits(text)
        pygame.display.flip()
    def Render(self):
        
        window.fill((0,0,0))
        TileSize = WindowSize[0]/self.size
        font = pygame.font.SysFont("arial", int(TileSize/1.25), False, False)
        text = []
        for tile in self.Uncovered:
            x = tile[0]*TileSize
            y = (tile[1]*TileSize)
            pygame.draw.rect(window,(255,255,255),((x,y),(TileSize,TileSize)))
            value = str(self.Tiles[tile[0]][tile[1]])
            if value == "9":
                value = "X"

            text.append((font.render(value, True, (0,0,0)),(x+TileSize/4,y)))
        window.blits(text)
        pygame.display.flip()
    def Uncover(self,x,y):
        if [x,y] not in self.Uncovered and 0 <= x < self.size and 0 <= y < self.size:
            self.Uncovered.append([x,y])
            if self.GetCellValue(x,y) == 0:
                self.Uncover(x-1,y-1)
                self.Uncover(x,y-1)
                self.Uncover(x+1,y-1)
                self.Uncover(x-1,y)
                self.Uncover(x+1,y)
                self.Uncover(x-1,y+1)
                self.Uncover(x,y+1)
                self.Uncover(x+1,y+1)
        
        
pygame.init()

pygame.font.init()

clock = pygame.time.Clock()

WindowSize = (600,600)
FPS = 40
window = pygame.display.set_mode(WindowSize, pygame.SRCALPHA)
pygame.display.set_caption("Minesweeper")
                    

Game1 = Game(20,60)
Game1.Start([10,10])
#Game1.Print()
Game1.Render()
#print(Game1.Tiles)
running = True
while running:
    Game1.Render()
    for event in pygame.event.get():

        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
    MousePos = pygame.mouse.get_pos()
    CellSize = WindowSize[0]/Game1.size
    if pygame.mouse.get_pressed(3)[0]:
        mx = max(min(MousePos[0],WindowSize[0]),0)
        my = max(min(MousePos[1],WindowSize[0]),0)
        X = math.floor(mx/CellSize)
        Y = math.floor(my/CellSize)
        Game1.Uncover(X,Y)
                     



    clock.tick(FPS)
           
pygame.display.quit()