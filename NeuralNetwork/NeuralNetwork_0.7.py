import ast
import numpy
import random
import math
import copy



def SortFunc(e):
    return(e[0])

def TrainNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss,TrainingLength):
    results = [TestNetwork(N,0,0,1,Data,Anss)]
    print("---INITIAL NETWORK SUCCESS---")
    print("")
    print(results[0][0])
    print("")
    print("------TRAINING------")
    print("")

    for i in range(TrainingLength):
        new = TestNetwork(results[0][1],BiasRange, WeightRange, Iterations,Data,Anss)
        results.append(new)
        results.sort(key=SortFunc)
        if i%5 == 0:
            print(str(i)+"/"+str(TrainingLength))
            
    print("")
    print("------TRAINING COMPLETE------")
    print("")
    print("--SUCCESS--")
    print(results[0][0])
    print("")
    
    return(results[0])

def TestSingleData(N,data,Answer):
    print("--Trying--")
    for Input in range(len(N[0])):
        N[0][Input].contents = data[Input]
    CalcNetwork(N)
    print(len(N[-1]))
    for out in range(len(N[-1])):
        if out == Answer:
            print("This should be a 1")
        else:
            print("This should be a 0")
        print(N[-1][out].contents)
    print("---------------")

    
def ModifyNetwork(N, BiasRange, WeightRange):
    output = copy.deepcopy(N)
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
        for output in range(len(N[-1])):
            if output == Anss[Inputs]:
                success += math.dist([N[-1][Anss[Inputs]].contents],[1])
            else:
                success += math.dist([N[-1][Anss[Inputs]].contents],[0])
#        success += math.dist([N[-1][ID].contents],[Anss[Inputs]])


    return(success/len(Data))
   
######################################PROBLEM##########################
def TestNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss):
    results = [[SuccessOfNetwork(N,Data,Anss),N]]
    for i in range(Iterations):
        testN = copy.deepcopy(N)
        testN = ModifyNetwork(testN, BiasRange, WeightRange)
        results.append([SuccessOfNetwork(testN,Data,Anss),testN])
    results.sort(key=SortFunc)
    if Iterations == 1:
        print("")
        print("----SUCCESS----")
        print(results[0][0])
        print("---------------")
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
    Return = copy.deepcopy(N)
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
    print("")
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
    print("-----------------------------------------------------")
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

#==================================================================================================================#
#-------------------------------------------------CONFIGURATIONS---------------------------------------------------#
#==================================================================================================================#
        
#NN = CreateNetwork("NewBasic",2,2,3,2,0)
#NN = CreateNetwork("Load",2,2,3,2,[[0, 0], [2.0543093035668014, 2.4741533138948926, 0.74837439199015, 0.7710422145200428, -0.16703234743542472, -1.3948079686367958], [0.6963457602649132, 0.12553388527032006, -2.3694761038700958], [2.435440616272797, 1.9188554333461445, -3.8291532540356243, 0.7361508322464702, -1.9752097672697253, -0.790850062550275, 1.0492845380613898, -1.6630668250032283, 4.492803920554506], [3.4401376310528105, 4.4674703470040855, 5.029476163010856], [10.154406963319992, 8.44502664914806, 6.935567874707492, 7.670671405224791, 10.81935284108959, 8.560818708283632], [11.695111826774442, 10.808641135677922]])

#TestSingleData(NN,[0,0],0)

#NN = copy.deepcopy(TrainNetwork(NN,0.5,0.5,20,DataSet,Answers,20)[1])

#SaveNetwork(NN)

#==================================================================================================================#
#-------------------------------------------------USER-INTERFACE---------------------------------------------------#
#==================================================================================================================#


def Commands():
    print("")
    print("-----COMMANDS-----")
    print("")
    print("Create")
    print("Load")
    print("Train")
    print("Save")
    print("Draw")
    print("Test")
    print("ManualTest")
    print("SetData")
    print("SetAnswers")
    print("GetData")
    print("GetAnswers")
    print("Exit")
    
def Create():
    global NetworkActive, NN
    print("")
    print("-----CREATING-NEURAL-NETWORK-----")
    print("")
    print("amount of input neurons?")
    inputs = int(input())
    print("amount of neuron layers?")
    layers = int(input())
    print("amount of neurons per layer?")
    npl = int(input())
    print("amount of output neurons?")
    outputs = int(input())
    NN = CreateNetwork("NewBasic",inputs,layers,npl,outputs,0)
    print("NEURAL NETWORK CREATED SUCCESSFULLY----")
    NetworkActive = True
    
def Load():
    global NetworkActive, NN
    print("")
    print("-----LOADING-NEURAL-NETWORK-----")
    print("")
    print("Paste here your Neural Network")
    load = ast.literal_eval(input())
    NN = CreateNetwork("Load",0,0,0,0,load)
    print("NEURAL NETWORK LOADED SUCCESSFULLY----")
    NetworkActive = True

def Train():
    global weightChange, biasChange, iterations, configurated, NN, DataSet, Answers
    print("")
    if configurated == False:
        print("How much should the weights vary?")
        weightChange = float(input())
        print("How much should the biases vary?")
        biasChange = float(input())
        print("How many different settings should be tested per iteration?")
        iterations = int(input())
        configurated = True 
    else:
        print("Do you want to change your configurations?(write yes or no)")
        yess = input()
        if yess == "yes":
            print("How much should the weights vary?")
            weightChange = float(input())
            print("How much should the biases vary?")
            biasChange = float(input())
            print("How many different settings should be tested per iteration?")
            iterations = int(input())
    print("How many iterations should the training last?")
    its = int(input())
    NN = copy.deepcopy(TrainNetwork(NN,weightChange,biasChange,iterations,DataSet,Answers,its)[1])
def ManualTest():
    print("")
    print("Write the data you want to input")
    data = ast.literal_eval(input())
    print("Which output neuron should activate?")
    outn = int(input())
    TestSingleData(NN,data,outn)
def Test():
    global DataSet, Answers
    print("")
    TestNetwork(NN,0,0,1,DataSet,Answers)
print("=================================================================================================")
print("-----------------------------------------NEURAL-NETWORK------------------------------------------")
print("=================================================================================================")
print("")

        
DataSet = [[0,0],[0,1],[1,0],[1,1]]
Answers = [0,1,1,0]

running = True

NetworkActive = False
configurated = False
weightChange = 0
biasChange = 0
iterations = 0

while running:
    print("")
    print("Type COMMANDS for a list of all commands available, Type HELP <command name> for details on what a command does")
    print("")
    command = input()
    if command == "COMMANDS":
        Commands()
    elif command == "Create":
        Create()
    elif command == "Load":
        Load()
    elif command == "SetData":
        DataSet = ast.literal_eval(input())
    elif command == "SetAnswers":
        Answers = ast.literal_eval(input())
    elif command == "GetData":
        print(DataSet)
    elif command == "GetAnswers":
        print(Answers)
    elif command == "Exit":
        running = False
    elif NetworkActive:
        if command == "Train":
            Train()
        elif command == "Save":
            SaveNetwork(NN)
        elif command == "ManualTest":
            ManualTest()
        elif command == "Test":
            Test()
        elif command == "Draw":
            DrawNetwork(NN)


#Lines and dotted lines
# [[1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0],[1,1,1,1,0,0,0,0],[0,0,0,1,0,1,0,1],[0,0,0,1,1,1,0,0],[1,0,1,0,1,0,0,0],[0,0,0,0,1,1,1,1],[0,0,1,0,1,0,0,0]]
# [0,1,0,1,0,1,0,1] Answers