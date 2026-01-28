# TO DO:
# Gradient descent for weights
# Redo the whole backpropagation function, i'm sure its all wrong.
# As of now it doesn't work for more than the last layer as it needs the loss values for the other layers.
# https://www.3blue1brown.com/lessons/backpropagation#title


from math import e as EULER
import random
import numpy
import math

print(numpy.exp(-900))

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
            for data in self.layers[layer].contents:
            
                line+=str(data)+";"
            
            line = line.rstrip(";")
            file.write(line+"\n")
        file.close()

            
        #file.writelines()
    def SetInputs(self,inputs:list[float]): # Loads the inputs to the neural network
        for input in range(len(inputs)):
            self.layers[0].contents[input].activation = inputs[input]
    def GetOutputs(self):
        return(list(map(lambda node:node.activation, self.layers[-1].contents)))        
    def Run(self, useSigmoid:bool):
        #print(">RUNNING")
        for layer in range(2,len(self.layers),2): # For each layer of nodes
            for node in self.layers[layer].contents: # For each node in the layer
                node.Activate(useSigmoid)
        #print(">FINISHED")
        #print(self.ReprActivations())
    def GetCost(self, desiredOutputs:list[float]):
        cost = 0
        outputs = self.GetOutputs()
        for i in range(len(outputs)):
            cost+=(desiredOutputs[i]-outputs[i])**2
        return cost
    def Exp(self,num):
        if num < -200:
            return 0
        else:
            return(numpy)
    def Backpropagation(self, desiredOutputs:list[float]):
        
        changes = [] # This will store all the changes done to the weights and biases
        activationDerivatives = [] # This will store the derivatives of the activation function for each neuron, to avoid having to calculate them repeatedly

        
        for i in range(len(self.layers)):
            changes.append([])
            activationDerivatives.append([])
            for j in self.layers[i].contents:
                changes[i].append(0)
                activationDerivatives[i].append(0)
            
        # To calculate the derivative of the output neuron's bias over the total cost, I just need to take into account the cost for that neuron, as the bias doesn't affect the other costs meaning they are constants

        for nodeY in range(self.layers[-1].size): # For each output node, calculates how much it should change to minimise cost
            node = self.layers[-1].contents[nodeY]
            biasSlope = 2*(node.activation-desiredOutputs[nodeY]) # Calculates the derivative of the cost function in relation to the output neuron's bias
            activationDerivatives[-1][nodeY] = node.activation * (1 - node.activation)
            #print(node.activation * (1 - node.activation), numpy.exp(-node.noSigmoidActivation)/((1+numpy.exp(-node.noSigmoidActivation))**2))
            #activationDerivatives[-1][nodeY] = numpy.exp(-node.noSigmoidActivation)/((1+numpy.exp(-node.noSigmoidActivation))**2) if node.noSigmoidActivation < 300 and node.noSigmoidActivation > -300 else 0 # Calculates the derivative of the neuron's activation function and stores it
            changes[-1][nodeY] = biasSlope*activationDerivatives[-1][nodeY] # The bias should be changed relative to the slope
        
        
        # Remove this, already handled by the following paragraph
