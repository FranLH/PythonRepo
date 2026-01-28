# TO DO:
# Load weights and biases from .csv file
# Better interface with pygame
# https://www.3blue1brown.com/lessons/backpropagation#title
# Consider switching to ReLu


from math import e as EULER
import random
import numpy
from mnist import MNIST
import copy


# d(sigmoid) = (e^-x) / (1 + e^-x)^2

class NeuralNetwork:
    def __init__(self, structure:list[int]):
        self.layers:list["Layer"] = []
        for layer in range(len(structure)-1):
            self.layers.append(Layer(structure[layer],layer*2, self))
            self.layers.append(Layer(structure[layer]*structure[layer+1], layer*2+1, self))
        layer+=1
        self.layers.append(Layer(structure[layer],layer*2, self))
        
        #self.layers = layers
    def SaveToFile(self, filename:str):
        file = open(filename, "w")
        for layer in range(len(self.layers)):
            line = ""
            if layer%2==0:
                for nodeIdx in range(self.layers[layer].size):
                    line+=str(self.layers[layer].contents[nodeIdx].bias)+";"
            else:
                for connIdx in range(self.layers[layer].size):
                    line+=str(self.layers[layer].contents[connIdx].weight)+";"
            
            line = line.rstrip(";")
            file.write(line+"\n")
        file.close()
    def LoadFromFile(self, filename:str):
        file = open(filename, "r")
        
        for layer in range(len(self.layers)):
            layerData = file.readline().split(";")
            #print(file.readline().split(";"))
            if layer%2==0:
                for nodeIdx in range(self.layers[layer].size):
                    self.layers[layer].contents[nodeIdx].bias = float(layerData[nodeIdx])
            else:
                for connIdx in range(self.layers[layer].size):
                    #print(float(layerData[connIdx]))
                    self.layers[layer].contents[connIdx].weight = float(layerData[connIdx])
        file.close()
        print("Successfully loaded ANN from",filename)
    def SetInputs(self,inputs:list[float]): # Loads the inputs to the neural network
        for input in range(len(inputs)):
            self.layers[0].contents[input].activation = inputs[input]
    def GetOutputs(self):
        return(list(map(lambda node : node.activation, self.layers[-1].contents)))        
    def Run(self, useSigmoid:bool):
        for layer in range(2,len(self.layers),2): # For each layer of nodes
            for node in self.layers[layer].contents: # For each node in the layer
                node.Activate(useSigmoid)
    def GetCost(self, desiredOutputs:list[float]):
        cost = 0
        outputs = self.GetOutputs()
        for outputIdx in range(len(outputs)):
            cost+=(desiredOutputs[outputIdx]-outputs[outputIdx])**2
        return cost
    def Exp(self,num):
        if num < -200:
            return 0
        else:
            return(numpy)
    def Backpropagation(self, desiredOutputs:list[float]):
        changes:list[list[float]] = [] # This will store all the changes done to the weights and biases
        activationDerivatives:list[list[float]] = [] # This will store the derivatives of the activation function for each neuron, to avoid having to calculate them repeatedly

        
        for layer in range(len(self.layers)):
            changes.append([])
            activationDerivatives.append([])
            for _ in self.layers[layer].contents:
                changes[layer].append(0)
                activationDerivatives[layer].append(0)
            
        # To calculate the derivative of the output neuron's bias over the total cost, I just need to take into account the cost for that neuron, as the bias doesn't affect the other costs meaning they are constants

        for nodeY in range(self.layers[-1].size): # For each output node, calculates how much it should change to minimise cost
            node = self.layers[-1].contents[nodeY]
            biasSlope = 2*(node.activation-desiredOutputs[nodeY]) # Calculates the derivative of the cost function in relation to the output neuron's bias
            activationDerivatives[-1][nodeY] = node.activation * (1 - node.activation)

            changes[-1][nodeY] = biasSlope*activationDerivatives[-1][nodeY] # The bias should be changed relative to the slope
            
        # Handle all neuron layers but the input and output ones
        for layer in range(len(self.layers)-3, 0, -2): # For each of the remaining neuron layers, backwards and ignoring the input and output layer
            neuronLayer = self.layers[layer]
            connectionsLayer = self.layers[layer+1]
            nextNeuronLayer = self.layers[layer+2]
            
            for nodeY, node in enumerate(neuronLayer.contents): # Calculates the derivative of the activation of each neuron
                activationDerivatives[layer][nodeY] = node.activation * (1 - node.activation)
                
            for nodeY, node in enumerate(neuronLayer.contents): # For each node in the layer
                
                connectedDerivatives = 0.0 # This will store the sum of the derivatives of the following nodes, propagating their values backwards
                
                for nextY in range(len(nextNeuronLayer.contents)): # For each node in the following nodes layer
                    connectionY = nodeY + nextY * neuronLayer.size
                    connectedDerivatives += connectionsLayer.contents[connectionY].weight * changes[layer+2][nextY]
                changes[layer][nodeY] = connectedDerivatives * activationDerivatives[layer][nodeY]
            
        # Calculates the gradient for the connections to the next layer
            for connY in range(len(connectionsLayer.contents)):

                previousNeuronY = connY % neuronLayer.size

                nextNeuronY = connY // neuronLayer.size if neuronLayer.size!=1 else 0
                changes[layer+1][connY] = neuronLayer.contents[previousNeuronY].activation * changes[layer+2][nextNeuronY]
                #changes[layer+1][connY] = neuronLayer.contents[nextNeuronY].activation * changes[layer+2][nextNeuronY]
        
        neuronLayer = self.layers[0]
        nextNeuronLayer = self.layers[2]
        for connY in range(len(self.layers[1].contents)): # Handles the gradient for the weights connected to the input layer
            previousNeuronY = connY % neuronLayer.size
            nextNeuronY = connY // neuronLayer.size
            changes[1][connY] = neuronLayer.contents[previousNeuronY].activation * changes[2][nextNeuronY]
        return(changes)
            
                 

    def ChangeWeightsAndBiases(self, changes, weightMult:float, biasMult:float):
        # Averages all of the changes together
        amount = len(changes)
        averageChanges = copy.deepcopy(changes[0])
        
        for i in range(len(averageChanges)):
            for j in range(len(averageChanges[i])):
                    averageChanges[i][j] /= amount  # divide the first one too

        for change in range(1,len(changes)):
            for i in range(len(changes[change])):
                for j in range(len(changes[change][i])):
                    averageChanges[i][j] += changes[change][i][j]/amount
                
        for layer in range(len(self.layers)):
            if layer%2==0:
                for i in range(self.layers[layer].size):
                    self.layers[layer].contents[i].bias -= averageChanges[layer][i]*biasMult    
            else:
                for i in range(self.layers[layer].size):
                    self.layers[layer].contents[i].weight -= averageChanges[layer][i]*weightMult
                
                 
    def __repr__(self): # Returns all of the biases and weights as a string
        string = "-STRUCTURE-\n"
        for layer in self.layers:
            string+=str(layer)+"\n"
        return(string)
    def ReprActivations(self): # Returns all of the activations as a string
        string = "-ACTIVATIONS-\n"
        for layer in range(0,len(self.layers),2):
            string+=str(list(map(lambda node: node.activation, self.layers[layer].contents)))+"\n"
        return(string)    

