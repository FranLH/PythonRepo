import math


Primes = [2,3]
def FindPrime(n):
    Num = 3
    while len(Primes) < n:
        Counter = 0
        Num += 2
        for i in Primes:
            Counter += 1
            if math.fmod(Num, i) == 0:
                break
#            if Counter == len(Primes):
            if Counter == len(Primes):
                Primes.append(Num)
                break
    return(Primes[n-1])

print(FindPrime(20001))
print(Primes)