# The programs finds the sum of all prime numbers below "Limit"
import math




Limit = 2000000

Primes = [2]

Ans = 2

def IsPrime(Num):
    Counter = 0
    Root = math.sqrt(Num)
    for i in Primes:
        Counter += 1
        if math.fmod(Num, i) == 0:
            return(False)
        if Counter == len(Primes) or i > Root:
            Primes.append(Num)
            return(True)

Number = 3

done = False
while Number <= Limit:
    if IsPrime(Number):
        Ans += Number

    Number += 2
print("Done")
print(Ans)
print(Primes)