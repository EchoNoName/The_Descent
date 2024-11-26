class card():
    def __init__(self, retain, ethereal, id):
        self.retain = retain
        self.ethereal = ethereal
        self.id = id

hand = [card(True, False, 'retain'), card(False, True, 'Ethereal'), card(False, False, 'none'), card(True, True, 'Both')]
discard = []
exhaust = []
print('Hand before: ')
for cards in hand:
    print(f'{cards.id} ', end='')
print(' ')
for i in range(len(hand) - 1, -1, -1):
    if hand[i].retain == True:
        continue
    elif hand[i].ethereal == True:
        exhaust.append(hand[i])
        hand.remove(hand[i])
    else:
        discard.append(hand[i])
        hand.remove(hand[i])
print('Hand After: ')
for cards in hand:
    print(f'{cards.id} ', end='')