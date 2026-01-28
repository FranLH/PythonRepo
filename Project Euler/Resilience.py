import math
data = open("10kPrimes.txt", "r")
Primes = data.read()
data.close()


LastPrime = 0

Objective = 15499/94744

#15499/94744

Primes = eval(Primes)


def IsCancellable(num,den):
    for i in Primes:
        if math.fmod(num,i) == 0 and math.fmod(den,i) == 0:
            return(True)
        if i > math.sqrt(num):
            return(False)

def Resilience(Num):
    global LastPrime
    if Num == Primes[LastPrime]:
        LastPrime += 1
        return(1)
    
#    for i in Primes:
#        if Num < i:
#            break
#        elif Num == i:
#            LastPrime += 1
#            return(1)

    NonResFracc = 1
    for j in range(2, Num):
        if IsCancellable(j,Num):
            NonResFracc += 1
        if (Num-1-NonResFracc)/Num > Objective:
            return(1)
    print(NonResFracc)
    return((Num-1-NonResFracc)/Num)


print(Resilience(12))

for i in range(2,100001):
#    print(i)
    ans = Resilience(i)
    if ans != 1:
        print("Found it!")
        print(i)
        print(ans)
        break
print("Nothing")



#def Resilience(Num):