import pygame
import math
import copy
# from typing import Self

class vec2:
    def __init__(self, x:int|float, y:int|float):
        self.x, self.y = x,y
    def __eq__(self, other):
        return(self.x==other.x and self.y==other.y)
    def __lt__(self, other:"vec2"): # <
        return(self.Length()<other.Length())
    def __gt__(self, other:"vec2"): # >
        return(self.Length()>other.Length())
    def __le__(self, other:"vec2"): # <=
        return(self.Length()<=other.Length())
    def __ge__(self, other:"vec2"): # >=
        return(self.Length()>=other.Length())
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
    def __init__(self, pos:vec2, nodes:int, segmentLengths:list[int|float], speed:int|float, MaxSpeed:int|float, MinSpeed:int|float, Size:int|float):
        self.pos, self.speed, self.MaxSpeed, self.MinSpeed, self.Size = pos, speed, MaxSpeed, MinSpeed, Size
        
        self.Segments = [] # List to store all the segments
        self.Nodes = [] # List to store all the nodes
        
        nodeY = self.pos.y # Keeps track of the nodes position so they are all the right distances apart, the tendril always starts hanging downwards
        for i in range(nodes): # Creates all the nodes
            self.Nodes.append(Node(vec2(self.pos.x,nodeY)))
            nodeY+=segmentLengths[min(i,len(segmentLengths)-1)]
            
        self.Start = self.Nodes[0] # The start of the tendril
        self.End = self.Nodes[-1] # The end,  or tip of the tendril
        
        self.Objective = self.End.pos # The 'Objective' variable holds the position that the tendril is trying to move towards
        
        for i in range(len(segmentLengths)): # Creates the segments that are between the nodes
            self.Segments.append(Segment(segmentLengths[i],self.Nodes[i],self.Nodes[i+1]))
            
        self.MaxLength = sum(segmentLengths) # The maximum extension of the tendril
    def Render(self):
        
#         for segment in self.Segments:
#             pygame.draw.line(window,(0,255,0), segment.nodeA.pos.ToList(), segment.nodeB.pos.ToList(),3)
        i = len(self.Nodes)
        for node in self.Nodes:
            pygame.draw.circle(window, (0,155,0), node.pos.ToList(), max(i/(len(self.Nodes)/self.Size), 2))
            i-=1
        #pygame.draw.circle(window, (255,0,0), self.Objective.ToList(), 4) # Renders the objective
        
    def Forwards(self,objective:vec2):
        if self.pos.Dist(objective)>2: # I can add a distance check here, so it doesn't keep trying when it has arrived at the objective
            if self.Objective.Dist(objective)>2:
                self.Objective -= (self.Objective - objective).Normalized() * min(max(self.speed * self.Objective.Dist(objective)/50, self.MaxSpeed), self.MinSpeed) # Moves the tendril's objective towards the 'real' objective, slowing down as it gets closer
                self.Objective = self.Start.pos + (self.Objective - self.Start.pos).Normalized() * min((self.Objective - self.Start.pos).Length(), self.MaxLength) # Prevents the objective from moving outside of the tendril's reach
                self.End.pos = self.Objective # Moves the end of the tendril to the objective
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
pygame.display.set_caption("Tendrils")

L1 = Limb(vec2(420,300),65,[2]*64, 4, 0.5, 4, 10)

L = Limb(vec2(180,300),165,[2]*164, 4, 0.5, 4, 10)
Limbs = [L1,L]
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



