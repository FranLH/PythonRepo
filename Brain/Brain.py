import random
import math
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
    def Randomize(self,noise, strength):
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
        print("--OUTPUTS--")
        for neuron in self.contents[-1]:
            print(neuron.activation)
            
class Brain:
    def __init__(self, TPUshape, CPUshape):
        #self.TPUshape = TPUshape
        self.CPUshape = CPUshape
        #self.TPU = NeuralNetwork(TPUshape)
        self.CPU = NeuralNetwork(CPUshape)
brain = Brain(10,[42,1596,38,836,22,352,16,64,4])
brain.CPU.Randomize(300,[3,25])
brain.CPU.Run()
brain.CPU.GetOutputs()