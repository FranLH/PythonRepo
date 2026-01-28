



def Step(x,y,size):
    global paths
    if x != size[0]:
        Step(x+1,y,size)
    if y != size[1] and x != 0:
        Step(x,y+1,size)
    if x == size[0] and y == size[1]:
        paths+=1


def Paths(size):
    #global paths
    #paths = 0
    #x, y = 0, 0
    #Step(x,y,size)
    #print(paths*2)
    values = []
    for y in range(size[1]+1):
        values.append([])
        for x in range(size[0]+1):
            values[y].append(0)
    values[0][0] = 1
    x, y = 0, 0

    for diagonal in range(size[0]+size[1]+1):
        its = 0  
        while x >= 0 and x <= size[0] and y >= 0 and y <= size[1]:
            val = 0
            if x-1 >=0:
                val += values[y][x-1]
            if y-1 >=0:
                val += values[y-1][x]
            if values[y][x] == 0:
                values[y][x] = val
            x+=1
            y-=1
            its += 1
        x-=its
        y+=its
        if diagonal < (size[0]+size[1])/2:
            y += 1

        else:
            x += 1
    print(values[size[1]][size[0]])
Paths((20,20))
    
