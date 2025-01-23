import card_constructor
import math
import random
import pygame

def deal_attack_damage(damage, times : int, context, combat):
    '''Repsonsable for card effects that deal attack danage

    ### args:
        damage: an integer representing base damage
        times: How many instances of the damage is dealt
        targets: A list of objects or single object representing the targets
        context: Information related to the current combat 
        combat: The current combat
    
    ### Returns: 
        attack_damage_dealt: Unblocked damage dealt by this effect
    '''
    attack_damage_dealt = 0
    # Initialize damage dealth variable
    actualDamage = 0
    # Initialize actual damage for damage calcs
    if not isinstance(damage, int):
        # If the damage isn't a number
        if damage == 'block':
            damage = context['user'].block
            # Execute start of combat effects of relics
        else:
            raise ValueError(f'Unknown damage value {damage}')
            # Invalid damage value error foe bebugging
    actualDamage = damage + context['user'].buffs['Strength'] + context['user'].buffs['Vigour']
    # Add user's buffs
    context['user'].buffs['Vigour'] = 0
    actualDamage = actualDamage - context['user'].debuffs['-Strength']
    if context['user'].debuffs['Weak'] > 0:
        actualDamage = int(actualDamage * 0.75)
    # Damage Calcs
    actualDamage = max(actualDamage, 0)
    targets = []
    if isinstance(context['target'], int):
        targets = combat.enemy_targeting(context, context['target'])
    else:
        targets = context['target']
    for i in range(0, times):
        for target in targets:
            attack_damage_dealt += target.damage_taken(actualDamage)
            # Deals damage to targets and saves damage dealt
            if target.buffs['Thorns'] > 0:
            # If the enemy has thorns
                context['user'].true_damage_taken(target.buffs['Thorns'])
                # Take damage equal to throns of the attacked
            if 'Parry' in target.buffs:
                if target.buffs['Parry'] > 0:
                # If the target has parry
                    context['user'].gain_debuff('Vulnerable', target.buffs['Parry'])
                    # Attacker gets applied 1 Vuln for every parry
            if 'Deflect' in target.buffs:
                if target.buffs['Deflect'] > 0:
                    # If the target has deflect
                    context['user'].true_damage_taken(target.buffs['Deflect'])
                    # Attacker takes damage for every stack of deflect
        mouse_pos = pygame.mouse.get_pos()
        combat.combat_surface.fill((30, 30, 30))
        combat.combat_surface.blit(combat.background_sprite, (0, 0))
        combat.update_game_state(mouse_pos)
        combat.draw_game_state(mouse_pos)
        combat.screen.blit(combat.combat_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)
    return attack_damage_dealt
    # Used for certain effects

def deal_damage(damage, context, combat):
    '''Repsonsable for card effects that deal damage

    ### args:
        damage: an integer representing damage
        context: Information related to the current combat 
        combat: The current combat
    '''
    # Gets the target of the effect
    targets = []
    if isinstance(context['target'], int):
        targets = combat.enemy_targeting(context, context['target'])
    else:
        targets = context['target']
    for entity in targets:
        entity.true_damage_taken(damage)
        # Deal the damage to all targets

def feed(damage : int, max_hp_increase : int, context, combat):
    '''Special attacks that increase the user's max hp if they dealt lethal damage

    ### args:
        damage: an integer representing base damage
        max_hp_increase: the amount to increase max hp by if succesful
        context: Information related to the current combat 
        combat: The current combat
    '''
    num_of_enemes = len(combat.enemies)
    # Aquire the number of enemies before the attack
    deal_attack_damage(damage, 1, context, combat)
    # Attack the enemy
    if len(combat.enemies) < num_of_enemes:
        # If the number of enemies decreases
        context['user'].maxHp += max_hp_increase
        context['user'].Hp += max_hp_increase
        # Increase the user's max hp

def reap(damage : int, context, combat):
    '''Special attacks that heals the user based on damage dealt

    ### args:
        damage: an integer representing base damage
        context: Information related to the current combat 
        combat: The current combat
    '''
    hp_recover = deal_attack_damage(damage, 1, context, combat)
    # Attack the enemy
    context['user'].hp_recovery(hp_recover)
    # Heal hp equal to the amount of unblocked damage dealt

