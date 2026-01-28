import random
DataSet = [[0],[1]]
Answers = [0, 1]

NeuralNetwork = [[0],[0],[0]]

print(0!=0)

bads = 0
goods = 0

def Iteration(Set,NN):
    Dataid = random.randrange(0,len(Set))
    Data = Set[Dataid]
    a = 0
    for i in NN[0]:
        i = Data[a]
        a +=1
    for i in NN[2]:
        i = 0
    for i in NN[1]:
        for j in NN[0]:
            for k in NN[2]:
                k = k + i + j
    return((Dataid,round(k)))

def Try(NN, iterations):#                      The middle layer gets randomized every time it gets an answer wrong, so it has an average
    global goods, bads, Answers#               of 50% correct answers
    it = 0
    while it < iterations:
        result = Iteration(DataSet,NN)
        if result[1] != Answers[result[0]]:
            bads+= 1
            a = 0
            for i in NN[1]:
                i = random.uniform(-1,1)
                NN[1][a] = i
                a+=1
        else:
            goods+=1
        it+=1


Try(NeuralNetwork, 100)
print(goods, bads)

print(NeuralNetwork)
print(Iteration(DataSet,NeuralNetwork))