import enemy_data
import card_data
import card_constructor
import effects
import random

class Combat:
    def __init__(self, run, player, deck, enemies, combat_type):
        self.run = run # The current run
        self.player = player # The Player, can also be accessed through run but this is here for ease of use
        self.enemies = enemies # The Enemies in a combat encounter
        self.deck = deck # The player's deck
        self.combat_type = combat_type # The Type of combat, (Normal, Elite, Boss)
        self.turn = 0 # Turn counter
        self.start_of_combat = True # Whether its the start of combat
        self.draw_pile = deck # Draw pile
        self.cards_played = 0 # num of cards played
        self.hand = [] # Cards in hand
        self.selected = [] # Selected cards
        self.discard_pile = [] # Discard pile
        self.exhaust_pile = [] # Exhaust pile
        self.playing = None # The card being played
        self.energy_cap = 10 # Energy gained at the start of the turn
        self.energy = 0 # Current energy
        self.retain = 0 # num of cards to keep at the end of the turn
        self.can_play_card = True # If the player can play cards
        self.combat_active = True # Whether the player is in this combat
        self.powers = [] # The powers the player has gained
        self.card_type_played = {}
        self.enemy_turn = False
        self.escaped = False
        self.necroed = True
    
    def combat_start(self):
        '''Method for starting combat'''
        if self.combat_type == 'Elite':
            if self.player.relics:
                for relic in self.player.relics:
                    relic.combatActionEff('Elite Start', self)
        if self.run.mechanics['Insect'] == True and self.combat_type == 'Elite':
            for enemy in self.enemies:
                enemy.hp = int(enemy.hp * 0.75)
        # check for preserved insect condition
        innate_or_bottled = []
        for card in reversed(self.draw_pile):
            if card.innate == True or card.bottled == True:
                innate_or_bottled.append(card)
                self.draw_pile.remove(card)
        random.shuffle(self.draw_pile)
        random.shuffle(innate_or_bottled)
        self.draw_pile.extend(innate_or_bottled)
        innate_or_bottled = []
        # put all innate and bottled cards at the top of the draw pile
        self.player_turn_start()

    def counter_reset(self):
        '''Method for resetting turn counters'''
        if self.player.relics:
            for relic in self.player.relics:
                if relic.counter != None:
                    if relic.counter_type != 'global':
                        relic.counter = 0

    def bonusEff(self, event):
        if self.player.relics:
            for relic in self.player.relics:
                # Go through all relics
                relic.eventBonus(event, self.run)
                # Execute condisional effects of relics

    def passive_check_and_exe(self, cond: str):
        '''Method to check if a power's condition or relic's condition is met and activates its effect if it is

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
                if 'Power' in card.effect and card.effect['Power'] != None:
                    # The power effect in a card
                    for power_cond, effect in card.effect['Power'].items():
                        # for every condition and effect
                        if cond == power_cond: # If the condition is met
                            for effects, effect_details in effect.items():
                                effects(*effect_details, context, self)
                                # Execute the power's effect
        if self.player.relics:
            for relic in self.player.relics:
                # Go through all relics
                relic.combatActionEff(cond)
                # Execute condisional effects of relics

    def get_energy_cap(self):
        '''Gets the energy cap of the player
        '''
        for relic in self.player.relics:
            # Goes throught every relic
            if relic.energy_relic == True:
                # If its an energy relic
                if relic.energy_relic != 'Elite':
                    self.energy_cap += 1
                else:
                    if self.combat_type == 'Elite':
                        self.energy_cap += 1
                # Add 1 energy to the cap if its a normal energy relic and add 1 for slavers collar in elites

    def curse_count(self):
        '''Counts the number of curses in play'''
        curse = 0
        if self.draw_pile:
            for card in self.draw_pile:
                if card.type == 4:
                    curse += 1
        if self.discard_pile:
            for card in self.discard_pile:
                if card.type == 4:
                    curse += 1
        if self.hand:
            for card in self.hand:
                if card.type == 4:
                    curse += 1
        if self.exhaust_pile:
            for card in self.exhaust_pile:
                if card.type == 4:
                    curse += 1
        return curse
        # counts the number of curses in play
    
    def enemy_targeting(self, context, target_code):
        '''Retrieves the target of a enemies based on the target code

        ### args:
            target_code (int): An int corresponding to a specific target or targets
        '''
        if target_code == None:
            return None
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

    def player_targeting(self, context, target_code):
        '''Retrieves the target of a card based on the cards target code

        ### args:
            target_code (int): An int corresponding to a specific target or targets
        '''
        if target_code == None:
            return None
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

    def add_card_to_pile(self, location, card_id, location_name, cost):
        '''adds a certain card to a certain pile

        ### args: 
            loctaion (int): represents which pile to add the card, 0 = hand, 1 = draw pile, 2 = discard pile. 3 = exhaust pile
            card (object): An object that represents the card
        '''
        card = card_constructor.create_card(card_id, card_data.card_info[card_id])
        # Creates a card object using methods in card_constructor and data in card_data
        if cost != 'na':
            # If a cost change is needed
            card.cost_change(*cost)
            # Modifies the cards cost
        if location_name == 'draw':
            if self.draw_pile:
            # If its the draw pile, insert is somewhere random
                location.insert(random.randint(0, len(location) - 1), card)
            else:
                location.append(card)
        else:
            # If its anywhere else adding it to the top works
            location.append(card)
    
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
                self.discard_pile[:] = []
                # Empty the discard pile
        else:
            if self.discard_pile:
                # If the discard pile is not empty
                self.draw_pile.extend(self.discard_pile)
                # Make the draw pile the discard pile
                random.shuffle(self.draw_pile)
                # Shuffle the draw pile
                self.discard_pile[:] = []
                # Empty the discard pile
        self.passive_check_and_exe('Shuffle')
            # Active the relic effects with the event being shuffling

    def draw(self, num: int):
        '''Method for drawing cards during combat
        
        ### args:
            num (int): The number of cards that needs to be drawn
        '''
        while num > 0: # While drawing still needs to be done
            if self.hand:
                if len(self.hand) == 10: 
                    # If the hand is full
                    num -= 1
                    # One less card to draw
                    continue
                    # To the next iteration
            if not self.draw_pile:
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
                if self.player.debuffs['Chaotic'] > 0:
                    self.hand[-1].chaos()
                # If the player is chaotic, randomize the cost of drawn cards
                if self.hand[-1].effect:
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
                if self.hand[-1].type in {3, 4}:
                    # If the card drawn is a negative card
                    self.passive_check_and_exe('Draw Negative')
                    # Check for effects
                    if self.hand[-1].type == 3:
                        self.passive_check_and_exe('Draw Status')
                    elif self.hand[-1].type == 4:
                        self.passive_check_and_exe('Draw Curse')
                    # If they drew a status or a curse and check for effects
                num -= 1
                # One less card to draw
    
    def soft_card_select(self, num : int, pile : list): # Needs to be changed to match hard card select
        '''A soft card select refers to when the game needs the player to select up to x amount of cards but can choose to select below x amount of cards or none at all
        
        ### args:
            num (int): Number of cards that needs to be selected
            pile (list): The place the player needs to select from

        ### Returns:
            Number of cards selected (If more than 1) or the type of card selected (If 1 card was selected) or None (No cards were selected)
            '''
        cards_selected = []
        if not pile:
            # If the pile to select from is empty
            return None
        else:
            confirm = True
            # Initialize confirm selection boolean
            while confirm:
                # While the player hasn't confirmed yet
                if pile:
                    i = 0
                    # If the pile to select from isn't empty
                    for card in pile:
                        # Prints all cards in the pile with relevent detail
                        print(f'{i}: {card}')
                        i += 1
                if cards_selected:
                    # If there has been cards already selected
                    print('selected: ')
                    print(cards_selected)
                select = input(f"Enter the index of the card u wish to select or unselect by typing the index and cs to confirm choices, you can selected up to {num} cards.")
                # Request for player input
                if select != 'cs' and 'r' not in select:
                    # Select another card
                    select = int(select)
                    if pile[select] in self.selected:
                        # Card is already selected
                        self.selected.remove(pile[select])
                        cards_selected.remove(select)
                        # Unselected the card
                    elif len(self.selected) == num:
                        # If they already selected the max num of cards
                        continue
                        # Do nothing
                    else:
                        self.selected.append(pile[select])
                        cards_selected.append(select)
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
        selected_cards = []
        if not pile:
            # If the pile to select from is empty
            return None
            # Doesn't select anything
        elif len(pile) <= num:
            # If the # of cards in pile is equal to or less then the # of cards that needs to be selected
            self.selected.extend(pile)
            # Add all cards in pile to selected
            pile[:] = []
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
                i = 0
                if pile:
                    # If the pile to select from isn't empty
                    for card in pile:
                        # Prints all cards in the pile with relevent detail
                        print(f'{i}: {card}')
                        i += 1
                if selected_cards:
                    # If there has been cards already selected
                    print('selected: ')
                    print(selected_cards)
                    # Prints the indexes of all selected cards
                select = input("Enter the index of the card u wish to select or unselect and cs to confirm choices")
                # Request for player input
                if select != 'cs':
                    # Select another card
                    select = int(select)
                    if pile[int(select)] in self.selected:
                        # Card is already selected
                        self.selected.remove(pile[select])
                        selected_cards.remove(select)
                        # Unselected the card
                    elif len(self.selected) == num:
                        # If they already selected the max num of cards
                        continue
                        # Do nothing
                    else:
                        self.selected.append(pile[select])
                        selected_cards.append(select)
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
            self.selected[:] = []
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
                        self.selected[:] = []
                        # Empty selected cards
                        break
                        # Exit the loop
                # Place them in the hand
                self.draw_pile.extend(eligible_cards)
                # Read the cards back to the draw pile
                random.shuffle(self.draw_pile)
                # Shuffle the draw pile
                eligible_cards = []
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
                    self.passive_check_and_exe('Exhaust')
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
                    self.passive_check_and_exe('Exhaust')
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
                    self.passive_check_and_exe('Exhaust')
    
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
            for card in reversed(self.selected):
                # Go through every selected card
                self.if_card_cond(card, 'Exhausted')
                self.exhaust_pile.append(card)
                self.selected.remove(card)
                # Exhaust all selected cards
                self.passive_check_and_exe('Exhaust')
                # check for effects
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
        self.energy = max(0, self.energy + amount)
        # Adds amount to energy, if energy becomes negative, becomes 0 instead

    def gold_gain(self, amount: int):
        '''Method for player gaining gold in the middle of combat
        
        ### args:
            amount: amount of gold gained'''
        self.run.gold_modification(amount)

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
                if self.run.mechanics['Cards_per_Turn'] != False:
                    # Checks for if there is a cards per turn limit set
                    if self.cards_played < self.run.mechanics['Cards_per_Turn']:
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
        if self.player.died == True:
            self.combat_active = False
        # Checks if the player has died and end sthe combat if so

    def havoc(self, num: int, special: bool):
        '''Havoc referrs to playing the top card of the draw pile, this Method will do that action a number of times
        
        ### args:
            num: Number of times to havoc
            special: true or false to represent whether to exhaust the card played this way'''
        for i in range(0, num):
            # Iterate a certain amount of times
            if self.draw_pile:
                # If there are cards in the draw pile
                holding = None
                # Initialize holding
                if self.playing:
                    holding = self.playing
                # temporily holds the current playing card
                self.playing = self.draw_pile[-1]
                # Make the top card the card being played
                self.draw_pile.pop(-1)
                # Remove the top card of the draw pile
                if special == True:
                    # If the played card needs to be exhausted
                    self.playing.exhaust = True
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
                context['target'] = self.player_targeting(context, 2)
                self.play_card(context)
                # Play the card
                if holding:
                    self.playing = holding
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
                    self.passive_check_and_exe('Exhaust')
        return cards_exhausted_type
        # Returns the list of types of all the cards exhausted, used for executing conditional effects on certain cards
    
    def escape(self):
        '''Method for ending combat without killing all enemies'''
        if self.combat_type != 'Boss':
            self.player.thieved = 0
            self.escaped = True
            self.combat_active = False
        else:
            print('You cannot escape from boss combats!')
        # Escape from non boss combats

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
                self.passive_check_and_exe('Exhaust')
                # Check for effects

    def play_card(self, override = None):
        '''Method used for playing cards in combat

        ### args:
            overide: A dictionary of information that is passed on to execute effects, only inputted if some info needs to be overrided to not be the default
        '''
        lethal_check = len(self.enemies)
        context = {
            # Default info to pass on for executing effects
            'user': self.player, # The player is playing the card
            'enemies': self.enemies, # List of enemies
            'draw': self.draw_pile, # The draw pile
            'discard': self.discard_pile, # The discard pile
            'hand': self.hand, # the hand
            'exhaust': self.exhaust_pile, # The exhaust pile
            'target': None # the target of the card, This is mainly the one that gets overrided
        }
        context['target'] = self.player_targeting(context, self.playing.target)
        if override: # If there is an override
            context = override # Use the override instead
        # Context used for certain effects such as attacking where getting buffs is needed
        if self.can_play_card == False:
            self.discard_pile.append(self.playing)
            # Add the card to the discard pile
        elif self.playing.cost == 'U':
            # If the card being played is Unplayable
            if self.playing.type == 3 and self.run.mechanics['Playable_Status']:
                # If the type of card is a status and the mechanic Playable_Status is activated
                self.exhaust_pile.append(self.playing)
                # Add the card to the exhaust pile
                self.playing = None
                # Empty the playing card
                self.passive_check_and_exe('Exhaust')
                # Check for effects
            elif self.playing.type == 4 and self.run.mechanics['Playable_Curse']:
                # If the type of card is a Curse and the mechanic Playable_Curse is activated
                effects.lose_hp(1, context, self)
                # Execute the effect for playing a curse
                self.exhaust_pile.append(self.playing)
                # Add the card to the exhaust pile
                self.passive_check_and_exe('Exhaust')
                # Check for effects
            else:
                self.discard_pile.append(self.playing)
                # Does nothing
        elif self.playing.cost == 'X':
            # If you are playing an X cost card (A card that spends all you energy and has effects scale off of energy spent)
            self.playing.play_x_cost(self.energy + self.run.mechanics['X_Bonus'])
            # Aquire the complete details of the effect being executed
            times = 1
            if self.necroed == True and self.run.mechanics['Necro'] == True and self.playing.type == 0:
                self.necroed = False
                times = 2
            for i in range(0, times):
                for effect, details in self.playing.x_cost_effect.items():
                    effect(*details, context, self)
                # Execute the X cost effect
            if self.playing.exhaust == True:
                rng = random.randint(1, 100)
                if rng <= self.run.mechanics['Exhaust Chance']:
                    # If the card exhausts
                    self.exhaust_pile.append(self.playing)
                    # Add the card to the exhaust pile 
                    self.if_card_cond(self.playing, 'Exhausted')
                    # Execute Exhausted effects
                    self.passive_check_and_exe('Exhaust')
                    # Check for effects
                else:
                    self.discard_pile.append(self.playing)
                    # Discard instead
            else:
                self.discard_pile.append(self.playing)
                # Add the card to the discard pile
        else: 
            if self.playing.effect:
                # If the card has an effect
                times = 1
                if self.necroed == True and self.run.mechanics['Necro'] == True and self.playing.type == 0:
                    self.necroed = False
                    times = 2
                for i in range(0, times):
                    for effect, details in self.playing.effect.items():
                        # Iterates through every effect
                        if not isinstance(effect, str):
                            effect(*details, context, self)
                            #  Performs the effects if its not a conditional
            if self.playing.type == 2:
                # If the card played was a power
                if 'Power' in self.playing.effect:
                    # If the power card played has an actual effect that isn't just giving an normal buff
                    self.powers.append(self.playing)
                    # Add the card played to the player powers
                    if f'{self.playing.name}' in self.player.buffs:
                        # If the power has been recorded in buffs
                        self.player.buffs[f'{self.playing.name}'] += 1
                        # add 1 for the player to see
                    else:
                        self.player.buffs[f'{self.playing.name}'] = 1
                        # Record that a power was played so the player knows what powers they have active
            elif self.playing.exhaust == True:
                rng = random.randint(1, 100)
                if rng <= self.run.mechanics['Exhaust Chance']:
                    # If the card exhausts
                    self.exhaust_pile.append(self.playing)
                    # Add the card to the exhaust pile 
                    self.if_card_cond(self.playing, 'Exhausted')
                    # Execute Exhausted effects
                    self.passive_check_and_exe('Exhaust')
                    # Check for effects
                else:
                    self.discard_pile.append(self.playing)
                    # Discard instead
            else:
                self.discard_pile.append(self.playing)
                # Add the card to the discard pile
        if self.playing.combat_cost[1] == 'Played':
            self.playing.combat_cost = (None, None)
        # Update cost of cards after being played
        self.resolve_action()
        if self.playing.type == 0:
            self.passive_check_and_exe('Attack Played')
            if lethal_check > len(self.enemies):
                self.passive_check_and_exe('Lethal')
        elif self.playing.type == 1:
            self.passive_check_and_exe('Skill Played')
        elif self.playing.type == 2:
            self.passive_check_and_exe('Power Played')
        elif self.playing.type == 3:
            self.passive_check_and_exe('Status Played')
        elif self.playing.type == 4:
            self.passive_check_and_exe('Curse Played')
        else:
            raise TypeError(f'Card type not found: {self.playing.type}')
        # Check for effects that occur when certain types of cards are played
        self.playing = None
        # Empty the currently playing card
        self.cards_played += 1
        # Increase the amount of cards played by 1
        self.passive_check_and_exe('Card Played')
        if self.hand:
            # if there are cards in hand
            for card in self.hand:
                # for all cards in hand
                self.if_card_cond(card, 'Card Played')
                # Execute effects for if a card is played
                self.resolve_action()
                # Resolve effects
    
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
            i = 1
            if self.player.relics:
                for relic in self.player.relics:
                    if relic.effect_type == 'Sacred Bark':
                        i = 2
                        break
            for times in range(0, i):
                for effect, details in potion.effect.items():
                    effect(*details, context, self)
                # Execute effects
            self.bonusEff('Used Potion')
            self.player.potions.remove(potion)
            # Remove the potion from combat and the player object
        elif potion.time_of_use == 'all':
            self.player.use_potion(potion)
            # Use potion using player method
        else:
            print(f'Invalid time of use: {potion.time_of_use}')
            # Invalid time of use

    def player_turn_start(self):
        '''Method for doing everything that needs to be done at the start of combat'''
        self.necroed = True
        self.enemy_turn = False
        # Player turn starts
        self.can_play_card = True
        # Set the ability to play cards to be true
        self.card_type_played = {}
        # Reset the card types that were played
        self.energy = 0
        # Set energy to 0
        self.turn += 1
        # Increase turn counter
        if self.player.relics:
            for relic in self.player.relics:
                relic.turnEff(self)
        # Execute effects for specific turns
        self.cards_played = 0
        # Set cards played to 0
        if not self.run.mechanics['Block_Loss']:
            self.player.block = 0
        else:
            self.player.block = max(0, self.player.block - self.run.mechanics['Block_Loss'])
        # Lose all block at the start of turn
        self.passive_check_and_exe('Turn Start')
        if self.start_of_combat == True:
            # If its the start of combat
            self.get_energy_cap()
            # Retrieve the enery cap for this combat
            self.passive_check_and_exe('Combat Start')
            # Execute start of combat effects of passives
        self.energy += self.energy_cap
        # Add energy cap to energy
        self.energy += self.player.buffs['Energized']
        self.player.buffs['Energized'] == 0
        # Add extra energy equal to energized
        self.draw(5 + self.player.buffs['Draw Card'] - self.player.debuffs['Draw Reduction'])
        # Draw 5 cards for the start of turn, modified depending on buffs and debuffs that affect draw
        self.player.buffs['Draw Card'] = 0
        # Said buff resets
        self.player.debuffs['Draw Reduction'] = 0
        # Said debuff resets
        # Check for powers that activate at the start of a turn
        self.display_intent()
        self.player_turn()
    # Not completed

    def display_intent(self):
        '''Method for displating all enemy intents to the player'''
        if self.run.mechanics['Intent'] == True:
            # If intents are enabled
            for enemy in self.enemies:
                # for every enemy
                if enemy.intent == None:
                    # If the intent has not been determained yet
                    enemy.intent_get(self)
                    # Determain intent
                print(enemy.combat_info())
                # Print enemy information
        else:
            for enemy in self.enemies:
                # for every enemy
                if enemy.intent == None:
                    # If the intent has not been determained yet
                    enemy.intent_get(self)
                    # Determain intent
                print(enemy)
                # Print enemy information without intent

    def player_turn(self):
        '''Execute actions the player does during their turn'''
        turn = True
        # Set turn to true
        while turn:
            if self.draw_pile:
                print('Draw Pile:')
                for card in self.draw_pile:
                    print(card.name)
            if self.discard_pile:
                print('Discard Pile:')
                for card in self.discard_pile:
                    print(card.name)
            if self.exhaust_pile:
                print('Exhaust Pile:')
                for card in self.exhaust_pile:
                    print(card.name)
            # While its still the player's turn
            print(self.player.combat_info())
            # print player info
            if self.hand:
                # If there are cards in hand
                i = 0
                for card in self.hand:
                    # For every card in hand
                    print(f'{i}: {card}')
                    i += 1
                    # Print details of card
            player_action = input(f'Enter the index of the card you wish to play or P# with # being index of the potion being used or END for end turn. You have {self.energy} energy left.')
            # Asks player for input on what to do
            if player_action == 'END':
                # If the player wants to end the turn
                turn = False
                # Turn to false
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
                    if cost == 'U':
                        if (self.run.mechanics['Playable_Curse'] == True and card.type == 4) or (self.run.mechanics['Playable_Status'] == True and card.type == 3):
                            # If its an unplayble card but the mechanics permit it
                            self.playing = card
                            self.hand.remove(card)
                            self.play_card()
                            # play the card
                            self.energy -= cost
                        else:
                            print('Card is Unplayable')
                            # If the card is unplayable
                    elif cost > self.energy:
                        # If the cost is higher then the energy the player has
                        print('Not enought energy')
                        # Gives feedback
                        continue
                    else:
                        # Hold the updated energy
                        self.playing = card
                        self.hand.remove(card)
                        self.play_card()
                        # play the card
                        self.energy -= cost
                        # Update energy
                else: 
                    # For potions
                    player_action = int(player_action[1])
                    # Gets the index of the potion being used
                    potion = self.player.potions[player_action]
                    # Retreives the correct potion
                    self.use_potion(potion) 
                    # Use the potion
            self.resolve_action()
            self.display_intent()
            # Display enemy intents
            # Resolve actions
        self.player_turn_end()

    def player_turn_end(self):
        '''Executes actions of the player's turn ending'''
        self.passive_check_and_exe('Turn End')
        # Execute all end of turn passives
        if self.player.debuffs['Vulnerable'] > 0:
            self.player.debuffs['Vulnerable'] -= 1
        if self.player.debuffs['Weak'] > 0:
            self.player.debuffs['Weak'] -= 1
        if self.player.debuffs['Frail'] > 0:
            self.player.debuffs['Frail'] -= 1
        # Lower some debuff counters by 1
        if self.player.debuffs['Last Chance'] > 0:
            self.exhaust_entire_pile(self.hand)
            self.exhaust_entire_pile(self.discard_pile)
            self.exhaust_entire_pile(self.draw_pile)
            self.player.debuffs['Last Chance'] = 0
        self.power_check_and_exe('Turn End')
        if self.hand:
            # If the hand isn't empty
            for card in reversed(self.hand):
                # Go through every card
                self.if_card_cond(card, 'Turn End')
                # Execute turn end effects
                if card.combat_cost[1] == 'Turn':
                    card.combat_cost == (None, None)
                # update card costs
            if self.run.mechanics['turn_end_discard']:
                # Check if the player needs to discard their hand
                if self.retain > 0:
                    self.soft_card_select(self.retain, self.hand)
                self.retain = 0
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
                        self.passive_check_and_exe('Exhaust')
                        # Check for effects
                    else:
                        self.discard_pile.append(card)
                        # Discard the card
                    self.hand.remove(card)
                    # removes the card from hand
                if self.selected:
                    # If cards were selected to be retained
                    self.hand.extend(self.selected)
                    # Add them back to hand
                    self.selected[:] = []
                    # empty selected
        if self.player.debuffs['Chained'] > 0:
            self.player.lose_buff('Strength', self.player.debuffs['Chained'])
            self.player.debuffs['Chained'] = 0
        # Chained effect
        self.counter_reset()
        self.enemy_turn_start()
        
    def discover(self, cards, cost):
        '''Ask user to add to hand one of the 3 cards given
        
        ### args:
            cards: A list of 3 cards to choose from
            cost: cost modifications to the cards
        '''
        for i in range(0, 3):
            cards[i] = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
        self.hard_card_select(1, cards)
        # Select 1 card from the list
        if self.hand:
            if len(self.hand) == 10:
                # If the player is at hand size
                self.discard_pile.append(self.selected)
                self.selected[:] = []
                # Add to discard pile
            else:
                self.hand.append(self.selected)
                self.selected[:] = []
                # Add to hand instead
        else:
            self.hand.append(self.selected)
            self.selected[:] = []
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
                if card.id + 100 in card_data.card_info:
                    # If a card can be upgraded
                    card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
                # upgrade the card by making its id and effects of the card 100 higher

    def enemy_turn_start(self):
        '''Method for the enemy turn starting'''
        self.enemy_turn = True
        for enemy in self.enemies:
            # For every enemy
            enemy.turn_start()
            # Execute the start of turn method
        self.enemy_action()

    def enemy_turn_end(self):
        '''Method for ending enemy's turn'''
        for enemy in self.enemies:
            # For every enemy
            enemy.turn_end()
            # Execute the end of turn method
        self.player_turn_start()

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
                    'target': enemy.intent[1], # the target of the card, This is mainly the one that gets overrided
                    'draw': self.draw_pile,
                    'discard': self.discard_pile,
                    'hand': self.hand,
                    'exhaust': self.exhaust_pile
                }
                if enemy.intent[0] != None:
                    for effect, details in enemy.intent[0].items():
                        effect(*details, context, self)
                # Execute the ffects
            enemy.intent = None
            # Clear intent
        self.resolve_action()
        # Resolves action
        self.enemy_turn_end()

    def bandit_run(self, context):
        '''Method for a bandit escape
        
        ### args:
        context: info related to the user and state of game'''
        self.player.thieved -= context['user'].buffs['Stolen']
        self.enemies.remove(context['user'])
        # Update info related to stolen gold and remove the escaping enemy

    def summon_enemies(self, enemies: list):
        '''Method for adding more enemies to the combat session
        
        ### args:
            enemies: A list of new enemy objects to be added
        '''
        return # Placeholder

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