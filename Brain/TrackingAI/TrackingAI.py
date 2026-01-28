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
    def __init__(self, CPUshape, parent):
        self.parent = parent
        self.CPUshape = CPUshape
        self.CPU = NeuralNetwork(CPUshape, self)
    def Run(self):

        CPUInpts = [self.parent.x-self.parent.objectivex, self.parent.y-self.parent.objectivey]
        self.CPU.LoadInputs(CPUInpts)
        self.CPU.Run()
        Outputs = self.CPU.GetOutputs()
        self.parent.Move(Outputs[0],Outputs[1])
        self.parent.UpdateScore()
class Creature:
    def __init__(self, x, y, objectivex, objectivey):
        self.x, self.y, self.objectivex, self.objectivey= x, y, objectivex, objectivey
        self.brain = Brain([2,6,3,6,2], self)
        self.score = 0
    def Move(self,vel,dir):
        self.x+=vel-0.5
        self.y+=dir-0.5
    def UpdateScore(self):
        self.score = math.dist([self.x,self.y],[self.objectivex,self.objectivey])
def Render(creatures):
    window.fill((0,0,0))
    for creature in creatures:
        pygame.draw.circle(window, (255,255,0), (creature.x, creature.y), 20)
    pygame.draw.circle(window, (0,0,255), (objective[0],objective[1]), 80, 2)
    pygame.draw.circle(window, (255,0,0), (300,300), 27.18, 2)
    pygame.display.flip()
def NewSim(parent):
    global objective
    creatures = []
    startPos = [300,300] #random.randint(0,600),random.randint(0,600)
    angle = random.randint(0,360)
    objective = [300+math.cos(math.radians(angle))*300,300+math.sin(math.radians(angle))*300]
    for j in range(5):
        for i in range(4):
            creatures.append(Creature(startPos[0],startPos[1], objective[0], objective[1]))
            if parent == True:
                creatures[i].brain.CPU.LoadContents("BestCPU1", (i+1)*2)
            if i != 0: # Keeps the original one alive in case the other ones are worse
                creatures[j*i].brain.CPU.Randomize(5,[10,20])
    return(creatures)
def Closing(creatures):
    global GlobalBest
    scores = []
    for creature in range(len(creatures)):
        scores.append([creatures[creature].score, creature])
    scores.sort()
    for creature in range(4):
        if creature == 0:
            creatures[scores[creature][1]].brain.CPU.SaveContents("BestCPU1", "w")
        else:
            creatures[scores[creature][1]].brain.CPU.SaveContents("BestCPU1", "a")
    print(scores[0][0])



pygame.init()
WindowSize = 600
window = pygame.display.set_mode((WindowSize, WindowSize), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Brain")


running = True
its = 0
while running:
    
    Creatures = NewSim(its>0)
    for its in range(1000):
        for creature in Creatures:
            creature.brain.Run()
        Render(Creatures)
    print(objective)
    Closing(Creatures)
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
    its+=1
pygame.display.quit()
#brain.CPU.LoadContents("NNs1",1)
#brain.CPU.SaveContents("NNs1", "w")