# A Pythagorean triplet is a set of three natural numbers, a < b < c, for which a*a + b*b = c*c


Objective = 1000
# Another one that works is 12

# Finds the only pythagorean triplet for which a + b + c = 1000, and prints the product of abc
def IsPyTriplet(a,b,c):
    if a*a+b*b == c*c and a<b and b<c:
        return(True)
    else:
        return(False)

for A in range(Objective+1):
    for B in range(A+1, Objective+1 - A):
        for C in range(B+1, Objective+1 - A - B):
            if IsPyTriplet(A,B,C) == True and A+B+C == Objective:
                print(str(A)+"+"+str(B)+"+"+str(C))
                print(A*B*C)
                break
    