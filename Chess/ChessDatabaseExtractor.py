# https://wtharvey.com/m8n2a.html
f = open("chessPuzzlesDatabase.txt", "r")
Converted = ""
puzzleList = f.read().splitlines()
for line in range(len(puzzleList)):
    if len(puzzleList[line])>0:
        if puzzleList[line][0] == "[":
            splt = puzzleList[line].strip("[]. ").split(" ")
            Converted+=puzzleList[line-1]+"\n"
            Converted+=splt[0]+"\n"
f.close()
f = open("chessPuzzlesDatabase.txt", "w")
f.write(Converted)
f.close()
