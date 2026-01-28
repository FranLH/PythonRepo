file = open("names.txt", "r") # Open the text file
names = eval("["+file.read()+"]") # Save the contents of the file into a list
file.close() # Close the text file

names.sort() # Sort the names alphabetically

Letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def Score(pos, name): # Returns the numerical score of the name, by multiplying the alphabetical position of the name with the sum of the values of each leter
    score = 0
    for letter in name:
        score+=Letters.index(letter)+1
    return(score*pos)

def SumList(lst):
    result = 0
    for item in lst:
        result+=item
    return(result)

Scores = []
for name in range(len(names)):
    Scores.append(Score(name+1,names[name]))
    
print(SumList(Scores))