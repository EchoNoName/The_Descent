import random

attack_card_1 = [1003, 1004, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1022, 1023, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1057, 1058, 1059, 1060, 1061, 1062]
skill_card_1 = [1005, 1006, 1007, 1008, 1017, 1018, 1019, 1020, 1021, 1024, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1063, 1064, 1065, 1066, 1067, 1068]
power_card_1 = [1050, 1051, 1052, 1053, 1054, 1055, 1056, 1069, 1070, 1071, 1072, 1073, 1074]
weak_curse = [0, 1, 2, 3, 4, 5, 6]
medium_curse = [8, 12]
strong_curse = [9, 10, 11]

def random_card(type, character = None):
    if type == 'curse':
        return random.choice(weak_curse + medium_curse + strong_curse)
    elif type == 'weak curse':
        return random.choice(weak_curse)
    elif type == 'status':
        return 'placeholer'
    elif type == 'atk':
        if character.character_class == 1:
            return random.choice(attack_card_1)
        else:
            return 'placeholder'

class Card():
    def __init__(self, id, name, rarity, type, cost, card_text, innate, exhaust, retain, ethereal, effect, target, removable = True, x_cost_effect = {}):
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
        self.x_cost_effect = x_cost_effect
        # rarity:(0 = starter, 1 = common, 2 = uncommon, 3 = rare, 4 = other), type: (0 = atk, 1 = skill, 2 = power, 3 = status, 4 = curse)

    def __str__(self):
        card_descrip = []
        if self.cost == 'U':
            card_descrip.append('Unplayable')
        if self.innate == True:
            card_descrip.append('Innate')
        if self.retain == True:
            card_descrip.append('Retain')
        if self.card_text != None and self.effect != None:
            card_descrip.append(self.card_text)
        if self.removable == False:
            card_descrip.append('Cannot be removed from your deck')
        if self.ethereal == True:
            card_descrip.append('Ethereal')
        if self.exhaust == True:
            card_descrip.append('Exhaust')
        card_descrip = str('. '.join(card_descrip))
        if card_descrip[-1] != ' ' and card_descrip[-2] != '.':
            card_descrip += '. '
        rarity = {
            0: 'Starter',
            1: 'Common',
            2: 'Uncommon',
            3: 'Rare',
        }
        if self.rarity in rarity:
            rarity = rarity[self.rarity]
        elif self.removable == True:
            rarity = 'Normal'
        else:
            rarity = 'Special'
        type = {
            0: 'Attack',
            1: 'Skill',
            2: 'Power',
            3: 'Status',
            4: 'Curse'
        }
        type = type[self.type]
        return f'{self.name}: {rarity} {type}. {card_descrip}Cost: {self.get_cost()}'

    def __repr__(self):
        return self.__str__()

    def modify_effect(self, effect_change, modifications):
        new_eff = {}
        for effect, details in self.effect.items():
            if effect == effect_change:
                new_magnitude = [*details]
                new_magnitude[0] += modifications
                new_eff[effect] = tuple(new_magnitude)
            else:
                new_eff[effect] = details
        self.effect = new_eff

    def get_cost(self, combat = None):
        if combat == None:
            if self.cost == 'c':
                return 6
            else: 
                return self.cost
        elif isinstance(self.cost, str):
            if self.cost == 'U':
                return 'U'
            elif self.cost == 'X':
                return combat.energy
            elif self.cost == 'c':
                return max(0, 6 - combat.curse_count())
        elif isinstance(self.combat_cost[0], int):
            return self.combat_cost[0]
        else:
            return self.cost

    def played(self):
        if isinstance(self.combat_cost[1], str):
            if self.combat_cost == 'Played':
                self.combat_cost = (None, None)

    def chaos(self):
        self.combat_cost = (random.randint(0, 3), 'combat')
    
    def cost_change(self, cost, duration):
        self.combat_cost = (cost, duration)

    def property_change(self, property, new_value):
        properties = {
            'innate': self.innate,
            'exhaust': self.exhaust,
            'retain': self.retain,
            'ethereal': self.ethereal,
            'chaotic': self.chaotic
        }
        properties[property] = new_value

    def play_x_cost(self, cost):
        for effect, details in self.effect.items():
            self.x_cost_effect[effect] = [i if i != 'X' else cost for i in details]

def create_card(card_id, card_data: tuple):
    return Card(card_id, *card_data)