def block_gain_card(block, times : int, context, combat):
    '''Effect used for cards that gives block to the user
    
    ### args: 
        block: The amount of block being gained
        times: how many times the block is being gained
        context: Information related to the current combat 
        combat: The current combat
    '''
    for i in range(0, times):
        context['user'].gain_block_card(block)
        # Grants the user block

def block_gain_power(block, context, combat):
    ''' Non card effects that grant block
    
    ### args: 
        block: The amount of block being gained
        context: Information related to the current combat 
        combat: The current combat
    '''
    context['user'].gain_block_power(block)
    # grants the user block

def rob(context, combat):
    '''Function for robbing the player of gold
    
    ### args:
        context: Info related to the user and combat
        combat: combat session currently'''
    gold_stolen = min(combat.player.gold, context['user'].buffs['Thievery'])
    combat.player.gold -= gold_stolen
    combat.player.thieved += gold_stolen
    context['user'].buffs['Stolen'] += gold_stolen
    # Steal gold from the player

def enemy_block_gain(block, context, combat):
    '''Gaining block for enemies
    
    ### args:
        block: the amount of block being gained
        context: Information related to targets
        combat: The current combat session
    '''
    # Aquire targets
    targets = 0
    if context['target'] not in {2, 3}:
        targets = [context['user']]
    else:
        targets = combat.enemy_targeting(context, context['target'])
    for entity in targets:
        # Loop through all targets
        entity.gain_block(block)
        # Give them block

def apply_buff(buffs: list, amount: list, context, combat):
    '''Grants a buff to the target
    
    ### args: 
        buffs: A list of buffs
        amount: The amount of a certain buff being applied
        context: Information related to the current combat 
        combat: The current combat
    '''
    targets = []
    if isinstance(context['target'], int):
        targets = combat.enemy_targeting(context, context['target'])
    else:
        targets = context['target']
    # Player's target is predetermained
    for entity in targets:
        # Go through all targets
        for i in range(len(buffs)):
            entity.gain_buff(buffs[i], amount[i])
            # Grants the targets the buffs

def apply_debuff(debuffs: list, amount: list, context, combat):
    '''Applies a debuff to the target
    
    ### args: 
        debuffs: A list of debuffs
        amount: The amount of a certain debuff being applied
        context: Information related to the current combat 
        combat: The current combat
    '''
    targets = []
    if isinstance(context['target'], int):
        targets = combat.enemy_targeting(context, context['target'])
    else:
        targets = context['target']
    # Player's target is predetermained
    for entity in targets:
        # Go through all the targets
        for i in range(len(debuffs)):
            entity.gain_debuff(debuffs[i], amount[i])
            # Applies the debuffs to the target

def add_card_to_pile(location: str, card_id, number_of_cards: int, cost, context, combat):
    '''Function that adds a card to a certain location
    
    ### args:
        location: The name of the location the card is being added to
        card_id: Can be the exact id of a card, if not an id, it will be a catagory of card
        number_of_cards: The number of copies a card will be added
        cost: Cost modifications to be done to the added card
        context: Information related to the current combat 
        combat: The current combat

        '''
    if isinstance(card_id, int):
        # If the card_id is a specific card_id
        for i in range(0, number_of_cards):
            combat.add_card_to_pile(context[location], card_id, location, cost)
            # Add the card to the location
    else:
        if card_id in {'atk', 'skill', 'power', 'weak curse', 'average curse', 'strong curse', 'curse', 'status', 'card'}:
            # If card_id is a known card type
            for i in range(0, number_of_cards):
                card = card_constructor.random_card(card_id, context['user'])
                # Constuct a card
                combat.add_card_to_pile(context[location], card, location, cost)
                # Add the card to the correct location
        else:
            raise ValueError(f'Unknown card type {card_id}')
            # An Invalid card type was inputted

def havoc(number_of_cards : int, special : bool, context, combat):
    '''Play the top card of the deck a number of times
    
    ### args: 
        number_of_cards: The number of top decks to do
        special: Whether to exhaust those played cards
        context: Information related to the current combat, unused but still an argument to prevent Type Errors, All future unused context or combat arguments will be for this reason
        combat: The current combat
    '''
    combat.havoc(number_of_cards, special)
    # Use the havoc method in combat to perform this effect

def potion_slot_addition(slots, run):
    addition = []
    for i in range(0, slots):
        addition.append(None)
    run.player.potions.extend(addition)

