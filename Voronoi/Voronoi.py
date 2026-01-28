import pygame
import math
import random
import copy
Width, Height = 600, 600
window = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF, 32)
window.fill((255,255,255))
pygame.init()
class LinearFunc:
    def __init__(self,pointA,pointB,perpendicular):
        if pointA[0]==pointB[0]:
            self.vertical = True
            self.origin = (pointA[0]+pointB[0])/2
        elif perpendicular and pointA[1]==pointB[1]:
            self.vertical = True
            self.origin = (pointA[0]+pointB[0])/2            
        else:
            self.vertical = False
            if perpendicular:
                self.slope = -1/((pointA[1]-pointB[1])/(pointA[0]-pointB[0]))
                self.origin = (pointA[1]+pointB[1]-(pointA[0]+pointB[0])*self.slope)/2
            else:
                self.slope = (pointA[1]-pointB[1])/(poinA[0]-pointB[0])
                self.origin = pointA[1]-self.slope*pointA[0]
    def Paint(self):
        if not vertical:
            start = [0,self.origin*600]
            end = [600,(self.slope+self.origin)*600]
        else:
            start = [self.origin*600,0]
            end = [self.origin*600,600]
        pygame.draw.line(window,(0,0,0), start, end, 2)
    def Paint(self):
        if not self.vertical:
            pygame.draw.line(window,(0,0,0),(0,self.origin),(Width,self.slope*Width + self.origin))
        else:
            pygame.draw.line(window,(0,0,0),(self.origin,0),(self.origin,Height))
    def Intersection(self, other):
        if not self.vertical:
            if not other.vertical:
                if self.slope != other.slope:
                    InterX = (self.origin-other.origin)/(self.slope-other.slope)
                    InterY = (self.slope*InterX+self.origin)
                else:
                    return(False)
            else:
                InterX = other.origin
                InterY = (self.slope*InterX+self.origin)
        else:
            if not other.vertical:
                InterX = self.origin
                InterY = (other.slope*InterX+other.origin)
            else:
                return(False)
        return([InterX,InterY])
class Site:
    def __init__(self,pos,col):
        self.pos, self.col = pos, col
    def Paint(self):
        global Sites
        self.sites = Sites
        for x in range(Width):
            for y in range(Height):
                draw = True
                closest = 1
                for site in self.sites:
                    if math.dist([x/Width,y/Height],site.pos)< closest:
                        closest = math.dist([x/Width,y/Height],site.pos)
                        if site!= self and closest<math.dist([x/Width,y/Height],self.pos):
                            draw = False
                            break
                if draw:
                    pygame.draw.circle(window, self.col, [x,y], 1)
        pygame.draw.circle(window, (0,0,0), [self.pos[0]*Width, self.pos[1]*Height], 3)
        pygame.display.flip()
    def Perimeter(self):
        Vertices = []
        withSides = copy.deepcopy(self.sites)
        withSides.extend([Site([0-self.pos[0],self.pos[1]],(0,0,0)),Site([2-self.pos[0],self.pos[1]],(0,0,0)),Site([self.pos[0],0-self.pos[1]],(0,0,0)),Site([self.pos[0],2-self.pos[1]],(0,0,0))])
#         print(len(withSides))
        for siteA in range(len(withSides)):
            if withSides[siteA] != self: # Prevents checking itself
                for siteB in range(siteA+1,len(withSides)):
                    if siteB != siteA and withSides[siteB] != self: # Prevents duplicates
                        a = LinearFunc(self.pos,withSides[siteA].pos,True)
                        b = LinearFunc(self.pos,withSides[siteB].pos,True)
                        a.Paint()
                        b.Paint()
                        center = a.Intersection(b) # Finds the center of the circumcircle made from the triangle formed by three sites, this will be one of the vertices of the perimeter
                        
                        if type(center) != bool:
                            pygame.draw.circle(window, (0,0,0), [center[0]*600,center[1]*600], 5, 2)
#                             print("Intersection")
                            Valid = True
                            for site in range(len(self.sites)):
                                if self.sites[site] != self and self.sites[site] != withSides[siteA] and self.sites[site] != withSides[siteB]: # Checks every site except the ones forming the circumcircle
                                    if math.dist(self.sites[site].pos,[center[0], center[1]])<math.dist(self.pos,[center[0], center[1]]): # If one of the other sites is inside of the circumcircle, it is not valid
                                        Valid = False
                                        break
                            if Valid:
                                Vertices.append(center)
#         print(len(Vertices))
        for point in range(len(Vertices)):
            if point != len(Vertices)-1:
                pygame.draw.line(window,(0,0,0),(Vertices[point][0]*600,Vertices[point][1]*600),(Vertices[point+1][0]*600,Vertices[point+1][1]*600), 2)
            else:
                pygame.draw.line(window,(0,0,0),(Vertices[point][0]*600,Vertices[point][1]*600),(Vertices[0][0]*600,Vertices[0][1]*600), 2)
#         print(Vertices)
        #DelaunayPoints = 
        #Lines
        #Corners
        #Sides
def NewVoronoi(Nsites):
    global Sites
    Sites = []
    PrivateSites = []
    for i in range(Nsites):
#         print("first")
        colors = [[i for i in range(256)],[i for i in range(256)],[i for i in range(256)]]
        random.shuffle(colors[0])
        random.shuffle(colors[1])
        random.shuffle(colors[2])
#         print(colors)
        PrivateSites.append(Site([random.uniform(0, 1),random.uniform(0, 1)], (colors[0][0],colors[1][0],colors[2][0])))
        colors[0].pop(0)
        colors[1].pop(0)
        colors[2].pop(0)
    for site in range(len(PrivateSites)):
#         print(site)
        choice = random.choice(PrivateSites)
        Sites.append(choice)
        Sites[site].Paint()
        PrivateSites.remove(choice)
        #Sites[site].Perimeter()
        
        
def SumOfPerimeters(Nsites):
    return(Nsites)

pygame.display.set_caption("Voronoi")

# Sites.append(Site([0.25,0.25], (0,0,255)))
# Sites[0].Paint()
# Sites.append(Site([0.5,0.5], (255,0,0)))
# Sites[1].Paint()
# Sites.append(Site([0.8,0.2], (0,255,0)))
# Sites[2].Paint()
# Sites.append(Site([0.1,0.7], (255,255,0)))
# Sites[3].Paint()
NewVoronoi(20)
pygame.image.save(window, "Voronoi_"+str(random.random())[2:]+".png")
running = True
while running:
    
    pygame.display.flip()

    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False

pygame.display.quit()