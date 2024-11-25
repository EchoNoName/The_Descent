class Card():
    def __init__(self, id, name, rarity, type, cost, card_text, innate, exhaust, retain, ethereal, effect, target):
        self.id = id # Card ID, which is an integer
        self.name = name # Name of the card, a string
        self.rarity = rarity # rarity represented by an integer
        self.type = type # type of card (attack, skill, power, curse, status), represented by an integer
        self.cost = cost # cost of the card, can be just a number, x or a special cost written like ('C', original cost, +/-, condition)
        self.card_text = card_text # Base card text, a string
        self.innate = innate # Boolean representing whether a card is innate
        self.exhaust = exhaust # Boolean representing whether a card is exhaust
        self.retain = retain # Boolean representing whether a card is retain
        self.ethereal = ethereal # Boolean representing whether a card is ethereal
        self.effect = effect # what the card actually does, represented by a dictonary that contains its actions
        self.target = target # The targets of the card, represented by an integer
        self.combat_cost = (None, None) #(Cost, Duration of cost (Played, Turn, Combat))
        self.chaotic = False # whether a card is chaotic, represented by boolean
        
def create_card(card_data: tuple):
    return Card(*card_data)