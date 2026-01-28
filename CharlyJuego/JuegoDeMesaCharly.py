import pygame
import math
import random


# TO DO:
# Limit the framerate to ~60FPS
# ------Moves per turn randomizer
# Text box For the amount of moves you have remaining
# Button to roll the moves dice
# ------Only allow valid moves
# Make it so you can't stack on enemy's color
# Make it so you can't jump over pieces
# Limit stack size to 6
# Add shooting?:
    # button to toggle aiming/moving
    # shooting range depends on height of stack, shooting ends your turn
    # can only shoot opposite color
    # delete pieces that get shot. (The topmost one on the stack)



# 120/72
# Relation = 5/3

TILESIZE = 90
WindowSize = [800,800]

IMAGES = {
"BLANCA" : pygame.transform.scale(pygame.image.load("ThinBlanca.png"), [TILESIZE,TILESIZE*3/5]),
"NEGRA" : pygame.transform.scale(pygame.image.load("ThinNegra.png"), [TILESIZE,TILESIZE*3/5]),
"CLARO" : pygame.transform.scale(pygame.image.load("LightTile.png"), [TILESIZE, TILESIZE]),
"OSCURO" : pygame.transform.scale(pygame.image.load("DarkTile.png"), [TILESIZE, TILESIZE]),
"SELECTEDB" : pygame.transform.scale(pygame.image.load("SelectedBlanca.png"), [TILESIZE,TILESIZE*3/5]),
"SELECTEDN" : pygame.transform.scale(pygame.image.load("SelectedNegra.png"), [TILESIZE,TILESIZE*3/5])
}

"""
8x8
[o][o][o][ ][ ][ ][ ][ ]
[o][o][o][ ][ ][ ][ ][ ]
[o][o][o][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][O][O][O]
[ ][ ][ ][ ][ ][O][O][O]
[ ][ ][ ][ ][ ][O][O][O]

"""

class Tablero:
    def __init__(self, pos:[int]):
        self.moves = random.randint(1,6)
        self.whitesTurn = True
        self.IMAGES, self.TILESIZE = IMAGES, TILESIZE
        self.pos = pos
        self.hand = []
        self.handSurface = pygame.Surface(WindowSize, pygame.SRCALPHA)
        self.selected = []
        self.tablero = []
        for i in range(8):
            self.tablero.append([])
            for j in range(8):
                self.tablero[i].append([])

        pos = [0,0]
        color = 0
        for i in range(2):
            for x in range(3):
                for y in range(3):
                    self.tablero[x+pos[0]][y+pos[1]].append(color)
            pos=[5,5]
            color=1
    def __repr__(self):
        longest = 1
        for i in self.tablero:
            for j in i:
                if len(j)>longest:
                    longest = len(j)
        string = ""
        for x in range(len(self.tablero)):
            for y in range(len(self.tablero)):
                for piece in self.tablero[x][y]:
                    string+=str(piece)
                if self.tablero[x][y] == []:
                    #string+=" "
                    pass
                string += "."*(longest-len(self.tablero[x][y]))
            string+="\n"
        return string
    
    def Move(self, start,end):

        if start[2] == 0:
            costo = len(self.tablero[start[0]][start[1]])*math.dist(start[:2],end[:2])
            if costo <= self.moves:
                
                pieces = self.tablero[start[0]][start[1]]
                self.tablero[start[0]][start[1]] = []
                self.tablero[end[0]][end[1]] = pieces
                self.moves -= costo

        else:
            costo = math.dist(start[:2],end[:2])

            if costo <= self.moves:
                pieces = self.tablero[start[0]][start[1]][start[2]]
                self.tablero[start[0]][start[1]].pop(-1)
                self.tablero[end[0]][end[1]] = [pieces]
                self.moves-=costo
            

        
    def Stack(self, start,end):
        costo = max(len(self.tablero[end[0]][end[1]]) - len(self.tablero[start[0]][start[1]]) +1, 1)
        if costo <= self.moves:
            piece = self.tablero[start[0]][start[1]].pop(-1)
            self.tablero[end[0]][end[1]].append(piece)
            self.moves-=costo
        

    def Action(self, start, end):
        if start != end and (start[0]==end[0] or start[1]==end[1]): # If you are moving orthagonally and not placing the piece back where it was
            if self.tablero[end[0]][end[1]] == []:
                self.Move(start,end)
            elif len(self.hand) == 1 and math.dist(start[:2],end[:2]) == 1:
                self.Stack(start,end)
                
            if self.moves == 0:
                self.moves = random.randint(1,6)
                self.whitesTurn = not self.whitesTurn
                if self.whitesTurn:
                    print("White's turn.", self.moves, "moves")
                else:
                    print("Black's turn.", self.moves, "moves")
            else:
                print("You have", int(self.moves), "move"+"s"*int(self.moves!=1) +" remaining")

                
            #self.whitesTurn = not self.whitesTurn
            
    def CheckPieces(self, piece):
        return True in list(map(lambda row:piece in list(map(lambda a:piece in a,row)), self.tablero))
    def Render(self, window, selection, mousePos):
        if selection == [] or selection[0] > 7 or selection[0] < 0 or selection[1] > 7 or selection[1] < 0:
            selection = []
        surface = pygame.Surface(window.get_size())
        blitsList = []
        pieceHeight = self.TILESIZE*3/5
        
        for x in range(8):
            for y in range(8):
                # Draws the board tiles
                if (x+y)%2==0:
                    blitsList.append((self.IMAGES["CLARO"],(x*self.TILESIZE,y*self.TILESIZE)))
                else:
                    blitsList.append((self.IMAGES["OSCURO"],(x*self.TILESIZE,y*self.TILESIZE)))
                    
                height = pieceHeight # Current height of the piece
                for piece in range(len(self.tablero[x][y])):
                    if not (self.selected == [x,y,piece] or self.selected == [x,y,0]): # Si la pieza esta en la mano

                        if self.tablero[x][y][piece] == 0: # Blanca
                            if selection != [] and [x,y] == selection[:2] and (selection[2] == 0 or piece == selection[2]): # Si esta seleccionada
                                blitsList.append((self.IMAGES["SELECTEDB"],(x*self.TILESIZE,(y+1)*self.TILESIZE-height)))
                            else:
                                blitsList.append((self.IMAGES["BLANCA"],(x*self.TILESIZE,(y+1)*self.TILESIZE-height)))
                        else: # Negra
                            if selection != [] and [x,y] == selection[:2] and (selection[2] == 0 or piece == selection[2]): # Si esta seleccionada
                                blitsList.append((self.IMAGES["SELECTEDN"],(x*self.TILESIZE,(y+1)*self.TILESIZE-height)))
                            else:
                                blitsList.append((self.IMAGES["NEGRA"],(x*self.TILESIZE,(y+1)*self.TILESIZE-height)))
                    height+=self.TILESIZE/10

        blitsList.append((self.handSurface, (mousePos[0]-self.TILESIZE,mousePos[1]-len(self.hand)*self.TILESIZE/10-pieceHeight*1.5))) # Dibuja las fichas seleccionadas
                    
        surface.blits(blitsList)
        window.blit(surface, self.pos)
        pygame.display.flip()
        

