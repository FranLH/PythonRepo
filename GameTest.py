import pygame, time
import math


WindowW = 800
WindowH = 500


clock = pygame.time.Clock()

class Screen:
    def __init__(self, Width, Height):
        self.Width = Width
        self.Height = Height
        self.display = pygame.display.set_mode((self.Width, self.Height), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("GameTest.py")
class Mobile:
    def __init__(self, pos):
        self.pos = pos
    def Move(self, SpeedVec):
        self.pos[0] += SpeedVec[0]
        self.pos[1] += SpeedVec[1]
class NewGameBus:
    def __init__(self, MaxFrameTime):
        self.Bus = []
        self.Clock = pygame.time.Clock()
        self.MaxFrameTime = MaxFrameTime
        self.FrameTime = 0
    def Step(self):
        if len(self.Bus) != 0:
            exec(self.Bus[0])
            self.Bus.pop(0)
        
    def Frame(self):
        self.FrameTime = 0
        self.Clock.tick()
        while self.FrameTime < self.MaxFrameTime:
            self.Step()
            self.FrameTime += self.Clock.tick()
        pygame.draw.circle(screen.display, (255,0,0), box.pos, 5)
        pygame.display.flip()

     
running = True
FPSCap = 60
FPS = 0
dt = 0
screen = Screen(800,600)
GameBus = NewGameBus(1000/FPSCap)
box = Mobile([0,20])
while running:
    dt = clock.tick(FPSCap)
    FPS = clock.get_fps()
    GameBus.Bus.append("box.Move([1,0])")
    GameBus.Frame()
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False

pygame.display.quit()