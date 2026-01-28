import pygame
import math

class point:
    def __init__(self,x,y,z):
        self.x, self.y, self.z = x, y, z

class SolidObject:
    def __init__(self,x,y,z, points, faces):
        self.x, self.y, self.z, self.points, self.faces = x, y, z, points, faces
#   x
# 1 0 0    x = x
# 0 c -s   y = y*cX + z*-sX
# 0 s c    z = y*sX + z*cX

#   y
# c 0 s    x = x*cY + z*sY
# 0 1 0    y = y
# -s 0 c   z = x*-sY + z*cY

#   z
# c -s 0   x = x*cZ + y*-sZ
# s c 0    y = x*sZ + y*cZ
# 0 0 1    z = z

#x = (x*cY + (y*sX + z*cX)*sY)*cZ + (y*cX + z*-sX)*-sZ
#y = (x*cY + (y*sX + z*cX)*sY)*sZ + (y*cX + z*-sX)*cZ
#z = x*-sY + (y*sX + z*cX)*cY

#x = (x*c + (y*sX + z*cX)*s)*c + (y*cX + z*-sX)*-s 
#y = (x*c + (y*sX + z*cX)*s)*s + (y*cX + z*-sX)*c
#z = x*-s + (y*s + z*c)*c

FL = 360
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
cube = [point(-10,-10,-10),point(-10,-10,10),point(-10,10,10),point(-10,10,-10),point(10,-10,-10),point(10,-10,10),point(10,10,10),point(10,10,-10)], [[(-20,0,0), 0,1,2,3, (255,0,0)], [(20,0,0),4,5,6,7, (255,0,0)], [(0,-20,0),0,1,5,4, (0,255,0)], [(0,20,0),2,3,7,6, (0,255,0)], [(0,0,-20),0,3,7,4, (0,0,255)], [(0,0,20),1,2,6,5, (0,0,255)]]
H1 = [[p2,p3],[p1,p3],[p2,p4],[p4,p1],[p5,p7],[p6,p7],[p6,p8],[p8,p5],[p1,p5],[p2,p6],[p3,p7],[p4,p8]]
HollowObjects = [H1]
S1 = SolidObject(200,0,0, *cube)
S2 = SolidObject(220,0,0,*cube)
S3 = SolidObject(220,0,20,*cube)
S4 = SolidObject(220,20,0,*cube)
SolidObjects = [S1,S2,S3,S4]
for x in range(13, 20):
    for z in range(0,18):
        SolidObjects.append(SolidObject(x*20,0,z*20, *cube))

def ToScreen(point,WSize):
    return([point[0]+WSize[0]/2,(0-point[1])+WSize[1]/2])
def Rotated(camR, p):
    return([(p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.cos(camR.z) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*-math.sin(camR.z), (p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.sin(camR.z) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*math.cos(camR.z), p.x*-math.sin(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.cos(camR.y)])
    #z and y easy
def Localize(camP, camR,p):
    return(Rotated(camR, point(*[p.x-camP.x,p.y-camP.y,p.z-camP.z])))
def Render(points):
    for obj in HollowObjects:
        processed = []
        for line in obj:
            valid = 0
            processedLine = []
            for p in line:
                P = point(*Localize(CamPos, CamRotation,p))
                y = (P.y*FL)/P.x
                x = (P.z*FL)/P.x
                if P.x <= 0: # Prevents objects rendering from behind the camera
                    valid+=1
                    break
                else:
                    processedLine.append([x,y])
            if valid == 0:
                processed.append(processedLine)
        for line in processed:
            pygame.draw.line(window,(255,255,255),ToScreen(line[0],WindowSize),ToScreen(line[1],WindowSize))
    processed = []
    for obj in SolidObjects:
        #processed = []
        for face in obj.faces:
            valid = 0
            faceCenter = [obj.x+face[0][0], obj.y+face[0][1], obj.z+face[0][2]]
            closest = math.dist([CamPos.x,CamPos.y,CamPos.z],faceCenter)
            processedFace = []
            for POINT in face[1:-1]:
                p = point(obj.x+obj.points[POINT].x, obj.y+obj.points[POINT].y, obj.z+obj.points[POINT].z)
                
                P = point(*Localize(CamPos, CamRotation,p))
                y = (P.y*FL)/P.x
                x = (P.z*FL)/P.x
                if P.x <= 0: # Prevents objects rendering from behind the camera
                    valid+=1
                    break
                else:
                    processedFace.append(ToScreen([x,y],WindowSize))
            if valid == 0:
                processedFace.append(face[-1])
                processedFace.insert(0,closest)
                processed.append(processedFace)
    processed.sort(reverse=True)
    for face in processed:
        pygame.draw.polygon(window,face[-1],face[1:-1])
                
    pygame.display.flip()


pygame.init()
WindowSize = (600,600)
window = pygame.display.set_mode(WindowSize,pygame.RESIZABLE)
pygame.display.set_caption("3D_Viewer")

running = True
its = 0
while running:

    #print(cam.ax)
    #p1.z+=0.1
    #p1.x+=0.1
    if its%20 == 0:
        window.fill((0, 0, 0))
        Render(HollowObjects)
    
    its +=1
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        CamPos.x -= math.cos(CamRotation.y+math.pi/2) * MoveSpeed
        CamPos.z -= math.sin(CamRotation.y+math.pi/2) * MoveSpeed
    if keys[pygame.K_RIGHT]:
        CamPos.x += math.cos(CamRotation.y+math.pi/2) * MoveSpeed
        CamPos.z += math.sin(CamRotation.y+math.pi/2) * MoveSpeed
    if keys[pygame.K_UP]:
        CamPos.x += math.cos(CamRotation.y) * MoveSpeed
        CamPos.z += math.sin(CamRotation.y) * MoveSpeed
    if keys[pygame.K_DOWN]:
        CamPos.x -= math.cos(CamRotation.y) * MoveSpeed
        CamPos.z -= math.sin(CamRotation.y) * MoveSpeed
    if keys[pygame.K_d]:
        CamRotation.y += RotSpeed
    if keys[pygame.K_a]:
        CamRotation.y -= RotSpeed
    if keys[pygame.K_l]:
        CamPos.y -= MoveSpeed
    if keys[pygame.K_o]:
        CamPos.y += MoveSpeed
    if keys[pygame.K_s]:
        CamRotation.z += RotSpeed
    if keys[pygame.K_w]:
        CamRotation.z -= RotSpeed

    if keys[pygame.K_p]:
        print(CamPos.x, CamPos.y, CamPos.z)
        print(p1.x, p1.y, p1.z)
        print(Localize(CamPos, CamRotation,p1))

pygame.display.quit()