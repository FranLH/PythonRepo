import numpy

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
    print(ConnectedNN[2][0].__class__.__name__)
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
CalcNetwork(NN)

for i in range(0,len(NN),2):
    pr = ""
    for j in NN[i]:
        pr = pr + str(j.contents) + "  "
    print(pr)


