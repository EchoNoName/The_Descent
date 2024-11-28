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
        self.mechanics = mechanics # {Intent: True/False, Ordered_Draw_Pile: True/False, Turn_End_Discard: True/False, Playable_Curse: Effect/False, Playable_Status: True/False, Exhaust_Chance: %, Cards_per_Turn: False/int}
        self.turn = 0
        self.start_of_combat = True
        self.draw_pile = deck
        self.cards_played = 0
        self.hand = []
        self.selected = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.playing = None
        self.energy_cap = 3
        self.energy = 0
        self.retain = 0
        self.can_play_card = True
        self.num_of_cards_played = 0
        self.combat_active = True
    
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
    
    def add_card_to_pile(self, location, card_id, location_name, cost):
        '''adds a certain card to a certain pile

        args: 
            loctaion: represents which pile to add the card, 0 = hand, 1 = draw pile, 2 = discard pile. 3 = exhaust pile
            card: An object that represents the card
        '''
        card = card_constructor.create_card(card_id, *card_data.Cards[card_id])
        if cost != 't':
            card.cost_change(*cost)
        if location:
            if location_name == 'draw':
                location.insert(random.randint(0, len(location) - 1), card)
            else:
                location.append(card)
        else:
            raise ValueError(f'Unknown location: {location_name}')
    
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
                            for effect, values in self.hand[-1].effect['Drawn'].items():
                                targets = self.get_targets(self.hand[-1].target)
                                effect(*values, targets)
                        self.draw_pile.pop(-1)
                        num -= 1
    
    def soft_card_select(self, num, pile):
        if not pile:
            return None
        else:
            confirm = True
            while confirm:
                if pile:
                    for card in pile:
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
                    pile.append(self.selected(int(select[1])))
                    self.selected.pop(int(select[1]))
                elif len(select) == 1:
                    if len(self.selected) == num:
                        continue
                    self.selected.append(self.hand[int(select)])
                    pile.pop(int(select))
                else:
                    if len(self.selected) == 1:
                        if pile == self.draw_pile:
                            random.shuffle(self.draw_pile)
                        return self.selected[0].type
                    else:
                        if pile == self.draw_pile:
                            random.shuffle(self.draw_pile)
                        return len(self.selected)

    def hard_card_select(self, num, pile):
        if not pile:
            return None
        elif len(pile) <= num:
            self.selected.extend(pile)
            pile.clear()
            if num == 1:
                return self.selected[0].type
            else:
                return len(self.selected)
        else:
            confirm = True
            while confirm:
                if pile:
                    for card in pile:
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
                    pile.append(self.selected(select[1]))
                    self.selected.pop(int(select[1]))
                elif len(select) == 1:
                    if len(self.selected) == num:
                        continue
                    self.selected.append(self.hand[int(select)])
                    pile.pop(int(select))
                else:
                    if len(self.selected) < num:
                        continue
                    else:
                        if len(self.selected) == 1:
                            if pile == self.draw_pile:
                                random.shuffle(pile)
                            return self.selected[0].type
                        else:
                            if pile == self.draw_pile:
                                random.shuffle(pile)
                            return len(self.selected)

    def place_selected_cards(self, end_pile, cost):
        if self.selected:
            if cost != 't':
                for card in self.selected:
                    card.cost_change(*cost)
            end_pile.extend(self.selected)
            self.selected.clear()
    
    def search(self, num, type = 'all'):
        if not self.draw_pile:
            return None
        eligible_cards = []
        if type == 'all':
            eligible_cards.extend(self.draw_pile)
        elif type in {'common', 'uncommon', 'rare'}:
            rarity = {
                'common': 1,
                'uncommon' : 2,
                'rare': 3
            }
            for card in reversed(self.draw_pile):
                if card.rarity == rarity[type]:
                    eligible_cards.append(card)
                    self.draw_pile.remove(card)
            if eligible_cards:
                self.hard_card_select(num, eligible_cards)
                self.place_selected_cards(self.hand)
                self.draw_pile.extend(eligible_cards)
                eligible_cards.clear()
        elif type in {'atk', 'skill', 'power'}:
            return None
        # Placeholder
        
    def exhaust_discard_curse(self, num):
        self.hard_card_select(num, self.hand)
        if self.selected:
            for card in reversed(self.selected):
                if card.type == 4:
                    self.exhaust_pile.append(card)
                    self.selected.remove(card)
                else:
                    self.discard_pile.append(card)
                    self.selected.remove(card)

    def random_discard(self, num):
        if self.hand:
            if len(self.hand) > num:
                for i in range(0, num):
                    card = random.choice(self.hand)
                    if card.effect:
                        if 'Discarded' in card.effect:
                            context = {
                                'user': self.player,
                                'enemies': self.enemies,
                                'draw': self.draw_pile,
                                'discard': self.discard_pile,
                                'hand': self.hand,
                                'exhaust': self.exhaust_pile,
                                'target': card.target
                            }
                            for effect, details in card.effect['Discarded']:
                                effect(*details, context, self)
                    self.discard_pile.append(card)
                    self.hand.remove(card)
            else:
                self.discard_pile.extend(self.hand)
                self.hand.clear()

    def choose_discard(self, num):
        self.hard_card_select(num, self.hand)
        if self.selected:
            for card in self.selected:
                if card.effect:
                    if 'Discarded' in card.effect:
                        context = {
                                'user': self.player,
                                'enemies': self.enemies,
                                'draw': self.draw_pile,
                                'discard': self.discard_pile,
                                'hand': self.hand,
                                'exhaust': self.exhaust_pile,
                                'target': card.target
                            }
                        for effect, details in card.effect['Discarded']:
                            effect(*details, context, self)
            self.discard_pile.extend(self.selected)
            self.selected.clear()

    def exhaust_random_hand(self, num):
        if self.hand:
            if len(self.hand) > num:
                for i in range(0, num):
                    card = random.choice(self.hand)
                    if card.effect:
                        if 'Exhausted' in card.effect:
                            context = {
                                'user': self.player,
                                'enemies': self.enemies,
                                'draw': self.draw_pile,
                                'discard': self.discard_pile,
                                'hand': self.hand,
                                'exhaust': self.exhaust_pile,
                                'target': card.target
                            }
                            for effect, details in card.effect['Exhausted']:
                                effect(*details, context, self)
                    self.exhaust_pile.append(card)
                    self.hand.remove(card)
            else:
                self.exhaust_pile.extend(self.hand)
                self.hand.clear()
    
    def exhaust_choose_hand(self, num):
        self.hard_card_select(num, self.hand)
        if self.selected:
            for card in self.selected:
                if card.effect:
                    if 'Exhausted' in card.effect:
                        context = {
                                'user': self.player,
                                'enemies': self.enemies,
                                'draw': self.draw_pile,
                                'discard': self.discard_pile,
                                'hand': self.hand,
                                'exhaust': self.exhaust_pile,
                                'target': card.target
                            }
                        for effect, details in card.effect['Exhausted']:
                            effect(*details, context, self)
            self.exhaust_pile.extend(self.selected)
            self.selected.clear()

    def retain_cards(self, num):
        self.retain += num

    def energy_change(self, amount):
        self.energy += amount
        if self.energy < 0:
            self.energy = 0

    def card_limit(self, limit):
        if limit:
            if self.num_of_cards_played >= limit:
                self.can_play_card = False
            else:
                if self.mechanics['Cards_per_Turn'] != False:
                    if self.num_of_cards_played < self.mechanics['Cards_per_Turn']:
                        self.can_play_card = True
                else: 
                    self.can_play_card = True

    def resolve_action(self):
        for enemy in reversed(self.enemies):
            if enemy.Hp <= 0:
                self.enemies.remove(enemy)
        if not self.enemies:
            self.combat_active = False

    def havoc(self, num, special):
        for i in range(0, num):
            if self.draw_pile:
                self.playing = self.draw_pile[-1]
                if special == True:
                    self.playing.property_change('exhaust', True)
                context = {
                    'user': self.player,
                    'enemies': self.enemies,
                    'draw': self.draw_pile,
                    'discard': self.discard_pile,
                    'hand': self.hand,
                    'exhaust': self.exhaust_pile,
                    'target': 2
                }
                self.play_card(context)
    
    def sever(self, card_type: set) -> list:
        cards_exhausted_type = []
        if self.hand:
            for card in reversed(self.hand):
                if card.type in card_type:
                    cards_exhausted_type.append(card.type)
                    self.exhaust_pile.append(card)
                    self.hand.remove(card)
        return cards_exhausted_type

    def play_card(self, override = None):
        '''Method used for playing cards in combat
        '''
        context = {
            'user': self.player,
            'enemies': self.enemies,
            'draw': self.draw_pile,
            'discard': self.discard_pile,
            'hand': self.hand,
            'exhaust': self.exhaust_pile,
            'target': self.playing.target
        }
        if override:
            context = override
        # Context used for certain effects such as attacking where getting buffs is needed
        if self.playing.get_cost(self) == 'U':
            if self.playing.type == 3 and self.mechanics['Playable_Status']:
                self.exhaust_pile.extend(self.playing)
                self.playing = None
            elif self.playing.type == 4 and self.mechanics['Playable_Curse']:
                for effect, details in self.mechanics['Playable_Curse'].items():
                    effect(details, context, self)
                self.exhaust_pile.extend(self.playing)
                self.playing = None
        elif self.playing.get_cost(self) == 'X':
            self.playing.play_x_cost(self.energy)
            for effect, details in self.playing.x_cost_effect:
                effect(*details, context, self)
            if self.playing.exhaust == True:
                self.exhaust_pile.extend(self.playing)
            else:
                self.discard_pile.extend(self.playing)
        elif self.playing.effect:
            for effect, details in self.playing.effect.items():
                # Iterates through every effect
                if not isinstance(effect, str):
                    effect(*details, context, self)
                    #  Performs the effects if its not a conditional
            if self.type == 2:
                self.player.power.apppend[self.playing]
            elif self.playing.exhaust == True:
                self.exhaust_pile.extend(self.playing)
            else:
                self.discard_pile.extend(self.playing)
        self.playing = None
        self.num_of_cards_played += 1
        if self.hand:
            for card in self.hand:
                if 'Card Played' in card.effect:
                    for effect, details in card.effect['Card Played']:
                        effect(*details, context, self)
                    self.resolve_action()
    
    def use_potion(self, potion):
        '''Method used for using potions in combat

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
            'target': potion.target
        }
        if potion.time_of_use in {'combat', 'all'}:
            for effect, details in potion.effect:
                effect(*details, context, self)
        self.potions.remove(potion)
        global potions
        potions.remove(potion)

    def player_turn_start(self):
        self.can_play_card = True
        self.energy = 0
        self.turn += 1
        self.num_of_cards_played = 0
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

    def player_turn(self):
        turn = True
        while turn:
            player_action = input('Enter the index of the card you wish to play or P# with # being index of the potion being used or E for end turn.')
            if player_action == 'E':
                turn = False
                self.player_turn_end()
                break
            else:
                if len(player_action) == 1:
                    if self.can_play_card == False:
                        print(f'You cannot play anymore cards!')
                        continue
                    player_action = int(player_action)
                    card = self.hand[player_action]
                    cost = card.get_cost(self)
                    if cost > self.energy:
                        print('Not enought energy')
                    else:
                        new_energy = self.energy - cost
                        self.play_card(card)
                        self.energy = new_energy
                else: 
                    player_action = player_action[1]
                    player_action = int(player_action)
                    potion = self.potions[player_action]
                    self.use_potion(potion)
            self.resolve_action()

    def player_turn_end(self):
        context = {
            'user': self.player,
            'enemies': self.enemies,
            'draw': self.draw_pile,
            'discard': self.discard_pile,
            'hand': self.hand,
            'exhaust': self.exhaust_pile,
            'target': card.target
        }
        if self.hand:
            for card in reversed(self.hand):
                if 'Turn End' in card.effect:
                    for effect, values in card.effect['Turn End'].items():
                        effect(*values, context, self)
            if self.mechanics['turn_end_discard']:
                self.soft_card_select(self.retain, self.hand)
                for card in reversed(self.hand):
                    if card.retain:
                        continue
                    elif card.ethereal:
                        self.exhaust_pile.append(card)
                        if card.effect:
                            if 'Exhausted' in card.effect:
                                for effect, details in card.effect['Exhausted']:
                                    effect(*details, context, self)
                    else:
                        self.discard_pile.append(card)
                        for card in self.selected:
                            if 'Discarded' in card.effect:
                                for effect, details in card.effect['Discarded']:
                                    effect(*details, context, self)
                    self.hand.remove(card)