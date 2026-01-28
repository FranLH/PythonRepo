import math
Decimals = ["zero","one","two","three","four","five","six","seven","eight","nine"]
Special = ["ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
Tens = ["twenty","thirty","fourty","fifty","sixty","seventy","eighty","ninety"]
Powers = ["hundred","thousand"]

def GetName(num):
    sections = []
    a = 0
    for i in range(1,len(num)+1):
        if a%3 == 0:
            sections.insert(0, num[-1*i])
        else:
            sections[-1 * math.ceil(i/3)] = num[-1*i] + sections[-1 * math.ceil(i/3)]
        a+=1
#     name = ""
#     if len(num) == 1:
#         name += Decimals[int(num)]
#     elif len(num) == 2:
#         if int(num) < 20:
#             name += Special[int(num[1])]
#         else:
#             name += Tens[int(num[0])-2] + Decimals[int(num)]
    return(sections)
print(GetName("12314364574747216"))