import math
import pygame


class Position:
    def __init__(self,x,y,z,ax,ay):
        self.x, self.y, self.z, self.ax, self.ay = x, y, z, ax, ay
    def Rotatex(self, angle, originx, originz):
        ox = self.x-originx
        oz = self.z-originz
        return([ox*math.cos(angle)+oz*math.sin(angle), ox*-1*math.sin(angle)+oz*math.cos(angle)])
    def Rotatey(self, angle, originx, originy, originz):
        oxz = math.dist([self.x-originx],[self.z-originz])
        oy = self.y-originy
        return([oy*math.cos(angle)+oxz*math.sin(angle), oy*-1*math.sin(angle)+oxz*math.cos(angle)])
class Point(Position):
    def __init__(self,x,y,z,color):
        Position.__init__(self,x,y,z,0,0)
        self.color = color
    def Draw(self):
        global cam, MainCanvas
        rotatedx = self.Rotatex(math.radians(-1*cam.ax), cam.x, cam.z)
        x = cam.screenDist*rotatedx[0]/rotatedx[1]
#         print(x)
        rotatedy = self.Rotatey(math.radians(-1*cam.ay), cam.x, cam.y, cam.z)######
        y = cam.screenDist*rotatedy[0]/rotatedx[1]
        pygame.draw.circle(MainCanvas.screen, self.color, (x/cam.screenSize[0]*MainCanvas.Width,y/cam.screenSize[1]*MainCanvas.Height), 1)
class Camera(Position):
    def __init__(self,x,y,z,ax,ay,FOV,screenDist):
        Position.__init__(self,x,y,z,ax,ay)
        self.FOV, self.screenDist = FOV, screenDist
        self.screenSize = [2*math.tan(FOV/2)*screenDist, 2*math.tan(30)*screenDist]
class Canvas:
    def __init__(self, Width, Height):
        self.Width, self.Height = Width, Height
        self.screen = pygame.display.set_mode((self.Width, self.Height), pygame.DOUBLEBUF, 32)
        
cam = Camera(0,0,0,1,0,90,10)
p1 = Point(50,0,0,(255,0,0))
MainCanvas = Canvas(800,600)

pygame.init()

pygame.display.set_caption("3D_Viewer")
running = True
while running:
    cam.ax+=1
    if cam.ax==180:
        cam.ax = -180
    elif cam.ax==0:
        cam.ax = 1
    
    #print(cam.ax)
    p1.Draw()
    pygame.display.flip()

    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False

pygame.display.quit()