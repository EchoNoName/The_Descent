import math

def deal_damage(damage, targets, *args):
    if isinstance(targets, list):
        for entity in targets:
            entity.damage_taken(damage)
    else:
        targets.damage_taken(damage)

def block_gain(block, targets, *args):
    if isinstance(targets, list):
        for entity in targets:
            entity.gain_block(block)
    else:
        targets.gain_block(block)

def small_damage_reduction(damage, cap, *args): # The reduce small damage to 1 effect
    if damage <= cap and damage > 1:
        return 1

def hp_loss_reduction(hp_loss, reduction, *args): # Hp Loss Reduction Effect
    return hp_loss - reduction

def revive(revive_percentage, max_hp, *args):
    return math.floor(max_hp * (revive_percentage / 100))

def healing_reduction(amount, reduction, *args):
    return max(amount - reduction, 0)

#def discover(card_type, pile):