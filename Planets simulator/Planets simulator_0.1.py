# Added some basic physics
import math
import pygame

pygame.init()

WindowSize = 600

window = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("Planets")

MoveSpeed = 1

Cam = {
    "X" : 0,
    "Y": 0,
    "Z": 0.2
    }
class Planet:
    def __init__(self, Name, X, Y, Size, Gravity, VX, VY):
        self.Name = Name
        self.X = X
        self.Y = Y
        self.Size = Size
        self.Gravity = Gravity
        self.VX = VX
        self.VY = VY

PlanetsROM = [
    ["Earth", 147190, 0, 13, 9.807, 0, 5],
    ["Sun", 0, 0, 1417, 274, 0, 0],
    ["Moon", 147574.4, 0, 3.5, 1.62, 0, 6]
    ]

Planets = []

def Render():
    window.fill((0, 0, 0))    
    for i in Planets:
        pygame.draw.circle(window, (0,0,255), ((i.X*Cam["Z"] - Cam["X"]*Cam["Z"])+WindowSize/2, (i.Y*Cam["Z"] - Cam["Y"]*Cam["Z"])+WindowSize/2), max(i.Size * Cam["Z"], 1))

    pygame.display.flip()

def CalcNewPos():
    for i in Planets:
        i.X = i.X + i.VX
        i.Y = i.Y + i.VY
        PosVec = pygame.Vector2(i.X, i.Y)
        for j in Planets:
            if j != i:
                OtherVec = pygame.Vector2(j.X, j.Y)
                i.VX = i.VX + (PosVec.move_towards(OtherVec, j.Gravity/math.dist(PosVec,OtherVec)) - PosVec)[0]
                i.VY = i.VY + (PosVec.move_towards(OtherVec, j.Gravity/math.dist(PosVec,OtherVec)) - PosVec)[1]    
    
def Init():
    for i in PlanetsROM:
        i[0] = Planet("{0}".format(i[0]), i[1], i[2], i[3], i[4], i[5], i[6])
        Planets.append(i[0])
    Render()    

Init()

running = True

while running == True:
    for event in pygame.event.get():
        
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
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
    if keys[pygame.K_e]:
        Cam["X"] = Planets[0].X
        Cam["Y"] = Planets[0].Y
    CalcNewPos()
    Render()
    pygame.time.wait(1)


















pygame.display.quit()