def entropic(run):
    '''Function for filling all empty potion slots with random potions
    
    ### args:
        player: The player using the effect'''
    empty_slots = run.player.potions.count(None)
    # get number of empty slots
    for i in range(0, empty_slots):
        run.gain_rand_potion()
        # Fill all empty slots

def purity(context, combat):
    '''Function for choosing and exhauting any number of cards from hand
    
    ### args:
        context: combat related info
        combat: Instance of the combat class'''
    if combat.hand:
        combat.soft_card_select(10, combat.hand)
    # Selected as many cards as the player wants in hand
    combat.exhaust_selected()
    # Exhausts all selected card

def smoke_bomb(context, combat):
    '''Function for the smoke bomb potion'''
    combat.escape()
    # Use the escape method in combat

def bandit_escape(context, combat):
    '''Function for bandits escaping combat'''
    combat.bandit_run(context)
    # Use bandit run method in combat

def blood(amount, run):
    '''Function for healing for a percentage of hp
    
    ### args:
        amount: the percentage that needs to be healed
        player: The player using the effect'''
    run.player.heal(amount)
    # heal for the percentage

def gamble(context, combat):
    '''Function for performing a Mulligan in combat'''
    combat.mulligan()
    # Uses the mulligan method in combat

def adapt(num, context, combat):
    '''The adapt power effect
    
    ### args: 
        num: number of cards that the player can exhuast
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.soft_card_select(num, context['hand'])
    # Select an amount of cards
    if combat.exhaust_selected():
        # If a card was exhausted
        block_gain_power(8, context, combat)
        # User gains 8 block

def remove_effect_from_type(card_type, context, combat):
    '''Completly removes the effect from cards of a certain type
    
    ### args: 
        card_type: Tje type of card the effects are being removed from
        context: Information related to the current combat 
        combat: The current combat
    '''
    if combat.hand:
        for card in combat.hand:
            if card.type == card_type:
                card.effect = None
    if combat.draw_pile:
        for card in combat.draw_pile:
            if card.type == card_type:
                card.effect = None
    if combat.discard_pile:
        for card in combat.discard_pile:
            if card.type == card_type:
                card.effect = None
    if combat.exhaust_pile:
        for card in combat.exhaust_pile:
            if card.type == card_type:
                card.effect = None
    # Goes through every pile and every card and removes all effects from the cards of a specific type

def exhaust_discard_curse(num : int, context, combat):
    '''Effect for discarding cards and exhausting curses discarded this way
    
    ### args: 
        num: number of cards being discarded
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.exhaust_discard_curse(num)
    # Uses the method in combat

def exhaust_from_hand(num : int, context, combat):
    '''Effect for choosing and exhausting selected cards from the hand
    
    ### args: 
        num: number of cards being exhausted
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.exhaust_choose_hand(num)
    # Uses method in combat

def exhaust_random_from_hand(num : int, context, combat):
    '''Effect exhausting random cards from the hand
    
    ### args: 
        num: number of cards being exhausted
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.exhaust_random_hand(num)
    # uses method in combat

def lose_hp(amount, context, combat):
    '''Effect for losing HP
    
    ### args: 
        amount: amount of Hp being lost
        context: Information related to the current combat 
        combat: The current combat
    '''
    targets = []
    if isinstance(context['target'], int):
        targets = combat.enemy_targeting(context, context['target'])
    else:
        targets = context['target']
    # Aquire the target using method in combat
    if not isinstance(amount, int):
        # If the amount lost is not a number
        amount = len(context[amount])
        # Retreive the number of cards in a certain place
    for entity in targets:
        entity.hp_loss(amount)
    # All targets lose Hp

def hp_cost(amount, context, combat):
    '''Effect for losing HP
    
    ### args: 
        amount: amount of Hp being lost
        context: Information related to the current combat 
        combat: The current combat
    '''
    context['user'].hp_loss(amount)
    # Make user lose hp

def retain_cards(num : int, context, combat):
    '''Effect retaining more cards in hand at the end of the turn
    
    ### args: 
        num: number of cards being retained
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.retain_cards(num)
    # Uses method in combat

def draw_cards(num : int, context, combat):
    '''Effect for drawing more cards
    
    ### args: 
        num: number of cards being drawn
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.draw(num)
    # Uses method in combat

