import random
import math
DataSet = [[0],[1],[2],[3]]
Answers = [0, 1, 2, 3]

NeuralNetwork = [[0],[0],[0]]

print(0!=0)

bads = 0
goods = 0

def Iteration(Data,NN):
    ans = 0
    NN[0]=[]
    for i in Data:
        NN[0].append(i)
    b = 0
    for i in NN[2]:
        NN[2][b] = 0
        b+=1
    for i in NN[1]:
        for j in NN[0]:
            for k in NN[2]:
                ans+= k + i + j
    return(ans)

def Try(NN, NeuronIts, TotalIts):
    global Answers
    for neuronID in range(len(NN[1])):
        TestNN = NN
        results = []
        Tit = 0

        Nit = 0
        for i in range(NeuronIts):
            success = 0
            ID = 0
            neuron = random.uniform(-1,1)
            TestNN[1][neuronID] = neuron
            for data in DataSet:
            
                result = Iteration(data,TestNN)

                success-= math.dist([result],[Answers[ID]])
                ID+=1
            Tit+=1
            results.append((success, neuron))
        results.sort()
        print(results)


Try(NeuralNetwork, 100, 10)
print(goods, bads)

print(NeuralNetwork)
