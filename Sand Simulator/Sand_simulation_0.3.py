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

PixelColorLookup = [(135,206,235),(0,0,0),(245,225,0),(0,0,200),(70,60,50),(255,150,0), (130,130,130), (100,0,0)]



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
                    case 1:
                        pass
                    case 2:
                        neighbours = self.GetNeighbours(x,y,self.updated)
                        if 7 in neighbours and random.randint(0,SandMeltSpeed) == 1:
                            self.updated[x][y] = 7
                        elif self.GetCellVal(x,y+1,self.updated) in (0,3,7,6): # Down
                            Other = copy.deepcopy(self.GetCellVal(x,y+1,self.updated))
                            match Other:
                                case 0:
                                    self.SetCellVal(x,y+1,self.updated[x][y], self.updated)
                                    self.updated[x][y] = Other
                                case 3:
                                    self.SetCellVal(x,y+1,self.updated[x][y], self.updated)
                                    self.updated[x][y] = Other
                                case 7: # NOT WORKING???
                                    if random.randint(0,LavaDensity) == 0:
                                        self.SetCellVal(x,y+1,self.updated[x][y], self.updated)
                                        self.updated[x][y] = Other
                                case 6:
                                    self.SetCellVal(x,y+1,self.updated[x][y], self.updated)
                                    self.updated[x][y] = Other
                                    
                        else:
                            if self.GetCellVal(x-1,y+1,self.updated) in (0,3): # Down left
                                Other = copy.deepcopy(self.GetCellVal(x-1,y+1,self.updated))
                                self.SetCellVal(x-1,y+1,self.updated[x][y], self.updated)
                                self.updated[x][y] = Other
                            elif self.GetCellVal(x+1,y+1,self.updated) in (0,3): # Down right
                                Other = copy.deepcopy(self.GetCellVal(x+1,y+1,self.updated))
                                self.GetCellVal(x+1,y+1,self.updated)
                                self.SetCellVal(x+1,y+1,self.updated[x][y], self.updated)
                                self.updated[x][y] = Other
                    case 3:
                        neighbours = self.GetNeighbours(x,y,self.updated)
                        if 7 in neighbours or neighbours.count(5) >=3:
                            self.updated[x][y] = 6
                        elif self.GetCellVal(x,y+1,self.updated) in (0,6):
                            Other = copy.deepcopy(self.GetCellVal(x,y+1,self.updated))
                            self.SetCellVal(x,y+1,self.updated[x][y], self.updated)
                            #updated[x][y+1] = self.grid[x][y]
                            self.updated[x][y] = Other
                        else:
                            if self.GetCellVal(x-1,y+1,self.updated) == 0: # Down left
                                self.SetCellVal(x-1,y+1,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y+1,self.updated) == 0: # Down right
                                self.SetCellVal(x+1,y+1,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x-1,y,self.updated) == 0: # Left
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x-i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x-i+1,y,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y,self.updated) == 0: # Right
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x+i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x+i-1,y,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                    case 4:
                        neighbours = self.GetNeighbours(x,y,self.updated)
                        if (5 in self.GetNeighbours(x,y,self.updated) and random.randint(0,FireSpreadSpeed) == 1) or 7 in neighbours:
                            self.updated[x][y] = 5
                    case 5:
                        neighbours = self.GetNeighbours(x,y,self.updated)
                        if (neighbours.count(3) >= 2 and random.randint(0,FireStrength) == 1) or (4 not in neighbours and random.randint(0,FireBurnoutSpeed) == 1):
                            self.updated[x][y] = 0
                    case 6: # Vapor
                        if random.randint(0,VaporLife) == 1:
                            self.updated[x][y] = 3
                        elif self.GetCellVal(x,y-1,self.updated) in (0,3,7):
                            Other = copy.deepcopy(self.GetCellVal(x,y-1,self.updated))
                            self.SetCellVal(x,y-1,self.updated[x][y], self.updated)
                            self.updated[x][y] = Other
                        else:
                            if self.GetCellVal(x-1,y-1,self.updated) == 0: # Down left
                                self.SetCellVal(x-1,y-1,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y-1,self.updated) == 0: # Down right
                                self.SetCellVal(x+1,y-1,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x-1,y,self.updated) == 0: # Left
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x-i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x-i+1,y,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y,self.updated) == 0: # Right
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x+i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x+i-1,y,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                    case 7: # Lava
                        neighbours = self.GetNeighbours(x,y,self.updated)
                        if neighbours.count(0) >= 3 and random.randint(0,round(LavaLife/neighbours.count(0)*4)) == 0: # In contact with air
                            self.updated[x][y] = 5
                        elif neighbours.count(0) >= 1 and random.randint(0,round(LavaLife/neighbours.count(0)/4)) == 0: # In contact with water
                            self.updated[x][y] = 5
                        elif neighbours.count(6) >= 1 and random.randint(0,round(LavaLife/neighbours.count(6)/2)) == 0: # In contact with water
                            self.updated[x][y] = 5

                        elif self.GetCellVal(x,y+1,self.updated) in (0,6):
                            Other = copy.deepcopy(self.GetCellVal(x,y+1,self.updated))
                            self.SetCellVal(x,y+1,self.updated[x][y], self.updated)
                            #updated[x][y+1] = self.grid[x][y]
                            self.updated[x][y] = Other
                        else:
                            if self.GetCellVal(x-1,y+1,self.updated) == 0: # Down left
                                self.SetCellVal(x-1,y+1,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y+1,self.updated) == 0: # Down right
                                self.SetCellVal(x+1,y+1,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x-1,y,self.updated) == 0: # Left
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x-i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x-i+1,y,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0
                            elif self.GetCellVal(x+1,y,self.updated) == 0: # Right
                                i = 1
                                while i <= WaterSpeed:
                                    if self.GetCellVal(x+i,y,self.updated) == 0:
                                        i+=1
                                    else:
                                        break

                                self.SetCellVal(x+i-1,y,self.updated[x][y], self.updated)
                                self.updated[x][y] = 0                      
                        
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
        GUI = arial.render("Controls: Air= 1 - Sand: 2 - Water= 3 - Wood= 4 - Fire= 5 - Steam= 6 - Lava= 7 - Wall= 0 ", True, (0,0,0), (255,255,255))
        GUI2 = arial.render("W, A, S, D to move around, Space to pause", True, (0,0,0), (255,255,255))
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
            return(1)
    def SetCellVal(self, ChunkX, ChunkY, CellX, CellY, Value, IsUpdated):
        if 0 <= ChunkX < self.size and 0 <= ChunkY < self.size:
            if IsUpdated:
                self.ChunksGrid[ChunkX][ChunkY].updated[CellX][CellY] = Value
            else:
                self.ChunksGrid[ChunkX][ChunkY].grid[CellX][CellY] = Value
    


