import base64


encoded = """‹      ÿ•‘ÏNÂ@Æ¿R ¥„Ôø‚"*$&’x[ÚÙvcÿ˜ízñE|>€ã­N‹Æ““L²óÍ~3¿ìz€‡Î]S*Œ
l8÷¤
•g lÝ
aÄâÜ2"dµ‰&7	°^_Ö<e™ë$œ…Ê¸»)­ñ`88sáWºÊ¢E"ŒÌuŠÊ"•Qü¼šJ±Ò*è¢=×ŠµjsY–#Î7Îwž¼uñþ?>Í[‘üËºìÏ¥TÉÄa
qt:Núãpx¼ð4ÐZªÐÄph_‘Šbƒ¯y«nE$eA¦"Âw0Ñ§‡öy’ Œã,DBÆ
?e¬@
i¦…É3BíêíT¡4KœúáŸŸ¶C­*ª^¶•µWm®üŽÿú:èÕà³Ìðoóoâ
Œ ¾Û  """


# base64_bytes = encoded.encode("ascii")

# sample_string_bytes = encoded.encode("ascii")
# sample_string = sample_string_bytes.decode("ascii")
characters = []
longest = "0"
for char in encoded:
    Bin = bin(ord(char))[2:]
    if len(Bin)>len(longest):
        longest=Bin
    Bin=("0"*(14-len(Bin)))+Bin
    characters.append(Bin)
full = ""
for num in characters:
    full+=num
    
sliced = []
text = ""
for i in range(0,len(full),6):
    binary = full[i:i+6]
    sliced.append(chr(int(binary)))
    text+=chr(int(full[i:i+6]))

print(sliced)
print(text)
print("aaa:",text.encode("utf16").decode("utf16"))

print("Longest:", longest)
#     print(bin(ord(char)).strip("0b"), ord(char), char)

print(characters)
a = ""
print(bin(ord(a)))
print(ord(a))


