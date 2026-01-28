# Made all the planets calculations happen at the same time
import math
import pygame

ConstG = 0.06

SimSpeed = 1

pygame.init()

WindowSize = 600

window = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("Planets")

Following = 2

Centered = 1

Cam = {
    "X" : 0,
    "Y": 0,
    "Z": 0.02
    }
class Planet:
    def __init__(self, Name, X, Y, Size, Mass, VX, VY, Color):
        self.Name = Name
        self.X = X
        self.Y = Y
        self.Size = Size
        self.Mass = Mass
        self.VX = VX
        self.VY = VY
        self.Color = Color

PlanetsROM = [
     ["Earth", 1600, 0, 30, 16, 0, -0.8, (0,255,20)],
     ["Arth", 0, 0, 24, 16, 0, 1, (0,0,240)],
     ["Berth", 500, 0, 128, 200, 0, 0, (240,0,240)],
#     ["Earth", 147190, 0, 13, 9.807, 0, 1, (0,0,240)],
#     ["Sun", 0, 0, 1417, 400000, 0, 0, (240,240,50)],
#     ["Moon", 147574.4, 0, 3.5, 1.62, 0, 1.06, (100,100,100)],
#     ["Mercury", 46001, 0, 4.879, 3.7, 0, 1, (100,0,0)],

]

Planets = []

def Render():
    window.fill((0, 0, 0))    
    for i in Planets:
        pygame.draw.circle(window, i.Color, ((i.X*Cam["Z"] - Cam["X"]*Cam["Z"])+WindowSize/2, (i.Y*Cam["Z"] - Cam["Y"]*Cam["Z"])+WindowSize/2), max(i.Size * Cam["Z"], 1))

    pygame.display.flip()

def CalcNewPos():
    for i in Planets:
        PosVec = pygame.Vector2(i.X, i.Y)
        for j in Planets:
            if j != i:
                OtherVec = pygame.Vector2(j.X, j.Y)
                AddForce = PosVec.move_towards(OtherVec, SimSpeed*ConstG*((j.Mass*i.Mass)/(math.dist(PosVec,OtherVec)*math.dist(PosVec,OtherVec))))
                i.VX = i.VX + AddForce[0] - PosVec[0]    
                i.VY = i.VY + AddForce[1] - PosVec[1]
    for i in Planets:
        i.X = i.X + i.VX
        i.Y = i.Y + i.VY
def Init():
    for i in PlanetsROM:
        i[0] = Planet("{0}".format(i[0]), i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        Planets.append(i[0])
    Render()    

Init()



running = True

window.fill((0, 0, 0)) 

while running == True:
    for event in pygame.event.get():
        
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Following -=1
            if event.key == pygame.K_d:
                Following +=1
            if event.key == pygame.K_c:
                Centered *= -1
            if Following > len(Planets)-1:
                Following = 0
            if Following < 0:
                Following = len(Planets)-1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        Cam["X"] -= 1/Cam["Z"]
    if keys[pygame.K_RIGHT]:
        Cam["X"] += 1/Cam["Z"]
    if keys[pygame.K_UP]:
        Cam["Y"] -= 1/Cam["Z"]
    if keys[pygame.K_DOWN]:
        Cam["Y"] += 1/Cam["Z"]
    if keys[pygame.K_s]:
        Cam["Z"] *= 0.999
    if keys[pygame.K_w]:
        Cam["Z"] /= 0.999
#    if keys[pygame.K_e]:


    if Centered == 1:
        Cam["X"] = Planets[Following].X
        Cam["Y"] = Planets[Following].Y

    CalcNewPos()
    Render()
#    pygame.time.wait(1)


















pygame.display.quit()
