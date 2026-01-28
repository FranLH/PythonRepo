import numpy
#NN = [[input],[conn],[neuron],[conn],[output]]
#NN = [[1,1],[0,0,0,0,0,0],[1,1,1],[0],[1,1]]

def CreateConnections(N, layer1, layer2, weights):
        cons = []
        for i in range(len(N[layer1])*len(N[layer2])):
            c = Connection(layer2, i, weights[i])
            cons.append(c)
        N.insert(layer2, cons)
def CalcNetwork(N):
    for i in range(2,len(N),2):
        for neuron in N[i]:
            neuron.CalcOutput()

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
    def CalcOutput(self):
        self.contents = 0
        counter = 0
        for i in NN[self.x-2]:

            self.contents += i.contents * NN[self.x-1][self.y*len(NN[self.x-2])+counter].weight
            counter+=1

        self.contents += self.bias
        #Sigmoid function, S(x) = 1/(1+e^-x)
        self.contents = 1/(1+numpy.exp(-self.contents))

       
i1 = Neuron(0,0,0,0)
i2 = Neuron(0,1,0,0)
c1 = Connection(1,0,1.1)
c2 = Connection(1,1,1)
c3 = Connection(1,2,0.1)
c4 = Connection(1,3,-3)
c5 = Connection(1,4,2)
c6 = Connection(1,5,1)
n1 = Neuron(2,0,0,0)
n2 = Neuron(2,1,0,0)
n3 = Neuron(2,2,0,0)
c7 = Connection(3,0,0.5)
c8 = Connection(3,1,1)
c9 = Connection(3,2,3)
c10 = Connection(3,3,1)
c11 = Connection(3,4,2)
c12 = Connection(3,5,2)
o1 = Neuron(4,0,0,0)
o2 = Neuron(4,1,0,0)

NN = [[i1,i2],[c1,c2,c3,c4,c5,c6],[n1,n2,n3],[c7,c8,c9,c10,c11,c12],[o1,o2]]
#[c1,c2,c3,c4,c5,c6]

#CreateConnections(NN, 0, 1, [1,1,0.1,0.1,5,0.1])
CalcNetwork(NN)

for i in range(0,len(NN),2):
    pr = ""
    for j in NN[i]:
        pr = pr + str(j.contents) + "  "
    print(pr)
#n1.CalcOutput()
#print(n1.contents)