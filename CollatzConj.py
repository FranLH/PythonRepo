import pygame
import math

pygame.init()

WindowW = 800
WindowH = 500

window = pygame.display.set_mode((WindowW, WindowH), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("CollatzConj")
camX = 400
camY = 480
camZ = 1
longest = (0,0)
def CalcHeight(x,maxIt):
    global longest
    its = 0
    num = x
    while its<maxIt and num != 1:
        if num%2 == 0:
            num = num/2
        else:
            num = 3*num + 1
        its+=1
    if its > longest[1]:
        longest = (x,its)
    return -1*its
def Render(x,y,z):
    for X in range(800):
        pygame.draw.line(window, (255,255,255), (X*z,y/z), (X*z,(y+CalcHeight(camX+X*z-WindowW/2,1000))/z))
running = True
its = 0
while running:
    window.fill((0,0,0))
    Render(camX,camY,camZ)
    pygame.display.flip()
    if its % 100 == 0:
        print(longest)
    camY+=0
    camX+=5
    #camZ+=0.01
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
    its += 1
pygame.display.quit()