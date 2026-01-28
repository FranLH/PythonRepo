import random
import math
import ast
import pygame
class Node:
    def __init__(self, bias, pos, parent, activation):
        self.bias, self.pos, self.parent, self.activation = bias, pos, parent, activation
    def Sigmoid(self,number):
        return(1/(1+math.exp(min(100,number))))

    def Activate(self):
        if self.pos[0] != 0:
            added = 0
            length = len(self.parent.contents[self.pos[0]-2])
            for neuron in self.parent.contents[self.pos[0]-2]:
                added+=neuron.activation*self.parent.contents[self.pos[0]-1][self.pos[1]*length+neuron.pos[1]].weight
            self.activation = self.Sigmoid(added+self.bias)  

class Connection:
    def __init__(self, weight, pos, parent):
        self.weight, self.pos, self.parent = weight, pos, parent

class NeuralNetwork:
    def __init__(self, shape, parent):
        self.parent = parent
        self.shape = shape
        self.contents = []
        for layer in range(len(shape)):
            self.contents.append([])
            for item in range(self.shape[layer]):
                if layer%2==0:
                    self.contents[layer].append(Node(0,(layer,item),self, 0))
                else:
                    self.contents[layer].append(Connection(1,(layer,item),self))
    def LoadContents(self, fileName, pos):
        global GlobalBest
        file = open(fileName+".txt", "r")
        contts = file.read().split("$")
        GlobalBest = float(contts[1])
        contts = contts[pos]
        contts = ast.literal_eval(contts)

        file.close()
        for layer in range(len(self.contents)):
            if layer%2==0:
                for neuron in self.contents[layer]:
                    neuron.bias = contts[layer][neuron.pos[1]]
            else:
                for connection in self.contents[layer]:
                    connection.weight = contts[layer][connection.pos[1]]
    def SaveContents(self, name, mode):

        file = open(name+".txt", mode)
        self.parent.parent.UpdateScore()
        fstring = "$"+str(self.parent.parent.score)+"$["
        for layer in range(len(self.contents)):
            fstring+="["
            if layer%2==0:
                for item in self.contents[layer]:
                    fstring+=str(item.bias)+","
            else:
                for item in self.contents[layer]:
                    fstring+=str(item.weight)+","
            
            fstring=fstring.rstrip(",")+"],"
        
        fstring=fstring.rstrip(",")+"]"
        file.write(fstring)
        file.close()
    def Randomize(self,noise, strength):
        for i in range(noise):
            layer = random.randrange(1,len(self.contents))
            if layer%2==0:
                self.contents[layer][random.randrange(0,len(self.contents[layer]))].bias+=(random.random()*strength[0]*random.choice((-1,1)))
            else:
                self.contents[layer][random.randrange(0,len(self.contents[layer]))].weight+=(random.random()*strength[1]*random.choice((-1,1)))
    def Run(self):
        for layer in range(0,len(self.contents),2):
            for neuron in self.contents[layer]:
                neuron.Activate()
    def PrintOutputs(self):
        print("--OUTPUTS--")
        for neuron in self.contents[-1]:
            print(neuron.activation)
    def GetOutputs(self):
        return(list(map(lambda a:a.activation, self.contents[-1])))
    def LoadInputs(self,values):
        for neuron in range(len(self.contents[0])):
            self.contents[0][neuron].activation = values[neuron]
            
class Brain:
    def __init__(self, TPUshape, CPUshape, parent):
        self.parent = parent
        self.Memory = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
        self.TPUshape = TPUshape
        self.CPUshape = CPUshape
        self.TPU = NeuralNetwork(TPUshape, self)
        self.CPU = NeuralNetwork(CPUshape, self)
    def Run(self):
        TPUInpts = self.Memory[1]
        TPUInpts.extend([self.parent.x, self.parent.y, self.parent.nearest, self.parent.inventory, self.parent.objective])
        self.TPU.LoadInputs(TPUInpts)
        self.TPU.Run()
        self.Memory[1] = self.TPU.GetOutputs()
        CPUInpts = self.TPU.GetOutputs()
        CPUInpts.extend(self.Memory[0])
        CPUInpts.extend([self.parent.x, self.parent.y, self.parent.nearest, self.parent.inventory, self.parent.objective])
        self.CPU.LoadInputs(CPUInpts)
        self.CPU.Run()
        Outputs = self.CPU.GetOutputs()
        if round(Outputs[0]) == 1:
            self.parent.LastSaid = self.TPU.GetOutputs()
        else:
            self.parent.LastSaid = [0,0,0,0,0,0,0,0,0,0,0]
        self.parent.Move(Outputs[1],Outputs[2])
        self.parent.trade = round(Outputs[3])
class Creature:
    def __init__(self, x, y, nearest,inventory, objective):
        self.x, self.y, self.nearest, self.inventory, self.objective= x, y, nearest, inventory, objective
        self.brain = Brain([15,180,12,144,12,120,10],[25,425,17,170,10,40,4], self)
        self.LastSaid = [0,0,0,0,0,0,0,0,0,0,0]
        self.trade = 0
        self.score = 0
    def Move(self,vel,dir):
        self.x+=math.cos(math.radians(dir*360))*vel
        self.y+=math.sin(math.radians(dir*360))*vel
    def UpdateScore(self):
        self.score = math.dist([self.x,self.y],[300,300])

def Render(creatures):
    window.fill((0,0,0))
    for creature in creatures:
        pygame.draw.circle(window, (255,255,0), (creature.x, creature.y), 20)
    pygame.draw.circle(window, (255,0,0), (300,300), 80, 2)
    pygame.draw.circle(window, (255,0,0), (300,300), 27.18, 2)
    pygame.display.flip()
def NewSim(parent):
    creatures = []
    for i in range(10):
        creatures.append(Creature(random.randint(0,600),random.choice([random.randint(0,100),random.randint(500,600)]),0,0,0))
        if parent == True:
            creatures[i].brain.CPU.LoadContents("BestCPU1", 2)
            creatures[i].brain.TPU.LoadContents("BestTPU1", 2)
        creatures[i].brain.CPU.Randomize(25,[2,2])
        creatures[i].brain.TPU.Randomize(25,[2,2])
    return(creatures)
def Closing(creatures):
    global GlobalBest
    for creature in creatures:
        creature.UpdateScore()
    bestScore = [creatures[0],creatures[0].score]
    for creature in creatures[1:]:
        if creature.score < bestScore[1]:
            bestScore = [creature, creature.score]
    print(GlobalBest)
    if bestScore[1] < GlobalBest:
        bestScore[0].brain.CPU.SaveContents("BestCPU1", "w")
        bestScore[0].brain.TPU.SaveContents("BestTPU1", "w")


file = open("BestCPU1.txt", "r")
GlobalBest = float(file.read().split("$")[1])
file.close()
pygame.init()
WindowSize = 600
window = pygame.display.set_mode((WindowSize, WindowSize), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Brain")


running = True
its = 0
while running:
    
    Creatures = NewSim(its>0)
    for its in range(500):
        for creature in Creatures:
            creature.brain.Run()
        Render(Creatures)
    Closing(Creatures)
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
    its+=1
pygame.display.quit()
#brain.CPU.LoadContents("NNs1",1)
#brain.CPU.SaveContents("NNs1", "w")