tab = Tablero([40,40])


pygame.init()



window = pygame.display.set_mode(WindowSize, pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption("Juego de mesa Charly")

mouseSelection = []
running = True
while running:

    MousePos = pygame.mouse.get_pos()
    #pygame.mouse.set_pos(300,300)
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            newSelection = [math.floor((MousePos[0] - tab.pos[0])/tab.TILESIZE), math.floor((MousePos[1] - tab.pos[1])/tab.TILESIZE), 0]
            if newSelection[0] >= 0 and newSelection[0] < 8 and newSelection[1] >= 0 and newSelection[1] < 8:
                if mouseSelection == []: # Selects a new piece
                    if tab.tablero[newSelection[0]][newSelection[1]] != [] and (tab.tablero[newSelection[0]][newSelection[1]][0] == 0) == tab.whitesTurn: # If it is your turn
                        mouseSelection = newSelection
                        tab.hand = tab.tablero[mouseSelection[0]][mouseSelection[1]] # The pieces that are now in your hand
                        height = len(tab.tablero[mouseSelection[0]][mouseSelection[1]])-1 # The amnount of pieces in the tile
                        if height > 0:
                            
                            selectedPiece = 9-math.floor((MousePos[1] - tab.pos[1] - mouseSelection[1]*tab.TILESIZE)/(tab.TILESIZE/10))
                            if height <= selectedPiece:
                                mouseSelection[2]=(height)
                                tab.hand = [tab.tablero[mouseSelection[0]][mouseSelection[1]][mouseSelection[2]]]
                        tab.selected = mouseSelection # The original locaiton of those pieces
                        
                        # Stores the pieces held in a separate surface
                        pieceHeight = TILESIZE*3/5
                        height = pieceHeight
                        blitsList = []
                        for piece in tab.hand:
                            if piece == 0: # Blanca
                                blitsList.append((IMAGES["SELECTEDB"],(0,(len(tab.hand)*tab.TILESIZE/10+tab.TILESIZE/2)-height)))
                            else:
                                blitsList.append((IMAGES["SELECTEDN"],(0,(len(tab.hand)*tab.TILESIZE/10+tab.TILESIZE/2)-height)))
                            height+=TILESIZE/10
                        tab.handSurface.fill((0,0,0,0))
                        tab.handSurface.blits(blitsList)
                        
                    
                else: # Drops the selected piece
                    tab.Action(tab.selected, newSelection)
                    tab.selected = []
                    tab.hand = []
                    mouseSelection = []
                    tab.handSurface.fill((0,0,0,0))
                    


        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False
        
    window.fill((0, 0, 0))
    tab.Render(window, mouseSelection, MousePos)

pygame.display.quit()

    



    

