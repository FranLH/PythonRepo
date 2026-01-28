import pygame
import math

pygame.init()

WindowSize = 640
TileSize = 32

window = pygame.display.set_mode((WindowSize, WindowSize), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("GridTest")

Tileset = pygame.image.load('Tileset.png')

Floor = pygame.Surface((WindowSize, WindowSize), pygame.SRCALPHA, 32)
Floor.fill((0,150,250,255))

Floor.blit(Tileset, (0,0), (0,0,TileSize, TileSize))
window.blit(Floor, (0,0))
pygame.display.flip()

FloorGrid = []
def InitGrid(tilemap, GridSize):
    for x in range(GridSize[0]):
        tilemap.append([])
        for j in range(GridSize[1]):
            tilemap[x].append(0)

running = True
while running:

    # Check for events
    for event in pygame.event.get():
        
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False


pygame.display.quit()