class Node:
    def __init__(self, Bias:float, xPos, yPos:int, network:NeuralNetwork):
        self.bias, self.xPos, self.yPos, self.network, self.EULER = Bias, xPos, yPos, network, EULER
        self.noSigmoidActivation = 0 # Will store the activation of the neuron, before the activation function is applied. (Required for backpropagation to work)
        self.activation = 0 # Will store the activation of the neuron
    def __repr__(self):
        return str(self.bias)
    def ActivationFunction(self,activation): # Sigmoid
        return 1/(1+numpy.exp(-activation)) # if -300 < activation < 300:

    def Activate(self,useSigmoid:bool): # A node's activation is the sum of each previous node multiplied by their respective weight, all of this added to the bias
        self.activation = self.bias
        self.noSigmoidActivation = self.bias
        previousNodeLayer = self.network.layers[self.xPos-2]
        weightsLayer = self.network.layers[self.xPos-1]
        for x in range(previousNodeLayer.size):
            self.noSigmoidActivation += previousNodeLayer.contents[x].activation * weightsLayer.contents[x + self.yPos*previousNodeLayer.size].weight
        if useSigmoid:

            self.activation = self.ActivationFunction(self.noSigmoidActivation)
        else:
            self.activation=self.noSigmoidActivation


class Connection:
    def __init__(self, Weight:float, yPos:int):
        self.weight, self.yPos = Weight, yPos
    def __repr__(self):
        return str(self.weight)        

