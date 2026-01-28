import math
from vector2 import vec2

global v
v = 10

print(type(v))
def Change(value):
    value = 30
Change(v)
print(v)

def Lerp(a,b):
    a=b
    
# Thread = [(Func,20)]

def Interpolate(a, b, time, thread):
    pass
# class Interpolate():
#     def __init__(self, a, b, time, type="linear"):
#         self.value = 0
#         self.a , self.b, self.time = a, b, time
#     def Lerp(self):
#         new = self.a+(self.b-self.a)*self.value
#         self.value+=1/self.time
#         return(new)
    
# c = 10
# interp = Interpolate(10, 30, 10)
# while c<30:
#     c = interp.Lerp()
#     print(c)


# Thread[0][0](*(Thread[0][1:]))