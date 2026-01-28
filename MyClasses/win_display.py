import pygame

class Window:
    def __init__(self, size:tuple[int,int], name:str, FPS:int, flags=0, vsync=0):
        self.size, self.name, self.FPS, self.flags, self.vsync = size, name, FPS, flags, vsync
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(self.size, self.flags, self.vsync)
        pygame.display.set_caption(self.name)
    def Tick(self):
        self.clock.tick(self.FPS)