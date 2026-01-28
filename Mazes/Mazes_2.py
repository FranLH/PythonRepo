import pygame
import random
import math
import copy
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2





class Maze:
    def __init__(self, pos:vec2, size:list):
        self.pos, self.size, self.data = pos, size, []
        self.longest=0
        for x in range(size[0]):
            self.data.append([])
            for y in range(size[1]):
                self.data[x].append(0)
    def Render(self, DrawWalls=False, width=0.3):
        # Only renders the parts of the maze that are inside of the screen
        dlCorner = cam.ToWorldSpace(vec2(0,cam.windowSize[1]))-self.pos
        urCorner = cam.ToWorldSpace(vec2(cam.windowSize[0],0))-self.pos
        dlCorner.x = round(max(dlCorner.x-1,0))
        dlCorner.y = round(max(dlCorner.y-1,0))
        urCorner.x = round(min(urCorner.x+2,self.size[0]))
        urCorner.y = round(min(urCorner.y+2,self.size[1]))

        if DrawWalls:
            for x in range(dlCorner.x, urCorner.x):
                for y in range(dlCorner.y, urCorner.y):
                    if self.data[x][y]==1:
                        pygame.draw.rect(window.surface, (0,0,0), [cam.ToScreen(self.pos+vec2(x,y)).ToList(), (vec2(1,1)*math.ceil(cam.SizeZoom(1))).ToList()])
#                     elif self.data[x][y]==2: # Draw the dead ends
#                         pygame.draw.rect(window.surface, (100,100,100), [cam.ToScreen(self.pos+vec2(x,y)).ToList(), (vec2(1,1)*math.ceil(cam.SizeZoom(1))).ToList()])
                    
                    elif self.data[x][y]==3: # Draw the beggining and ending squares
                        pygame.draw.rect(window.surface, (255,0,0), [cam.ToScreen(self.pos+vec2(x,y)).ToList(), (vec2(1,1)*math.ceil(cam.SizeZoom(1))).ToList()])
                    
#                     elif self.data[x][y]!=0:   # Depth gradient
#                         color = round(255-255*self.data[x][y]/self.longest)
#                         pygame.draw.rect(window.surface, (color,color,color), [cam.ToScreen(self.pos+vec2(x,y)).ToList(), (vec2(1,1)*math.ceil(cam.SizeZoom(1))).ToList()])

        else:
            lineWidth=round(cam.SizeZoom(width))
            for x in range(dlCorner.x, urCorner.x):
                for y in range(dlCorner.y, urCorner.y):
                    if self.data[x][y]==1:
                        centre = self.pos+vec2(x+0.5,y+0.5)
                        centreDraw = cam.ToScreen(centre).ToList()
                        if self.Get(self.data,vec2(x+1,y)) == 1:
                            pygame.draw.line(window.surface, (0,0,0), centreDraw, cam.ToScreen(centre+vec2(0.5,0)).ToList(),lineWidth)
                        if self.Get(self.data,vec2(x-1,y)) == 1:
                            pygame.draw.line(window.surface, (0,0,0), centreDraw, cam.ToScreen(centre+vec2(-0.5,0)).ToList(),lineWidth)
                        if self.Get(self.data,vec2(x,y+1)) == 1:
                            pygame.draw.line(window.surface, (0,0,0), centreDraw, cam.ToScreen(centre+vec2(0,0.5)).ToList(),lineWidth)
                        if self.Get(self.data,vec2(x,y-1)) == 1:
                            pygame.draw.line(window.surface, (0,0,0), centreDraw, cam.ToScreen(centre+vec2(0,-0.5)).ToList(),lineWidth)
                    elif self.data[x][y]==3:
                        pygame.draw.rect(window.surface, (255,100,100), [cam.ToScreen(self.pos+vec2(x,y+1)).ToList(), (vec2(1,1)*math.ceil(cam.SizeZoom(1))).ToList()])

        pygame.display.flip()



    def Get(self,data, pos):
        lx = len(data)
        ly = len(data[0])
        if pos.x >= 0 and pos.x < lx and pos.y >=0 and pos.y < ly:
#             print(pos)
            return(data[pos.x][pos.y])
        else:
            return("out")
    def Fill(self,num):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.data[x][y]=num
    def Fix(self, startPos):
        fixed = copy.deepcopy(self.data)
        EvenX = (startPos.x)%2
        EvenY = (startPos.y)%2
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if x>0 and x<(self.size[0]-1) and y>0 and y<(self.size[1]-1) and x%2==EvenX and y%2==EvenY and self.data[x][y] == 1:
#                     try:
                    fixed[x][y-1]=1
                    fixed[x][y+1]=1
                    fixed[x-1][y]=1
                    fixed[x+1][y]=1
                    fixed[x-1][y-1]=1
                    fixed[x-1][y+1]=1
                    fixed[x+1][y-1]=1
                    fixed[x+1][y+1]=1
