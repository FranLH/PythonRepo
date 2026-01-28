import pygame
import math
import copy
import random




def GetFullGrid(CellType):
    Grid = []
    for i in range(ChunkSize):
        Grid.append([])
        for j in range(ChunkSize):
            Grid[i].append(CellType)
    return(Grid)

PixelColorLookup = [(0,0,0),(0,0,80),(245,225,0),(0,0,200),(70,60,50),(0,0,255)]



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
                    pygame.draw.rect(window, PixelColorLookup[self.grid[x][y]], ((X,Y),(CellSize, CellSize)))
    def Fill(self, CellType):
        for x in range(ChunkSize):
            for y in range(ChunkSize):
                self.grid[x][y] = CellType
    def Update(self):
#         self.updated = copy.deepcopy(self.grid)
        #for x in range(ChunkSize):
        #    for y in range(ChunkSize):
        random.shuffle(RandomArray)
        for i in RandomArray:
            x, y = i[0], i[1]
            if self.grid[x][y] != 0:
                match self.grid[x][y]:
                    case 2:
                        if self.GetCellVal(x,y+1,self.updated) in (0,3): # Down
                            Other = copy.deepcopy(self.GetCellVal(x,y+1,self.updated))
                            #/print("Other=", Other)
                            self.SetCellVal(x,y+1,self.grid[x][y], self.updated)
                            #updated[x][y+1] = self.grid[x][y]
                            self.updated[x][y] = Other
                        else:
                            if self.GetCellVal(x-1,y+1,self.updated) in (0,3): # Down left
                                Other = copy.deepcopy(self.GetCellVal(x-1,y+1,self.updated))
                                self.SetCellVal(x-1,y+1,self.grid[x][y], self.updated)
                                self.updated[x][y] = Other
                            elif self.GetCellVal(x+1,y+1,self.updated) in (0,3): # Down right
                                Other = copy.deepcopy(self.GetCellVal(x+1,y+1,self.updated))
                                self.GetCellVal(x+1,y+1,self.updated)
                                self.SetCellVal(x+1,y+1,self.grid[x][y], self.updated)
                                self.updated[x][y] = Other
                    case 3:
                        if self.GetCellVal(x,y+1,self.updated) == 0:
                            self.SetCellVal(x,y+1,self.grid[x][y], self.updated)
                            #updated[x][y+1] = self.grid[x][y]
                            self.updated[x][y] = 0
                        else:
                            if self.GetCellVal(x-1,y+1,self.updated) == 0: # Down left
                                self.SetCellVal(x-1,y+1,self.grid[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y+1,self.updated) == 0: # Down right
                                self.SetCellVal(x+1,y+1,self.grid[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x-1,y,self.updated) == 0: # Left
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x-i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x-i+1,y,self.grid[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y,self.updated) == 0: # Right
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x+i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x+i-1,y,self.grid[x][y], self.updated)
                                self.updated[x][y] = 0
                    case 4:
                        pass
                        
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
    


ChunkSize = 40
FPS = 60
WindowSize = (640,640)
CellSize = 4
SimSpeed = 1
WaterSpeed = 1

RandomArray = []
for i in range(ChunkSize):
    for j in range(ChunkSize):
        RandomArray.append((i,j))

Cam = Camera(1,1)
MoveSpeed = 1
World = world(2, Cam)



#World.SetCellVal(0,0,39,39,2)

#for i in range(160):
#    for j in range(100,160):
#        World.ChunksGrid[0][0].grid[i][j] = 0
#World.ChunksGrid[1][1].Fill(2)


pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode(WindowSize, pygame.HWSURFACE, vsync=1)
pygame.display.set_caption("Sand simulation")




#c00 = chunk(0,0,0)
#c00.grid[39][39] = 1
#c10 = chunk(1,0,2)

#Chunks = [c00]
running = True
x = 0
its = 0
Selection = 0
while running:
    its +=1
    
    World.Update()
    

    if its % SimSpeed == 0:
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
            if event.key == pygame.K_1:
                Selection = 0
            elif event.key == pygame.K_2:
                Selection = 2
            elif event.key == pygame.K_3:
                Selection = 3
            elif event.key == pygame.K_4:
                Selection = 4
    if pygame.mouse.get_pressed(3)[0]:     
        CX = math.floor((MousePos[0]/CellSize+ Cam.x)/(ChunkSize))
        CY = math.floor((MousePos[1]/CellSize+ Cam.y)/(ChunkSize))
        X = math.floor(MousePos[0]/CellSize - CX*ChunkSize + Cam.x)
        Y = math.floor(MousePos[1]/CellSize - CY*ChunkSize + Cam.y)
        if 0 <= CX < World.size and 0 <= CY < World.size:
            Chunk = World.ChunksGrid[CX][CY]
            World.SetCellVal(CX,CY,X,Y,Selection, True)
            Chunk.SetCellVal(X-1,Y,Selection,Chunk.updated)
            Chunk.SetCellVal(X+1,Y,Selection,Chunk.updated)
            Chunk.SetCellVal(X,Y+1,Selection,Chunk.updated)
            Chunk.SetCellVal(X-1,Y+1,Selection,Chunk.updated)
            Chunk.SetCellVal(X+1,Y+1,Selection,Chunk.updated)


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