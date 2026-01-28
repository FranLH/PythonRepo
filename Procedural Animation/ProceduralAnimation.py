import pygame
import math
import copy
# from typing import Self

class vec2:
    def __init__(self, x:int|float, y:int|float):
        self.x, self.y = x,y
    def __eq__(self, other):
        return(self.x==other.x and self.y==other.y)
    def __add__(self, other):
        return(vec2(self.x+other.x,self.y+other.y))
    def __sub__(self, other):
        return(vec2(self.x-other.x,self.y-other.y))
    def __mul__(self, other):
        match str(type(other))[8:-2].replace("__main__.",""):
            case "vec2":
                return(vec2(self.x*other.x,self.y*other.y))
            case "int":
                return(vec2(self.x*other,self.y*other))
            case "float":
                return(vec2(self.x*other,self.y*other))
    def __truediv__(self, other):
        match str(type(other))[8:-2].replace("__main__.",""):
            case "vec2":
                return(vec2(self.x/other.x,self.y/other.y))
            case "int":
                return(vec2(self.x/other,self.y/other))
            case "float":
                return(vec2(self.x/other,self.y/other))
    def __repr__(self):
        return("("+str(self.x)+","+str(self.y)+")")
    def Length(self):
        return(math.sqrt(self.x**2 + self.y**2))
    def Normalize(self):
        angle = math.atan2(self.x,self.y)
        self.contents = [math.sin(angle),math.cos(angle)]
    def Normalized(self):
        angle = math.atan2(self.x,self.y)
        return(vec2(math.sin(angle),math.cos(angle)))
    def Dist(self,other:"vec2"):
        return(math.dist([self.x,self.y],[other.x,other.y]))
    def ToList(self):
        return([self.x,self.y])
        
class Node:
    def __init__(self, pos:vec2):
        self.pos = pos
    def __repr__(self):
    
        return(str(self.pos))
class Segment:
    def __init__(self, length:int|float, nodeA:Node, nodeB:Node):
        self.length, self.nodeA, self.nodeB = length, nodeA, nodeB
    def __repr__(self):
        return(str([self.nodeA,self.nodeB]))
class Limb:
    def __init__(self, pos:vec2, nodes:int, segmentLengths:list[int|float]):
        self.pos = pos
        self.Segments = []
        self.Nodes = []
        nodeY = self.pos.y
        for i in range(nodes):
            self.Nodes.append(Node(vec2(self.pos.x,nodeY)))
            nodeY+=segmentLengths[min(i,len(segmentLengths)-1)]
        self.Start = self.Nodes[0]
        self.End = self.Nodes[-1]
        for i in range(len(segmentLengths)):
            self.Segments.append(Segment(segmentLengths[i],self.Nodes[i],self.Nodes[i+1]))
    def Render(self):
        
        for segment in self.Segments:
            pygame.draw.line(window,(0,255,0), segment.nodeA.pos.ToList(), segment.nodeB.pos.ToList(),3)
        for node in self.Nodes:
            pygame.draw.circle(window, (0,155,0), node.pos.ToList(), 6)
        
    def Forwards(self,objective:vec2):
        if True:
            self.End.pos = objective
            for segment in range(len(self.Segments)-1,-1,-1):
                
                # Moves the node in the segments to the desired positions
                self.Segments[segment].nodeA.pos = self.Segments[segment].nodeB.pos + (self.Segments[segment].nodeA.pos - self.Segments[segment].nodeB.pos).Normalized()*self.Segments[segment].length

            self.Backwards()
    def Backwards(self):
        self.Start.pos = self.pos
        for segment in range(len(self.Segments)):
                # Moves the node in the segments to the desired positions
                self.Segments[segment].nodeB.pos = self.Segments[segment].nodeA.pos + (self.Segments[segment].nodeB.pos - self.Segments[segment].nodeA.pos).Normalized()*self.Segments[segment].length


pygame.init()
clock = pygame.time.Clock()
WindowSize = (600,600)
window = pygame.display.set_mode(WindowSize, pygame.HWSURFACE, vsync=1)
pygame.display.set_caption("Procedural Animation")

L1 = Limb(vec2(420,300),5,[45,37,30,22])
L = Limb(vec2(180,300),5,[45,37,30,22])
Limbs = [L,L1]
#L.Backwards()
#print(vec2(23,45)/2)

running = True
FPS = 60
x = 2
MousePos = [400,400]
while running:

    window.fill((0,0,0))
    MousePos = pygame.mouse.get_pos()
    for limb in Limbs:
        for i in range(1):
            limb.Forwards(vec2(MousePos[0],MousePos[1]))
        limb.Render()
    pygame.display.flip()
    
    for event in pygame.event.get():
        MousePos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    x-=2
pygame.display.quit()
exit()



