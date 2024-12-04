import effects

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
    def __init__(self, name, desciption, time_of_use, effect, target):
        self.name = name
        self.description = desciption
        self.time_of_use = time_of_use
        self.effect = effect
        self.target = target
    

potions = {
    "Attack Potion": ("Add 1 of 3 random Attack cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Attack', 0)}, 0),
    "Skill Potion": ("Add 1 of 3 random Skill cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Skill', 0)}, 0),
    "Power Potion": ("Add 1 of 3 random Power cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Power', 0)}, 0),
    "Utilities Potion": ("Add 1 of 3 random Non-class cards to your hand, it costs 0 this turn.", 'combat', {'add': ('hand', 'trial atk', 1, 0)}, 0),
    "Blessing of the Forge": ("Upgrade all cards in your hand for the rest of combat.", 'combat', {effects.upgrade: ('hand', )}, 0),
    "Block Potion": ("Gain 12 block.", 'combat', {effects.block_gain_power: (12, )}, 0),
    "Strength Potion": ("Gain 2 Strength.", 'combat', {effects.apply_buff: (['Strength'], [2])}, 0),
    "Dexterity Potion": ("Gain 2 Dexterity.", 'combat', {effects.apply_buff: (['Dexterity'], [2])}, 0),
    "Flex Potion": ("Gain 5 Temporary Strength.", 'combat', {effects.apply_buff: (['Strength'], [5]), effects.apply_debuff: (['Chained'], [5])}, 0),
    "Speed Potion": ("Gain 5 Temporary Dexterity.", 'combat', {effects.apply_buff: (['Dexterity'], [5]), effects.apply_debuff: (['Atrophy'], [5])}, 0),
    "Fire Potion": ("Deal 20 Damage.", 'combat', {effects.deal_damage: (20, )}, 1),
    "Explosive Potion": ("Deal 10 Damage to all enemies.", 'combat', {effects.deal_damage: (10, )}, 3),
    "Fear Potion": ("Apply 3 Vulnerable to an enemy.", 'combat', {effects.apply_debuff: (['Vulnerable'], [3])}, 1),
    "Weak Potion": ("Apply 3 Weak to an enemy.", 'combat', {effects.apply_debuff: (['Weak'], [3])}, 1),
    "Energy Potion": ("Gain 2 Energy.", 'combat', {effects.energy_manip: (2, )}, 0),
    "Swift Potion": ("Draw 3 cards.", 'combat', {effects.draw_cards: (3, )}, 0),
    "Ancient Potion": ("Gain 1 Artifact.", 'combat', {effects.apply_buff: (['Artifact'], [1])}, 0),
    "Thorns Potion": ("Gain 3 Thorns.", 'combat', {effects.apply_buff: (['Thorns'], [3])}, 0),
    "Liquid Metal": ("Gain 4 Plated Armour.", 'combat', {effects.apply_buff: (['Plated Armour'], [4])}, 0),
    "Regen Potion": ("Gain 5 Regeneration.", 'combat', {effects.apply_buff: (['Regen'], [5])}, 0),
    "Memory Potion": ("Choose 1 card from the discard pile and add it to the hand, it costs 0 this turn.", 'combat', {effects.place_card_in_loction: ('discard', 1, 'hand', 0)}, 0),
    "Duplicate Potion": ("Your next card is played twice.", 'combat', {effects.apply_buff: (['Duplicate'], [1])}, 0),
    "Gambler's Potion": ("Discard any number of cards, then draw that many.", 'combat', {effects.gamble: ()}),
    "Chaos Potion": ("Play the top 3 cards of your Draw pile (This doesn't spend Energy).", 'combat', {effects.havoc: (3, False)}, 2),
    "Ritual Potion": ("Gain 1 Ritual.", 'combat', {effects.apply_buff: (['Ritual'], [1])}, 0),
    "Entropic Brew": ("Fill all your empty potion slots with random potions.", 'all', {effects.entropic: ()}, 0),
    "Fairy in a Bottle": ("When you would die, heal to 30% of your Max HP instead and discard this potion.", 'died', {effects.revive: (30, )}, 0),
    "Fruit Juice": ("Gain 5 Max HP.", 'all', {effects.max_hp_change: (5, )}, 0),
    "Smoke Bomb": ("Escape from a non-boss combat. Receive no rewards.", 'combat', {effects.smoke_bomb: ()}, 0),
    "Chaotic Potion": ("Draw 5 cards. Randomize the costs of all cards in your hand for the rest of the combat.", 'combat', {effects.draw_cards: (5, ), 'Placeholder': ()}),
    "Blood Potion": ("Heal for 20% of your Max Hp", 'all', {effects.blood: ('20', )}),
    "Holy Water": ("Exhaust any number of cards in your hand.", 'combat', {effects.purity: ()}, 0)
}
