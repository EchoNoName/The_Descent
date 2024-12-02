import card_constructor
import math
import random

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
            actualDamage = context['user'].block
            # Execute start of combat effects of relics
        else:
            raise ValueError(f'Unknown damage value {damage}')
            # Invalid damage value error foe bebugging
    actualDamage = damage + context['user'].buffs['Strength'] + context['user'].buffs['Vigour']
    # Add user's buffs
    actualDamage = actualDamage - context['user'].debuffs['-Strength']
    if context['user'].debuffs['Weak'] > 0:
        actualDamage = actualDamage // 4
    # Damage Calcs
    if context['target'] == 2:
        # If the target is random
        for i in range(0, times):
            entity = random.choice(context['enemies'])
            attack_damage_dealt += entity.damage_taken(actualDamage)
            # Causes random target to take damage and saves amount dealt
            if entity.buffs['Thorns'] > 0:
                # If the enemy has thorns
                context['user'].damage_taken(entity.buffs['Thorns'])
                # Take damage equal to throns of the attacked
    else:
        enemies = combat.get_targets(context)
        # Aquires target of the card
        for i in range(0, times):
            for target in enemies:
                attack_damage_dealt += target.damage_taken(actualDamage)
                # Deals damage to targets and saves damage dealt
                if entity.buffs['Thorns'] > 0:
                # If the enemy has thorns
                    context['user'].damage_taken(entity.buffs['Thorns'])
                    # Take damage equal to throns of the attacked
    return attack_damage_dealt
    # Used for certain effects

def deal_damage(damage, context, combat):
    '''Repsonsable for card effects that deal attack danage

    ### args:
        damage: an integer representing damage
        context: Information related to the current combat 
        combat: The current combat
    '''
    targets = combat.get_targets(context)
    # Gets the target of the effect
    for entity in targets:
        entity.damage_taken(damage)
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

def enemy_block_gain(block, context, combat):
    '''Gaining block for enemies
    
    ### args:
        block: the amount of block being gained
        context: Information related to targets
        combat: The current combat session
    '''
    targets = combat.get_targets(context)
    # Aquire targets
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
    for entity in combat.get_targets(context):
        # Go through all targets
        for i in range(len(buffs)):
            entity.gain_buffs(buffs[i], amount[i])
            # Grants the targets the buffs

def apply_debuff(debuffs: list, amount: list, context, combat):
    '''Applies a debuff to the target
    
    ### args: 
        debuffs: A list of debuffs
        amount: The amount of a certain debuff being applied
        context: Information related to the current combat 
        combat: The current combat
    '''
    for entity in combat.get_targets(context):
        # Go through all the targets
        for i in range(len(debuffs)):
            entity.gain_debuffs(debuffs[i], amount[i])
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
        if card_id in {'atk', 'skill', 'power', 'weak curse', 'average curse', 'strong curse', 'curse', 'status'}:
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
    # Use the havoc function in combat to perform this effect

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
    # Uses the function in combat

def exhaust_from_hand(num : int, context, combat):
    '''Effect for choosing and exhausting selected cards from the hand
    
    ### args: 
        num: number of cards being exhausted
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.exhaust_choose_hand(num)
    # Uses fucntion in combat

def exhaust_random_from_hand(num : int, context, combat):
    '''Effect exhausting random cards from the hand
    
    ### args: 
        num: number of cards being exhausted
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.exhaust_random_hand(num)
    # uses function in combat

def lose_hp(amount, context, combat):
    '''Effect for losing HP
    
    ### args: 
        amount: amount of Hp being lost
        context: Information related to the current combat 
        combat: The current combat
    '''
    targets = combat.get_targets(context)
    # Aquire the target using function in combat
    if not isinstance(amount, int):
        # If the amount lost is not a number
        amount = len(context[amount])
        # Retreive the number of cards in a certain place
    for entity in targets:
        entity.hp_loss(amount)
    # All targets lose Hp

