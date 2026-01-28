import pygame
import math
import copy
import random


PixelColorLookup = [(0,0,0),(255,255,255)]

def GetFullGrid(CellType):
    Grid = []
    for i in range(ChunkSize):
        Grid.append([])
        for j in range(ChunkSize):
            Grid[i].append(CellType)
    return(Grid)

def GetSurrounding(x,y):
    return(((x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)))



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
                if 0 <= X <= WindowSize[0] and 0 <= Y <= WindowSize[1]:
                    if self.grid[x][y] == 1:
                        pygame.draw.rect(window, PixelColorLookup[1], ((X,Y),(CellSize, CellSize)))
    def Fill(self, CellType):
        for x in range(ChunkSize):
            for y in range(ChunkSize):
                self.grid[x][y] = CellType
    def Update(self):
#         self.updated = copy.deepcopy(self.grid)
        #for x in range(ChunkSize):
        #    for y in range(ChunkSize):
        for x in range(len(self.grid)):
            for y in range(len(self.grid)):


                match self.grid[x][y]:
                    case 0:
                        pass
#                         neighbours = self.GetNeighbours(x,y,self.grid)
#                         if neighbours.count(1) == 3:
#                             self.updated[x][y] = 1
                    case 1:
                        self.CellUpdate(x,y)
#                         neighbours = self.GetNeighbours(x,y,self.grid)
#                         if neighbours.count(1) < 2:
#                             self.updated[x][y] = 0
#                         elif neighbours.count(1) > 3:
#                             self.updated[x][y] = 0
                            
#                     elif 2 <= neighbours.count(1) <= 3:
#                         pass



                        
        #self.grid = updated
    def CellUpdate(self,x,y):
        if 0 <= x < ChunkSize and 0 <= y < ChunkSize:
            match self.grid[x][y]:
                case 0:
                    neighbours = self.GetNeighbours(x,y,self.grid)
                    if neighbours.count(1) == 3:
                        self.updated[x][y] = 1
                case 1:
                    neighbours = self.GetNeighbours(x,y,self.grid)
                    if neighbours.count(1) < 2:
                        self.updated[x][y] = 0
                    elif neighbours.count(1) > 3:
                        self.updated[x][y] = 0
                    for cell in GetSurrounding(x,y):
                        if self.GetCellVal(cell[0],cell[1],self.grid) == 0:
                            self.CellUpdate(cell[0],cell[1])
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
            
            World.CellUpdate(X,Y,CX,CY)
        
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
                X = self.x+int(abs(x)/x)
                if x > ChunkSize-1:
                    CX = x - ChunkSize
                if x < 0:
                    CX = ChunkSize + x
                #CX = x - (ChunkSize) * (x > ChunkSize-1)
            if not (0 <= y < ChunkSize):
                Y = self.y+int(abs(y)/y)
                if y > ChunkSize-1:
                    CY = y - ChunkSize
                if y < 0:
                    CY = ChunkSize + y
                #CY = y - (ChunkSize) * (y > ChunkSize-1)
            IsUpdated = (grid is self.updated)
            self.World.SetCellVal(X, Y, CX, CY, Value, IsUpdated)
    def GetNeighbours(self,x,y,grid):
        neighbours = []
        neighbours.append(self.GetCellVal(x-1,y-1,grid))
        neighbours.append(self.GetCellVal(x,y-1,grid))
        neighbours.append(self.GetCellVal(x+1,y-1,grid))
        neighbours.append(self.GetCellVal(x-1,y,grid))
        neighbours.append(self.GetCellVal(x+1,y,grid))
        neighbours.append(self.GetCellVal(x-1,y+1,grid))
        neighbours.append(self.GetCellVal(x,y+1,grid))
        neighbours.append(self.GetCellVal(x+1,y+1,grid))
        return(neighbours)
        
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
        FpsText = arial.render("FPS: " + str(round(fps,2)), True, (0,0,0), (255,255,255))
        GUI = arial.render("Left click to draw, right click to erase, space to pause", True, (0,0,0), (255,255,255))
        GUI2 = arial.render("W, A, S, D to move around", True, (0,0,0), (255,255,255))
        window.blits([(FpsText,(0,20)),(GUI,(0,0)),(GUI2,(0,10))])
        #window.blit(GUI,(0,0))
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
            return(0)
    def SetCellVal(self, ChunkX, ChunkY, CellX, CellY, Value, IsUpdated):
        if 0 <= ChunkX < self.size and 0 <= ChunkY < self.size:
            if IsUpdated:
                self.ChunksGrid[ChunkX][ChunkY].updated[CellX][CellY] = Value
            else:
                self.ChunksGrid[ChunkX][ChunkY].grid[CellX][CellY] = Value
    def CellUpdate(self, ChunkX, ChunkY, CellX, CellY):
        if 0 <= ChunkX < self.size and 0 <= ChunkY < self.size:
            self.ChunksGrid[ChunkX][ChunkY].CellUpdate(CellX,CellY)       
    


