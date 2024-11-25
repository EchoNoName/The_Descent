import effects
import card_data
import card_constructor
import random

class Combat():
    def __init__(self, player, deck, relics, potions, enemies, combat_type, mechanics):
        self.player = player
        self.enemies = enemies
        self.deck = deck
        self.relics = relics
        self.potions = potions
        self.combat_type = combat_type
        self.mechanics = mechanics # {Intent: True/False, Ordered_Draw_Pile: True/False, Turn_End_Discard: True/False, Playable_Curse: True/False, Playable_Status: True/False, Exhaust_Change: %, }
        self.turn = 0
        self.start_of_combat = True
        self.draw_pile = deck
        self.cards_played = 0
        self.hand = []
        self.discard_pile = []
        self.exhaust_pile = []

    def get_targets(self, target_code):
        if target_code == 0:
            return self.player
        elif target_code == 1:
            return int(input('Enter the index of the enemy'))
        elif target_code == 2:
            return self.enemies[random.randint(0, len(self.enemies) - 1)]
        elif target_code == 3:
            return self.enemies
        else:
            raise ValueError(f"Unknown target code: {target_code}")
    
    def add_card_to_pile(self, location_code, card_id):
        '''adds a certain card to a certain pile

        args: 
            loctaion: represents which pile to add the card, 0 = hand, 1 = draw pile, 2 = discard pile. 3 = exhaust pile
            card: An object that represents the card
        '''
        if location_code == 0:
            self.hand.append(card_constructor.create_card(*card_data.Cards[card_id]))
        elif location_code == 1:
            self.draw_pile.append(card_constructor.create_card(*card_data.Cards[card_id]))
        elif location_code == 2:
            self.discard_pile.append(card_constructor.create_card(*card_data.Cards[card_id]))
        elif location_code == 3:
            self.exhaust_pile.append(card_constructor.create_card(*card_data.Cards[card_id]))
        else:
            raise ValueError(f'Unknown location code: {location_code}')
    
    def shuffle(self):
        if self.draw_pile:
            if self.discard_pile:
                self.draw_pile.extend(self.discard_pile)
                random.shuffle(self.draw_pile)
                self.discard_pile.clear()
            else:
                random.shuffle(self.draw_pile)
        else:
            if self.discard_pile:
                self.draw_pile = self.discard_pile
                self.discard_pile.clear()
        for relic in self.relics:
            relic.combatActionEff('shuffle')

    def draw(self, num):
        while num > 0:
            if not self.draw_pile:
                self.shuffle()
                if not self.draw_pile:
                    num -= 0
                else:
                    if self.hand:
                        self.hand.append(self.draw_pile[-1])
                        self.draw_pile.pop(-1)
                        num -= 1


    def player_turn_start(self):
        self.turn += 1
        if self.start_of_combat == True:
            for relic in self.relics:
                relic.combatActionEff('Combat Start')