import effects
import random
#effect:
# dmg: (#, Times, target(Override)
# block: (#, Times)
# buff: (id, stacks, id, stacks, id, stacks...)
# debuff: (id, stacks, id, stacks, id, stacks...)
# draw: #
# discard: #
# place: (start, #, end, position if needed, cost)
# exhaust: (#, location, choice/random/condition/position)
# add: (location, card, #, cost(if applicable))
# search: (location, card/type, #)
# condition (Based on previous effect): (cond, cond eff, norm eff)
# retain: (location, #)
# play: (location, position, discard/exhaust, #)
# Hp: #
# Drawn: (eff)
# turn end: (eff)
# cost: (target, #, cond if applicable)
# modify: (target, eff, modification, combat/Perm)
# power: (name, duration(# OR Perm), amount)
# E: # 
# Exhausted: {eff}
# Discarded: {eff}
# upgrade: (target(s), #, combat/perm)
# gamble: # (Do a mulligan # of times)
# potion: (Slots, Type), adds potions to empty slots
# MaxHp: #
# Chaotic: Location

# 'NAME': ('DESCRIPTION', 'TIME OF USE', ('EFFECT': 'MAGNITUDE'...), 'TARGET')
class Potion:
    def __init__(self, name, desciption, time_of_use, effect, target, rarity):
        self.name = name
        self.description = desciption
        self.time_of_use = time_of_use
        self.effect = effect
        self.target = target
        self.rarity = rarity
    
    def __str__(self):
        return f'{self.name}: {self.description}'
    
    def __repr__(self):
        return self.__str__()

potions = {
    "Attack Potion": ("Add 1 of 3 random Attack cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Attack', 0)}, 0, 0),
    "Skill Potion": ("Add 1 of 3 random Skill cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Skill', 0)}, 0, 0),
    "Power Potion": ("Add 1 of 3 random Power cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Power', 0)}, 0, 0),
    "Blessing of the Forge": ("Upgrade all cards in your hand for the rest of combat.", 'combat', {effects.upgrade: ('hand', )}, 0, 0),
    "Block Potion": ("Gain 12 block.", 'combat', {effects.block_gain_power: (12, )}, 0, 0),
    "Strength Potion": ("Gain 2 Strength.", 'combat', {effects.apply_buff: (['Strength'], [2])}, 0, 0),
    "Dexterity Potion": ("Gain 2 Dexterity.", 'combat', {effects.apply_buff: (['Dexterity'], [2])}, 0, 0),
    "Flex Potion": ("Gain 5 Temporary Strength.", 'combat', {effects.apply_buff: (['Strength'], [5]), effects.apply_debuff: (['Chained'], [5])}, 0, 0),
    "Speed Potion": ("Gain 5 Temporary Dexterity.", 'combat', {effects.apply_buff: (['Dexterity'], [5]), effects.apply_debuff: (['Atrophy'], [5])}, 0, 0),
    "Fire Potion": ("Deal 20 Damage.", 'combat', {effects.deal_damage: (20, )}, 1, 0),
    "Explosive Potion": ("Deal 10 Damage to all enemies.", 'combat', {effects.deal_damage: (10, )}, 3, 0),
    "Fear Potion": ("Apply 3 Vulnerable to an enemy.", 'combat', {effects.apply_debuff: (['Vulnerable'], [3])}, 1, 0),
    "Weak Potion": ("Apply 3 Weak to an enemy.", 'combat', {effects.apply_debuff: (['Weak'], [3])}, 1, 0),
    "Energy Potion": ("Gain 2 Energy.", 'combat', {effects.energy_manip: (2, )}, 0, 1),
    "Swift Potion": ("Draw 3 cards.", 'combat', {effects.draw_cards: (3, )}, 0, 1),
    "Ancient Potion": ("Gain 1 Artifact.", 'combat', {effects.apply_buff: (['Artifact'], [1])}, 0, 1),
    "Thorns Potion": ("Gain 3 Thorns.", 'combat', {effects.apply_buff: (['Thorns'], [3])}, 0, 1),
    "Liquid Metal": ("Gain 4 Plated Armour.", 'combat', {effects.apply_buff: (['Plated Armour'], [4])}, 0, 1),
    "Regen Potion": ("Gain 5 Regeneration.", 'combat', {effects.apply_buff: (['Regen'], [5])}, 0, 1),
    "Memory Potion": ("Choose 1 card from the discard pile and add it to the hand, it costs 0 this turn.", 'combat', {effects.place_card_in_loction: ('discard', 1, 'hand', 0)}, 0, 1),
    "Duplicate Potion": ("Your next card is played twice.", 'combat', {effects.apply_buff: (['Duplicate'], [1])}, 0, 1),
    "Gambler's Potion": ("Discard any number of cards, then draw that many.", 'combat', {effects.gamble: ()}, 0, 1),
    "Chaos Potion": ("Play the top 3 cards of your Draw pile (This doesn't spend Energy).", 'combat', {effects.havoc: (3, False)}, 2, 1),
    "Ritual Potion": ("Gain 1 Ritual.", 'combat', {effects.apply_buff: (['Ritual'], [1])}, 0, 2),
    "Entropic Brew": ("Fill all your empty potion slots with random potions.", 'all', {effects.entropic: ()}, 0, 2),
    "Fairy in a Bottle": ("When you would die, heal to 30% of your Max HP instead and discard this potion.", 'died', {effects.revive: (30, )}, 0, 2),
    "Fruit Juice": ("Gain 5 Max HP.", 'all', {effects.max_hp_change: (5, )}, 0, 2),
    "Smoke Bomb": ("Escape from a non-boss combat. Receive no rewards.", 'combat', {effects.smoke_bomb: ()}, 0, 2),
    "Chaotic Potion": ("Draw 5 cards. Randomize the costs of all cards in your hand for the rest of the combat.", 'combat', {effects.draw_cards: (5, ), effects.chaos: ()}, 0, 2),
    "Blood Potion": ("Heal for 20% of your Max Hp", 'all', {effects.blood: ('20', )}, 0, 0),
    "Holy Water": ("Exhaust any number of cards in your hand.", 'combat', {effects.purity: ()}, 0, 1)
}

def createPotion(name, data):
    return Potion(name, *data)

def randomPotion():
    name = ''
    data = ()
    rng = random.randint(1, 100)
    if rng <= 65:
        rng = 0
    elif rng <= 90:
        rng = 1
    else:
        rng = 2
    while True:
        name, data = random.choice(list(potions.items()))
        if data[4] != rng:
            continue
        else:
            break
    return createPotion(name, data)

