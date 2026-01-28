import moderngl_window as mglw
import pygame
import numpy as np
import copy

# Zoom where pixelating starts 233474


# outsideColorPalette = [
# [0.5, 0, 0],
# [0.75, 0, 0],
# [1, 0, 0],
# [1, 0.3, 0],
# [1, 0.6, 0],
# [0.75, 0.3, 0],
# [0.75, 0, 0]]

# Fire palette: [[0,0,0],[1,0,0],[1,1,0],[1,1,1],[1,1,0],[1,0,0]]
# Chocolate and cream palette : [[0,0,0],[0.74,0.53,0.36],[1,1,0.93],[0.74,0.53,0.36]]
# Coral palette: [[0,0,0.7],[0.8,0,0.5],[1,0,1]]      # Inside: [0.9,0.8,0.3]
outsideColorPalette = [[0,0,0.7],[0.8,0,0.5],[1,0,1]]  
insideColor = [0,0,0]
    


def ExpandColorPalette(palette, repetitions):
    finalList = copy.deepcopy(palette)
    for i in range(repetitions):
        newList = []
        for j in range(len(finalList)-1):
            newList.append(finalList[j])
            newList.append(list(map(lambda a : (finalList[j][a]+finalList[j+1][a])/2, [0,1,2])))
        newList.append(finalList[j+1])
        newList.append(list(map(lambda a : (finalList[0][a]+finalList[j+1][a])/2, [0,1,2])))
        finalList=copy.deepcopy(newList)
        
    return newList
outsideColorPalette = ExpandColorPalette(outsideColorPalette, 5)


class Cam:
    def __init__(self, zoom, pos):
        self.zoom, self.pos = zoom, pos

class App(mglw.WindowConfig):
    window_size = [820,820]
    resource_dir = 'Shaders'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.quad = mglw.geometry.quad_fs()
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl', fragment_shader='fragment_shader.glsl')
        self.set_uniform('resolution', self.window_size)
        self.set_uniform('inColor', insideColor)
        self.set_uniform('outPalette', outsideColorPalette)
        self.set_uniform('paletteSize', len(outsideColorPalette))
        
        self.camera = Cam(0.2, [0 , 0])
        self.fractalOrigin = [0,0]
        print(type(self.camera.pos[1]))
        self.keyStates = {
        "W" : False,
        "A" : False,
        "S" : False,
        "D" : False,
        "UP" : False,
        "LEFT" : False,
        "DOWN" : False,
        "RIGHT" : False,
        "=" : False,
        "-" : False,
        "Q" : False,
        "E" : False}
        self.BASESPEED = 0.01
        self.moveSpeed = self.BASESPEED
        self.zoomSpeed = 1.01
        self.depth = 100
    
    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            #print(f'uniform: {u_name} - not used in shader')
            pass
    def resize(self,width, height):
        self.window_size = [width, height]
        print(self.window_size)
        self.set_uniform('resolution', self.window_size)
    def render(self, time, frame_time):
        if self.keyStates["W"]:
            self.camera.pos[1]+=self.moveSpeed
        if self.keyStates["S"]:
            self.camera.pos[1]-=self.moveSpeed
        if self.keyStates["D"]:
            self.camera.pos[0]+=self.moveSpeed
        if self.keyStates["A"]:
            self.camera.pos[0]-=self.moveSpeed
        if self.keyStates["UP"]:
            self.fractalOrigin[1]+=0.01
        if self.keyStates["DOWN"]:
            self.fractalOrigin[1]-=0.01
        if self.keyStates["RIGHT"]:
            self.fractalOrigin[0]+=0.01
        if self.keyStates["LEFT"]:
            self.fractalOrigin[0]-=0.01        
        if self.keyStates["="]:
            self.camera.zoom*=self.zoomSpeed
        if self.keyStates["-"]:
            self.camera.zoom/=self.zoomSpeed
        if self.keyStates["Q"]:
            self.depth-=1
        if self.keyStates["E"]:
            self.depth+=1
        
        self.moveSpeed=self.BASESPEED/self.camera.zoom
        
        
        self.ctx.clear()
        self.set_uniform('DEPTH', self.depth)
        self.set_uniform('time', time)
        self.set_uniform('zoom', self.camera.zoom)
        self.set_uniform('camPos', self.camera.pos)
        self.set_uniform('fractalPos', self.fractalOrigin)
        self.quad.render(self.prog)

    def key_event(self, key, action, modifiers):
        
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.P:
                print("Zoom:", self.camera.zoom)
                print("camPos:", self.camera.pos)
                print("Depth:", self.depth)
                print("FractalOrigin:", self.fractalOrigin)
            if key == self.wnd.keys.H:
                self.camera.pos = [0,0]
                self.camera.zoom = 0.2
                self.fractalOrigin = [0,0]

            if key == self.wnd.keys.EQUAL:
                self.keyStates["="] = True
            if key == self.wnd.keys.MINUS:
                self.keyStates["-"] = True
            if key == self.wnd.keys.W:
                self.keyStates["W"] = True
            if key == self.wnd.keys.S:
                self.keyStates["S"] = True
            if key == self.wnd.keys.D:
                self.keyStates["D"] = True
            if key == self.wnd.keys.A:
                self.keyStates["A"] = True
            if key == self.wnd.keys.UP:
                self.keyStates["UP"] = True
            if key == self.wnd.keys.DOWN:
                self.keyStates["DOWN"] = True
            if key == self.wnd.keys.RIGHT:
                self.keyStates["RIGHT"] = True
            if key == self.wnd.keys.LEFT:
                self.keyStates["LEFT"] = True
            if key == self.wnd.keys.Q:
                self.keyStates["Q"] = True
            if key == self.wnd.keys.E:
                self.keyStates["E"] = True
 
        else:
            if key == self.wnd.keys.EQUAL:
                self.keyStates["="] = False
            if key == self.wnd.keys.MINUS:
                self.keyStates["-"] = False
            if key == self.wnd.keys.W:
                self.keyStates["W"] = False
            if key == self.wnd.keys.S:
                self.keyStates["S"] = False
            if key == self.wnd.keys.D:
                self.keyStates["D"] = False
            if key == self.wnd.keys.A:
                self.keyStates["A"] = False
            if key == self.wnd.keys.UP:
                self.keyStates["UP"] = False
            if key == self.wnd.keys.DOWN:
                self.keyStates["DOWN"] = False
            if key == self.wnd.keys.RIGHT:
                self.keyStates["RIGHT"] = False
            if key == self.wnd.keys.LEFT:
                self.keyStates["LEFT"] = False
            if key == self.wnd.keys.Q:
                self.keyStates["Q"] = False
            if key == self.wnd.keys.E:
                self.keyStates["E"] = False 


if __name__ == '__main__':
    mglw.run_window_config(App)
    