def double_block(num : int, context, combat):
    '''Effect for doubling the amount of block the user has
    
    ### args: 
        num: number of times to double
        context: Information related to the current combat 
        combat: The current combat
    '''
    for i in range(0, num):
        context['user'].block *= 2
        # Doubles block of the user

def discard_cards(num : int, type : bool, context, combat): 
    '''Effect for discarding cards from the hand
    
    ### args: 
        num: number of cards being discarded
        type: whether the discards are random or selected
        context: Information related to the current combat 
        combat: The current combat
    '''
    if type == 'random':
        # Random discards
        combat.random_discard(num)
    elif type == 'choose':
        # Selective discards
        combat.choose_discard(num)

def place_card_in_loction(start_pos, num, end_pos, cost, context, combat):
    '''Moving a card from one place to another and possibly modifying its cost
    
    ### args: 
        start_pos: Original location of the card
        num: Number of cards to move
        end_pos: Where the cards will end up
        cost: An int if the cost needs to be modified, 'na' if no changes need to be made
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.hard_card_select(num, context[start_pos])
    # Select cards from the starting locations
    combat.place_selected_cards(context[end_pos], cost)
    # Place them in the end location with its correct cost

def card_search(type, num, context, combat):
    '''Effect for searching cards out from the deck
    
    ### args: 
        type: type of card being searched
        num: number of cards being searched
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.search(num, type)
    # uses method from combat

def energy_manip(amount : int, context, combat):
    '''Effect for manipulating energy
    
    ### args: 
        amount: The value the energy is modified by
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.energy_change(amount)
    # Uses method from combat

def card_play_limit(limit, context, combat):
    '''Effect limiting number of cards that can be played
    
    ### args: 
        limit: number of cards that can be played
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.card_limit(limit)
    # Uses method from combat


