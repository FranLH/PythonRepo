import pygame
import math

class point:
    def __init__(self,x,y,z):
        self.x, self.y, self.z = x, y, z
    def __add__(self, other): # +
        return(point(self.x+other.x,self.y+other.y,self.z+other.z))
    def __sub__(self, other): # -
        return(point(self.x-other.x,self.y-other.y,self.z-other.z))
    def __mul__(self, other): # *
        return(point(self.x*other,self.y*other,self.z*other))


class SolidObject:
    def __init__(self,pos, points, faces):
        self.pos, self.points, self.faces = pos, points, faces
   
CHUNKSIZE = 16
   
class Chunk:
    def __init__(self,pos:point, data=[0]):
        self.pos, self.data = pos, []
        if self.data == []:
            for z in range(CHUNKSIZE):
                self.data.append([])
                for y in range(CHUNKSIZE):
                    self.data[z].append([])
                    for x in range(CHUNKSIZE):
                        self.data[z][y].append(data[0])

class World:
    def __init__(self, chunks:[[[Chunk]]]):
        self.chunks = chunks
    def GetBlock(self, block:point):
        c = point(math.floor(block.x/CHUNKSIZE),math.floor(block.y/CHUNKSIZE),math.floor(block.z/CHUNKSIZE))
        b = block-(c*CHUNKSIZE)
        
        if c.x >=0 and c.y>=0 and c.z>=0 and c.z < len(self.chunks) and c.y < len(self.chunks[c.z]) and c.x < len(self.chunks[c.z][c.y]):
            return(self.chunks[c.z][c.y][c.x].data[c.z][c.y][c.x])
        else:
            return(0)

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

CHUNKSIZE = 16
CUBESSIZE = 20

# chunk = Chunk(point(0,0,0), [[[0,0,0],[1,0,1],[0,0,0]],[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[1,0,1],[0,0,0]]])
chunk = Chunk(point(0,0,0), [1])
world = World([[[chunk]]])

#x = (x*cY + (y*sX + z*cX)*sY)*cY + (y*cX + z*-sX)*-sY
#y = (x*cY + (y*sX + z*cX)*sY)*sY + (y*cX + z*-sX)*cY
#z = x*-sY + (y*sX + z*cX)*cY

#x = (p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.cos(camR.y) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*-math.sin(camR.y)
#y = (p.x*math.cos(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.sin(camR.y))*math.sin(camR.y) + (p.y*math.cos(camR.x) + p.z*-math.sin(camR.x))*math.cos(camR.y)
#z = p.x*-math.sin(camR.y) + (p.y*math.sin(camR.x) + p.z*math.cos(camR.x))*math.cos(camR.y)

CUBE = [point(-10,-10,-10),point(-10,-10,10),point(-10,10,10),point(-10,10,-10),point(10,-10,-10),point(10,-10,10),point(10,10,10),point(10,10,-10)], [[(-20,0,0), 0,1,2,3, (255,0,0)], [(20,0,0),4,5,6,7, (255,0,0)], [(0,-20,0),0,1,5,4, (0,255,0)], [(0,20,0),2,3,7,6, (0,255,0)], [(0,0,-20),0,3,7,4, (0,0,255)], [(0,0,20),1,2,6,5, (0,0,255)]]


# S1 = SolidObject(200,0,0, *cube)
# S2 = SolidObject(220,0,0,*cube)
# S3 = SolidObject(220,0,20,*cube)
# S4 = SolidObject(220,20,0,*cube)
# S5 = SolidObject(-100,-100,-100,*cube)

# SolidObjects = [S1,S2,S3,S4,S5]




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
def LoadCubes(chunk:Chunk,world:World):
    cubes = []
    for z in range(CHUNKSIZE):
        for y in range(CHUNKSIZE):
            for x in range(CHUNKSIZE): # for each cube in the chunk
                if chunk.data[z][y][x] == 1:
                    pos = point(x,y,z) + (chunk.pos * CHUNKSIZE)
                    if world.GetBlock(pos+point(1,0,0)) == 0 or world.GetBlock(pos+point(-1,0,0)) == 0 or world.GetBlock(pos+point(0,1,0)) == 0 or world.GetBlock(pos+point(0,-1,0)) == 0 or world.GetBlock(pos+point(0,0,1)) == 0 or world.GetBlock(pos+point(0,0,-1)) == 0:
                        cubes.append(SolidObject((chunk.pos+point(x,y,z))*CUBESSIZE, *CUBE))

    return(cubes)
    
def Render(objects):
    processed = []
    for obj in objects:
        #processed = []
        if Localize(CamPos, CamRotation, obj.pos)[0] >= 0: # Roughly checks if the object is inside the viewport
             
            for face in obj.faces:
                valid = 0
                faceCenter = [obj.pos.x+face[0][0], obj.pos.y+face[0][1], obj.pos.z+face[0][2]]
                closest = math.dist([CamPos.x,CamPos.y,CamPos.z],faceCenter)

                processedFace = []
                for POINT in face[1:-1]:
                    p = point(obj.pos.x+obj.points[POINT].x, obj.pos.y+obj.points[POINT].y, obj.pos.z+obj.points[POINT].z)
                    
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
    Render(LoadCubes(chunk,world))
    
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

