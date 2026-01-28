import math


Objective = 600851475143
Primes = [2]
Result = 0
running = True
Num = 2

while Objective != 1:
    Num += 1
    Counter = 0
    for i in Primes:
        Counter += 1
        if math.fmod(Num, i) == 0:
            break
        if Counter == len(Primes):
            Primes.append(Num)
            if math.fmod(Objective, Num) == 0:
                Objective = Objective/Num
                Result = Num
print(Result)

    
#465585120