#         neuronLayer = self.layers[-3] # The second to last layer of neurons
#         for connY in range(self.layers[-2].size): # For each connection to the last neurons
#             nextNeuronY = connY//neuronLayer.size
#             weightSlope = 2*(self.layers[-1].contents[nextNeuronY].activation-desiredOutputs[nextNeuronY]) # Calculates the derivative of the cost function in relation to the weight
#             #print(self.layers[-1].contents[nextNeuronY].activation, desiredOutputs[nextNeuronY], weightSlope)
#             previousNeuronY = connY%neuronLayer.size # The previous neuron  WORKS
#             #print(activationDerivatives[-1][nextNeuronY])
#             changes[-2][connY] = -weightSlope * neuronLayer.contents[previousNeuronY].activation * activationDerivatives[-1][nextNeuronY]
#             #print(activationDerivatives[-1][0])
            
        # Handle all neuron layers but the input and output ones
        for layer in range(len(self.layers)-3, 0, -2): # For each of the remaining neuron layers, backwards and ignoring the input and output layer
            neuronLayer = self.layers[layer]
            connectionsLayer = self.layers[layer+1]
            nextNeuronLayer = self.layers[layer+2]
            
            for nodeY, node in enumerate(neuronLayer.contents): # Calculates the derivative of the activation of each neuron
                activationDerivatives[layer][nodeY] = node.activation * (1 - node.activation)
                
            for nodeY, node in enumerate(neuronLayer.contents): # For each node in the layer
                
                connectedDerivatives = 0 # This will store the sum of the derivatives of the following nodes, propagating their values backwards
                
                for nextY, nextNode in enumerate(nextNeuronLayer.contents): # For each node in the following nodes layer
                    connectionY = nodeY + nextY * neuronLayer.size
                    connectedDerivatives += connectionsLayer.contents[connectionY].weight * changes[layer+2][nextY]
                changes[layer][nodeY] = connectedDerivatives * activationDerivatives[layer][nodeY]
            
            
        # Calculates the gradient for the connections to the next layer
            for connY, connection in enumerate(connectionsLayer.contents):
                previousNeuronY = connY % neuronLayer.size
                nextNeuronY = connY // neuronLayer.size
                changes[layer+1][connY] = neuronLayer.contents[nextNeuronY].activation * changes[layer+2][nextNeuronY]
        
        
        neuronLayer = self.layers[0]
        nextNeuronLayer = self.layers[2]
        for connY, connection in enumerate(self.layers[1].contents): # Handles the gradient for the weights connected to the input layer
            previousNeuronY = connY % neuronLayer.size
            nextNeuronY = connY // neuronLayer.size
            changes[1][connY] = neuronLayer.contents[previousNeuronY].activation * changes[2][nextNeuronY]
        return(changes)
            
                 

    def ChangeWeightsAndBiases(self, changes, weightMult:float, biasMult:float):
        # Averages all of the changes together
        amount = len(changes)
        averageChanges = changes[0]
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
    def __init__(self, bias:float, xPos, yPos:int, network:NeuralNetwork):
        self.bias, self.xPos, self.yPos, self.network, self.EULER = bias, xPos, yPos, network, EULER
        self.noSigmoidActivation = 0 # Will store the activation of the neuron, before the activation function is applied. (Required for backpropagation to work)
        self.activation = 0 # Will store the activation of the neuron
    def __repr__(self):
        return str(self.bias)
    def ActivationFunction(self,activation):
        #SIGMOID
        
#         if -300 < activation < 300:
        return 1/(1+numpy.exp(-activation))
            #return(1/(1+self.EULER**(-1*activation)))
#         else:
#             return(0)
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
    def __init__(self, weight:float, yPos:int):
        self.weight, self.yPos = weight, yPos
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
                self.contents.append(Connection(1,i))
    def __repr__(self):
        return str(self.contents)
        

    

        
LNN = NeuralNetwork([2,2])


Wmult = 30
WmultDropoff = 1.001
Bmult = 0.01



for j in range(100): # Simple example that compares if a number is larger than another one
    modifications = []
    bigCost = 0
    for i in range(100): 
        
        num = random.randint(0,100)
        num2 = random.randint(0,100)
        LNN.SetInputs([num/100, num2/100])
        LNN.Run(True)
        modifications.append(LNN.Backpropagation([int(num>num2), int(num2>num)]))
        bigCost+=LNN.GetCost([int(num>num2), int(num2>num)])
        
        #print(modifications)

    
        #print("Changes:",changes)
    #print(modifications)
    #print("COST:", bigCost)
    LNN.ChangeWeightsAndBiases(modifications, Wmult, Bmult)
    Wmult/=WmultDropoff

        #print(modifications)
    if j > 750:
        
        print([int(num>num2), int(num2>num)], num,num2, "-->", LNN.GetOutputs()[0], LNN.GetOutputs()[1])
        #print(modifications)
        print("cost:",LNN.GetCost([int(num>num2), int(num2>num)]))
print(Wmult)
LNN.SetInputs([89/100,90/100])
LNN.Run(True)
print(LNN.GetOutputs()[0], LNN.GetOutputs()[1])
print("BIG COST", bigCost/100)
print(LNN)
print(LNN.ReprActivations())
LNN.SaveToFile("NN.csv")



