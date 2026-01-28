import random
import math
import pygame
import copy

class Node:
    def __init__(self, bias, pos, parent, activation):
        self.bias, self.pos, self.parent, self.activation = bias, pos, parent, activation
    def Sigmoid(self,number):
        return(1/(1+math.exp(number)))
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
    def __init__(self, shape):
        self.shape = shape
        self.contents = []
        for layer in range(len(shape)):
            self.contents.append([])
            for item in range(self.shape[layer]):
                if layer%2==0:
                    self.contents[layer].append(Node(0,(layer,item),self, 0))
                else:
                    self.contents[layer].append(Connection(1,(layer,item),self))
    def LoadInputs(self,inputs):
        for i in range(len(inputs)):
            self.contents[0][i].activation = inputs[i]
    def Mutate(self,noise, strength):
        for i in range(random.randint(0,noise)):
            layer = random.randrange(1,len(self.contents))
            if layer%2==0:
                self.contents[layer][random.randrange(0,len(self.contents[layer]))].bias+=(random.random()*strength[0]*random.choice((-1,1)))
            else:
                self.contents[layer][random.randrange(0,len(self.contents[layer]))].weight+=(random.random()*strength[1]*random.choice((-1,1)))
    def Run(self):
        for layer in range(0,len(self.contents),2):
            for neuron in self.contents[layer]:
                neuron.Activate()
    def GetOutputs(self):
        Outputs = []
        for neuron in self.contents[-1]:
            Outputs.append(neuron.activation)
        return(Outputs)
    def Randomize(self, weightsRange, biasRange):
        for layer in self.contents:
            if layer[0].pos[0] % 2 == 0: # If neuron layer
                for node in layer:
                    node.bias = random.randint(biasRange[0], biasRange[1])
            else:
                for connection in layer:
                    connection.weight = random.random()*random.randint(weightsRange[0], weightsRange[1])

# INPUTS---
# SeesFood
# DistToFood
# X
# Y
# Hunger
# OUTPUTS---
# MoveX
# MoveY
# WantsToEat
class Creature:
    def __init__(self, x, y, ID, environment, brain):
        self.x, self.y, self.ID, self.environment, self.brain, self.MAXHUNGER = x, y, ID, environment,  brain, 100
        self.hunger = self.MAXHUNGER
        self.MoveSpeed = 10
        self.SightRange = 300
        self.Time = 0
    def Tick(self):
        SeesFood = 0
        DistToFood = self.SightRange
        for food in self.environment.Foods:
            dist = math.dist([self.x,self.y],[food.x,food.y])
            if dist<=self.SightRange:
                SeesFood = 1
                DistToFood = dist/self.SightRange
                
        self.brain.LoadInputs([SeesFood, DistToFood, self.x/self.environment.size, self.y/self.environment.size, self.hunger/self.MAXHUNGER])
        self.brain.Run()
        out = self.brain.GetOutputs()
        self.x = min(max(self.x+(out[0]-0.5)*self.MoveSpeed,0),self.environment.size)
        self.y = min(max(self.y+(out[1]-0.5)*self.MoveSpeed,0),self.environment.size)
        
        if round(out[2] == 1 and self.hunger != self.MAXHUNGER): # If trying to eat
            for food in self.environment.Foods:
                dist = math.dist([self.x,self.y],[food.x,food.y])
                if dist<=30:
                    self.hunger = min(self.hunger + food.strength, self.MAXHUNGER)
                    self.environment.Foods.remove(food)
                    print("EATEN")
        self.hunger-=1
        if self.hunger <= 0:
            self.environment.Creatures.remove(self)
            self.environment.Results.append([self.Time, self.brain])
        else:
            self.Time += 1
                   
class Food:
    def __init__(self, x, y, strength):
        self.x, self.y, self.strength = x, y, strength

def SortFunc(creature):
    return(creature[0])

class Environment:
    def __init__(self, creatures, FoodSpawnRate, size):
        self.FoodSpawnRate, self.size = FoodSpawnRate, size
        self.Creatures = []
        self.Foods = []
        self.Results = []
        for creatureID in range(creatures):
            self.Creatures.append(Creature(random.randint(0,self.size),random.randint(0,self.size),creatureID,self,copy.deepcopy(CreatureBrain))) # Creates a new creature
            #self.Creatures[creatureID].brain.Mutate(2,[20,0.3])
            self.Creatures[creatureID].brain.Randomize([-1,1],[-8,8])
    def Tick(self):
        if random.randint(0,self.FoodSpawnRate) == 0:
            self.Foods.append(Food(random.randint(0,self.size),random.randint(0,self.size),60)) # Creates food at a given interval
        for creature in self.Creatures:
            creature.Tick()
        if len(self.Creatures) == 0:
            self.Results.sort(reverse=True,key=SortFunc)
            print(self.Results[0:10])
            print("All Died")
            NewCreatures = []
            for c in self.Results[0:10]:
                NewCreatures.append(c[1])
            self.Reset(NewCreatures)
    def Render(self):
        window.fill((0,0,0))
        for c in self.Creatures:
            pygame.draw.circle(window, (0,255,0), (c.x, c.y), 15)
        for f in self.Foods:
            pygame.draw.circle(window, (255,0,0), (f.x, f.y), 12)
    def Reset(self, creatures):
        self.Results = []
        self.Creatures = []
        self.Foods = []
        for creature in range(len(creatures)):
            for i in range(5):
                self.Creatures.append(Creature(random.randint(0,self.size),random.randint(0,self.size),creature*i,self,copy.deepcopy(creatures[creature])))
                self.Creatures[creature*i].brain.Mutate(3,[5,0.2])
        for i in range(50):
            self.Creatures.append(Creature(random.randint(0,self.size),random.randint(0,self.size),50+i,self,copy.deepcopy(CreatureBrain))) # Creates a new creature
            #self.Creatures[creatureID].brain.Mutate(2,[20,0.3])
            self.Creatures[50+i].brain.Randomize([-2,2],[-10,10])
# CreatureBrain = NeuralNetwork([5,10,2,6,3])
CreatureBrain = NeuralNetwork([5,15,3])
Env = Environment(100, 5, 600)

pygame.init()
#clock = pygame.time.Clock()
WindowSize = (600,600)
window = pygame.display.set_mode(WindowSize, pygame.HWSURFACE)
pygame.display.set_caption("Life simulation")
running = True
its = 0
while running:
    its +=1
    if its%20 == 0:
        Env.Tick()
        Env.Render()
        pygame.display.flip()
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for neuron in Env.Creatures[0].brain.contents[0]:
                    print(neuron.activation)
                print(Env.Creatures[0].brain.GetOutputs())
        if event.type == pygame.QUIT:
            running = False
            
            
pygame.display.quit()
    
# class Brain:
#     def __init__(self, TPUshape, CPUshape):
#         #self.TPUshape = TPUshape
#         self.CPUshape = CPUshape
#         #self.TPU = NeuralNetwork(TPUshape)
#         self.CPU = NeuralNetwork(CPUshape)

# brain = Brain(10,[42,1596,38,836,22,352,16,64,4])
# brain.CPU.Mutate(300,[3,25])
# brain.CPU.Run()
# brain.CPU.GetOutputs()