ChunkSize = 80
FPS = 80
WindowSize = (680,680)
CellSize = 4
SimSpeed = 1


Cam = Camera(-2,-2)
MoveSpeed = 1
World = world(3, Cam)

# World.ChunksGrid[0][0].Fill(1)
# World.ChunksGrid[0][1].Fill(0)
# World.ChunksGrid[1][0].Fill(0)
# World.ChunksGrid[1][1].Fill(1)

#World.SetCellVal(0,0,39,39,2)

#for i in range(160):
#    for j in range(100,160):
#        World.ChunksGrid[0][0].grid[i][j] = 0
#World.ChunksGrid[1][1].Fill(2)


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
arial = pygame.font.SysFont("arial", 10, False, False)

window = pygame.display.set_mode(WindowSize, pygame.HWSURFACE, vsync=1)
pygame.display.set_caption("Conway's game of life")




#c00 = chunk(0,0,0)
#c00.grid[39][39] = 1
#c10 = chunk(1,0,2)

#Chunks = [c00]
running = True
x = 0
its = 0
Selection = 0
fps = FPS
paused = True
Next = False
while running:
    its +=1
    if not paused or Next:
        World.Update()
    Next = False


    World.Render()
    #Cam.x+=2
    #Cam.y+=2
    
    MousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
#         if pygame.mouse.get_pressed(3)[0]:
#             
#             CX = math.floor((MousePos[0]/CellSize+ Cam.x)/(ChunkSize))
#             CY = math.floor((MousePos[1]/CellSize+ Cam.y)/(ChunkSize))
#             X = math.floor(MousePos[0]/CellSize - CX*ChunkSize + Cam.x)
#             Y = math.floor(MousePos[1]/CellSize - CY*ChunkSize + Cam.y)
#            World.SetCellVal(CX,CY,X,Y,Selection, True)
        if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_1:
#                 Selection = 1
                
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_RIGHT:
                Next = True
            if event.key == pygame.K_UP:
                CellSize+=2
            if event.key == pygame.K_DOWN:
                CellSize = max(CellSize-2,1)                

    if pygame.mouse.get_pressed(3)[0]:     
        CX = math.floor((MousePos[0]/CellSize+ Cam.x)/(ChunkSize))
        CY = math.floor((MousePos[1]/CellSize+ Cam.y)/(ChunkSize))
        X = math.floor(MousePos[0]/CellSize - CX*ChunkSize + Cam.x)
        Y = math.floor(MousePos[1]/CellSize - CY*ChunkSize + Cam.y)
        if 0 <= CX < World.size and 0 <= CY < World.size:
            Chunk = World.ChunksGrid[CX][CY]
            World.SetCellVal(CX,CY,X,Y,1, False)
    if pygame.mouse.get_pressed(3)[2]:     
        CX = math.floor((MousePos[0]/CellSize+ Cam.x)/(ChunkSize))
        CY = math.floor((MousePos[1]/CellSize+ Cam.y)/(ChunkSize))
        X = math.floor(MousePos[0]/CellSize - CX*ChunkSize + Cam.x)
        Y = math.floor(MousePos[1]/CellSize - CY*ChunkSize + Cam.y)
        if 0 <= CX < World.size and 0 <= CY < World.size:
            Chunk = World.ChunksGrid[CX][CY]
            World.SetCellVal(CX,CY,X,Y,0, False)
#             Chunk.SetCellVal(X-1,Y,Selection,Chunk.updated)
#             Chunk.SetCellVal(X+1,Y,Selection,Chunk.updated)
#             Chunk.SetCellVal(X,Y+1,Selection,Chunk.updated)
#             Chunk.SetCellVal(X-1,Y+1,Selection,Chunk.updated)
#             Chunk.SetCellVal(X+1,Y+1,Selection,Chunk.updated)


            #round(CellSize*(x-camera.x+self.x*ChunkSize))
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Cam.x -= MoveSpeed
    if keys[pygame.K_d]:
        Cam.x += MoveSpeed
    if keys[pygame.K_w]:
        Cam.y -= MoveSpeed
    if keys[pygame.K_s]:
        Cam.y += MoveSpeed

         

    clock.tick(FPS)
    fps = clock.get_fps()
pygame.display.quit()
