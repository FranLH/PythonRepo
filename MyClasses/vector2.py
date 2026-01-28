import math
# from MyClasses import Vector2 # If you want to import the vec2 class
# vec2 = Vector2.vec2


class vec2:
    def __init__(self, x:int|float, y:int|float):
        self.x, self.y = x,y
    def __eq__(self, other:"vec2"): # ==
        return(self.x==other.x and self.y==other.y)
    def __lt__(self, other:"vec2"): # <
        return(self.Length()<other.Length())
    def __gt__(self, other:"vec2"): # >
        return(self.Length()>other.Length())
    def __le__(self, other:"vec2"): # <=
        return(self.Length()<=other.Length())
    def __ge__(self, other:"vec2"): # >=
        return(self.Length()>=other.Length())
    def __abs__(self): # abs()
        return(vec2(abs(self.x), abs(self.y)))
    def __round__(self): # round()
        return(vec2(round(self.x), round(self.y)))
    def __add__(self, other): # +
        return(vec2(self.x+other.x,self.y+other.y))
    def __sub__(self, other): # -
        return(vec2(self.x-other.x,self.y-other.y))
    def __mul__(self, other): # *
        typ = str(type(other))
        if "vec2" in typ:
            return(vec2(self.x*other.x,self.y*other.y))
        if "int" in typ:
            return(vec2(self.x*other,self.y*other))
        if "float" in typ:
            return(vec2(self.x*other,self.y*other))
    def __truediv__(self, other): # /
        typ = str(type(other))
        if "vec2" in typ:
            return(vec2(self.x/other.x,self.y/other.y))
        if "int" in typ:
            return(vec2(self.x/other,self.y/other))
        if "float" in typ:
            return(vec2(self.x/other,self.y/other))
    def __complex__(self) -> complex:# complex() 
        return(complex(self.x,self.y))
    def __repr__(self): # str()
        return("("+str(self.x)+","+str(self.y)+")")
    def Length(self):
        return(math.sqrt(self.x**2 + self.y**2))
    def Normalize(self):
        angle = math.atan2(self.x,self.y)
        self.contents = [math.sin(angle),math.cos(angle)]
    def Normalized(self):
        angle = math.atan2(self.x,self.y)
        return(vec2(math.sin(angle),math.cos(angle)))
    def Dist(self,other:"vec2"):
        return(math.dist([self.x,self.y],[other.x,other.y]))
    def ToList(self):
        return([self.x,self.y])
    def Angle(self):
        return(math.degrees(math.atan2(self.y,self.x)))
    def Right(self):
        n = self.Normalized()
        return(vec2(n.y, -1*n.x))
    def Left(self):
        n = self.Normalized()
        return(vec2(-1*n.y, n.x))
    def Rotated(self,radians:float):
        return(vec2(math.cos(radians)*self.x - math.sin(radians)*self.y, math.sin(radians)*self.x+math.cos(radians)*self.y))

# a = vec2(3,5)
# b = vec2(3,3)
# print(type(min(a,b)))

class vec3:
    def __init__(self, x:int|float, y:int|float, z:int|float):
        self.x, self.y, self.z = x,y,z
    def __eq__(self, other:"vec3"): # ==
        return(self.x==other.x and self.y==other.y and self.z==other.z)
    def __lt__(self, other:"vec3"): # <
        return(self.Length()<other.Length())
    def __gt__(self, other:"vec3"): # >
        return(self.Length()>other.Length())
    def __le__(self, other:"vec3"): # <=
        return(self.Length()<=other.Length())
    def __ge__(self, other:"vec3"): # >=
        return(self.Length()>=other.Length())
    def __abs__(self): # abs()
        return(vec3(abs(self.x), abs(self.y), abs(self.z)))
    def __round__(self): # round()
        return(vec3(round(self.x), round(self.y), round(self.z)))
    def __add__(self, other): # +
        return(vec3(self.x+other.x,self.y+other.y,self.z+other.z))
    def __sub__(self, other): # -
        return(vec3(self.x-other.x,self.y-other.y,self.z-other.z))
    def __mul__(self, other): # *
        typ = str(type(other))
        if "vec3" in typ:
            return(vec3(self.x*other.x,self.y*other.y,self.z*other.z))
        if "int" in typ:
            return(vec3(self.x*other,self.y*other,self.z*other))
        if "float" in typ:
            return(vec3(self.x*other,self.y*other,self.z*other))
    def __truediv__(self, other): # /
        typ = str(type(other))
        if "vec3" in typ:
            return(vec3(self.x/other.x,self.y/other.y,self.z/other.z))
        if "int" in typ:
            return(vec3(self.x/other,self.y/other,self.z/other))
        if "float" in typ:
            return(vec3(self.x/other,self.y/other,self.z/other))
    def __repr__(self): # str()
        return("("+str(self.x)+","+str(self.y)+","+str(self.z)+")")
    def Length(self):
        return(math.sqrt(self.x**2 + self.y**2 + self.z**2))
    def Normalize(self):
        self.contents = [self.x/self.Length(),self.y/self.Length(),self.z/self.Length()]
    def Normalized(self):
        return(vec3(self.x/self.Length(),self.y/self.Length(),self.z/self.Length()))
    def Dist(self,other:"vec3"):
        return(math.dist([self.x,self.y,self.z],[other.x,other.y,other.z]))
    def ToList(self):
        return([self.x,self.y,self.z])
    def Angle(self):
        return([math.degrees(math.atan2(self.y,self.x)), math.degrees(math.atan2(self.z,self.x))])