def modify_effect(effect, modifications, context, combat):
    '''Modifies the effect of a card

    ### args: 
        effect: the effect being modified
        modifications: The changes to the effect
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.playing.modify_effect(effect, modifications)
    # Uses method from combat

def hand_for_card_exhausted(exhaust_card_type: set, card_type_cond: set, cond_effect: list, cond_effect_details: list, context, combat):
    '''Effect for exhausting all cards of a certain type in hand and executing effects if the type of the card matches the condtion
    
    ### args:  
        exhaust_card_type: A set of card type codes representing the cards that are being exhausted
        card_type_cond: The card type that when exhausted will execute the effect
        cond_effect: The effect being executed
        cond_effect_details: The specifics of the effect being executed
        context: Information related to the current combat 
        combat: The current combat
    '''
    cards_exhausted_type = combat.sever(exhaust_card_type)
    # Exhaust all corresponding cards and retrive the types of all the cards exhausted
    if cards_exhausted_type:
        # If a card was exhausted
        for card_type in cards_exhausted_type:
            # for all the card types of the cards exhausted
            if card_type in card_type_cond:
                # If it matches the conditions
                for i in range(0, len(cond_effect)):
                    cond_effect[i](*cond_effect_details[i], context, combat)
                    # Execute the conditional effects

def for_card_type_in_hand(effect, effect_details, card_type: set, context, combat):
    '''Executes an effect a number of times equal to the number of a specific card type in hand
    
    ### args: 
        effect: The effect being executed
        effect_details: The specifics of the effect being executed
        card_type: The card type that is needed
        context: Information related to the current combat 
        combat: The current combat
    '''
    times = 0
    # Initialize times
    if combat.hand:
        # If cards are in hand
        for card in combat.hand:
            # for every card in hand
            if card.type in card_type:
                times += 1
                # if its the correct type, add 1 to times
    for i in range(0, times):
        effect(*effect_details, context, combat)
        # Execute the effect a certain number of times

def final_gambit(x, additional, context, combat):
    '''Effect for the card final gambit
    
    ### args: 
        x: Final gambit is an X cost card, this represents the amount of energy spent on this card
        additional: bonuses added on to X
        context: Information related to the current combat 
        combat: The current combat
    '''
    x = x + additional
    # add additional to x
    if combat.player.debuffs['Last Chance'] == 0:
        # If another final gambit has not been played this turn
        combat.exhaust_entire_pile(context['hand'])
        combat.exhaust_entire_pile(context['draw'])
        combat.exhaust_entire_pile(context['discard'])
        # Exhaust everything
        place_card_in_loction('exhaust', x, 'hand', (0, 'Played'), context, combat)
        # add x cards from the discard pile to the hand and make them cost 0
        apply_debuff(['Last Chance'], [1], context, combat)
    # Apply the Final Gambit debuff to the user
    else:
        energy_manip(x - additional, context, combat)
        # Refund energy back if final gambit has been played already

def combat_gold_gain(amount, context, combat):
    '''Function for gaining gold in combat
    
    ### args:
        amount: the amount of gold to gain
        context: Information related to the current combat 
        combat: The current combat'''
    combat.gold_gain(amount)
    
def card_removal_cost_set(amount, run):
    '''Function for setting the cost of removing a card
    
    ### args:
        amount: the amount of gold to gain
        run: The run object'''
    return amount

def temporal_hiccup(context, combat):
    '''Function for the effect of temporal hiccup
    
    ### args:
        context: Information related to the current combat 
        combat: The current combat'''
    if combat.turn <= 3:
        combat.start_of_combat == True

def no_block_buffer(amount, context, combat):
    '''Function for gaining block at the end of the turn if the player has no block
    
    ### args:
        amount: the amount of block to gain
        context: Information related to the current combat 
        combat: The current combat'''
    if combat.player.block == 0:
        # If the player has no block
        block_gain_power(amount, context, combat)
        # Gain block

def discover(card_type, cost, context, combat):
    '''Function for a discover effect (Select from 3 random cards of a type)
    
    ### args: 
        card_type: The type of cards being discovered
        cost: The cost change if needed
        context: Info related to targets and the user
        combat: The combat session
    '''
    card_list = {}
    # Initialize set of cards to pick from
    if card_type in {'Attack', 'Skill', 'Power'}:
        # If its a type of card
        if context['user'].character_class == 1:
            # If the user is the Class 1
            if card_type == 'Attack':
                # Attack cards
                card_list = set(card_constructor.attack_card_1)
            elif card_type == 'Skill':
                # Skill cards
                card_list = set(card_constructor.skill_card_1)
            elif card_type == 'Power':
                # Power cards
                card_list = set(card_constructor.power_card_1)
            else:
                card_type == 'Card'
                card_list = set(card_constructor.attack_card_1 + card_constructor.skill_card_1 + card_constructor.power_card_1)

    card_list = list(card_list)
    random.shuffle(card_list)
    cards = [card_list[0], card_list[1], card_list[2]]
    # Choose 3 random cards from valid list
    combat.discover(cards, cost)
    # Use method in combat for user to choose one of the three
    # Unfinished

def eventChange(encounter, run):
    '''Function to change the next event
    
    ### args:
        encounter: the event to change to
        run: the run object'''
    run.eventList.append(encounter)

def campfire_change(action: str, run):
    '''Function for changing the campfire action
    
    ### args:
        action: the action to change to
        run: the run object'''
    run.campfire_restrict(action)

def sneko_eye(context, combat):
    if combat.turn in {0, 1}:
        apply_debuff(['Chaotic'], [1], context, combat)
    draw_cards(2, context, combat)

def upgrade(target, context, combat):
    '''Function for upgrading cards in combat
    
    ### args:
        target: the cards to be upgraded
    '''
    if target in {'hand', 'draw', 'discard', 'exhaust'}:
        # If the target is a pile
        combat.upgrade(context[target])
        # Upgrade all cards of that pile
    elif target == 'all':
        combat.upgrade(context['draw'])
        combat.upgrade(context['hand'])
        combat.upgrade(context['discard'])
        combat.upgrade(context['exhaust'])
        # Upgrade all cards
    else:
        combat.hard_card_select(1, context['hand'])
        combat.upgrade(combat.selected)
        combat.hand.append(combat.selected)
        # Choose 1 card in hand and upgrade it

def rand_card_no_cost(context, combat):
    '''Function for changing the cost of a random card in hand to 0
    
    ### args:
        context: Information related to the current combat 
        combat: The current combat'''
    if combat.hand:
        card = random.choice(combat.hand)
        card.cost_change(0, 'Played')

def upgrade_card(cards, run):
    '''Function for upgrading cards prermanatly from effects
    
    ### args:
        cards: The cards being upgraded
        run: The run object'''
    run.player.upgrade_card(cards)
    
def transform_card(cards, run):
    '''Function for transforming cards prermanatly from effects
    
    ### args:
        cards: The cards being transformed
        run: The run object'''
    if cards == 'Basic':
        # If transforming a type of card
        cards = []
        for card in run.player.deck:
            if card.rarity == 0:
                cards.append(card)
        run.player.transform_card(cards)
    else:
        run.player.transform_card(cards)

def remove_card(cards, run):
    '''Function for removing cards permantly from effects
    
    ### args:
        cards: The cards being removed
        run: The run object'''
    run.player.remove_card(cards)

def duplicate_card(card, run):
    '''Function for duplicating cards
    
    ### args:
        cards: The cards being duplicated
        run: The run object'''
    run.player.duplicate_card(card)

def chaos(context, combat):
    '''Function to randomize all costs in hand for the rest of combat
    
    ### args:
        context: Info related to targets and the user
        combat: The combat session'''
    if combat.hand:
        for card in combat.hand:
            card.chaos()

def effect_for_card_type_not_played(card_type: int, effects: list, effect_details: list, context, combat):
    '''Function for executing effects if a certain type of card was not played
    
    ### args:
        card_type: the type of card
        effects: a list of effect funtions
        effect_details: a list of the arguments for the effects
        context: Info related to targets and the user
        combat: The combat session'''
    if card_type not in combat.card_type_played:
        for i in range(0, len(effects)):
            effects[i](*effect_details[i], context, combat)

def egg(type, run):
    '''Function for adding a egg relic'''
    run.egg_relic(type)

def bottle(type, run):
    '''Function for bottled card effects from relics, causes a card to become innate
    
    ### args:
        type: the type of card to be bottled
        run: the run object'''
    if type == 0:
        if card_select(1, {1, 2, 3, 4}, run) != False:
            run.bottle()
    elif type == 1:
        if card_select(1, {0, 2, 3, 4}, run) != False:
            run.bottle()
    elif type == 2:
        if card_select(1, {0, 1, 3, 4}, run) != False:
            run.bottle()
    else:
        raise TypeError(f'Unknown card type_id: {type}')

def card_select(num, restrictions, run):
    '''Function for selecting cards from the deck outside of combat
    
    ### args:
        num: Number of cards that needs selecting
        player: The character object that the player controlls
        restrictions = None: What type of cards can't be selected, none by default'''
    run.card_select(num, restrictions)

