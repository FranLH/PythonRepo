



def iteration(num):
    if num%2 == 0:
        return(num/2)
    else:
        return(num*3+1)
def ChainLength(num):
    start = num
    Length = 0
    while num != 1:
        num = iteration(num)
        Length+= 1
    return(Length+1,start)


largest = [1,1]
for N in range(1,1000001):
    length = ChainLength(N)
    if length[0]>largest[0]:
        largest = length
print(largest)