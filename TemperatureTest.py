import pygame
import math

pygame.init()

WindowSize = 400

window = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("Temperature Test")


Temperature = []
def InitTilemap(tilemap, InitType):
    for x in range(WindowSize):
        tilemap.append([])
        for j in range(WindowSize):
            tilemap[x].append(0)
            
    # Gradient
    if InitType == 1:
        for x in range(len(tilemap)):
            for y in range(len(tilemap[x])):
                tilemap[x][y] = y
    elif InitType == 2:
        for x in range(len(tilemap)):
            for y in range(len(tilemap[x])):
                if math.dist((x,y),(0,0))<10:
                    tilemap[x][y] = 600-(math.dist((x,y),(0,0))/10)*600
                else:
                    tilemap[x][y] = 0
def CalcColor(value, mode):
    # Monochromatic from 0 to 600
    maxim = 600
    if value > maxim:
        maxim = value
    if mode == 0:
        col = round((value/maxim)*255)
        return((col,col,col))
    
    # Temperature gradient from 0F to 600F
    elif mode == 1:
        T = value/maxim
        if T <= 0.5:
            T = T/0.5
            R = T*255
            G = 100+T*155
            B = 255
        else:
            T = (T-0.5)/0.5
            R = 255
            G = 255-T*155
            B = 255-T*255
        if math.isnan(R) or math.isnan(G) or math.isnan(B):
            return(255,100,0)
        else:
            return((round(R),round(G),round(B)))

def DrawTilemap(tilemap):
    for x in range(len(tilemap)):
        for y in range(len(tilemap[x])):
            pygame.draw.line(window, CalcColor(tilemap[x][y],1), (x,y), (x,y))

def DrawTiles(tiles):
    for tile in tiles:
        pygame.draw.line(window, tile[2], (tile[0],tile[1]), (tile[0],tile[1]))
    pygame.display.flip()

def StabilizeTemp(tilemap,x,y):
    AdjTiles = []
    if x != 0:
        AdjTiles.append((tilemap[x-1][y],x-1,y))
    if x != WindowSize-1:
        AdjTiles.append((tilemap[x+1][y],x+1,y))
    if y != 0:
        AdjTiles.append((tilemap[x][y-1],x,y-1,))
    if y != WindowSize-1:
        AdjTiles.append((tilemap[x][y+1],x,y+1))
#    print(AdjTiles)
    a = tilemap[x][y]
    for i in AdjTiles:
        a+= i[0]
    if a/(len(AdjTiles)+1) != tilemap[x][y]:
        AdjTiles.sort()

        for tile in range(len(AdjTiles)):
            # If the tile has a higher temperature
            if AdjTiles[tile][0] > tilemap[x][y]:
                stable = (AdjTiles[tile][0] + tilemap[x][y])/2
                tilemap[AdjTiles[tile][1]][AdjTiles[tile][2]], tilemap[x][y] = stable, stable

            # If it has a lower temperature
            else:
                stable = tilemap[x][y]
                for i in range(tile,len(AdjTiles)):
                    stable += AdjTiles[i][0]
                stable = stable/(len(AdjTiles)+1-tile)
                tilemap[x][y] = stable
                for i in range(tile,len(AdjTiles)):
                    tilemap[AdjTiles[i][1]][AdjTiles[i][2]] = stable
            
InitTilemap(Temperature,2)
DrawTilemap(Temperature)
pygame.display.flip()

print(Temperature[WindowSize-1][WindowSize-1])
print(Temperature)


running = True
iterations = 0
while running:
    for x in range(len(Temperature)):
        for y in range(len(Temperature[x])):
            StabilizeTemp(Temperature,x,y)
    DrawTilemap(Temperature)
    if iterations%1 == 0:
        pygame.display.flip()
    # Check for events
    for event in pygame.event.get():
        
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
    if iterations == 100:
        print(Temperature)
    iterations+=1


pygame.display.quit()