def transform_and_upgrade(cards, run):
    run.transform_and_upgrade(cards)

def additonal_rewards(reward_type, amount, additional_rewards):
    '''Function to add additional rewards
    
    ### args:
        rewards: A dictonary that contains the different catagory of rewards
        additional: the amount of additional rewards with the type and amount
    
    ### returns:
        rewards: Updated rewards dictonary'''
    for type in reward_type:
        additional_rewards[type] += amount
    return additional_rewards

def pocket_watch(amount, context, combat):
    context['target'] = [combat.player]
    if combat.cards_played <= 3:
        apply_buff(['Draw Card'], [amount], context, combat)

def potion_chance_mod(mod, run):
    '''Function to modify to the potion chance
    
    ### args:
        mod: The modification
        run: the run object'''

def gain_rand_potion(run):
    run.gain_rand_potion()

def change_next_event(event, run):
    '''Function to change the next random encounter
    
    ### args:
        type: the event to change to
        run: the run object'''
    run.eventList.append(event)

def add_card_to_deck(card_id, run):
    '''Function to call the mathod in run add a card to deck
    
    ### args:
        card_id: id of the card being added
        run: the run object'''
    if isinstance(card_id, int):
        run.card_pickup_from_id(card_id)
    else:
        card_id = card_constructor.random_card(card_id, run.player.character_class)
        run.card_pickup_from_id(card_id)

def heal_player(amount, run):
    '''Function to heal the player from effects
    
    ### args:
        amount: the amount of healing
        run: the run object'''
    run.player.heal(amount)

def eternal_feather(run):
    '''Function for healing the player when they enter a fireplace for every 5 cards they have
    
    ### args:
        run: the run object'''
    amount = len(run.player.deck) // 5
    heal_player(amount, run)

def card_reward_option_mod(mod, run):
    run.card_reward_option_mod(mod)

