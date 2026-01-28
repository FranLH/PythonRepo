Num_A = 999
Num_B = 999

Done = False

def IsPalindrome(num):
    reverse = ""
    for i in range(len(str(num))):
        reverse = reverse + str(num)[len(str(num))-i-1]
    if num == int(reverse):
        return(True)
    else:
        return(False)
while Done == False:
    for j in range(Num_A):
        if Done == True:
            break
        A = Num_A - j
        for k in range(Num_B):
            B = Num_B - k
            if IsPalindrome(A*B) == True:
                print(str(A)+"x"+str(B))
                Done = True
                break