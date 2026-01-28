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
    def GetCost(self,desiredOutputs):
        outputs = self.GetOutputs()
        cost = 0
        for index in outputs:
            cost+= (outputs[index]-desiredOutputs[index])*(outputs[index]-desiredOutputs[index])
    def GradientDescent(self, desiredOutputs):
        changes = []
        outputs = self.GetOutputs()
        Nudges = list(map(lambda a,b : a-b, desiredOutputs, outputs))
        for indexNeuron in self.contents[-1]: # For each neuron in the output layer
            neuronChanges = []
            for i in range(len(self.contents)):
                neuronChanges.append([])
            neuronChanges[-1]=[0]*len(self.contents[-1]) # Doesn't change the biases of the other neurons
            neuronChanges[-1][indexNeuron] = Nudges[indexNeuron] # Changes the bias of the output neuron
            for connection in self.contents[-2][indexNeuron*len(self.contents[-3]):indexNeuron*len(self.contents[-3])+len(self.contents[-3])]:
                # Change the weights in relation to how activated the previous neuron is
                neuronChanges[-2][indexNeuron] =
                
        
    def Randomize(self, weightsRange, biasRange):
        for layer in self.contents:
            if layer[0].pos[0] % 2 == 0: # If neuron layer
                for node in layer:
                    node.bias = random.randint(biasRange[0], biasRange[1])
            else:
                for connection in layer:
                    connection.weight = random.random()*random.randint(weightsRange[0], weightsRange[1])
    