def retain_cards(num : int, context, combat):
    '''Effect retaining more cards in hand at the end of the turn
    
    ### args: 
        num: number of cards being retained
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.retain_cards(num)
    # Uses function in combat

def draw_cards(num : int, context, combat):
    '''Effect for drawing more cards
    
    ### args: 
        num: number of cards being drawn
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.draw(num)
    # Uses function in combat

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
    # uses function from combat

def energy_manip(amount : int, context, combat):
    '''Effect for manipulating energy
    
    ### args: 
        amount: The value the energy is modified by
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.energy_change(amount)
    # Uses function from combat

def card_play_limit(limit, context, combat):
    '''Effect limiting number of cards that can be played
    
    ### args: 
        limit: number of cards that can be played
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.card_limit(limit)
    # Uses function from combat

def conditional_effect(effect, effect_details, context_condition, norm_effect, norm_effect_details, cond_effect, cond_effect_details, context, combat):
    '''Complex effects where the first effect is executed and based on the result of that, a non conditional or conditional effect is executed
    
    ### args: 
        effect: Effect the condition will be based on (Ex: deal_attack_damage, etc)
        effect_details: The specifics of the effect being executed
        context_condtion: The condition based on the first effect (Ex: Type of card exhausted, number of cards exhausted, etc)
        norm_effect: effect for if the condition is not met
        norm_effect_details: The specifics of the normal effect
        cond_effect: effect for if the condtion is met
        cond_effect_details: The specifics of the conditional effect
        context: Information related to the current combat 
        combat: The current combat
    '''
    cond = effect(*effect_details, context, combat)
    # Executes first effect and retreives result
    if cond:
        # If a result was retrieved
        if context_condition == cond:
            # If the condition is met
            context['target'] = context['target'][1]
            # Retreives the target for conditional effect
            cond_effect(*cond_effect_details, context, combat)
            # Execute the conditional effect
        else:
            context['target'] = context['target'][0]
            # Retreives target for normal effect
            norm_effect(*norm_effect_details, context, combat)
            # Execute normal effect
    else:
        context['target'] = context['target'][0]
        # Retreives target for normal effect
        norm_effect(*norm_effect_details, context, combat)
        # Executes normal effect 

def modify_effect(effect, modifications, context, combat):
    '''Modifies the effect of a card

    ### args: 
        effect: the effect being modified
        modifications: The changes to the effect
        context: Information related to the current combat 
        combat: The current combat
    '''
    combat.playing.modify_effect(effect, modifications)
    # Uses function from combat

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

def FINAL_GAMBIT(x, additional, context, combat):
    '''Effect for the card final gambit
    
    ### args: 
        x: Final gambit is an X cost card, this represents the amount of energy spent on this card
        additional: bonuses added on to X
        context: Information related to the current combat 
        combat: The current combat
    '''
    x = x + additional
    # add additional to x
    combat.exhaust_entire_pile(context['hand'])
    combat.exhaust_entire_pile(context['draw'])
    combat.exhaust_entire_pile(context['discard'])
    # Exhaust everything
    place_card_in_loction('exhaust', x, 'hand', 0, context, combat)
    # add x cards from the discard pile to the hand and make them cost 0
    apply_debuff(['Last Chance'], [1], context, combat)
    # Apply the Final Gambit debuff to the user

def discover(card_type, cost, context, combat):
    return # Placeholder

def split(slime_type, context, combat):
    '''Function for slime splitting into smaller slimes
    
    ### args:
        slime_type: The type of slime splitting
        context: Info related to the combat
        combat: the current combat session
    '''
    hp = context['user'].hp
    # Get hp of the big slime
    combat.enemies.remove(context['user'])
    # Remove the big slime
    combat.split(slime_type, hp)
    # Use function in combat to add 2 more slimes

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

def hp_loss_reduction(hp_loss, reduction, *args): # Hp Loss Reduction Effect
    '''Reduces Hp Loss
    
    ### args: 
        hp_loss: The amount of hp being loss
        reduction: The amount to reduce by
        *args: Avoid value errors
    
    ### Returns: 
        The reduced amount
    '''
    return hp_loss - reduction
    # Apply reduction

def revive(revive_percentage, max_hp, *args): # Revive effect
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

