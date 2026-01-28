import pygame

pygame.init()
WindowSize = (600,600)
window = pygame.display.set_mode(WindowSize,pygame.RESIZABLE)
pygame.display.set_caption("Game")

cam = [0,0,200]

def Iteration(c,z):
    Z = ((z[0]*z[0]-z[1]*z[1])+c[0],(z[0]*z[1]+z[1]*z[0])+c[1])
    return(Z)

def IsInside(point,depth):
    z = Iteration(point,(0,0))
    for it in range(2,depth-2):
        z = Iteration(point,z)
        if z[0]>2 or z[1]>2:
            return(it)
    return(0)
def Calculate(windowSize,depth):
    image = []
    for x in range(windowSize):
        image.append([])
        for y in range(windowSize):
            image[x].append(IsInside(((x-windowSize/2)/cam[2]+cam[0],(y-windowSize/2)/cam[2]+cam[1]),depth))
    return(image)
#image = []
#for x in range(-300,300):
#    image.append([])
#    for y in range(-300,300):
#        image[x+300].append(IsInside((x/300,y/300),100))
#print(image)
image = Calculate(600,100)
for x in range(600):
    for y in range(600):
        if image[x][y] == 0:
            pygame.draw.line(window,(0,255,0),(x,y),(x,y),1)
pygame.display.flip()


running = True
while running:

    # Check for events
    for event in pygame.event.get():
        
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
    


           
pygame.display.quit()