def generate_rewards(name, run):
    '''Function that generates a reward screen
    
    ### args:
        name: the name of the reward screen
        run: the run object'''
    run.generate_reward_screen_instance(False, name)
    run.reward.listRewards()

def combat_mechanic_change(mechanic, change, run):
    '''Function to call the mathod in run to change the combat mechanic
    
    ### args:
        mechanic: The mechanic that is being changed
        change: the changes that need to be made
        run: the run object'''
    run.mechanics_change(mechanic, change)

def additional_campfire(action, run):
    run.campfire_add_action(action)

def rare_base_chance_mult(amount, run):
    run.rareChanceMult = amount

def meat(run):
    '''Function for the meat on the bone effect'''
    if run.player.maxHp // 2 >= run.player.hp:
        heal_player(12, run)

def combat_heal_player(amount, context, combat):
    '''Function for healing the player in combat
    
    ### args:
        amount: amount of healing
        context: Info related to the combat
        combat: the current combat session
    '''           
    combat.player.hp_recovery(amount)

def split(slime_type, context, combat):
    '''Function for slime splitting into smaller slimes
    
    ### args:
        slime_type: The type of slime splitting
        context: Info related to the combat
        combat: the current combat session
    '''
    hp = context['user'].hp
    # Get hp of the big slime
    combat.enemies.remove_enemy(context['user'])
    # Remove the big slime
    combat.split(slime_type, hp)
    # Use method in combat to add 2 more slimes

def small_damage_reduction(damage, cap, *args): 
    '''Reduces damage small enought to 1
    
    ### args: 
        damage: The amount of damage being dealt
        cap: the maximum the reduction effect can apply
        *args: Avoid value errors
    
    ### Returns: 1 or unchanged damage
    '''
    if damage <= cap and damage > 1:
        # If the damage is below or equal to the cap and above 1
        return 1
        # return 1
    else:
        return damage
        # returns damage unchanged

def gold_gain(amount, run):
    '''Function for gaining gold outseide of combat
    
    ### args:
        amount: the amoung being gained
        run: The run object'''
    run.gold_modification(amount)

def price_discount(price, discount, *args):
    '''Function for discounting the price of a card
    
    ### args:
        price: the price of the card
        discount: the discount to apply
        *args: Avoid value errors'''
    return math.floor(price * discount)

def gold_amount_mod(amount, mod, *args):
    '''Function for modifying the amount of gold
    
    ### args:
        amount: the amount of gold
        mod: the modification
        *args: Avoid value errors'''
    if amount < 0:
        return amount
    return max(0, amount + mod)

def potion_to_nothing(*args):
    '''Function for setting the cost of removing a potion to 0
    
    ### args:
        *args: Avoid value errors'''
    return None

def card_to_nothing(*args):
    '''Function for setting the cost of removing a card to 0
    
    ### args:
        *args: Avoid value errors'''
    return None

def debuff_reduction(amount, reduction, *args):
    '''Function for reducing the amount of debuffs
    
    ### args:
        amount: the amount of debuffs
        reduction: the amount to reduce by
        *args: Avoid value errors'''
    return amount - reduction

def hp_loss_reduction(hp_loss, reduction, *args): # Hp Loss Reduction Effect
    '''Reduces Hp Loss
    
    ### args: 
        hp_loss: The amount of hp being loss
        reduction: The amount to reduce by
        *args: Avoid value errors
    
    ### Returns: 
        The reduced amount
    '''
    return max(0, hp_loss - reduction)
    # Apply reduction

def max_hp_change(amount, run):
    '''Function for gaining max hp from relics or events
    
    ### args:
        amount: amount of max hp gained
        player: the player using the effect'''
    run.player.increase_max_hp(amount)
    # Uses method in player class to perform the action

def revive(max_hp, revive_percentage, *args): # Revive effect
    '''Revives the player when dead
    
    ### args: 
        revive_percentage: The percentage of max hp the player will get after being revived
        max_hp: The player's max Hp
        *args: Avoid value errors
    
    ### Returns: 
        Updated health'''
    return math.floor(max_hp * (revive_percentage / 100))

def healing_reduction(amount, reduction, *args): # Healing reduction effect
    '''Reduces healing

    ### args: 
        amount: The amount of healing
        reduction: The amount to reduce by
        *args: Avoid value errors
    
    ### Returns: 
        The reduced amount
    '''
    return max(amount - reduction, 0)

