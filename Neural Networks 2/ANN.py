# TO DO:
# Gradient descent for weights
# Redo the whole backpropagation function, i'm sure its all wrong.
# As of now it doesn't work for more than the last layer as it needs the loss values for the other layers.
# https://www.3blue1brown.com/lessons/backpropagation#title

from math import e as EULER
import random
import numpy

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
    def Backpropagation(self, desiredOutputs:list[float], weightMult:float, biasMult:float):
        
        changes = [] # This will store all the changes done to the weights and biases
        activationDerivatives = [] # This will store the derivatives of the activation function for each neuron, to avoid having to calculate them repeatedly
        for i in range(len(self.layers)):
            changes.append([])
            activationDerivatives.append([])
            for j in self.layers[i].contents:
                changes[i].append(0)
                activationDerivatives[i].append(0)

        for layer in range(len(self.layers)-1,1,-2): # For each layer of nodes (backwards)
            previousNodeLayer = self.layers[layer-2]
            connectionsLayer = self.layers[layer-1]
            for nodeY in range(self.layers[layer].size): # For each node in the layer
                node = self.layers[layer].contents[nodeY]
                
                #activationNoSigmoid = 
                activationDerivatives[layer][nodeY]=numpy.exp()
        
#         
#         loss = []
#         outputs = self.GetOutputs()
#         for i in range(len(outputs)):
#             loss.append(desiredOutputs[i]-outputs[i])
#             
#         
#         for layer in range(len(self.layers)-1,1,-2): # For each layer of nodes (backwards)
#             previousNodeLayer = self.layers[layer-2]
#             connectionsLayer = self.layers[layer-1]
#             for nodeY in range(self.layers[layer].size): # For each node in the layer
#                 node = self.layers[layer].contents[nodeY]
#                 #changes[layer][node.yPos] += loss[nodeY] * biasMult
#                 changes[layer][node.yPos] += (int(loss[nodeY]>0)*2-1) * biasMult # The bias just changes in direct proportion to the loss
#                 if True: # connectionsLayer.xPos!=1
#                     for otherNode in previousNodeLayer.contents: # For each node in the previous layer
#                         if otherNode.activation != 0:
#                             #changes[layer-1][otherNode.yPos*self.layers[layer].size + node.yPos] += loss[nodeY]*weightMult / otherNode.activation
#                             changes[layer-1][otherNode.yPos*self.layers[layer].size + node.yPos] += ((int(loss[nodeY]>0)*2-1) * weightMult) # Changes the weights of the connections depending of the loss and their "importance"
#                 else:
#                     for otherNode in previousNodeLayer.contents: # For each node in the previous layer
#                         changes[layer-1][otherNode.yPos*self.layers[layer].size + node.yPos] += loss[nodeY]*weightMult # Changes the weights of the connections depending of the loss                 
# 
# #                 for connectionY in range(nodeY, connectionsLayer.size, self.layers[layer].size): # For each connection that 
# #                     connection = connectionsLayer.contents[connectionY]
# #                     changes[layer][node.yPos]+=loss[nodeX] # The bias just changes in direct proportion to the loss                
#                 
#         # Now do the weights
                 
        return changes
    def ChangeWeightsAndBiases(self, changes):
        for layer in range(len(self.layers)):
            for i in range(self.layers[layer].size):
                if layer%2==0:
                    self.layers[layer].contents[i].bias += changes[layer][i]
                else:
                    self.layers[layer].contents[i].weight += changes[layer][i]
                 
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
        self.activation = 0
    def __repr__(self):
        return str(self.bias)
    def ActivationFunction(self,activation):
        #SIGMOID
        try:
            return 1/(1+numpy.exp(-activation))
            #return(1/(1+self.EULER**(-1*activation)))
        except:
            print("error",activation)
    def Activate(self,useSigmoid:bool): # A node's activation is the sum of each previous node multiplied by their respective weight, all of this added to the bias
        self.activation = self.bias
        previousNodeLayer = self.network.layers[self.xPos-2]
        weightsLayer = self.network.layers[self.xPos-1]
        for x in range(previousNodeLayer.size):
            self.activation += previousNodeLayer.contents[x].activation * weightsLayer.contents[x + self.yPos*previousNodeLayer.size].weight
        if useSigmoid:
            self.activation = self.ActivationFunction(self.activation)

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
                self.contents.append(Node(1,xPos,i,network))
        else:
            for i in range(size):
                self.contents.append(Connection(1,i))
    def __repr__(self):
        return str(self.contents)
        

    

        
LNN = NeuralNetwork([2,2])
# print(LNN)
# LNN.SetInputs([20])
# LNN.Run()
# print(LNN.GetOutputs())

Wmult = 0.0005
Bmult = 0



for j in range(1000):
    modifications = []
    for i in range(50): # Simple Neural network test, trains a model with a single neuron to recognize if a number is smaller or bigger than 50
        num = random.randint(0,100)
        num2 = random.randint(0,100)
        LNN.SetInputs([num, num2])
        LNN.Run(True)
        modifications.append(LNN.Backpropagation([int(num>num2), int(num2>num)], Wmult, Bmult))
    
        #print("Changes:",changes)
    for change in modifications:
        LNN.ChangeWeightsAndBiases(change)
    if j > 900:
        print(num,num2, "-->", round(LNN.GetOutputs()[0]), round(LNN.GetOutputs()[1]))
        print(modifications[-1])
        print("cost:",LNN.GetCost([int(num>num2), int(num2>num)]))
print(LNN)
print(LNN.ReprActivations())
LNN.SaveToFile("NN.csv")

# 100 -> 200
# 100 -> 0 loss=200
# 
# 100 -> 200
# 100 -> 180 loss = 20

# 0 -> 0
# 0 -> 0.1 loss = -0.1

