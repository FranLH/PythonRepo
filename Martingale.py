import math

def Martingale(probability, money, startBet):
    remaining = money
    bet = startBet
    bets = 0
    while remaining>bet:
        bets+=1
        remaining-=bet
        bet=bet*2
    losingChance = (1-probability)**bets
    
    print("If you have", str(money)+"$,", "starting with a bet of", str(startBet)+"$,", "you can bet", bets, "times")
    print("If you have a",str(probability)+"% chance","of winning, the probability of you losing every single time is of", str(losingChance)+"%")
    print("If you play", math.floor(1/losingChance), "times, you will lose all of your money")
    print("Each time that you win you will be up", str(startBet)+"$", ", meaning what you will make", str(startBet*math.floor(1/losingChance))+"$", "before losing all of your money")
    print("The biggest bet you will have made will be of", str(startBet*(2**bets))+"$")

# 0.421296 Lucky dice probability of winning
Martingale(0.73, 2198, 200)

#print(0.5**4)