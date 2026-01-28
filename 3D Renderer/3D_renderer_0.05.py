import pygame
import math
class point:
    def __init__(self,x,y,z):
        self.x, self.y, self.z = x, y, z

#   x
# 1 0 0    x = x
# 0 c -s   y = y*cX + z*-sX
# 0 s c    z = y*sX + z*cX

#   y
# c 0 s    x = x*cY + z*sY
# 0 1 0    y = y
# -s 0 c   z = x*-sY + z*cY

#   z
# c -s 0   x = x*cY + y*-sY
# s c 0    y = x*sY + y*cY
# 0 0 1    z = z

#x = (x*cY + (y*sX + z*cX)*sY)*cY + (y*cX + z*-sX)*-sY
#y = (x*cY + (y*sX + z*cX)*sY)*sY + (y*cX + z*-sX)*cY
#z = x*-sY + (y*sX + z*cX)*cY

#x = (x*c + (y*sX + z*cX)*s)*c + (y*cX + z*-sX)*-s 
#y = (x*c + (y*sX + z*cX)*s)*s + (y*cX + z*-sX)*c
#z = x*-s + (y*s + z*c)*c

FL = 540
MoveSpeed = 0.1
RotSpeed = 0.001
CamPos = point(0,0,0)
CamRotation = point(0,0,0)
p1 = point(120,-20,-20)
p2 = point(120,20,20)
p3 = point(120,-20,20)
p4 = point(120,20,-20)
p5 = point(160,-20,-20)
p6 = point(160,20,20)
p7 = point(160,-20,20)
p8 = point(160,20,-20)

#x = (x*cY + (y*sX + z*cX)*sY)*cY + (y*cX + z*-sX)*-sY
#y = (x*cY + (y*sX + z*cX)*sY)*sY + (y*cX + z*-sX)*cY
#z = x*-sY + (y*sX + z*cX)*cY

#x = (p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.cos(camR.y) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*-math.sin(camR.y)
#y = (p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.sin(camR.y) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*math.cos(camR.y)
#z = p.x*-math.sin(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.cos(camR.y)

Points = [p1,p2,p3,p4,p5,p6,p7,p8]
def ToScreen(point,WSize):
    return([point[0]+WSize[0]/2,(0-point[1])+WSize[1]/2])
def Rotated(camR, p):
    return([(p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.cos(camR.z) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*-math.sin(camR.z), (p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.sin(camR.z) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*math.cos(camR.z), p.x*-math.sin(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.cos(camR.y)])
    #z and y easy
def Localize(camP, camR,p):
    Point = point(*Rotated(camR, p))
    return([Point.x-camP.x,Point.y-camP.y,Point.z-camP.z])
def Render(points):
    processed = []
    for p in points:
        P = point(*Localize(CamPos, CamRotation,p))
        y = (P.y*FL)/P.x
        x = (P.z*FL)/P.x
        processed.append([x,y])
    for p in processed:
        for P in processed:
            pygame.draw.line(window,(255,255,255),ToScreen(p,WindowSize),ToScreen(P,WindowSize))
    pygame.display.flip()


pygame.init()
WindowSize = (600,600)
window = pygame.display.set_mode(WindowSize,pygame.RESIZABLE)
pygame.display.set_caption("3D_Viewer")

running = True
while running:

    #print(cam.ax)
    #p1.z+=0.1
    #p1.x+=0.1
    
    window.fill((0, 0, 0))
    Render(Points)
    

    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        CamPos.z -= MoveSpeed
    if keys[pygame.K_RIGHT]:
        CamPos.z += MoveSpeed
    if keys[pygame.K_UP]:
        CamPos.y += MoveSpeed
    if keys[pygame.K_DOWN]:
        CamPos.y -= MoveSpeed
    if keys[pygame.K_w]:
        CamRotation.y += RotSpeed
    if keys[pygame.K_s]:
        CamRotation.y -= RotSpeed
    if keys[pygame.K_l]:
        CamPos.x -= MoveSpeed
    if keys[pygame.K_o]:
        CamPos.x += MoveSpeed
    if keys[pygame.K_a]:
        CamRotation.x += RotSpeed
    if keys[pygame.K_d]:
        CamRotation.x -= RotSpeed

    if keys[pygame.K_p]:
        print(CamPos.x, CamPos.y, CamPos.z)
        print(p1.x, p1.y, p1.z)

pygame.display.quit()