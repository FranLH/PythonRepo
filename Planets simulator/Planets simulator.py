import pygame

pygame.init()

WindowSize = 600

window = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("Planets")

MoveSpeed = 1

Cam = {
    "X" : 0,
    "Y": 0,
    "Z": 2
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
    ["Earth", 100, 100, 50, 5, 0, 0],
    ["Mars", 600, 600, 90, 5, 0, 0]
    ]

Planets = []

def Render():
    window.fill((0, 0, 0))    
    for i in Planets:
        pygame.draw.circle(window, (0,0,255), ((i.X*Cam["Z"] - Cam["X"]*Cam["Z"])+WindowSize/2, (i.Y*Cam["Z"] - Cam["Y"]*Cam["Z"])+WindowSize/2), i.Size * Cam["Z"])

    pygame.display.flip()

    
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
    Render()
    pygame.time.wait(1)


















pygame.display.quit()
