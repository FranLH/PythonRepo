import pygame
import math

pygame.init()
WindowSize = 500
window = pygame.display.set_mode((WindowSize, WindowSize), pygame.DOUBLEBUF)
pygame.display.set_caption("")

running = True

class Rope():
    def __init__(self, color, nodes):
        self.color = color
        self.Nodes = []
        for i in nodes:
            n = Node(i)
            self.Nodes.append(n)
        
    def Draw(self):
        pygame.draw.circle(window, (255,255,255), (self.Nodes[0].x, self.Nodes[0].y), self.Nodes[0].radius, 1)
        for i in range(len(self.Nodes)-1):
            pygame.draw.line(window, r1.color, (self.Nodes[i].x, self.Nodes[i].y), (self.Nodes[i+1].x, self.Nodes[i+1].y), 1)
            pygame.draw.circle(window, (255,255,255), (self.Nodes[i+1].x, self.Nodes[i+1].y), self.Nodes[i+1].radius, 1)
    
    def Constrain(self):
        for i in range(len(self.Nodes)):
            if math.dist((self.Nodes[i].x, self.Nodes[i].y), (self.Nodes[i+1].x, self.Nodes[i+1].y)) > self.Nodes[i].radius:
                pass   
    
class Node():
    def __init__(self, vals):
        self.x = vals[0]
        self.y = vals[1]
        self.radius = vals[2]



r1 = Rope((255,0,0), ((50,100,50),(100,100,50)))

while running:
    window.fill((0,0,0))
    r1.Draw()
    pygame.display.flip()
    