import numpy
import random
import math

DataSet = [[0,0],[0,1],[1,0],[1,1]]
Answers = [0, 1, 1, 0]

def TrainNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss,TrainingLength):
    best = TestNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss)
    for i in range(TrainingLength):
        best = TestNetwork(best[1],BiasRange, WeightRange, Iterations,Data,Anss)
    return(best)

def ModifyNetwork(N, BiasRange, WeightRange):
    for neurons in range(2,len(N),2):
        for neuron in range(len(N[neurons])):
            N[neurons][neuron].bias += random.uniform(-BiasRange,BiasRange)
    for connections in range(1,len(N),2):
        for connection in range(len(N[connections])):
            N[connections][connection].weight += random.uniform(-WeightRange,WeightRange)

def SuccessOfNetwork(N,Data,Anss):
    success = 0
    for Inputs in range(len(Data)):
        for Input in range(len(N[0])):
            N[0][Input].contents = Data[Inputs][Input]
            CalcNetwork(N)
            for i in range(len(N[-1])):
                success += math.dist([N[-1][i].contents],[Anss[i]])
    return(success/len(Data))
            
def TestNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss):
    results = [[SuccessOfNetwork(N,Data,Anss),N]]
    for i in range(Iterations):
        ModifyNetwork(N, BiasRange, WeightRange)
        results.append([SuccessOfNetwork(N,Data,Anss),N])
    results.sort()
    return(results[0])
    
def CreateNetwork(inputs, layers, NeuronsPerLayer, outputs):
    NN = []
    for layer in range(0,layers):
        NN.append([])
        for i in range(NeuronsPerLayer):
            neuron = Neuron(layer+1,i,0,0)
            NN[layer].append(neuron)
    NN.insert(0,[])
    NN.append([])
    for i in range(inputs):
        neuron = Neuron(0,i,0,0)
        NN[0].append(neuron)
    for i in range(outputs):
        neuron = Neuron(len(NN)-1,i,0,0)
        NN[-1].append(neuron)
    ConnectedNN = NN
    for i in range(len(NN)-1):
        ConnectedNN = CreateConnections(ConnectedNN, i*2, i*2+1, 0)
    return(ConnectedNN)
def CreateConnections(N, layer1, layer2, weights):
    cons = []
    Return = N
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
            
def DrawNetwork(N):
    for layer in range(len(N)):
        if layer%2 != 0:
            connections = []
            for connection in range(len(N[layer])):
                connections.append(N[layer][connection].weight)
            print(connections)
        else:
            neurons = []
            for neuron in range(len(N[layer])):
                neurons.append(N[layer][neuron].bias)
            print(neurons)
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
    def CalcOutput(self,NN):
        self.contents = 0
        counter = 0
        for i in NN[self.x-2]:
            self.contents += i.contents * NN[self.x-1][self.y*len(NN[self.x-2])+counter].weight
            counter+=1

        self.contents += self.bias
        #Sigmoid function, S(x) = 1/(1+e^-x)
        self.contents = 1/(1+numpy.exp(-self.contents))

NN = CreateNetwork(2,2,3,2)
#CalcNetwork(NN)
#DrawNetwork(NN)

print(TrainNetwork(NN,0.2,0.01,20,DataSet,Answers,100))
DrawNetwork(NN)

#print(TestNetwork(NN,0.5,0.2,10,DataSet,Answers))



#ModifyNetwork(NN,0.5,0.2)

#0.00147 success neurons and connections
#[0.24059022992150425, -0.507590057952861, 0.18567948365304907, -0.022499593878765645, 0.21688796887891926, -0.05115616077172881]
#[4.8625220093361206, 11.601280954032983, -6.923480451558224]
#[0.30352684535546276, -0.2227713629714769, -0.045180213628622505, -0.002460545635218506, -0.46000222793152545, 0.0570847476908263, -0.19284064399196094, -0.04914125799543748, -0.11521174478363445]
#[-0.9886871523651097, -1.1394313950346364, -3.1069526684766435]
#[0.39729916308757574, -0.5418151827728571, -0.269888358015674, 0.1425584059784902, -0.18506198449552158, -0.21052636548371484]

