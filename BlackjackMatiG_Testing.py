import random

CARDnames = ["As de treboles", "As de diamantes", "As de corazones", "As de picas", "Dos de treboles", "Dos de diamantes", "Dos de corazones", "Dos de picas", "Tres de treboles", "Tres de diamantes", "Tres de corazones", "Tres de picas", "Cuatro de treboles", "Cuatro de diamantes", "Cuatro de corazones", "Cuatro de picas", "Cinco de treboles", "Cinco de diamantes", "Cinco de corazones", "Cinco de picas", "Seis de treboles", "Seis de diamantes", "Seis de corazones", "Seis de picas", "Siete de treboles", "Siete de diamantes", "Siete de corazones", "Siete de picas", "Ocho de treboles", "Ocho de diamantes", "Ocho de corazones", "Ocho de picas", "Nueve de treboles", "Nueve de diamantes", "Nueve de corazones", "Nueve de picas", "Diez de treboles", "Diez de diamantes", "Diez de corazones", "Diez de picas", "Jota de treboles", "Jota de diamantes", "Jota de picas", "Reina de treboles", "Reina de diamantes", "Reina de corazones", "Reina de picas", "Rey de treboles", "Rey de diamantes", "Rey de corazones", "Rey de picas"]
CARDvalues = [11,11,11,11,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]

PLAYER_DAMAGE_MULT = 10
DEALER_DAMAGE_MULT = 10


class TABLE: # Stores all the players and cards data
    def __init__(self,playerNames): # Creates the player objects and assigns them a team and position randomly
        dealer = random.randint(0,len(playerNames)-1)
        self.players = []
        for player in range(len(playerNames)):
            if player == dealer:
                DEALER = PLAYER(playerNames[player],500,1)
            else:
                self.players.append(PLAYER(playerNames[player],150,0))
        random.shuffle(self.players)
        self.players.append(DEALER) # The dealer goes at the end of the list
        self.deck = DECK() # Creates a new deck
    def GetPlayersInfo(self): # Prints all players data
        for player in self.players:
            player.PrintData()
    def DealCards(self):
        for player in self.players:
            if player.HP > 0:
                player.hand.append(self.deck.cards.pop(-1)) # Deals a card to each player from the top of the deck
        for player in self.players:
            if player.HP > 0:
                player.hand.append(self.deck.cards.pop(-1)) # Deals a card to each player from the top of the deck
    def PlayerTurn(self,player):
        if player.Action() == "hit":
            player.hand.append(self.deck.cards.pop(-1)) # Deals a card to the player from the top of the deck
            if player.GetScore() < 21:
                self.PlayerTurn(player)
    def Round(self):
        self.deck.Shuffle()
        self.DealCards()
        for player in self.players:
            self.PlayerTurn(player)
        
        # The dealer attacks first
        dealerScore = self.players[-1].GetScore()
        areaDamage = random.randint(1,6)*DEALER_DAMAGE_MULT 
        for player in self.players:
            if dealerScore <= 21 and (player.GetScore()<dealerScore or player.GetScore() > 21) and player.HP > 0:
                player.HP -= areaDamage

        # Then the players attack
        for player in self.players:
            if player.GetScore() <= 21 and (player.GetScore() > self.players[-1].GetScore() or self.players[-1].GetScore() > 21) and self.players[-1].HP > 0:
                Damage = random.randint(1,6)*PLAYER_DAMAGE_MULT
                if self.players[-1].HP > 0:
                    self.players[-1].HP -= Damage
        allHP = 0
        for player in self.players:
            if player.team == 0:
                allHP += max(0, player.HP)
        if allHP > 0 and self.players[-1].HP > 0:
            for player in self.players:
                player.ReturnCards(self.deck.cards)
            return(self.Round())
        else:
            if allHP > 0:
                return(0)
            else:
                return(1)

class PLAYER: # Player class
    def __init__(self, name, MaxHP, team):
        self.name, self.MaxHP, self.HP, self.team, self.hand = name, MaxHP, MaxHP, team, []
    def GetCardsSTR(self): # Returns the player's hand as a string for printing
        string = ""
        for card in self.hand:
            string+=card.name+", "
        return(string[:-2])
    def GetScore(self):
        score = 0
        scores = []
        for card in self.hand:
                scores.append(card.value)
        for i in scores:
            score+=i
        for i in range(scores.count(11)): # For each ace that exceeds 21, subtract 10 from the score
            if score>21:
                score-=10
       
        return(score)
    
    def Action(self):
        return(random.choice(["hit","stand"]))
    def PrintData(self):
        print(self.name, "- HP:", self.HP, "- Equipo:", self.team, "- Puntuacion:", self.GetScore(), "   Mano: ", self.GetCardsSTR())
    def ReturnCards(self, deck):
        for i in range(len(self.hand)):
            deck.append(self.hand.pop(-1))
class CARD: # Card class
    def __init__(self, name, value):
        self.name, self.value = name, value
        
class DECK: # Deck class
    def __init__(self): # Creates a new deck of cards from the list of card names and values
        self.cards = []
        for card in range(len(CARDnames)):
            self.cards.append(CARD(CARDnames[card],CARDvalues[card]))
    def Print(self): # Prints the contents of the deck
        for card in self.cards:
            print(card.name, ":",card.value)
    def Shuffle(self): # Shuffles the deck
        random.shuffle(self.cards)
  
playerWins = 0
dealerWins = 0
def Test():
    global playerWins, dealerWins
    Table = TABLE(["Fran","Mati","Nacho","Martin"])
    if Table.Round() == 1:
        dealerWins+=1
    else:
        playerWins+=1
for i in range(10000):
    Test()
print(playerWins, dealerWins)


#Table.deck.Shuffle()
#Table.DealCards()

#Deck = DECK()
#Deck.Shuffle()
#Deck.Print()