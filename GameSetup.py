import pygame
UpdatesPerFrame = 10
running = True


def Start():
    pygame.init()
    WindowSize = 500
    window = pygame.display.set_mode((WindowSize, WindowSize))
    pygame.display.set_caption("Fractals")

def Update():
    pygame.display.flip()

    
    
def FixedUpdate():
    for event in pygame.event.get():
        
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()

    return()
    




Start()
while running == True:
    FixedUpdate()
    
