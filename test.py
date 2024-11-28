import random

potions = ['test', 'other potion']

class card():
    def __init__(self, name, potion):
        self.name = name
        self.potion = potion

class combat():
    def __init__(self, hand, discard_pile, potion):
        self.hand = hand
        self.discard_pile = discard_pile
        self.potion = potion

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

    def remove_potion(self, potion):
        global potions
        potions.remove(potion)

Cc = combat([], [], potions)
Cc.remove_potion(Cc.potion[0])
print(Cc.potion)
print(potions)
Cc.potion = 1
Cc.potion + 1


