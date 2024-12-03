import effects
import enemy_data
import card_data
import card_constructor
import random

class Combat:
    def __init__(self, player, deck, relics, potions, enemies, combat_type, mechanics):
        self.player = player # The Player 
        self.enemies = enemies # The Enemies in a combat encounter
        self.deck = deck # The player's deck
        self.relics = relics # The player's relics
        self.potions = potions # The player's potions
        self.combat_type = combat_type # The Type of combat, (Normal, Elite, Boss)
        self.mechanics = mechanics # {Intent: True/False, Ordered_Draw_Pile: True/False, Turn_End_Discard: True/False, Playable_Curse: Effect/False, Playable_Status: True/False, Exhaust_Chance: %, Cards_per_Turn: False/int}
        self.turn = 0 # Turn counter
        self.start_of_combat = True # Whether its the start of combat
        self.draw_pile = deck # Draw pile
        self.cards_played = 0 # num of cards played
        self.hand = [] # Cards in hand
        self.selected = [] # Selected cards
        self.discard_pile = [] # Discard pile
        self.exhaust_pile = [] # Exhaust pile
        self.playing = None # The card being played
        self.energy_cap = 3 # Energy gained at the start of the turn
        self.energy = 0 # Current energy
        self.retain = 0 # num of cards to keep at the end of the turn
        self.can_play_card = True # If the player can play cards
        self.combat_active = True # Whether the player is in this combat
        self.powers = [] # The powers the player has gained
        self.enemy_turn = False
    
    def power_check_and_exe(self, cond: str):
        '''Method to check if a power's condition is met and activates its effect if it is

        ### args:
            cond (string): The event that is occuring
        '''
        if self.powers: # If there are powers played
            for card in self.powers: # For all powers
                context = {
                    # Basic info to be passed on for executing effects
                    'user': self.player,
                    'enemies': self.enemies,
                    'draw': self.draw_pile,
                    'discard': self.discard_pile,
                    'hand': self.hand,
                    'exhaust': self.exhaust_pile,
                    'target': card.target
                }
                if 'Power' in card.effect:
                    # The power effect in a card
                    for power_cond, effect in card.effect['Power'].items():
                        # for every condition and effect
                        if cond == power_cond: # If the condition is met
                            for effects, effect_details in effect.items():
                                effects(*effect_details, context, self)
                                # Execute the power's effect

    def get_energy_cap(self):
        '''Gets the energy cap of the player
        '''
        for relics in self.relics:
            # Goes throught every relic
            if relics.effect_class == 'Energy Relic':
                # If its an energy relic
                self.energy_cap += 1
                # Add 1 energy to the cap

    def get_targets(self, context):
        '''Retrieves the target of a card based on the cards target code

        ### args:
            target_code (int): An int corresponding to a specific target or targets
        '''
        target_code = context['target']
        if self.enemy_turn == False:
            # If its the players turn
            if target_code == 0:
                # If its 0
                return [context['user']]
                # Returns the player
            elif target_code == 1:
                # If its 1
                i = int(input('Enter the index of the enemy'))
                # Asks the player for which enemy to target
                return [self.enemies[i]]
                # returns that target
            elif target_code == 2:
                # if its 2
                return [self.enemies[random.randint(0, len(self.enemies) - 1)]]
                # Returns a random enemy
            elif target_code == 3:
                # if its 3
                return self.enemies
                # Returns all the enemies
            else:
                raise ValueError(f"Unknown target code: {target_code}")
                # Errors
        else:
            # If its the enemies turn
            if target_code == 0:
                # If its 0
                return [context['user']]
                # Returns the player
            elif target_code == 1:
                # If its 1
                return [self.player]
                # returns that player
            elif target_code == 2:
                # if its 2
                return [self.enemies[random.randint(0, len(self.enemies) - 1)]]
                # Returns a random enemy
            elif target_code == 3:
                # if its 3
                return self.enemies
                # Returns all the enemies
            else:
                raise ValueError(f"Unknown target code: {target_code}")
                # Errors
    
    def add_card_to_pile(self, location, card_id, location_name, cost):
        '''adds a certain card to a certain pile

        ### args: 
            loctaion (int): represents which pile to add the card, 0 = hand, 1 = draw pile, 2 = discard pile. 3 = exhaust pile
            card (object): An object that represents the card
        '''
        card = card_constructor.create_card(card_id, *card_data.card_info[card_id])
        # Creates a card object using methods in card_constructor and data in card_data
        if cost != 'na':
            # If a cost change is needed
            card.cost_change(*cost)
            # Modifies the cards cost
        if location:
            # If a locations was specified, to which it should
            if location_name == 'draw':
                # If its the draw pile, insert is somewhere random
                location.insert(random.randint(0, len(location) - 1), card)
            else:
                # If its anywhere else adding it to the top works
                location.append(card)
        else:
            raise ValueError(f'Unknown location: {location_name}')
            # Error
    
    def shuffle(self):
        '''
        Method for shuffling the discard pile into the draw pile and shuffling the order of the draw pile
        '''
        if self.draw_pile:
            # If the draw pile is not empty
            if self.discard_pile:
                # If the discard pile is not empty
                self.draw_pile.extend(self.discard_pile)
                # Add the discard pile to the draw pile
                random.shuffle(self.draw_pile)
                # Shuffle the draw pile
                self.discard_pile.clear()
                # Empty the discard pile
        else:
            if self.discard_pile:
                # If the discard pile is not empty
                self.draw_pile = self.discard_pile
                # Make the draw pile the discard pile
                random.shuffle(self.draw_pile)
                # Shuffle the draw pile
                self.discard_pile.clear()
                # Empty the discard pile
        for relic in self.relics:
            # Go through every relic
            relic.combatActionEff('shuffle')
            # Active the relic effects with the event being shuffling

    def draw(self, num: int):
        '''Method for drawing cards during combat
        
        ### args:
            num (int): The number of cards that needs to be drawn
        '''
        while num > 0: # While drawing still needs to be done
            if len(self.hand) == 10: 
                # If the hand is full
                num -= 1
                # One less card to draw
                continue
                # To the next iteration
            elif not self.draw_pile:
                # If the draw piel is empty
                self.shuffle()
                # shuffle the draw pile
                if not self.draw_pile:
                    # If the draw pile is still empty
                    num -= 1
                    # One less card to draw
                    continue
                    # To the next iteration
            else:
                self.hand.append(self.draw_pile[-1])
                # "draw" a card
                if 'Drawn' in self.hand[-1].effect:
                    # If the card has a when drawn effect
                    for effect, details in self.hand[-1].effect['Drawn'].items():
                        context = {
                            # Basic info to be passed on for executing effects
                            'user': self.player,
                            'enemies': self.enemies,
                            'draw': self.draw_pile,
                            'discard': self.discard_pile,
                            'hand': self.hand,
                            'exhaust': self.exhaust_pile,
                            'target': self.hand[-1].target
                        }
                        effect(*details, context, self)
                        # Execute the drawn effect
                self.draw_pile.pop(-1)
                # Remove the top card of the draw pile as thats where we drew from
                num -= 1
                # One less card to draw
    
    def soft_card_select(self, num : int, pile : list):
        '''A soft card select refers to when the game needs the player to select up to x amount of cards but can choose to select below x amount of cards or none at all
        
        ### args:
            num (int): Number of cards that needs to be selected
            pile (list): The place the player needs to select from

        ### Returns:
            Number of cards selected (If more than 1) or the type of card selected (If 1 card was selected) or None (No cards were selected)
            '''
        if not pile:
            # If the pile to select from is empty
            return None
        else:
            confirm = True
            # Initialize confirm selection boolean
            while confirm:
                # While the player hasn't confirmed yet
                if pile:
                    # If the pile to select from isn't empty
                    for card in pile:
                        # Prints all cards in the pile with relevent detail
                        i = 0
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                if self.selected:
                    # If there has been cards already selected
                    for card in self.selected:
                        # Prints all cards in the selected pile with relevent detail
                        i = 0
                        print('selected: ')
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                select = input("Enter the index of the card u wish to select or unselect by typing the index and cs to confirm choices")
                # Request for player input
                if len(select) == 1:
                    # Select another card
                    if pile[int(select)] in self.selected:
                        # Card is already selected
                        self.selected.remove(pile[int(select)])
                        # Unselected the card
                    elif len(self.selected) == num:
                        # If they already selected the max num of cards
                        continue
                        # Do nothing
                    else:
                        self.selected.append(self.hand[int(select)])
                        # Add the chosen card to selected
                else:
                    confirm = False
                    # Confirming choices
                    if len(self.selected) == 1:
                        # If only 1 card was selected
                        if pile == self.draw_pile:
                            # If its the draw pile
                            random.shuffle(self.draw_pile)
                            # Shuffle the draw pile
                        pile.remove(self.selected[0])
                        # Remove the selected card from the pile
                        return self.selected[0].type
                        # Returns the type of card selected
                    else:
                        if pile == self.draw_pile:
                            # If its the draw pile
                            random.shuffle(self.draw_pile)
                            # Shuffle the draw pile
                        for card in self.selected:
                            pile.remove(card)
                            # Remove the selected card from the pile
                        return len(self.selected)
                        # Returns the number of cards selected

    def hard_card_select(self, num, pile):
        '''A hard card select refers to when the game needs the player to select x amount of cards and they must choose the maximum amount of cards to select
        
        ### args:
            num (int): Number of cards that needs to be selected
            pile (list): The place the player needs to select from

        ### Returns:
            Number of cards selected (If more than 1) or the type of card selected (If 1 card was selected) or None (No cards were selected)
        '''
        if not pile:
            # If the pile to select from is empty
            return None
            # Doesn't select anything
        elif len(pile) <= num:
            # If the # of cards in pile is equal to or less then the # of cards that needs to be selected
            self.selected.extend(pile)
            # Add all cards in pile to selected
            pile.clear()
            # Empty the pile
            if num == 1:
                return self.selected[0].type
            else:
                return len(self.selected)
            # Returns the # of cards selected or type of card selected depending on if more than 1 card was selected
        else:
            confirm = True
            # Initialize confirm selection boolean
            while confirm:
                # While the player hasn't confirmed yet
                if pile:
                    # If the pile to select from isn't empty
                    for card in pile:
                        # Prints all cards in the pile with relevent detail
                        i = 0
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                if self.selected:
                    # If there has been cards already selected
                    for card in self.selected:
                        # Prints all cards in the selected pile with relevent detail
                        i = 0
                        print('selected: ')
                        print(f'{i}: {card.name}, cost: {card.combat_cost}, effect: {card.effect}')
                        i += 1
                select = input("Enter the index of the card u wish to select or unselect by typine r followed by the index and c to confirm choices")
                # Request for player input
                if len(select) == 1:
                    # Select another card
                    if pile[int(select)] in self.selected:
                        # Card is already selected
                        self.selected.remove(pile[int(select)])
                        # Unselected the card
                    elif len(self.selected) == num:
                        # If they already selected the max num of cards
                        continue
                        # Do nothing
                    else:
                        self.selected.append(self.hand[int(select)])
                        # Add the chosen card to selected
                else:
                    if len(self.selected) < num:
                        # If not enought cards were selected
                        continue
                        # Does nothing
                    else:
                        confirm = False
                        # Turns off loop
                        for card in self.selected:
                            pile.remove(card)
                            # Remove the selected card from the pile
                        if len(self.selected) == 1:
                            if pile == self.draw_pile:
                                # If its the draw pile
                                random.shuffle(self.draw_pile)
                                # Shuffle the draw pile
                            return self.selected[0].type
                            # Returns the type of card selected
                        else:
                            if pile == self.draw_pile:
                                # If its the draw pile
                                random.shuffle(self.draw_pile)
                                # Shuffle the draw pile
                            return len(self.selected)
                            # Returns the number of cards selected

    def place_selected_cards(self, end_pile, cost):
        '''Method for placing a selected card into a specific pile

        ### args: 
            end_pile: The location the selected cards end up
            cost: Any cost modifcations to the cards, na for no modifications
        '''
        if self.selected:
            # If there are cards selected
            if cost != 'na':
                # If there is a cost change needed
                for card in self.selected:
                    # Change the cost for everycard in selected
                    card.cost_change(*cost)
            end_pile.extend(self.selected)
            # Adds all selected cards to the top of the end pile
            self.selected.clear()
            # Empty selected cards
    
    def search(self, num, type = 'all'):
        ''' Add a card from the draw pile to the hand (Searching)

        ### args: 
            num: Number of cards you can add from the draw pile to the hand
            type: The type of cards that you can search, all by default
        '''
        if not self.draw_pile:
            # If there are no cards in the draw pile
            return None
            # Returns nothing
        eligible_cards = []
        # Initilize eligible_cards
        if type == 'all':
            # If all cards can be searched
            eligible_cards.extend(self.draw_pile)
            # Make eligible_cards the entire draw pile
        elif type in {'common', 'uncommon', 'rare'}:
            # If searching based on rarity
            rarity = {
                'common': 1,
                'uncommon' : 2,
                'rare': 3
            }
            for card in reversed(self.draw_pile):
                # Go through every card in the draw pile
                if card.rarity == rarity[type]:
                    # The the rarity match the seach type
                    eligible_cards.append(card)
                    # Add it to eligible cards
                    self.draw_pile.remove(card)
                    # Remove the cards from the draw pile
            if eligible_cards:
                # If there are eligible cards
                self.hard_card_select(num, eligible_cards)
                # Select from the cards
                for card in reversed(self.selected):
                    # Loop through every card in selected
                    if len(self.hand) < 10:
                        # While the hand is below the hand size limit
                        self.hand.append(self.selected)
                        # Add the selected card to hand
                        self.selected.remove(card)
                        # Remove it from selected
                    else:
                        self.discard_pile.extend(self.selected)
                        # Add remaining cards the discard pile
                        self.selected.clear()
                        # Empty selected cards
                        break
                        # Exit the loop
                # Place them in the hand
                self.draw_pile.extend(eligible_cards)
                # Read the cards back to the draw pile
                random.shuffle(self.draw_pile)
                # Shuffle the draw pile
                eligible_cards.clear()
                # Empty eligible cards

        elif type in {'atk', 'skill', 'power'}:
            return None
        # Placeholder
        
    def exhaust_discard_curse(self, num):
        '''Discard X amounts of cards from hand and exhaust all discarded curses
        
        ### args: 
            num: Number of cards that needs to be discarded
        '''
        self.hard_card_select(num, self.hand)
        # Select cards from hand
        if self.selected:
            # If there were cards selected
            for card in reversed(self.selected):
                # Loop through cards selected
                if card.type == 4:
                    # If the card is a curse
                    self.exhaust_pile.append(card)
                    # add the card to the exhaust pile
                    self.if_card_cond(card, 'Exhausted')
                    # Executes exhausted effects
                    self.selected.remove(card)
                    # Remove the card from selected
                else:
                    self.discard_pile.append(card)
                    # Add the card to the discard pile
                    self.if_card_cond(card, 'Discarded')
                    # Executes Discarded effects
                    self.selected.remove(card)
                    # Discards the card instead

    def random_discard(self, num: int):
        '''Randomly discards cards from the hand
        
        ### args:
            num: The Number of cards to randomly discard'''
        if self.hand:
            # If there are cards in hand
            if len(self.hand) > num:
                # There are more cards in hand than the amount needed to be discarded
                for i in range(0, num):
                    # Iterate num amount of times
                    card = random.choice(self.hand)
                    # Choose a random card
                    if card.effect:
                        self.if_card_cond(card, 'Discarded')
                        # Execute the discarded effect
                    self.discard_pile.append(card)
                    # Add the card to the discard pile
                    self.hand.remove(card)
                    # Remove the card from hand
            else:
                for card in reversed(self.hand):
                    # Go throught every card
                    if card.effect:
                        self.if_card_cond(card, 'Discarded')
                        # Execute the discarded effect
                    self.discard_pile.append(card)
                    # Add the card to the discard pile
                    self.hand.remove(card)
                    # Remove the card from hand

    def choose_discard(self, num: int):
        '''Selected a number of cards to discard from the hand
        
        ### args:
            num: The number of cards that needs to be discarded
        '''
        self.hard_card_select(num, self.hand)
        # Selected a certain amount of cards from the hand
        if self.selected:
            # If there were cards selected
            for card in reversed(self.selected):
                # Go through every selected card
                if card.effect:
                    self.if_card_cond(card, 'Discarded')
                    # Executes all if Discarded effects
                self.discard_pile.append(card)
                # Add the card to the discard pile
                self.selected.remove(card)
                # remove the card from selected

    def exhaust_random_hand(self, num: int):
        '''Exhausts a number of random cards from the hand
        
        ### args:
            num: The number of cards that needs to be exausted'''
        if self.hand:
            # If there are cards in hand
            if len(self.hand) > num:
                # There are more cards in hand than the amount needed to be Exhausted
                for i in range(0, num):
                    # Iterate num amount of times
                    card = random.choice(self.hand)
                    # Choose a random card
                    if card.effect:
                        # If that card has a effect when exhausted
                        self.if_card_cond(card, 'Exhausted')
                    self.exhaust_pile.append(card)
                    # Add the card to the Exhausted pile
                    self.hand.remove(card)
                    # Remove the card from hand
            else:
                for card in reversed(self.hand):
                    # Go throught every card
                    if card.effect:
                        self.if_card_cond(card, 'Exhausted')
                        # Execute the Exhausted effect
                    self.exhaust_pile.append(card)
                    # Add the card to the Exhausted pile
                    self.hand.remove(card)
                    # Remove the card from hand
    
    def exhaust_choose_hand(self, num : int):
        '''Exhaust a number choosen cards from hand
        
        ### args: 
            num: Number of cards that needs to be exhausted'''
        self.hard_card_select(num, self.hand)
        # Select a number of cards
        self.exhaust_selected()

    def exhaust_selected(self):
        '''Exhausts selected cards
        
        ### Returns: 
            True or False depending on if a card was exhausted'''
        if self.selected:
            # If there are selected cards
            for card in self.selected:
                # Go through every selected card
                self.if_card_cond(card, 'Exhausted')
            self.exhaust_pile.extend(self.selected)
            # Add all selected cards to exhaust pile
            self.selected.clear()
            # Empty selected cards
            return True
        return False
    
    def if_card_cond(self, card, cond : str, override = None):
        '''Executes card effects that happens when something happens to a card (IE: Discarded, Exhausted, etc)
        
        ### args:
            card: The card being exhausted
            cond: The condition that is happening
            override: Info override for certain situations
        '''
        context = {
            # Info to be passed on in effect execution
            'user': self.player,
            'enemies': self.enemies,
            'draw': self.draw_pile,
            'discard': self.discard_pile,
            'hand': self.hand,
            'exhaust': self.exhaust_pile,
            'target': card.target
        }
        if override:
            context = override
        # uses override context if there is one
        if card.effect:
            # If the cards have effects
            if cond in card.effect:
                # If the cards have an exhausted effect
                for effect, details in card.effect[cond].items():
                    effect(*details, context, self)
                    # Executing effects

    def retain_cards(self, num: int):
        '''Increase the amount of cards you can keep at the end of the turn

        ### args:
            num: The amount to increase by
        '''
        self.retain += num

    def energy_change(self, amount: int):
        '''Updates the amount of energy the player has
        
        ### args:
            amount: The number to change the energu by, can be positive or negative'''
        self.energy = min(0, self.energy + amount)
        # Adds amount to energy, if energy becomes negative, becomes 0 instead

    def card_limit(self, limit = False):
        '''Checks for if the player can play anymore cards
        
        ### args:
            limit: The Number of cards you can play per turn, False if there is none given'''
        if limit:
            # If limit is not false
            if self.cards_played >= limit:
                # If the number of cards played is above or equal to the limit
                self.can_play_card = False
                # Disable the ability to play cards
            else:
                if self.mechanics['Cards_per_Turn'] != False:
                    # Checks for if there is a cards per turn limit set
                    if self.cards_played < self.mechanics['Cards_per_Turn']:
                        # If its below the amount
                        self.can_play_card = True
                        # can play cards
                    else:
                        self.can_play_card = False
                        # Disable the ability to play cards
                else: 
                    self.can_play_card = True
                    # No Limit set

    def resolve_action(self):
        '''Resolves an action done by the player, mainly just checks for deaths of enemies and if a end of combat condition is met'''
        for enemy in reversed(self.enemies):
            # Goes throught every enemy
            if enemy.died(self) == True:
                # If they're dead
                self.enemies.remove(enemy)
                # Remove them from the enemy list
        if not self.enemies:
            # If there are no more enemies
            self.combat_active = False
            # End the combat

    def havoc(self, num: int, special: bool):
        '''Havoc referrs to playing the top card of the draw pile, this Method will do that action a number of times
        
        ### args:
            num: Number of times to havoc
            special: true or false to represent whether to exhaust the card played this way'''
        for i in range(0, num):
            # Iterate a certain amount of times
            if self.draw_pile:
                # If there are cards in the draw pile
                self.playing = self.draw_pile[-1]
                # Make the top card the card being played
                self.draw_pile.pop(-1)
                # Remove the top card of the draw pile
                if special == True:
                    # If the played card needs to be exhausted
                    self.playing.property_change('exhaust', True)
                    # Make the card exhaust
                context = {
                    # Info to be passed on for executing effects
                    'user': self.player,
                    'enemies': self.enemies,
                    'draw': self.draw_pile,
                    'discard': self.discard_pile,
                    'hand': self.hand,
                    'exhaust': self.exhaust_pile,
                    'target': 2
                }
                self.play_card(context)
                # Play the card
            else:
                break
                # end the loop
    
    def sever(self, card_type: set) -> list:
        ''' Sever refers to exhausting all cards of certain types from hand
        
        ### args:
            card_type (set): Contains all the card type ids of the cards that needs to be exhausted'''
        cards_exhausted_type = []
        # Initialize a list for storing the types of all cards exhausted
        if self.hand:
            # If the hand is not empty
            for card in reversed(self.hand):
                # Go through all cards in the hand
                if card.type in card_type:
                    # If the card type is a type that needs to be exhausted
                    cards_exhausted_type.append(card.type)
                    # Save the type of the card exhausted to the list
                    self.exhaust_pile.append(card)
                    # Add the card to the exhaust pile
                    self.hand.remove(card)
                    # remove the card from hand
        return cards_exhausted_type
        # Returns the list of types of all the cards exhausted, used for executing conditional effects on certain cards
    
    def mulligan(self):
        '''Method for performing a mulligan which refers to discarding any number of cards from the hand and drawing that many back
        '''
        if self.hand:
            # If the player even has cards in the hand
            self.soft_card_select(len(self.hand), self.hand)
            # Selected as many cards in hand as the player wants
            if self.selected:
                # If there were cards selected
                amount = len(self.selected)
                # Save amount of cards selected
                for card in reversed(self.selected):
                    self.discard_pile.append(card)
                    self.selected.remove(card)
                # Add cards to discard pile
                self.draw(amount)
                # Draw same amount back

    def exhaust_entire_pile(self, pile):
        '''Exhausts an entire pile
        
        ### args:
            pile: The pile that needs to be exhausted'''
        if pile:
            # if the pile is not empty
            for card in reversed(pile):
                # Goes through every card in the pile
                self.exhaust_pile.append(card)
                # Add the card to the exhaust pile
                pile.remove(card)
                # remove the card from the pile

    def play_card(self, override = None):
        '''Method used for playing cards in combat

        ### args:
            overide: A dictionary of information that is passed on to execute effects, only inputted if some info needs to be overrided to not be the default
        '''
        context = {
            # Default info to pass on for executing effects
            'user': self.player, # The player is playing the card
            'enemies': self.enemies, # List of enemies
            'draw': self.draw_pile, # The draw pile
            'discard': self.discard_pile, # The discard pile
            'hand': self.hand, # the hand
            'exhaust': self.exhaust_pile, # The exhaust pile
            'target': self.playing.target # the target of the card, This is mainly the one that gets overrided
        }
        if override: # If there is an override
            context = override # Use the override instead
        # Context used for certain effects such as attacking where getting buffs is needed
        if self.can_play_card == False:
            self.discard_pile.append(self.playing)
            # Add the card to the discard pile
        elif self.playing.get_cost(self) == 'U':
            # If the card being played is Unplayable
            if self.playing.type == 3 and self.mechanics['Playable_Status']:
                # If the type of card is a status and the mechanic Playable_Status is activated
                self.exhaust_pile.append(self.playing)
                # Add the card to the exhaust pile
                self.playing = None
                # Empty the playing card
            elif self.playing.type == 4 and self.mechanics['Playable_Curse']:
                # If the type of card is a Curse and the mechanic Playable_Curse is activated
                for effect, details in self.mechanics['Playable_Curse'].items():
                    effect(*details, context, self)
                    # Execute the effect for playing a curse
                self.exhaust_pile.append(self.playing)
                # Add the card to the exhaust pile
        elif self.playing.get_cost(self) == 'X':
            # If you are playing an X cost card (A card that spends all you energy and has effects scale off of energy spent)
            self.playing.play_x_cost(self.energy)
            # Aquire the complete details of the effect being executed
            for effect, details in self.playing.x_cost_effect.items():
                effect(*details, context, self)
                # Execute the X cost effect
            if self.playing.exhaust == True:
                # If the card exhausts
                self.exhaust_pile.append(self.playing)
                # Add the card to the exhaust pile 
                self.if_card_cond(self.playing, 'Exhausted')
                # Execute Exhausted effects
            else:
                self.discard_pile.append(self.playing)
                # Add the card to the discard pile
        elif self.playing.effect:
            # If the card has an effect
            for effect, details in self.playing.effect.items():
                # Iterates through every effect
                if not isinstance(effect, str):
                    effect(*details, context, self)
                    #  Performs the effects if its not a conditional
            if self.type == 2:
                # If the card played was a power
                self.powers.append[self.playing]
                # Add the card played to the player powers
            elif self.playing.exhaust == True:
                # If the card played exhausts
                self.exhaust_pile.append(self.playing)
                # Add the card to the exhaust pile
                self.if_card_cond(self.playing, 'Exhausted')
                # Execute Exhausted effects
            else:
                self.discard_pile.append(self.playing)
                # Add the card to the discard pile
        self.playing = None
        # Empty the currently playing card
        self.cards_played += 1
        # Increase the amount of cards played by 1
        if self.hand:
            # if there are cards in hand
            for card in self.hand:
                # for all cards in hand
                self.if_card_cond(card, 'Card Played')
                # Execute effects for if a card is played
                self.resolve_action()
                # Resolve effects
        self.resolve_action()
    
    def use_potion(self, potion):
        '''Method used for using potions in combat

        ### args:
            Potion: The potion that is being used
        '''
        context = {
            # Info for executing effects
            'user': self.player,
            'enemies': self.enemies,
            'draw': self.draw_pile,
            'discard': self.discard_pile,
            'hand': self.hand,
            'exhaust': self.exhaust_pile,
            'target': potion.target
        }
        if potion.time_of_use == 'combat':
            # If the potion that is being used can be used during combat
            for effect, details in potion.effect.items():
                effect(*details, context, self)
                # Execute effects
            self.potions.remove(potion)
            global potions
            potions.remove(potion)
            # Remove the potion from combat and the player object
        elif potion.time_of_use == 'all':
            self.player.use_potion(potion)
            self.potions.remove(potion)
            # Use potion using player method
        else:
            print(f'Invalid time of use: {potion.time_of_use}')
            # Invalid time of use

    def player_turn_start(self):
        '''Method for doing everything that needs to be done at the start of combat'''
        self.can_play_card = True
        # Set the ability to play cards to be true
        self.energy = 0
        # Set energy to 0
        self.turn += 1
        # Increase turn counter
        self.cards_played = 0
        # Set cards played to 0
        if self.player.debuffs['Vulnerable'] > 0:
            self.player.debuffs['Vulnerable'] -= 1
        if self.player.debuffs['Weak'] > 0:
            self.player.debuffs['Weak'] -= 1
        if self.player.debuffs['Frail'] > 0:
            self.player.debuffs['Frail'] -= 1
        # Lower some debuff counters by 1
        if self.start_of_combat == True:
            # If its the start of combat
            self.get_energy_cap()
            # Retrieve the enery cap for this combat
            for relic in self.relics:
                # Go through all relics
                relic.combatActionEff('Combat Start')
                # Execute start of combat effects of relics
        for relic in self.relics:
            # Go through all relics
            relic.combatActionEff('Turn Start')
            # Execute start of turn effects of relics
        self.energy += self.energy_cap
        # Add energy cap to energy
        self.draw(5 + self.player.buffs['Draw Card'] - self.player.debuffs['Draw Reduction'])
        # Draw 5 cards for the start of turn, modified depending on buffs and debuffs that affect draw
        self.player.buffs['Draw Card'] = 0
        # Said buff resets
        self.player.debuffs['Draw Reduction'] = 0
        # Said debuff resets
    # Not completed

    def player_turn(self):
        '''Execute actions the player does during their turn'''
        turn = True
        # Set turn to true
        while turn:
            # While its still the player's turn
            player_action = input('Enter the index of the card you wish to play or P# with # being index of the potion being used or E for end turn.')
            # Asks player for input on what to do
            if player_action == 'E':
                # If the player wants to end the turn
                turn = False
                # Turn to false
                self.player_turn_end()
                # Executes turn end actions
                break
                # Exits the loop
            else:
                if len(player_action) == 1:
                    # if the player is playing a card
                    if self.can_play_card == False:
                        # If they can't play anymore cards
                        print(f'You cannot play anymore cards!')
                        # Give player feedback
                        continue
                    player_action = int(player_action)
                    # Convert to an int
                    card = self.hand[player_action]
                    # Retrieve the card that is attempting to be played
                    cost = card.get_cost(self)
                    # Retreive the cost of the card
                    if cost > self.energy:
                        # If the cist is higher then the energy the player has
                        print('Not enought energy')
                        # Gives feedback
                        continue
                    else:
                        new_energy = self.energy - cost
                        # Hold the updated energy
                        self.playing = card
                        self.play_card()
                        # play the card
                        self.energy = new_energy
                        # Update energy
                else: 
                    # For potions
                    player_action = int(player_action[1])
                    # Gets the index of the potion being used
                    potion = self.potions[player_action]
                    # Retreives the correct potion
                    self.use_potion(potion) 
                    # Use the potion
            self.resolve_action()
            # Resolve actions

    def player_turn_end(self):
        '''Executes actions of the player's turn ending'''
        if self.hand:
            # If the hand isn't empty
            for card in reversed(self.hand):
                # Go through every card
                self.if_card_cond(card, 'Turn End')
                # Execute turn end effects
            if self.mechanics['turn_end_discard']:
                # Check if the player needs to discard their hand
                self.soft_card_select(self.retain, self.hand)
                # Select a number of cards to keep
                for card in reversed(self.hand):
                    # goes through everycard in hand
                    if card.retain:
                        # If its retain
                        continue
                        # skip over
                    elif card.ethereal:
                        # if its ethereal
                        self.exhaust_pile.append(card)
                        # Exhaust the card
                        self.if_card_cond(card, 'Exhaust')
                        # Activate Exhausted effects
                    else:
                        self.discard_pile.append(card)
                        # Discard the card
                        self.if_card_cond(card, 'Discarded')
                        # Activate discarded effects
                    self.hand.remove(card)
                    # removes the card from hand
                if self.selected:
                    # If cards were selected to be retained
                    self.hand.extend(self.selected)
                    # Add them back to hand
                    self.selected.clear()
                    # empty selected
        
    def discover(self, cards, cost):
        '''Ask user to add to hand one of the 3 cards given
        
        ### args:
            cards: A list of 3 cards to choose from
            cost: cost modifications to the cards
        '''
        self.hard_card_select(1, cards)
        # Select 1 card from the list
        if self.hand:
            if len(self.hand) == 10:
                # If the player is at hand size
                self.discard_pile.append(self.selected)
                self.selected.clear()
                # Add to discard pile
            else:
                self.hand.append(self.selected)
                self.selected.clear()
                # Add to hand instead
        else:
            self.hand.append(self.selected)
            self.selected.clear()
            # Add to hand instead
        if cost != 'na':
            # If the cost needs to be modified
            self.hand[-1].cost_change(cost, 'Turn')
            # Change the cost until end of turn

    def upgrade(self, cards):
        '''Method to upgrade cards temporily for the combat
        
        ### args:
            cards: a list of cards to upgrade
        '''
        if cards:
            # If there are cards to be upgraded
            for card in cards:
                # go through every card
                card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
                # upgrade the card by making its id and effects of the card 100 higher

    def enemy_action(self):
        '''Execute all enemy actions
        '''
        for enemy in self.enemies:
            # Go through every enemy
            if enemy.intent[0]:
                # If the enemy has an intent
                context = {
                    # Default info to pass on for executing effects
                    'user': enemy, # The enemy doing the action
                    'enemies': self.enemies, # List of enemies
                    'target': enemy.intent[1] # the target of the card, This is mainly the one that gets overrided
                }
                for effect, details in enemy.intent[0].items():
                    effect(*details, context, self)
                # Execute the ffects

    def summon_enemies(self, enemies: list):
        '''Method for adding more enemies to the combat session
        
        ### args:
            enemies: A list of new enemy objects to be added
        '''

    def split(self, slime_type, hp):
        '''Method for larger slimes splitting when they hit half health
        
        ### args: 
            slime_type: the type of slime that is splitting
            hp: health of the slimes the bigger slime split into
        '''
        if slime_type == 'Slime Boss':
            # if the slime boss is splitting
            enemies = [enemy_data.LargeBlueSlime(hp), enemy_data.LargeGreenSlime(hp)]
            self.enemies.extend(enemies)
            # Add 2 smaller slimes of the each type with the current hp of the bigger slime
        elif slime_type == 'Blue':
            # If a large Blue slime is splitting
            enemies = [enemy_data.MediumBlueSlime(hp), enemy_data.MediumBlueSlime(hp)]
            self.enemies.extend(enemies)
            # Add 2 smaller slimes of the same type with the current hp of the bigger slime
        elif slime_type == 'Green':
            # If a large green slime is splitting
            enemies = [enemy_data.MediumGreenSlime(hp), enemy_data.MediumGreenSlime(hp)]
            self.enemies.extend(enemies)
            # Add 2 smaller slimes of the same type with the current hp of the bigger slime
        else:
            raise ValueError(f'Unknown slime type {slime_type}')