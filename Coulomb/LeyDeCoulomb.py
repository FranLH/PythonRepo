import pygame
import math
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2


Constante = 8.99*math.pow(10,9) # 8.99
NanoCoulomb = math.pow(10,-9)
MicroCoulomb = math.pow(10,-6)

def TrueAngle(angle):
    if angle<0:
        return(360+angle)
    else:
        return(angle)
    
class Particula():
    def __init__(self, carga, pos:vec2):
        self.carga, self.pos, self.fuerza, self.angulo, self.positivo = carga, pos, vec2(0,0), 0, carga>0
    def CalculateForce(self, particles):
        FDir = vec2(0,0)
        for particle in particles:
            if particle != self:
                F = (Constante*abs(self.carga)*NanoCoulomb*abs(particle.carga)*NanoCoulomb)/math.pow(self.pos.Dist(particle.pos),2)
                if self.positivo == particle.positivo:
                    Dir = (self.pos-particle.pos).Normalized()
                else:
                    Dir = (particle.pos-self.pos).Normalized()
                FDir+= Dir*F
                #print(Dir, F, Dir*F, self.pos.Dist(particle.pos))
        self.fuerza = FDir
        self.angulo = TrueAngle(FDir.Angle())
    def PrintForce(self):
        print("Fuerza: " + str(self.fuerza.Length()) + " Newtons")
    def PrintAngle(self):
        print("Angulo: " + str(self.angulo) + " Grados")
        
        
# --PARTICULAS-- #
P1 = Particula(3, vec2(0,1))
P2 = Particula(2, vec2(0,0))
P3 = Particula(6, vec2(0.5,0.5))


Particulas = [P1,P2,P3]
for p in Particulas:
    p.CalculateForce(Particulas)
    p.PrintForce()
    p.PrintAngle()
# P1.PrintAngle()
# P2.PrintAngle()
# P3.PrintAngle()

# print(P2.CalculateForce(Particulas))
# print(P3.CalculateForce(Particulas))