#                 else:
#                     print(x>0 , x<(self.size[0]-1) , y>0 , y<(self.size[1]-1) , x%2==EvenX , y%2==EvenY , self.data[x][y] == 1)
#                     print(x,y)
#                     except:
#                         pass
        self.data = fixed
        
    def Generate(self, startPos, maxDepth, maxAnts, antProb, seed=0):
        if seed!=0: # Uses the selected seed
            random.seed(seed)
        else: # If no seed is specified it selects a random one
            seed = random.randint(1,1000)
            random.seed(seed)
        if maxDepth == 0: # Estimates the max amount of iterations needed to create the maze
            maxDepth=math.ceil(self.size[0]/2-1)*math.ceil(self.size[1]/2-1)*2
            
        dataClone = copy.deepcopy(self.data) # This will hold the information of the maze as it gets created
        depthClone = copy.deepcopy(self.data) # This will hold the depth of the maze, to help find the longest path
        
        pos = startPos
        dataClone[pos.x][pos.y]=3
        Longest = [0, pos]
        
        ants = [startPos] # Creates the first ant
        
        removeAnts = [] # This will store the ants that got stuck
        
        i=0
        newAnt = [False, vec2(0,0)]
        while i < maxDepth and len(ants)!=0:
            for antID in range(len(ants)):
                pos = ants[antID]
                length=depthClone[pos.x][pos.y]
                options = []
                if pos.x>2 and self.Get(dataClone, pos+vec2(-2,0)) == 1 and pos+vec2(-2,0) not in ants: # Move left
                    options.append(vec2(-2,0))
                if pos.x<self.size[0]-3 and self.Get(dataClone, pos+vec2(2,0)) == 1 and pos+vec2(2,0) not in ants: # Move right
                    options.append(vec2(2,0))
                if pos.y>2 and self.Get(dataClone, pos+vec2(0,-2)) == 1 and pos+vec2(0,-2) not in ants: # Move left
                    options.append(vec2(0,-2))
                if pos.y<self.size[1]-3 and self.Get(dataClone, pos+vec2(0,2)) == 1 and pos+vec2(0,2) not in ants: # Move right
                    options.append(vec2(0,2))
                
                if options != []:
                    move = round((random.choice(options))/2)
                    pos+=move
                    dataClone[pos.x][pos.y]=0
                    
                    depthClone[pos.x][pos.y]=0
                    pos+=move
                    dataClone[pos.x][pos.y]=0
                    if len(ants)<maxAnts and newAnt[0] == False and random.randint(0,antProb)==0:
                        newAnt = [True, pos]
                        
                    
                    ants[antID] = pos
                    if length+1>Longest[0]:
                        Longest = [length+1, pos]
                    depthClone[pos.x][pos.y]=length+1
                else:
                    
                    if pos.x>2 and self.Get(dataClone, pos+vec2(-2,0)) == 0 and self.Get(dataClone, pos+vec2(-1,0)) == 0 and pos+vec2(-2,0) not in ants: # Move left
                        options.append(vec2(-2,0))
                    if pos.x<self.size[0]-3 and self.Get(dataClone, pos+vec2(2,0)) == 0 and self.Get(dataClone, pos+vec2(1,0)) == 0 and pos+vec2(2,0) not in ants: # Move right
                        options.append(vec2(2,0))
                    if pos.y>2 and self.Get(dataClone, pos+vec2(0,-2)) == 0 and self.Get(dataClone, pos+vec2(0,-1)) == 0 and pos+vec2(0,-2) not in ants: # Move left
                        options.append(vec2(0,-2))
                    if pos.y<self.size[1]-3 and self.Get(dataClone, pos+vec2(0,2)) == 0 and self.Get(dataClone, pos+vec2(0,1)) == 0 and pos+vec2(0,2) not in ants: # Move right
                        options.append(vec2(0,2))
                    if len(options)<=1:
                        dataClone[pos.x][pos.y]=2
                    if options != []:
                        pos += random.choice(options)
                        ants[antID] = pos
                    else:
                        removeAnts.append(antID)
                        #i=maxDepth #FIX#
            if newAnt[0]:
                ants.append(newAnt[1])
                newAnt = [False, vec2(0,0)]
            removeAnts.sort(reverse=True)
            for a in removeAnts:
                ants.pop(a)
            removeAnts = []
            i+=1
            
        dataClone[Longest[1].x][Longest[1].y]=3 # Marks the end of the maze
        self.data = dataClone # Stores the final maze
        self.longest = Longest[0] # Stores the max length of the maze
        
        print("Seed:", seed)
        print("Length:", self.longest)
            


window = Window((800,800), "Mazes", 60, pygame.HWSURFACE | pygame.SRCALPHA, vsync=1)
cam = Camera(vec2(50,50), 0.14, window.size)
MoveSpeed = 0.5

maze = Maze(vec2(0,0), [91,91])
maze.Fill(1)



# maze.data[18] = [0]*30
# maze.data[19] = [0]*30
# maze.data[20] = [0]*30
# maze.data[21] = [0]*30
# maze.data[18].extend([1]*11)
# maze.data[19].extend([1]*11)
# maze.data[20].extend([1]*11)
# maze.data[21].extend([1]*11)




maze.Fix(vec2(1,1))
maze.Generate(vec2(1,1),0, 5, 90)


#Seed=156
# n1 = Node(vec2(0,0),[])
# n2 = Node(vec2(40,0),[n1])

running = True
selection = 0
MousePos = [400,400]
positive = True
while running:
    window.surface.fill((255,255,255))
    
    maze.Render(False,0.4)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze.Fill(1)
                maze.Generate(vec2(1,1),0, 8, 20)
            if event.key == pygame.K_RETURN:
                im = pygame.image.save(window.surface,"maze.bmp")
                print("Image saved!")
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_a]:
        cam.pos.x -= MoveSpeed*cam.zoom*window.clock.get_time()
    if keys[pygame.K_d]:
        cam.pos.x += MoveSpeed*cam.zoom*window.clock.get_time()
    if keys[pygame.K_w]:
        cam.pos.y += MoveSpeed*cam.zoom*window.clock.get_time()
    if keys[pygame.K_s]:
        cam.pos.y -= MoveSpeed*cam.zoom*window.clock.get_time()
    if keys[pygame.K_UP]:
        cam.zoom*=0.99
    if keys[pygame.K_DOWN]:
        cam.zoom/=0.99

        
    window.Tick()
pygame.display.quit()