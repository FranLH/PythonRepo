def GetDecimalLength(num):
    result = 1/num
    decimals = str(result).strip("0.")
    print(len(decimals))
GetDecimalLength(4)