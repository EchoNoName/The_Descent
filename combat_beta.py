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
        self.mechanics = mechanics # {Intent: True/False, Ordered_Draw_Pile: True/False, Turn_End_Discard: True/False, Playable_Curse: Effect/False, Playable_Status: Effect/False, Exhaust_Chance: %, }
        self.turn = 0
        self.start_of_combat = True
        self.draw_pile = deck
        self.cards_played = 0
        self.hand = []
        self.selected = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.energy_cap = 3
        self.energy = 0
    
    def get_energy_cap(self):
        for relics in self.relics:
            if relics.effect_class == 'Energy Relic':
                self.energy_cap += 1

    def get_targets(self, target_code):
        if target_code == 0:
            return [self.player]
        elif target_code == 1:
            i = int(input('Enter the index of the enemy'))
            return [self.enemies[i]]
        elif target_code == 2:
            return [self.enemies[random.randint(0, len(self.enemies) - 1)]]
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
            self.hand.append(card_constructor.create_card(card_id, *card_data.Cards[card_id]))
        elif location_code == 1:
            self.draw_pile.append(card_constructor.create_card(card_id, *card_data.Cards[card_id]))
        elif location_code == 2:
            self.discard_pile.append(card_constructor.create_card(card_id, *card_data.Cards[card_id]))
        elif location_code == 3:
            self.exhaust_pile.append(card_constructor.create_card(card_id, *card_data.Cards[card_id]))
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
            if len(self.hand) == 0:
                continue
            if not self.draw_pile:
                self.shuffle()
                if not self.draw_pile:
                    num -= 0
                else:
                    if self.hand:
                        self.hand.append(self.draw_pile[-1])
                        if 'Drawn' in self.hand[-1].effect:
                            for effect, values in self.hand[-1].effect['Turn End'].items():
                                targets = self.get_targets(self.hand[-1].target)
                                effect(*values, targets)
                        self.draw_pile.pop(-1)
                        num -= 1
    
    def soft_card_select(self, num):
        if not self.hand:
            return None
        else:
            confirm = True
            while confirm:
                if self.hand:
                    for card in self.hand:
                        i = 0
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                if self.selected:
                    for card in self.selected:
                        i = 0
                        print('selected: ')
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                select = input("Enter the index of the card u wish to select or unselect by typine r followed by the index and c to confirm choices")
                if select[0] == 'r':
                    self.selected.pop(int(select[1]))
                elif len(select) == 1:
                    if len(self.selected) == num:
                        continue
                    self.selected.append(self.hand[int(select)])
                    self.hand.pop(int(select))
                else:
                    if len(self.selected) == 1:
                        return self.selected[0].type
                    else:
                        return len(self.selected)

    def hard_card_select(self, num):
        if not self.hand:
            return None
        else:
            confirm = True
            while confirm:
                if self.hand:
                    for card in self.hand:
                        i = 0
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                if self.selected:
                    for card in self.selected:
                        i = 0
                        print('selected: ')
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                select = input("Enter the index of the card u wish to select or unselect by typine r followed by the index and c to confirm choices")
                if select[0] == 'r':
                    self.selected.pop(int(select[1]))
                elif len(select) == 1:
                    if len(self.selected) == num:
                        continue
                    self.selected.append(self.hand[int(select)])
                    self.hand.pop(int(select))
                else:
                    if self.hand == False:
                        if len(self.selected) == 1:
                            return self.selected[0].type
                        else:
                            return len(self.selected)
                    elif len(self.selected) < num:
                        continue
                    else:
                        if len(self.selected) == 1:
                            return self.selected[0].type
                        else:
                            return len(self.selected)
    
    def choose_discard(self, num):
        self.hard_card_select(num)
        self.discard_pile.extend(self.selected)
        self.selected.clear()

    def play_card(self, card):
        '''Method used for playing cards in combat

        args:
            card: card object made using card_constructor, contains all data of a card
        '''
        context = {
            'user': self.player,
            'enemies': self.enemies,
            'draw': self.draw_pile,
            'discard': self.discard_pile,
            'hand': self.hand,
            'exhaust': self.exhaust_pile,
            'target': card.target
        }
        # Context used for certain effects such as attacking where getting buffs is needed
        for effect, details in card.effect:
            # Iterates through every effect
            effect(*details, context, self)
            #  Performs the effects

    def player_turn_start(self):
        self.turn += 1
        if self.player.debuffs['Vulnerable'] > 0:
            self.player.debuffs['Vulnerable'] -= 1
        if self.player.debuffs['Weak'] > 0:
            self.player.debuffs['Weak'] -= 1
        if self.player.debuffs['Frail'] > 0:
            self.player.debuffs['Frail'] -= 1
        if self.start_of_combat == True:
            self.get_energy_cap()
            for relic in self.relics:
                relic.combatActionEff('Combat Start')
        for relic in self.relics:
            relic.combatActionEff('Turn Start')
        self.energy += self.energy_cap
        self.draw(5 + self.player.buffs['Draw Card'] - self.player.debuffs['Draw Reduction'])
        self.player.buffs['Draw Card'] = 0
        self.player.debuffs['Draw Reduction'] = 0
    # Not completed

    def player_turn_end(self):
        for card in reversed(self.hand):
            if 'Turn End' in card.effect:
                for effect, values in card.effect['Turn End'].items():
                    targets = self.get_targets(card.target)
                    effect(*values, targets)
            if card.retain == True:
                continue
            elif card.ethereal == True:
                self.exhaust_pile.append(card)
                self.hand.remove(card)
            else:
                self.discard_pile.append(card)
                self.hand.remove(card)