class Layer:
    def __init__(self, size:int, xPos:int, network:NeuralNetwork):
        self.xPos, self.size, self.network = xPos, size, network
        self.contents:list[Node]|list[Connection] = []
        if xPos%2==0:
            for i in range(size):
                self.contents.append(Node(0,xPos,i,network))
        else:
            for i in range(size):
                self.contents.append(Connection(random.random()*random.choice([-0.0025,0.0025]),i)) # random.random()*random.choice([-1,1])
    def __repr__(self):
        return str(self.contents)

def OutputEncoder(value):
    output = [0]*10
    output[value] = 1
    return (output)
def OutputDecoder(output:list):
    outputs = output
    biggest = 0
    for i in range(len(output)):
        if output[i]>output[biggest]:

            biggest = i
    #outputs = list(map(lambda a:a*100, outputs))
    return (biggest)

def TestNetwork():
    averageCost = 0
    for i in range(700,1000):
        
        LNN.SetInputs(testImages[i])
        LNN.Run(True)
        averageCost+=LNN.GetCost(OutputEncoder(testLabels[i]))
    print("Final network cost:", averageCost/300)
    
def NormalizeInput(inputs:list):
    return(list(map(lambda a:(a/255), inputs))) # a/255 vs a/255+0.5


# Loads the MNIST dataset
mndata = MNIST("archive",mode="vanilla",gz=False)
testImages, testLabels = mndata.load_testing()
trainImages, trainLabels = mndata.load_training()

LNN = NeuralNetwork([784,40,10])
#LNN.LoadFromFile("TotalNN.csv")


Wmult = 0.05 # 2
Bmult = 0.1 # 3

BATCHSIZE = 100 # 64
BATCHES = 600 #120

#OverfitTest = True

print(OutputDecoder([0.1,0.1,0.2,0.1,0.1,0,0,0,0]))

averageCost = 0
for i in range(700,1000):
    
    LNN.SetInputs(testImages[i])
    LNN.Run(True)
    averageCost+=LNN.GetCost(OutputEncoder(testLabels[i]))
print(i)
print("Initial network cost:", averageCost/300)

print("INITIATING TRAINING")
for _ in range(1):
    for batch in range(BATCHES):
        print("Starting batch", batch, "/", BATCHES)
        modifications = []
        averageBatchCost = 0
        for example in range(BATCHSIZE):
            trainingIdx = batch*BATCHSIZE + example
            LNN.SetInputs(NormalizeInput(trainImages[trainingIdx])) # 
            LNN.Run(True)
            modifications.append(LNN.Backpropagation(OutputEncoder(trainLabels[trainingIdx])))
            averageBatchCost+=LNN.GetCost(OutputEncoder(trainLabels[trainingIdx]))
        print("Average batch cost:", averageBatchCost/BATCHSIZE)
        LNN.ChangeWeightsAndBiases(modifications, Wmult, Bmult)

TestNetwork()

print(len(trainImages))
LNN.SetInputs(trainImages[100])
LNN.Run(True)
print(trainLabels[100], "-->", OutputDecoder(LNN.GetOutputs()))

print(LNN.GetOutputs())
total = 0
for i in range(100,200):
    LNN.SetInputs(testImages[i])
    LNN.Run(True)
    #print(testLabels[i], "-->", OutputDecoder(LNN.GetOutputs()))
    if (testLabels[i] == OutputDecoder(LNN.GetOutputs())):
        total += 1
print(total)

LNN.SaveToFile("TotalNN.csv")

# BestNN 0.8922682382331336
# Best784,30,10 0.36201794799070824

