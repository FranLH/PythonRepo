def Divisors(num):
    divs = []
    for n in range(1,num):
        if n not in divs:
            if round(num/n) == num/n:
                divs.append(n)
                if n != round(num/n) and round(num/n) != num:
                    divs.append(round(num/n))
        else:
            break
    return(divs)

def SumList(lst):
    result = 0
    for item in lst:
        result+=item
    return(result)

def AmicablesUnder(Range):
    Numbers = [0,1]
    Amicables = []
    for num in range(2,Range):
        numDivs = SumList(Divisors(num))
        if (num in Numbers) and num == SumList(Divisors(numDivs)):
            Amicables.append(numDivs)
            Amicables.append(num)
        Numbers.append(numDivs)
    return(Amicables)

print(SumList(AmicablesUnder(10000)))
print(AmicablesUnder(10000))
