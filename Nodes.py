import random

class Node:
    def __init__(self, ID, content, connections=[]):
        self.ID, self.content, self.connections = ID, content, connections
    def __repr__(self):
        return(str(self.ID) + "---content: "+str(self.content) + ", connections: " + self.getConnections() + "\n")
    def getConnections(self):
        s = ""
        for i in self.connections:
            s+= str(i.ID)+", "
        return (s[:-2])
        
nodes = []
for i in range(10):
    nodes.append(Node(i,random.randint(0,100)))

#print(nodes)
for i in range(1,len(nodes)):
    other = nodes[i-1]
    other.connections.append(nodes[i])
    nodes[i].connections.append(other)
    print(nodes[i].connections)

print(nodes)        