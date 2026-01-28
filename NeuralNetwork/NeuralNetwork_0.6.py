import numpy
import random
import math

DataSet = [[0,1,1,1,1,1,0,0],[1,1,1,1,0,0,0,0],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,0],[0,0,0,0,0,1,1,1],[0,0,0,1,0,1,0,0],[1,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0]]
Answers = [0,0,1,1,0,1,0,1]

def SortFunc(e):
    return(e[0])

def TrainNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss,TrainingLength):
    results = [TestNetwork(N,0,0,1,Data,Anss)]
#    best = TestNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss)
    for i in range(TrainingLength):
        new = TestNetwork(results[0][1],BiasRange, WeightRange, Iterations,Data,Anss)
        results.append(new)
        results.sort(key=SortFunc)
#        if new[0]<best[0]:
#            print("better")
#            print(new)
#            best = new
        if i%50 == 0:
            print(i)
#        if i > 450:
#            print(new)
#    print(TestNetwork(best[1],0,0,1,Data,Anss))
#    print(best)
#    print(TestNetwork(best[1],0,0,1,Data,Anss))
    print("now")
    print(results)
    print(TestNetwork(results[0][1],0, 0, 1,Data,Anss))
    return(results)

def TestSingleData(N,data,Answer):
    print("--Trying--")
    for Input in range(len(N[0])):
        N[0][Input].contents = data[Input]
    CalcNetwork(N)
    for out in range(len(N[-1])):
        if out == Answer:
            print("This should be a 1")
        print(N[-1][out].contents)


    
def ModifyNetwork(N, BiasRange, WeightRange):
    output = N
    for neurons in range(2,len(output),2):
        for neuron in range(len(output[neurons])):
            output[neurons][neuron].bias += random.uniform(-BiasRange,BiasRange)
    for connections in range(1,len(output),2):
        for connection in range(len(output[connections])):
            output[connections][connection].weight += random.uniform(-WeightRange,WeightRange)
    return(output)
def SuccessOfNetwork(N,Data,Anss):
    success = 0
    for Inputs in range(len(Data)):
        for Input in range(len(N[0])):
            N[0][Input].contents = Data[Inputs][Input]
        CalcNetwork(N)
        success += math.dist([N[-1][Anss[Inputs]].contents],[1])
#        success += math.dist([N[-1][ID].contents],[Anss[Inputs]])
    return(success/len(Data))
   
######################################PROBLEM##########################
def TestNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss):
    results = [[SuccessOfNetwork(N,Data,Anss),N]]
    testN = N
    for i in range(Iterations):
        testN = ModifyNetwork(testN, BiasRange, WeightRange)
        results.append([SuccessOfNetwork(testN,Data,Anss),testN])
    results.sort(key=SortFunc)
    if Iterations>1:
        print("Same?")
        print(TestNetwork(results[0][1],0,0,1,Data,Anss))
        print(results[0])
    return(results[0])
    
def CreateNetwork(Type, inputs, layers, NeuronsPerLayer, outputs, load):
    if Type == "NewBasic":
        NewN = []
        for layer in range(0,layers):
            NewN.append([])
            for i in range(NeuronsPerLayer):
                neuron = Neuron(layer+1,i,0,0)
                NewN[layer].append(neuron)
        NewN.insert(0,[])
        NewN.append([])
        for i in range(inputs):
            neuron = Neuron(0,i,0,0)
            NewN[0].append(neuron)
        for i in range(outputs):
            neuron = Neuron(len(NewN)-1,i,0,0)
            NewN[-1].append(neuron)
        ConnectedNN = NewN
        for i in range(len(NewN)-1):
            ConnectedNN = CreateConnections(ConnectedNN, i*2, i*2+1, 0)
        return(ConnectedNN)
    elif Type == "Load":
        NewN = []

        for layer in range(len(load)):


            if layer%2 != 0:
                connections = []


                for i in range(len(load[layer])):
                    c = Connection(layer, i, load[layer][i])
                    connections.append(c)
                NewN.insert(layer,connections)

            else:
                neurons = []
                for i in range(len(load[layer])):
                    n = Neuron(layer, i, load[layer][i], 0)
                    neurons.append(n)
                NewN.insert(layer,neurons)
        
        return(NewN)
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
def SaveNetwork(N):
    output = []
    for layer in range(len(N)):
        if layer%2 != 0:
            connections = []
            for connection in range(len(N[layer])):
                connections.append(N[layer][connection].weight)
            output.append(connections)
        else:
            neurons = []
            for neuron in range(len(N[layer])):
                neurons.append(N[layer][neuron].bias)
            output.append(neurons)
    print("---------SAVE---------")
    print(output)
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
    def CalcOutput(self,N):
        self.contents = 0
        counter = 0
        for i in N[self.x-2]:
            self.contents += i.contents * N[self.x-1][self.y*len(N[self.x-2])+counter].weight
            counter+=1

        self.contents += self.bias
        #Sigmoid function, S(x) = 1/(1+e^-x)
        self.contents = 1/(1+numpy.exp(-self.contents))

#NN = CreateNetwork("NewBasic",8,2,4,2,0)
NN = CreateNetwork("Load",2,2,3,2,[[0, 0, 0, 0, 0, 0, 0, 0], [-20.996118933702274, -77.69273988918225, 83.24029944447717, 119.36775773730692, 149.3425942087484, -128.32086773306622, 36.67155999294739, 36.63024352470409, 14.062203812897922, -136.98346060243568, 56.97231106463003, -157.78207337205214, -145.04760712330233, -62.31726174701751, 25.53070962802381, -12.176496065179052, 76.19608909434133, 189.51520496366, -107.91148838886501, -3.5467284414671756, 29.040833994368292, -247.0451699381649, -22.98765222969776, 28.720097003813063, 111.09741766470104, 31.712160855834146, 189.17837676330808, 152.24265308160008, 123.88150273396357, -222.32383426969, 46.30871789463183, 135.4822602504532], [8.853114782725882, 77.56287958259114, -29.37757511638403, -49.09038597972813], [-120.72783303914925, -32.641010187718614, -31.68949516949565, 231.3818180313495, -34.7789244648062, -26.71505811340331, -13.575719864561268, 40.07636904583791, 19.957190598995933, 75.3181835378791, 51.86521096614326, 154.2855877982211, -47.50364064120732, 19.628607308336814, 191.4995458369665, 56.25189304004078], [243.50953667572645, 43.62610970415956, 115.9443725866013, 8.266177570555575], [42.46847467758367, -60.64173201827577, -109.43511664844323, -217.28581440162412, -113.64010063874183, -135.03070887606185, 67.39918082809798, 96.48285664797545], [180.62738649663308, -20.331360174197336]])


#TestSingleData(NN,[0,1,0,1,0,1,0,0],1)
Trained = TrainNetwork(NN,0.5,0.5,40,DataSet,Answers,200)

print(Trained[0])
NN = Trained[0][1]
#-----------BUG--------------
#print(TestNetwork(NN,0,0,1,DataSet,Answers))
#print(TestNetwork(NN,0,0,1,DataSet,Answers))
print(TestNetwork(NN,0,0,1,DataSet,Answers))

#print(NN)

print(SuccessOfNetwork(NN,DataSet,Answers))


SaveNetwork(NN)
#0.1250096505244198