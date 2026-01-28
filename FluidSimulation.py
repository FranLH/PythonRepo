import pygame
import math
import random
import copy
Width, Height = 600, 600
window = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF, 32)
window.fill((255,255,255))
pygame.init()


class Tile:
    def __init__(self,pos,vel,density,parent):
        self.pos, self.vel, self.density, self.parent = pos, vel, density, parent
        self.nextDensity = density
    def Diffuse(self):
        neighbours = self.parent.GetNeighbours(self.pos)
        NewDens = 0
        for neighbour in neighbours:
            NewDens+=neighbour.density
        NewDens = NewDens/len(neighbours)
        self.nextDensity = NewDens
    def Advect(self):
        origins = self.parent.GetClosest([self.pos[0]-self.vel[0],self.pos[1]-self.vel[1]])
        NewDens = 0
        for tile in origins:
            NewDens+= max(1-math.dist([self.pos[0]-self.vel[0],self.pos[1]-self.vel[1]],tile.pos),0)*tile.density
        self.nextDensity = NewDens
class Fluid:
    def __init__(self,size):
        self.size = size
        self.grid = []
        for i in range(size):
            self.grid.append([])
            for j in range(size):
                self.grid[i].append(Tile([i,j],[0,0],random.random(),self))
    def GetNeighbours(self,pos):
        neighbours = []
        if pos[0]>0:
            neighbours.append(self.grid[pos[0]-1][pos[1]])
        if pos[0]<self.size-1:
            neighbours.append(self.grid[pos[0]+1][pos[1]])
        if pos[1]>0:
            neighbours.append(self.grid[pos[0]][pos[1]-1])
        if pos[1]<self.size-1:
            neighbours.append(self.grid[pos[0]][pos[1]+1])
        return(neighbours)
    def GetClosest(self,pos):
        closest = []
        if pos[0]>0 and pos[1]>0:
            closest.append(self.grid[math.floor(pos[0])][math.floor(pos[1])]) 
        if pos[0]>0 and pos[1]<self.size-1:
            closest.append(self.grid[math.floor(pos[0])][math.ceil(pos[1])])
        if pos[0]<self.size-1 and pos[1]>0:
            closest.append(self.grid[math.ceil(pos[0])][math.floor(pos[1])]) 
        if pos[0]<self.size-1 and pos[1]<self.size-1:
            closest.append(self.grid[math.ceil(pos[0])][math.ceil(pos[1])])
        return(closest)
    def Diffusion(self,speed):
        for x in self.grid:
            for tile in x:
                tile.Diffuse()
        for x in self.grid:
            for tile in x:
                tile.density += (tile.nextDensity-tile.density)*speed
    def Advection(self):
        for x in self.grid:
            for tile in x:
                tile.Advect()
        for x in self.grid:
            for tile in x:
                tile.density = tile.nextDensity      

    def Render(self,pos,size):
        for x in self.grid:
            for tile in x:
                pygame.draw.rect(window, (tile.density*255,tile.density*255,tile.density*255), ([tile.pos[0]*size+pos[0],tile.pos[1]*size+pos[1]],[size,size]))

fluid = Fluid(10)
#fluid.Diffusion()
#fluid.Render([100,100],10)

running = True
while running:
    fluid.Diffusion(0.01)
    #fluid.Advection()
    fluid.Render([100,100],40)
    pygame.display.flip()

    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False

pygame.display.quit()