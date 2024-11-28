import card_constructor
import math
import random

def deal_attack_damage(damage, times, context, combat):
    '''Repsonsable for card effects that deal attack danage

    args:
        damage: an integer representing base damage
        targets: A list of objects or single object representing the targets
        buffs: list of buffs the entity doing the attack has
        debuffs: list of debufs the entity doing the attack has
    '''
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
            random.choice(context['enemies']).damage_taken(actualDamage)
    else:
        enemies = combat.get_targets(context['target'])
        for i in range(0, times):
            for target in enemies:
                target.damage_taken(actualDamage)
    # Applies damage to all targets

def deal_damage(damage, targets, *args):
    for entity in targets:
        entity.damage_taken(damage)

def block_gain_card(block, times, context, combat):
    for i in range(0, times):
        for entity in combat.get_targets(context['user']):
            entity.gain_block_card(block)

def block_gain_power(block, targets, *args):
    if isinstance(targets, list):
        for entity in targets:
            entity.gain_block_power(block)
    else:
        targets.gain_block_power(block)
# Modify later

def apply_buff(buffs, amount, context, combat):
    for entity in combat.get_targets(context['target']):
        for i in range(len(buffs)):
            entity.gain_buffs(buffs[i], amount[i])

def apply_debuff(debuffs, amount, context, combat):
    for entity in combat.get_targets(context['target']):
        for i in range(len(debuffs)):
            entity.gain_debuffs(debuffs[i], amount[i])

def add_card_to_pile(location, card_id, number_of_cards, cost, context, combat):
    if isinstance(card_id, int):
        for i in range(0, number_of_cards):
            combat.add_card_to_pile(context[location], card_id, location, cost)
    else:
        if card_id in {'atk', 'skill', 'power', 'weak curse', 'average curse', 'strong curse', 'curse', 'status'}:
            for i in range(0, number_of_cards):
                card = card_constructor.random_card(card_id)
                combat.add_card_to_pile(context[location], card, location, cost)

def havoc(number_of_cards, end, context, combat):
    combat.havoc(number_of_cards, end)

def exhaust_discard_curse(num, context, combat):
    combat.exhaust_discard_curse(num)

def exhaust_from_hand(num, context, combat):
    combat.exhaust_choose_hand(num)

def exhaust_random_from_hand(num, context, combat):
    combat.exhaust_random_hand(num)

def lose_hp(amount, context, combat):
    targets = combat.get_targets(context['target'])
    if not isinstance(amount, int):
        amount = len(context[amount])
    for entity in targets:
        entity.hp_loss(amount)

def retain_cards(num, context, combat):
    combat.retain_cards(num)

def draw_cards(num, context, combat):
    combat.draw(num)

def discard_cards(num, type, context, combat): 
    if type == 'random':
        combat.random_discard(num)
    elif type == 'choose':
        combat.choose_discard(num)

def place_card_in_loction(start_pos, num, end_pos, cost, context, combat):
    combat.hard_card_select(num, context[start_pos])
    combat.place_selected_cards(context[end_pos], cost)

def card_search(type, num, context, combat):
    combat.search(num, type)

def energy_manip(amount, context, combat):
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
    combat.playing.effect[effect][0] += modifications

def hand_for_card_exhausted(exhaust_card_type: set, card_type_cond: set, cond_effect: list, cond_effect_details: list, context, combat):
    cards_exhausted_type = combat.sever(exhaust_card_type)
    if cards_exhausted_type:
        for card_type in combat.sever(exhaust_card_type):
            if card_type in card_type_cond:
                for i in range(0, len(cond_effect)):
                    cond_effect[i](*cond_effect_details[i], context, combat)


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