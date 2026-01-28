import pygame
import math
import copy
import random

ChunkSize = 80
FPS = 100
WindowSize = (640,640)
CellSize = 4
SimSpeed = 1


def GetFullGrid(CellType):
    Grid = []
    for i in range(ChunkSize):
        Grid.append([])
        for j in range(ChunkSize):
            Grid[i].append(CellType)
    return(Grid)

PixelColorLookup = [(0,0,0),(0,0,80),(255,255,255),(255,0,0),(0,255,0),(0,0,255)]

class Camera:
    def __init__(self, x, y):
        self.x, self.y = x, y

        
class chunk:
    def __init__(self, x, y, World, CellType = 0):
        self.x, self.y, self.grid, self.World = x, y, GetFullGrid(CellType), World
        self.updated = GetFullGrid(CellType)
    def Render(self, camera):
        
        for x in range(ChunkSize):
            X = round(CellSize*(x-camera.x+self.x*ChunkSize))
            for y in range(ChunkSize):
                Y = round(CellSize*(y-camera.y+self.y*ChunkSize))
                pygame.draw.rect(window, PixelColorLookup[self.grid[x][y]], ((X,Y),(CellSize, CellSize)))
    def Fill(self, CellType):
        for x in range(ChunkSize):
            for y in range(ChunkSize):
                self.grid[x][y] = CellType
    def Update(self):
#         self.updated = copy.deepcopy(self.grid)
        for x in range(ChunkSize):
            for y in range(ChunkSize):
                if self.grid[x][y] != 0:
                    if self.GetCellVal(x,y+1,self.grid) == 0 and self.GetCellVal(x,y+1,self.updated) == 0:
                        self.SetCellVal(x,y+1,self.grid[x][y], self.updated)
                        #updated[x][y+1] = self.grid[x][y]
                        self.updated [x][y] = 0
                    if self.GetCellVal(x,y+1,self.grid) != 0 and self.GetCellVal(x,y+1,self.updated) != 0:
                        ran = random.choice([-1,1])
                        if self.GetCellVal(x+ran,y+1,self.grid) == 0 and self.GetCellVal(x+ran,y+1,self.updated) == 0:
                            self.SetCellVal(x+ran,y+1,self.grid[x][y], self.updated)
                            self.updated [x][y] = 0
                        elif self.GetCellVal(x-ran,y+1,self.grid) == 0 and self.GetCellVal(x-ran,y+1,self.updated) == 0:
                            self.SetCellVal(x-ran,y+1,self.grid[x][y], self.updated)
                            self.updated [x][y] = 0
        #self.grid = updated
    def GetCellVal(self, x, y, grid):
        if 0 <= x < ChunkSize and 0 <= y < ChunkSize:
            return(grid[x][y])
        else:
            X, Y, CX, CY = self.x, self.y, x, y
            if not (0 <= x < ChunkSize):
                X = self.x+int(abs(x)/x)
                if x > ChunkSize-1:
                    CX = x - ChunkSize
                if x < 0:
                    CX = ChunkSize + x
                #CX = (ChunkSize * x<0) - x - (ChunkSize) * (x > ChunkSize-1)
            if not (0 <= y < ChunkSize):
                Y = self.y+int(abs(y)/y)
                if y > ChunkSize-1:
                    CY = y - ChunkSize
                if y < 0:
                    CY = ChunkSize + y
                #CY = y - (ChunkSize) * (y > ChunkSize-1)
            IsUpdated = (grid is self.updated)
            return(self.World.GetCellVal(X, Y, CX, CY, IsUpdated))

    def SetCellVal(self, x, y, Value, grid):
        if 0 <= x < ChunkSize and 0 <= y < ChunkSize:
            grid[x][y] = Value
        else:
            X, Y, CX, CY = self.x, self.y, x, y
            if not (0 <= x < ChunkSize):
                X = int(abs(x)/x)
                if x > ChunkSize-1:
                    CX = x - ChunkSize
                if x < 0:
                    CX = ChunkSize + x
                #CX = x - (ChunkSize) * (x > ChunkSize-1)
            if not (0 <= y < ChunkSize):
                Y = int(abs(y)/y)
                if y > ChunkSize-1:
                    CY = y - ChunkSize
                if y < 0:
                    CY = ChunkSize + y
                #CY = y - (ChunkSize) * (y > ChunkSize-1)
            IsUpdated = (grid is self.updated)
            self.World.SetCellVal(X, Y, CX, CY, Value, IsUpdated)
        
class world:
    def __init__(self, size, camera):
        self.size, self.camera = size, camera
        self.ChunksGrid = []
        for i in range(size):
            self.ChunksGrid.append([])
            for j in range(size):
                self.ChunksGrid[i].append(chunk(i,j, self))
    def Render(self):
        window.fill((0, 0, 0))
        for i in self.ChunksGrid:
            for Chunk in i:
                Chunk.Render(self.camera)
        pygame.display.flip()
    def Update(self):
        for i in self.ChunksGrid:
            for Chunk in i:
                Chunk.updated = copy.deepcopy(Chunk.grid)
        for i in self.ChunksGrid:
            for Chunk in i:
                Chunk.Update()
        for i in self.ChunksGrid:
            for Chunk in i:
                Chunk.grid = Chunk.updated
    def GetCellVal(self, ChunkX, ChunkY, CellX, CellY, IsUpdated):
        if 0 <= ChunkX < self.size and 0 <= ChunkY < self.size:
            if IsUpdated:
                return(self.ChunksGrid[ChunkX][ChunkY].updated[CellX][CellY])
            else:
                return(self.ChunksGrid[ChunkX][ChunkY].grid[CellX][CellY])

        else:
            return(1)
    def SetCellVal(self, ChunkX, ChunkY, CellX, CellY, Value, IsUpdated):
        if 0 <= ChunkX < self.size and 0 <= ChunkY < self.size:
            if IsUpdated:
                self.ChunksGrid[ChunkX][ChunkY].updated[CellX][CellY] = Value
            else:
                self.ChunksGrid[ChunkX][ChunkY].grid[CellX][CellY] = Value
    



        
pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode(WindowSize, pygame.HWSURFACE, vsync=1)
pygame.display.set_caption("Sand simulation")


Cam = Camera(0,0)

World = world(2, Cam)

#World.SetCellVal(0,0,39,39,2)
World.ChunksGrid[0][1].Fill(3)
for i in range(20):
    for j in range(ChunkSize):
        World.SetCellVal(0,1,i,j,0,False)
for i in range(20):
    World.SetCellVal(0,1,i,1,0,False)
for j in range(40, 80):
    for i in range(80):
        World.SetCellVal(0,1,i,j,0,False)
#c00 = chunk(0,0,0)
#c00.grid[39][39] = 1
#c10 = chunk(1,0,2)

#Chunks = [c00]
running = True
x = 0
its = 0
col = 2
while running:
    its +=1
    if its %2 == 0:
        x += 1
        if x == 79:
            col = random.randint(1,5)
            x = 0
        World.SetCellVal(0,0, x, 0, col, False)
        World.SetCellVal(0,0, x+1, 1, col, False)
        World.SetCellVal(0,0, x+1, 0, col, False)
        World.SetCellVal(0,0, x, 1, col, False)
    
    World.Update()
    

    if its % SimSpeed == 0:
        World.Render()
    #Cam.x+=2
    #Cam.y+=2


    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False


         

    clock.tick(FPS)
    fps = clock.get_fps()
pygame.display.quit()