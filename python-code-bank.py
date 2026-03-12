arw = random.sample(Names_B, random.randint(1, 4))
if not [el for el in arw if arw.count(el) > 1]:
        r - random.choice(arr)
        ind = arr.index(r)
        arw.insert(ind, r)



# Email Generator

def EmailGen():
 while True: 
  for i in range(10):
        boy = (''.join(random.sample(Names_B, random.randint(1, 1))))
        girl = (''.join(random.sample(Names_G, random.randint(1, 1))))
        surname = (''.join(random.sample(Names_LN, random.randint(1, 1))))

        print( boy + surname + '@gmail.com' )






# Valid Credit Card Number Geb

def CCV():

 global first_6 
 
 card_no = [int(i) for i in str(first_6)]

 card_num = [int(i) for i in str (first_6)]

 seventh_15 = random.sample(range(14), 14)

 for i in seventh_15:
         card_no.append(i)
         card_num.append(i)

 for t in range(0, 15, 2):
        card_no[t] = card_no[t] * 2

 for i in range( len(card_no) ):

  if card_no[i] > 9:
          card_no[i] -= 9

          s = sum(card_no)
          mod = s % 10
          check_sum = 0 if mod == 0 else (10 - mod )
          card_num.append(check_sum)
          card_num = [str(i) for i in card_num]
          return ''.join(card_num)

import pyttsx3
engine = pyttsx3.init()


class Card (object):
    # These list are class attributes
    suitList = ["Clubs", "Diamonds", "Hearts", "Spades"]

    rankList = ["narf", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    
    def __init__(self, suite = 0, rank = 0) -> None:
        self.suite = suite;
        self.rank = rank;

    def __str__(self) -> str:
        return (self.rankList[self.rank] + " of " + self.suitList[self.suite])

    def __cmp__(self, other) -> int:
        # check the suits
        if self.suite > other.suite: return 1
        if self.suite < other.suite: return -1
        # if the suits are the same... check ranks
        if self.rank > other.rank: return 1
        if self.rank < other.rank: return -1
        # ranks are the same... it’s a tie
        return 0


 
class Deck (object):

    def __init__(self) -> None:
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))
    
    def __str__(self) -> str:        
        string = ""  #Empty string. 
        for i in range(len(self.cards)):
            string = string + " "*i + str(self.cards[i]) + "\n" # S here acts as an accumulator
        return string

    def shuffle(self) -> str:
        import random
        for i in range(len(self.cards)):
            t = random.randrange( i, len(self.cards))
            self.cards[i], self.cards[t] = self.cards[t], self.cards[i]
            return str(self.cards[i]), str(self.cards[t])

    def removeCard(self, card) -> str:
        if card in self.cards:
            self.cards.remove(card)
            engine.say(f"{card} has been removed successfully")
            engine.runAndWait()
            return 1
        else:
            engine.say(f"system failed to removed {card}.")
            engine.runAndWait()
            return 0
    
    def pop(self) -> str:
        return self.cards.pop()

    def isEmpty(self) -> bool:
        return (len(self.cards) == 0)

    def deal(self, hands, nCards = 999) -> str:
        for i in range(len(nCards)):
            if self.isEmpty(): break
            card = self.pop()
            hand = hands[i % len(hands)]
            hand.addCard(card)



class Hand (Deck):

    def __init__(self, name = "") -> None:
        self.cards = []
        self.name = name

    def addCard(self, card) -> str:
        self.cards.append(card)

    def __str__(self) -> str:
        s = "Hand" + self.name
        if self.isEmpty():
            return s + " is empty\n"
        else:
            return s + " contains\n" + Deck.__str__(self)






card = Deck()
card2 = Card( 2, 3)

print(card.removeCard(card2))

        
        

