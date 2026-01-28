import pygame

MoveSpeed = 0.5

running = True

pygame.init()
WindowSize = 500
window = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("Fractals")

class Transform:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    def Move(self,x,y):
        self.x += x
        self.y += y
    def Rotate(self, degrees):
        self.direction += degrees
        if self.direction >= 360:
            self.direction = -1 + degrees 
        if self.direction < 0:
            self.direction = 361 + degrees
    def IsOnScreen(self, ScreenX, ScreenY, Size):
        if self.x > ScreenX and self.y > ScreenY and self.x < ScreenX+Size and self.y < ScreenY+Size:
            return(True)
        else:
            return(False)
    def RelativePos(self, ToX, ToY):
        return((self.x - ToX, self.y - ToY))

class ObjRenderer:
    def __init__(self, rgb, size, points, lines):
        self.rgb = rgb
        self.size = size
        self.points = points
        self.lines = lines
    def Render(self, pos, cam):
        for line in self.lines:
            pygame.draw.line(window,self.rgb, ((pos[0]*cam.z+self.points[line[0]][0]*self.size*cam.z+WindowSize/2),pos[1]*cam.z+self.points[line[0]][1]*self.size*cam.z+WindowSize/2 ), (pos[0]*cam.z+self.points[line[1]][0]*self.size*cam.z+WindowSize/2, pos[1]*cam.z+self.points[line[1]][1]*self.size*cam.z+WindowSize/2))

class Object(Transform, ObjRenderer):
    def __init__(self, x, y, direction, rgb, size, points, lines):
        Transform.__init__(self, x, y, direction)
        ObjRenderer.__init__(self, rgb, size, points, lines)
class Camera(Transform):
    def __init__(self,x,y,direction,z):
        Transform.__init__(self,x,y,direction)
        self.z = z


player = Object(0, 0, 90, (0,255,0), 15, [(-1,-1),(1,-1),(1,1),(-1,1)], [(0,1),(1,2),(2,3),(3,0),(0,2)])
pinochoto = Object(100, 100, 90, (0, 100, 0), 20, [(-1, 0), (1,0), (0, -2)], [(0,1), (1,2), (0,2)])
Objetos = [player,pinochoto]

cam1 = Camera(0, 0, 90,1)


#print(dir(player))
#print(player.points)

while running == True:
    for event in pygame.event.get():
        
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= MoveSpeed
    if keys[pygame.K_RIGHT]:
        player.x += MoveSpeed
    if keys[pygame.K_UP]:
        player.y -= MoveSpeed
    if keys[pygame.K_DOWN]:
        player.y += MoveSpeed
    if keys[pygame.K_s]:
        cam1.z *= 0.999
    if keys[pygame.K_w]:
        cam1.z /= 0.999

    window.fill((0, 0, 0))
#    print(player.IsOnScreen(cam1.x-WindowSize/2, cam1.x-WindowSize/2, WindowSize))
    for i in Objetos:
        i.Render(i.RelativePos(cam1.x,cam1.y),cam1)
    pygame.display.flip()

