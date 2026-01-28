from vector2 import vec2


class Camera:
    def __init__(self, pos:vec2, zoom:int|float, windowSize:tuple[int,int]):
        self.pos, self.zoom, self.windowSize = pos, zoom, windowSize
    def ToScreen(self,point:vec2) -> vec2:
        final = ((point-self.pos)/ self.zoom - vec2(self.windowSize[1]/-2,self.windowSize[1]/2)) * vec2(1,-1)
        return(((point-self.pos)/ self.zoom - vec2(self.windowSize[1]/-2,self.windowSize[1]/2)) * vec2(1,-1))
    def SizeZoom(self,size):
        return(size/self.zoom)
    def IsInScreen(self,point):
        toScreen = self.ToScreen(point)
        return (0 < toScreen.x < self.windowSize[0] and 0 < toScreen.y < self.windowSize[1])
    def ToWorldSpace(self, point:vec2) -> vec2:
        return ((point / vec2(1,-1) + vec2(self.windowSize[1]/-2,self.windowSize[1]/2)) * self.zoom + self.pos)