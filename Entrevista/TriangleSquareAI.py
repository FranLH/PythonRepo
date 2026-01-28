import pygame
import math
import ast


from math import e as EULER
import random
import numpy
import copy


# d(sigmoid) = (e^-x) / (1 + e^-x)^2



class Connection:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
class Neuron:
    def __init__(self, x, y, bias, contents):
        self.x = x
        self.y = y
        self.bias = bias
        self.contents = contents
    def CalcOutput(self,N):
        self.contents = 0
        counter = 0
        for i in N[self.x-2]:
            self.contents += i.contents * N[self.x-1][self.y*len(N[self.x-2])+counter].weight
            counter+=1

        self.contents += self.bias
        #Sigmoid function, S(x) = 1/(1+e^-x)
        self.contents = 1/(1+numpy.exp(-self.contents))
def CreateNetwork(Type, inputs, layers, NeuronsPerLayer, outputs, load):
    if Type == "NewBasic":
        NewN = []
        for layer in range(0,layers):
            NewN.append([])
            for i in range(NeuronsPerLayer):
                neuron = Neuron(layer+1,i,0,0)
                NewN[layer].append(neuron)
        NewN.insert(0,[])
        NewN.append([])
        for i in range(inputs):
            neuron = Neuron(0,i,0,0)
            NewN[0].append(neuron)
        for i in range(outputs):
            neuron = Neuron(len(NewN)-1,i,0,0)
            NewN[-1].append(neuron)
        ConnectedNN = NewN
        for i in range(len(NewN)-1):
            ConnectedNN = CreateConnections(ConnectedNN, i*2, i*2+1, 0)
        return(ConnectedNN)
    elif Type == "Load":
        NewN = []

        for layer in range(len(load)):


            if layer%2 != 0:
                connections = []


                for i in range(len(load[layer])):
                    c = Connection(layer, i, load[layer][i])
                    connections.append(c)
                NewN.insert(layer,connections)

            else:
                neurons = []
                for i in range(len(load[layer])):
                    n = Neuron(layer, i, load[layer][i], 0)
                    neurons.append(n)
                NewN.insert(layer,neurons)
        
        return(NewN)
def CreateConnections(N, layer1, layer2, weights):
    cons = []
    Return = copy.deepcopy(N)
    if weights != 0:
        for i in range(len(N[layer1])*len(N[layer2])):
            c = Connection(layer2, i, weights[i])
            cons.append(c)
    else:
        for i in range(len(N[layer1])*len(N[layer2])):
            c = Connection(layer2, i, 0)
            cons.append(c)
    Return.insert(layer2, cons)
    for i in Return[layer2+1]:
        i.x = layer2+1
    return(Return)
def CalcNetwork(N):
    for i in range(2,len(N),2):
        for neuron in N[i]:
            neuron.CalcOutput(N)


def Run(picture):
    #global Picture
    data = []
    ratio = int(GridSize/8)
    for y in range(0,len(picture),ratio):
        num = 0
        #print(len(picture))
        for i in range(ratio):
            num += picture[y+i]
        data.append(num/ratio)
    for Input in range(len(NN[0])):
        NN[0][Input].contents = data[Input]
    CalcNetwork(NN)
    outputs = []
    #print(NN[-1][0].contents,NN[-1][1].contents )
    for i in range(len(NN[-1])):
        outputs.append((NN[-1][i].contents,i))
    outputs.sort()
    print(OutputNames[outputs[-1][1]])
    print(math.floor(outputs[-1][0]*100), "%")
    print("---------------")

OutputNames = ["CUADRADO","TRIANGULO"]







def DrawGrid():
    global Canvas
    Canvas = []
    window.fill((0, 0, 0))
    for y in range(GridSize):
        Canvas.append([])
        for x in range(GridSize):
            Canvas[y].append(0)
            pygame.draw.rect(window, (255,255,255), (TileSize*x+LineWidth,TileSize*y+LineWidth,TileSize-LineWidth, TileSize-LineWidth))
    pygame.display.flip()


def GrayscalePaint(pos,color):
    if color != 255:
        #x, y = round((pos[0]-TileSize/2)/TileSize), round((pos[1]-TileSize/2)/TileSize)
        for y in range(GridSize):
            for x in range(GridSize):
                col = round(math.dist([pos[0],pos[1]], [TileSize*x+LineWidth+TileSize/2, TileSize*y+LineWidth+TileSize/2])*grayRange,ColDecimals)

                if col < 1-Canvas[y][x]:
                    if col <= 1:
                        Canvas[y][x] = round(1-col,ColDecimals)
                    col = col * 255
                    col = (col,col,col)
                    pygame.draw.rect(window, col, (TileSize*x+LineWidth,TileSize*y+LineWidth,TileSize-LineWidth, TileSize-LineWidth))








f = open(r"STNN_BIGGEST_0.075.txt","r")
load = ast.literal_eval(f.read())
f.close()

NN = CreateNetwork("Load", 0, 0, 0, 0, load)


pygame.init()
WindowSize = 600
window = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("PaintGrid")

s = [1,0]
t = [0,1]

ColDecimals = 2

GridSize = 8
BrushMult = 1.2
BrushMult = BrushMult/(GridSize/8)
LineWidth = 1
TileSize = (WindowSize/GridSize)-LineWidth
grayRange = 1/TileSize*BrushMult

#=================================================
#=================================================
#               --- CONTROLES ---
# 
# Click izquierdo para dibujar 
# Tecla 'E' para borrar el canvas
# Tecla 'Q' para ejecutar la red neuronal

#=================================================
#=================================================


Pictures = []
running = True
DrawGrid()
pygame.display.flip()

time = 0
while running:
#    try:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save = []
                for i in Canvas:
                    save.extend(i)
                Pictures.append([save,s])
            elif event.key == pygame.K_t:
                save = []
                for i in Canvas:
                    save.extend(i)
                Pictures.append([save,t])
            elif event.key == pygame.K_q:
                save = []
                for i in Canvas:
                    save.extend(i)
                Picture = save
                #print(Picture)
                Run(Picture)
            elif event.key == pygame.K_e:
                DrawGrid()
            if event.key == pygame.K_p:
                print(Pictures)
    if pygame.mouse.get_pressed()[0] == True:
        GrayscalePaint(pygame.mouse.get_pos(),0)
    if pygame.mouse.get_pressed()[2] == True:
        Paint(pygame.mouse.get_pos(),(255,255,255))
  
    pygame.display.flip()     
    #except:
#        pass
    time += 1
pygame.display.quit()