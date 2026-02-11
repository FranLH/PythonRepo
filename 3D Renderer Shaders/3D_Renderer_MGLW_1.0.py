import moderngl_window as mglw
import pygame
import numpy as np
import copy



blurStrength = 0.5

vecPositions = np.array([[0,0],[0.5,0.5],[1,1]])
vecColors = np.array([[1,0,0],[0,1,0],[0,0,1]])

class vec3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    

class Cam:
    def __init__(self, pos:vec3, rotation:vec3):
        self.pos, self.rotation = pos, rotation

class App(mglw.WindowConfig):
    window_size = [820,820]
    resource_dir = 'Shaders'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        self.quad = mglw.geometry.quad_fs()
        
        self.prog = self.load_program(vertex_shader='vertex_shader.glsl', fragment_shader='fragment_shader.glsl')
        self.vao = mglw.opengl.vao.VAO("vertices")

        #self.set_uniform('resolution', self.window_size)
        
        
        #self.post_prog = self.load_program(vertex_shader='vertex_shader.glsl', fragment_shader='post_processing.glsl')
        #self.post_prog['blurStrength'] = blurStrength
        #self.post_prog['resolution'] = self.window_size
        
        # -------------- CONFIG -------------------
        self.camera = Cam(vec3(0,0,0), vec3(0,0,0))
        # -----------------------------------------
        
        self.keyStates = {
        "W" : False,
        "A" : False,
        "S" : False,
        "D" : False}
        
        self.BASESPEED = 0.01

        

        
        self.resize(*self.wnd.buffer_size) # Updates window size at the start

    
    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            #print(f'uniform: {u_name} - not used in shader')
            pass
        
    def resize(self,width, height):
        self.window_size = [width, height]
        self.ctx.viewport = (0, 0, width, height)
        self.set_uniform('resolution', self.window_size)


    def render(self, time, frame_time):
        w, h = self.window_size
        
        if self.keyStates["W"]:
            self.camera.pos[1]+=self.moveSpeed
        if self.keyStates["S"]:
            self.camera.pos[1]-=self.moveSpeed
        if self.keyStates["D"]:
            self.camera.pos[0]+=self.moveSpeed
        if self.keyStates["A"]:
            self.camera.pos[0]-=self.moveSpeed
            
            
        self.ctx.screen.use()
        self.ctx.clear()
        self.vao.buffer(vecPositions, '3f', ['in_position'])
        self.vao.buffer(vecColors, '3f', ['in_normal'])
        self.vao.render(self.prog)
        
        self.quad.render(self.prog)
        
        

    def key_event(self, key, action, modifiers):
        
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.P:
                print("camPos:", self.camera.pos)
                print("Rotation:", self.camera.rotation)
            if key == self.wnd.keys.H:
                self.camera.pos = vec3(0,0,0)
            if key == self.wnd.keys.W:
                self.keyStates["W"] = True
            if key == self.wnd.keys.S:
                self.keyStates["S"] = True
            if key == self.wnd.keys.D:
                self.keyStates["D"] = True
            if key == self.wnd.keys.A:
                self.keyStates["A"] = True

        else:
            if key == self.wnd.keys.W:
                self.keyStates["W"] = False
            if key == self.wnd.keys.S:
                self.keyStates["S"] = False
            if key == self.wnd.keys.D:
                self.keyStates["D"] = False
            if key == self.wnd.keys.A:
                self.keyStates["A"] = False



#if __name__ == '__main__':
mglw.run_window_config(App)


    