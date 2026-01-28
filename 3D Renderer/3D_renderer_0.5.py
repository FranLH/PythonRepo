import pygame
import math

class point:
    def __init__(self,x,y,z):
        self.x, self.y, self.z = x, y, z

class SolidObject:
    def __init__(self,x,y,z, points, faces):
        self.x, self.y, self.z, self.points, self.faces = x, y, z, points, faces
        
class Sphere:
    def __init__(self,x,y,z,radius, color):
        self.x, self.y, self.z, self.radius, self.color = x, y, z, radius, color
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

fps = 0
FPS = 60
FL = 270
ZCamLimit = 1.5
Y_Speed = 0.3
MoveSpeed = 0.2
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

plane = [point(-20,0,-20),point(-20,0,20),point(20,0,20),point(20,0,-20)], [[(0,0,0), 0,1,2,3, (255,255,255)]]
cube = [point(-10,-10,-10),point(-10,-10,10),point(-10,10,10),point(-10,10,-10),point(10,-10,-10),point(10,-10,10),point(10,10,10),point(10,10,-10)], [[(-20,0,0), 0,1,2,3, (255,0,0)], [(20,0,0),4,5,6,7, (255,0,0)], [(0,-20,0),0,1,5,4, (0,255,0)], [(0,20,0),2,3,7,6, (0,255,0)], [(0,0,-20),0,3,7,4, (0,0,255)], [(0,0,20),1,2,6,5, (0,0,255)]]
H1 = [[p2,p3],[p1,p3],[p2,p4],[p4,p1],[p5,p7],[p6,p7],[p6,p8],[p8,p5],[p1,p5],[p2,p6],[p3,p7],[p4,p8]]
HollowObjects = [H1]

S1 = SolidObject(200,0,0, *cube)
S2 = SolidObject(220,0,0,*cube)
S3 = SolidObject(220,0,20,*cube)
S4 = SolidObject(220,20,0,*cube)
S5 = SolidObject(-100,-100,-100,*cube)

SolidObjects = [S1,S2,S3,S4,S5]

SP = Sphere(-100,-100,-100,30,(255,255,0))
SP2 = Sphere(-160,-100,-100,30,(0,255,0))
Spheres = [SP,SP2]

for x in range(10):
    for z in range(10):
        SolidObjects.append(SolidObject(100+x*40,0,100+z*40, *plane))

def ToScreen(point,WSize):
    return([point[0]+WSize[0]/2,(0-point[1])+WSize[1]/2])
def Rotated(camR, p):
    return([(p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.cos(camR.z) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*-math.sin(camR.z), (p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.sin(camR.z) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*math.cos(camR.z), p.x*-math.sin(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.cos(camR.y)])
    #z and y easy
def Localize(camP, camR,p):
    return(Rotated(camR, point(*[p.x-camP.x,p.y-camP.y,p.z-camP.z])))
def LimitRotation():
    CamRotation.z = max(min(CamRotation.z, ZCamLimit), -1*ZCamLimit)
    if CamRotation.y > 6.28319:
        CamRotation.y -= 6.28319
    elif CamRotation.y < -6.28319:
        CamRotation.y += 6.28319
def Render():
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
    for sphere in Spheres:
        p = point(sphere.x,sphere.y,sphere.z)
        P = point(*Localize(CamPos, CamRotation,p))
        y = (P.y*FL)/P.x
        x = (P.z*FL)/P.x
        #p.x+=sphere.radius
        
        R = point(*Localize(CamPos, CamRotation,p))
        angle = math.atan(math.dist([R.z], [CamPos.z])/math.dist([R.x], [CamPos.x]))
        Rotated = point(CamRotation.x, CamRotation.y, CamRotation.z+angle+0.0000000001)
        RR = point(*Localize(CamPos, Rotated,p))
        RR.z+=sphere.radius
        rx = (R.z*FL)/R.x
        ry = (R.y*FL)/R.x
        rrx = (RR.z*FL)/(RR.x)
        rry = (RR.y*FL)/(RR.x)

        if P.x <= 0:
            continue
        else:
            distance = math.dist([CamPos.x,CamPos.y,CamPos.z],[sphere.x,sphere.y,sphere.z])
            processed.append([distance-sphere.radius,x,y, sphere.color, math.dist(ToScreen([rrx,rry],WindowSize),ToScreen([rx,ry],WindowSize))])
    if len(processed)!=0:
        processed.sort(reverse= True, key=lambda pos : pos[0])
    for circ in processed:
        
        pygame.draw.circle(window,circ[3],ToScreen([circ[1],circ[2]],WindowSize),circ[4])
    processed = []
    for obj in SolidObjects:
        #processed = []
        objPos = point(obj.x,obj.y,obj.z)
        if Localize(CamPos, CamRotation, objPos)[0] <= 0:
            continue
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
    
    text = arial.render("FPS: " + str(round(fps,2)), True, (255,0,0), (0,0,0))
    window.blit(text,(0,0))
    pygame.display.flip()


pygame.init()
pygame.font.init()
arial = pygame.font.SysFont("arial", 10, False, False)
clock = pygame.time.Clock()
WindowSize = pygame.display.get_desktop_sizes()[0]
window = pygame.display.set_mode(WindowSize, pygame.FULLSCREEN | pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption("3D_Viewer")

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
running = True

while running:
    
    #print(cam.ax)
    #p1.z+=0.1
    #p1.x+=0.1

    window.fill((0, 0, 0))
    Render()
    
    mouse_axis = pygame.mouse.get_rel()
    CamRotation.y += mouse_axis[0]*RotSpeed
    CamRotation.z += mouse_axis[1]*RotSpeed
    LimitRotation()
    #pygame.mouse.set_pos(300,300)
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        CamPos.x -= math.cos(CamRotation.y+math.pi/2) * MoveSpeed * clock.get_time()
        CamPos.z -= math.sin(CamRotation.y+math.pi/2) * MoveSpeed * clock.get_time()
    if keys[pygame.K_d]:
        CamPos.x += math.cos(CamRotation.y+math.pi/2) * MoveSpeed * clock.get_time()
        CamPos.z += math.sin(CamRotation.y+math.pi/2) * MoveSpeed * clock.get_time()
    if keys[pygame.K_w]:
        CamPos.x += math.cos(CamRotation.y) * MoveSpeed * clock.get_time()
        CamPos.z += math.sin(CamRotation.y) * MoveSpeed * clock.get_time()
    if keys[pygame.K_s]:
        CamPos.x -= math.cos(CamRotation.y) * MoveSpeed * clock.get_time()
        CamPos.z -= math.sin(CamRotation.y) * MoveSpeed * clock.get_time()
    if keys[pygame.K_LSHIFT]:
        CamPos.y -= Y_Speed * clock.get_time()
    if keys[pygame.K_SPACE]:
        CamPos.y += Y_Speed * clock.get_time()
    if keys[pygame.K_ESCAPE]:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        running = False 
    if keys[pygame.K_p]:
        print(CamPos.x, CamPos.y, CamPos.z)
        print(p1.x, p1.y, p1.z)
        print(Localize(CamPos, CamRotation,p1))
        print(CamRotation.y,CamRotation.z)
    clock.tick(FPS)
    fps = clock.get_fps()
pygame.display.quit()