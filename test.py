import random

class card():
    def __init__(self, name):
        self.name = name

class combat():
    def __init__(self, hand, discard_pile):
        self.hand = hand
        self.discard_pile = discard_pile

    def random_discard(self, num):
        if self.hand:
            if len(self.hand) > num:
                for i in range(0, num):
                    card = random.choice(self.hand)
                    self.discard_pile.append(card)
                    self.hand.remove(card)
            else:
                self.discard_pile.extend(self.hand)
                self.hand.clear()

hand = [card('card 1'), card('card 2'), card('card 3')]
Combat = combat(hand, [])
for Card in Combat.hand:
    print(Card.name)
Combat.random_discard(1)
for Card in Combat.hand:
    print(Card.name)
print('Discard: ')
for Card in Combat.discard_pile:
    print(Card.name)
