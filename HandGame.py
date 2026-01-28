import pygame
import copy
StartPos = [[1,1],[1,1],0]

def FixAddition(pos):
    for player in range(2):
        for hand in range(2):
            if pos[player][hand]>4:
                pos[player][hand] = 0
#    return(pos)
def GetValidMoves(pos):
    Moves = []
    if 0 in pos[pos[2]] and (2 in pos[pos[2]] or 4 in pos[pos[2]]):
        copied = copy.deepcopy(pos)
        for hand in range(2):
            if pos[pos[2]][hand]!=0:
                copied[copied[2]] = [round(pos[pos[2]][hand]/2),round(pos[pos[2]][hand]/2)]
        Moves.extend(GetValidMoves(copied))
    for hand in range(1+(pos[pos[2]][0]!=pos[pos[2]][1])):
        if pos[pos[2]][hand] != 0:
            for opphand in range(1+(pos[1-pos[2]][0]!=pos[1-pos[2]][1])):
                if pos[1-pos[2]][opphand] != 0:
                    Moves.append(copy.deepcopy(pos))
                    Moves[-1][1-pos[2]][opphand]+=pos[pos[2]][hand]
                    Moves[-1][2] = 1-Moves[-1][2]
                    FixAddition(Moves[-1])
    
    return(Moves)

movesList = []
orderMoves = []
def AllPlays(depth,moves):
    global movesList, orderMoves
    finals = []
    its = 0
    for pos in moves:
        if [0,0] not in pos:
            valids = GetValidMoves(pos)
            for valid in valids:
                if valid not in movesList and valid not in finals:
                    finals.append(valid)
                    its+=1
                    
    if its>200:
        print(movesList)
    if its>0:
        movesList.extend(finals)
        orderMoves.extend(map(lambda pos:[depth,pos], finals))
        AllPlays(depth+1,movesList)

AllPlays(0, [[[1,1],[1,1],0]])
print(len(movesList))
print(movesList)
orderMoves.sort()
print(orderMoves)

out = ""
for move in range(len(movesList)):
    out+=str(movesList[move]).replace("[","").replace("]","").replace(", ","-")+", "
    for char in str(movesList[move]):
        
        if char != "[" and char != "]":
            out+=char
    out+="\n"
print(out)

pygame.init()
window = pygame.display.set_mode((800,800), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Simulation")

running = True

for move in movesList:
    pygame.draw.circle(window, (255,255,255), (40+move[0][0]*10+move[0][1]*200+move[2]*20, 40+move[1][0]*10+move[1][1]*20), move[2]*10, 1)
pygame.display.flip()
while running:


    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False

pygame.display.quit()
