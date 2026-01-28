def Factorial(num):
    result = 1
    for n in range(1,num+1):
        result *= n
    return(result)

def DigitSum(num): # Returns the sum of each digit of the number
    result = 0
    for digit in str(num):
        result += int(digit)
    return(result)

print(DigitSum(Factorial(100)))