ChunkSize = 80
FPS = 80
WindowSize = (680,680)
CellSize = 8
SimSpeed = 1
WaterSpeed = 1
FireSpreadSpeed = 60
FireBurnoutSpeed = 8
FireStrength = 2
VaporLife  = 300
SandMeltSpeed = 100
LavaDensity = 10
WaterDensity = 0
LavaLife = 1200

RandomArray = []
for i in range(ChunkSize):
    for j in range(ChunkSize):
        RandomArray.append((i,j))

Cam = Camera(-2,-2)
MoveSpeed = 1
World = world(1, Cam)

# World.ChunksGrid[1][2].Fill(7)
# World.ChunksGrid[0][2].Fill(3)
# World.ChunksGrid[0][1].Fill(4)
# World.ChunksGrid[1][1].Fill(7)

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
pygame.display.set_caption("Sand simulation")




#c00 = chunk(0,0,0)
#c00.grid[39][39] = 1
#c10 = chunk(1,0,2)

#Chunks = [c00]
running = True
x = 0
its = 0
Selection = 0
fps = FPS
Paused = False
while running:
    its +=1
    if not Paused:
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
            if event.key == pygame.K_SPACE:
                Paused = not Paused
            if event.key == pygame.K_1:
                Selection = 0
            elif event.key == pygame.K_2:
                Selection = 2
            elif event.key == pygame.K_3:
                Selection = 3
            elif event.key == pygame.K_4:
                Selection = 4
            elif event.key == pygame.K_5:
                Selection = 5#
            elif event.key == pygame.K_6:
                Selection = 6
            elif event.key == pygame.K_7:
                Selection = 7
            elif event.key == pygame.K_0:
                Selection = 1
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
