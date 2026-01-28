import moderngl_window as mglw
import pygame
import copy
import numpy as np

blurStrength = 0

class Cam:
    def __init__(self, zoom, pos):
        self.pos, self.zoom = pos, zoom

class App(mglw.WindowConfig):
    window_size = [820,820]
    simulation_size = [820,820]
    resource_dir = 'Shaders'
    frame = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # -------------- CONFIG -------------------
        self.camera = Cam(8, [0 , -210])
        self.BASESPEED = 1
        self.colors = [
        [0,0,0],
        [0,0.4,0.7],
        [1,1,0]
        
        ]
        
        # -----------------------------------------
        
        self.game_texture_a = self.ctx.texture(self.simulation_size, components=4, dtype='u1', data=None)# 8-bit integers
        self.game_texture_b = self.ctx.texture(self.simulation_size, components=4, dtype='u1', data=None)# 
        self.game_texture_a.filter = (self.ctx.NEAREST, self.ctx.NEAREST)
        self.game_texture_b.filter = (self.ctx.NEAREST, self.ctx.NEAREST)
        self.game_fbo_a = self.ctx.framebuffer(color_attachments = [self.game_texture_a])
        self.game_fbo_b = self.ctx.framebuffer(color_attachments = [self.game_texture_b])
        self.read_from_tex = self.game_texture_a
        self.write_to_fbo = self.game_fbo_b
        
        
        self.quad = mglw.geometry.quad_fs()
        self.baseProg = self.load_program(vertex_shader='vertex_shader.glsl', fragment_shader='fragment_shader.glsl')
        self.baseProg['simResolution'] = self.simulation_size
        self.baseProg['gameTex'] = 0
        
        self.postProg = self.load_program(vertex_shader='vertex_shader.glsl', fragment_shader='post_processing.glsl')
        self.postProg['simResolution'] = self.simulation_size
        #self.postProg['resolution'] = self.window_size
        #self.postProg['blurStrength'] = blurStrength

        self.postProg['gameTex'] = 0
        self.postProg['cellColors'] = self.colors
#         
        

        
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

        self.moveSpeed=self.BASESPEED


        self.resize(*self.wnd.buffer_size) # Updates window size at the start
        self.clear_simulation()
            


    def clear_simulation(self, value=(1,0,0,0)):
        arr = np.zeros((self.simulation_size[1], self.simulation_size[0], 4),dtype=np.uint8)
        arr[:] = value
        self.read_from_tex.write(arr.tobytes())

    
    def set_uniform(self, program, u_name, u_value):
        try:
            program[u_name] = u_value
        except KeyError:
            #print(f'uniform: {u_name} - not used in shader')
            pass
    def resize(self,width, height):
        self.window_size = [width, height]
        self.ctx.viewport = (0, 0, width, height)
        self.set_uniform(self.postProg, 'resolution', self.window_size)
        
        # TODO add release for new fbos and textures
        

        



    def render(self, time, frame_time):

        # ======================================================= Input detection
        if self.keyStates["W"]:
            self.camera.pos[1]+=self.moveSpeed
        if self.keyStates["S"]:
            self.camera.pos[1]-=self.moveSpeed
        if self.keyStates["D"]:
            self.camera.pos[0]+=self.moveSpeed
        if self.keyStates["A"]:
            self.camera.pos[0]-=self.moveSpeed
        if self.keyStates["="]:
            self.camera.zoom*=1.01
        if self.keyStates["-"]:
            self.camera.zoom/=1.01      

        # ======================================================= Render passes
        

        
        # ---------------------------------------- Pass 1 (Simulation pass)
        w, h = self.simulation_size
        self.write_to_fbo.use() 
        self.ctx.viewport = (0, 0, w, h)
        
        self.set_uniform(self.baseProg, 'time', time)
        self.set_uniform(self.baseProg, 'frame', self.frame)
        

        self.read_from_tex.use(0)
        self.quad.render(self.baseProg)
        
        self.read_from_tex = self.write_to_fbo.color_attachments[0] # Switch the active texture
        self.write_to_fbo = self.game_fbo_a if self.write_to_fbo is self.game_fbo_b else self.game_fbo_b # Switch the active fbo
        
        # ---------------------------------------- Pass 2 (post processing)
        w, h = self.window_size
        self.ctx.screen.use() # Pass 2
        self.ctx.viewport = (0, 0, w, h)
        self.ctx.clear()
        
        self.postProg['resolution'] = self.window_size
        self.postProg['zoom'] = self.camera.zoom
        self.set_uniform(self.postProg, 'camPos', self.camera.pos)
        
        self.read_from_tex.use(0)
        self.quad.render(self.postProg)
        
        
        
        self.frame +=1

        

    def key_event(self, key, action, modifiers):
        
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.P:
                print("camPos:", self.camera.pos)

            if key == self.wnd.keys.H: # Reset camera position
                self.camera.pos = [0,0]

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


#if __name__ == '__main__':
mglw.run_window_config(App)



    