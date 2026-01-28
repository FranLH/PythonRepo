# Five alive
import random


CARDTYPES = ["0","1","2","3","4","5","6","7","Draw1","Draw2","PassMe","Reverse","Skip","=21","=10","ReDeal","Bomb"]

class Card:
    def __init__(self, cardType:str):
        self.cardType = cardType
    def __repr__(self):
        return(self.cardType)
    
def ListOfNCards(cardType:str,amount:int):
    List = []
    for i in range(amount):
        List.append(Card(cardType))
    return List    

class Player:
    def __init__(self, cards=[]):
        self.cards = cards

        
class Environment:
    def __init__(self, PlayersAmount:int):
        self.players = []
        for i in range(PlayersAmount):
            self.players.append(Player())
        self.deck = []
        self.deck.extend(ListOfNCards("7",1))
        self.deck.extend(ListOfNCards("6",2))
        self.deck.extend(ListOfNCards("5",4))
        self.deck.extend(ListOfNCards("4",8))
        self.deck.extend(ListOfNCards("3",8))
        self.deck.extend(ListOfNCards("2",8))
        self.deck.extend(ListOfNCards("1",8))
        self.deck.extend(ListOfNCards("0",8))
        self.deck.extend(ListOfNCards("Bomb",1))
        self.deck.extend(ListOfNCards("ReDeal",1))
        self.deck.extend(ListOfNCards("=0",3))
        self.deck.extend(ListOfNCards("=10",2))
        self.deck.extend(ListOfNCards("Draw1",2))
        self.deck.extend(ListOfNCards("Draw2",2))
        self.deck.extend(ListOfNCards("Reverse",6))
        self.deck.extend(ListOfNCards("Skip",6))
        self.deck.extend(ListOfNCards("=21",5))
        self.deck.extend(ListOfNCards("PassMe",4))
        
        self.deck = self.GetShuffled(self.deck)
    def GetShuffled(self,cards):
        shuffledCards = cards
        random.shuffle(shuffledCards)
        return(shuffledCards)
    def DealCards(self):
        for i in range(10):
            for player in self.players:
                player.cards.append(self.deck[0])
                self.deck.pop(0)
            
env = Environment(1)
print(env.deck)
        
