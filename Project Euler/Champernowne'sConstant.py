# Champernowne's Constant

# Brute force method:
constant = ""
i = 1
while len(constant) < 1000000:
    constant+=str(i)
    i+=1
print(i)
print(int(constant[0]) * int(constant[9]) * int(constant[99]) * int(constant[999]) * int(constant[9999]) * int(constant[99999]) * int(constant[999999]))

# Smart method:
# def GetNthDigit(n):
#     >=0<=10 : 1
#     >=11<=100
#     10-100-1000-10000