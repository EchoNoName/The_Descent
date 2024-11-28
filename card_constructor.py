import random

attack_card_1 = [1003, 1004, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1022, 1023, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1057, 1058, 1059, 1060, 1061, 1062]
skill_card_1 = [1005, 1006, 1007, 1008, 1017, 1018, 1019, 1020, 1021, 1024, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1063, 1064, 1065, 1066, 1067, 1068]
power_card_1 = [1050, 1051, 1052, 1053, 1054, 1055, 1056, 1069, 1070, 1071, 1072, 1073, 1074]

def random_card(type, character_class):
    if type == 'curse':
        return 'placeholder'
    elif type == 'status':
        return 'placeholer'
    elif type == 'atk':
        if character_class == 1:
            return
        else:
            return 'placeholder'

class Card():
    def __init__(self, id, name, rarity, type, cost, card_text, innate, exhaust, retain, ethereal, effect, target, removable = True):
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
        self.removable = removable # Whether the card can be removed from the deck
        self.combat_cost = (None, None) #(Cost, Duration of cost (Played, Turn, Combat))
        self.chaotic = False # whether a card is chaotic, represented by boolean
    
    def chaos(self):
        self.combat_cost = (random.randint(0, 3), 'combat')
    
    def cost_change(self, cost, duration):
        self.combat_cost = (cost, duration)
    


def create_card(card_id, card_data: tuple):
    return Card(card_id, *card_data)