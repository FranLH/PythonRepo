import pygame
import copy
import math

pygame.init()
WindowSize = (1200,600)
window = pygame.display.set_mode(WindowSize,pygame.RESIZABLE)
pygame.display.set_caption("PyCharts")



# ---FONTS--- #
CSMS = 'Comic Sans MS'
# ----------- #



def Render(OBJS):
    window.fill((255,255,255))
    for OBJ in OBJS:
        OBJ.render()
    pygame.display.flip()

class Text:
    def __init__(self, contents, pos, color, size, font):
        self.contents = contents
        self.pos = pos
        self.color = color
        self.size = size
        self.font = font
        self.dimensions = pygame.font.Font.size(pygame.font.SysFont(self.font, self.size), self.contents)
    def render(self):
        New_font = pygame.font.SysFont(self.font, self.size)
        text = New_font.render(self.contents, False, self.color)
        window.blit(text, self.pos)
class Graph:
    def __init__(self, xy_names, xy_mults, contents, pos, bg):
        self.xy_names = xy_names
        self.xy_mults = xy_mults
        self.contents = contents
        self.pos = pos
        self.bg = bg
    def Get_size(self):
        y_values = list(copy.deepcopy(self.contents[1]))
        y_values.sort()
        y_max = y_values[len(y_values)-1]/self.xy_mults[1]
        
        x_values = list(copy.deepcopy(self.contents[0]))
        x_values.sort()
        x_max = x_values[len(x_values)-1]/self.xy_mults[0]        
        return(round(x_max), round(y_max))
    def render(self):
        size = self.Get_size()
        pygame.draw.rect(window,self.bg, ((self.pos[0]-math.ceil(1/self.xy_mults[0])/2,self.pos[1]-size[1]), (size[0]+math.ceil(1/self.xy_mults[0]+1),size[1]+1)))
        for data in range(len(self.contents[0])):
            x = self.pos[0]+self.contents[0][data]/self.xy_mults[0]
            y = self.pos[1]
            pygame.draw.line(window, (255,0,0), (x,y),(x,y-self.contents[1][data]/self.xy_mults[1]), math.ceil(1/self.xy_mults[0]))

T1 = Text("Hello World", (0,0), (0,0,0), 20, CSMS)
G1 = Graph(("x","y"), (1,0.5), ((0,1,2,3,5,10,12,20,40,55,78),(5,5,5,5,20,45,13,59,24,9,32)), (50,200), (200,200,200))
Objects = [T1, G1]
print(G1.Get_size())


running = True
while running:
    Render(Objects)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
       
pygame.display.quit()