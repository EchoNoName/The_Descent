import card_constructor
import math
import random

def deal_attack_damage(damage, times : int, context, combat):
    '''Repsonsable for card effects that deal attack danage

    args:
        damage: an integer representing base damage
        targets: A list of objects or single object representing the targets
        buffs: list of buffs the entity doing the attack has
        debuffs: list of debufs the entity doing the attack has
    '''
    attack_damage_dealt = 0
    actualDamage = 0
    if not isinstance(damage, int):
        if damage == 'block':
            actualDamage = context['user'].block
    actualDamage = damage + context['user'].buffs['Strength'] + context['user'].buffs['Vigour']
    actualDamage = actualDamage - context['user'].debuffs['-Strength']
    if context['user'].debuffs['Weak'] > 0:
        actualDamage = actualDamage // 4
    # Damage Calcs
    if context['target'] == 2:
        for i in range(0, times):
            attack_damage_dealt += random.choice(context['enemies']).damage_taken(actualDamage)
    else:
        enemies = combat.get_targets(context['target'])
        for i in range(0, times):
            for target in enemies:
                attack_damage_dealt += target.damage_taken(actualDamage)
    return attack_damage_dealt
    # Applies damage to all targets

def deal_damage(damage, context, combat):
    targets = combat.get_targets(context['target'])
    for entity in targets:
        entity.damage_taken(damage)

def feed(damage : int, max_hp_increase : int, context, combat):
    num_of_enemes = len(combat.enemies)
    deal_attack_damage(damage, 1, context, combat)
    if len(combat.enemies) < num_of_enemes:
        context['user'].maxHp += max_hp_increase
        context['user'].Hp += max_hp_increase

def reap(damage : int, context, combat):
    hp_recover = deal_attack_damage(damage, 1, context, combat)
    context['user'].hp_recovery(hp_recover)

def block_gain_card(block, times : int, context, combat):
    for i in range(0, times):
        context['user'].gain_block_card(block)

def block_gain_power(block, context, combat):
    context['user'].gain_block_power(block)

def apply_buff(buffs: list, amount: list, context, combat):
    for entity in combat.get_targets(context['target']):
        for i in range(len(buffs)):
            entity.gain_buffs(buffs[i], amount[i])

def apply_debuff(debuffs: list, amount: list, context, combat):
    for entity in combat.get_targets(context['target']):
        for i in range(len(debuffs)):
            entity.gain_debuffs(debuffs[i], amount[i])

def add_card_to_pile(location: str, card_id, number_of_cards: int, cost, context, combat):
    if isinstance(card_id, int):
        for i in range(0, number_of_cards):
            combat.add_card_to_pile(context[location], card_id, location, cost)
    else:
        if card_id in {'atk', 'skill', 'power', 'weak curse', 'average curse', 'strong curse', 'curse', 'status'}:
            for i in range(0, number_of_cards):
                card = card_constructor.random_card(card_id, context['user'])
                combat.add_card_to_pile(context[location], card, location, cost)

def havoc(number_of_cards : int, end : bool, context, combat):
    combat.havoc(number_of_cards, end)

def adapt(num, context, combat):
    combat.soft_card_select(num, context['hand'])
    if combat.exhaust_selected():
        block_gain_power(8, context, combat)

def remove_effect_from_type(card_type, context, combat):
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

def exhaust_discard_curse(num : int, context, combat):
    combat.exhaust_discard_curse(num)

def exhaust_from_hand(num : int, context, combat):
    combat.exhaust_choose_hand(num)

def exhaust_random_from_hand(num : int, context, combat):
    combat.exhaust_random_hand(num)

def lose_hp(amount : int, context, combat):
    targets = combat.get_targets(context['target'])
    if not isinstance(amount, int):
        amount = len(context[amount])
    for entity in targets:
        entity.hp_loss(amount)

def retain_cards(num : int, context, combat):
    combat.retain_cards(num)

def draw_cards(num : int, context, combat):
    combat.draw(num)

def double_block(num : int, context, combat):
    for i in range(0, num):
        context['user'].block *= 2

def discard_cards(num : int, type : bool, context, combat): 
    if type == 'random':
        combat.random_discard(num)
    elif type == 'choose':
        combat.choose_discard(num)

def place_card_in_loction(start_pos, num, end_pos, cost, context, combat):
    combat.hard_card_select(num, context[start_pos])
    combat.place_selected_cards(context[end_pos], cost)

def card_search(type, num, context, combat):
    combat.search(num, type)

def energy_manip(amount : int, context, combat):
    combat.energy_change(amount)

def card_play_limit(limit, context, combat):
    combat.card_limit(limit)

def conditional_effect(effect, effect_details, context_condition, norm_effect, norm_effect_details, cond_effect, cond_effect_details, context, combat):
    cond = effect(*effect_details, context, combat)
    if cond:
        if context_condition == cond:
            context['target'] = context['target'][1]
            cond_effect(*cond_effect_details, context, combat)
        else:
            context['target'] = context['target'][0]
            norm_effect(*norm_effect_details, context, combat)
    else:
        context['target'] = context['target'][0]
        norm_effect(*norm_effect_details, context, combat)

def modify_effect(effect, modifications, context, combat):
    combat.playing.modify_effect(effect, modifications)

def hand_for_card_exhausted(exhaust_card_type: set, card_type_cond: set, cond_effect: list, cond_effect_details: list, context, combat):
    cards_exhausted_type = combat.sever(exhaust_card_type)
    if cards_exhausted_type:
        for card_type in combat.sever(exhaust_card_type):
            if card_type in card_type_cond:
                for i in range(0, len(cond_effect)):
                    cond_effect[i](*cond_effect_details[i], context, combat)

def for_card_type_in_hand(effect, effect_details, card_type: set, context, combat):
    times = 0
    if combat.hand:
        for card in combat.hand:
            if card.type in card_type:
                times += 1
    for i in range(0, times):
        effect(*effect_details, context, combat)

def FINAL_GAMBIT(x, additional, context, combat):
    x = x + additional
    combat.exhaust_entire_pile(context['hand'])
    combat.exhaust_entire_pile(context['draw'])
    combat.exhaust_entire_pile(context['discard'])
    place_card_in_loction('exhaust', x, 0, context, combat)
    apply_debuff(['Final Gambit'], [1], context, combat)

def small_damage_reduction(damage, cap, *args): # The reduce small damage to 1 effect
    if damage <= cap and damage > 1:
        return 1

def hp_loss_reduction(hp_loss, reduction, *args): # Hp Loss Reduction Effect
    return hp_loss - reduction

def revive(revive_percentage, max_hp, *args):
    return math.floor(max_hp * (revive_percentage / 100))

def healing_reduction(amount, reduction, *args):
    return max(amount - reduction, 0)

# def discover(card_type, pile):