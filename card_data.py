import effects
import pygame

#the card ids will consist of 4 numbers, ABCD, A represents the class of cards, and the rest represents the card number, adding 100 is the upgraded version of the card.
# A = 0, Classless cards, curses, statuses. A = 1, Cursed Swordsman cards

# 0000: (name: rarity:(0 = starter, 1 = common, 2 = uncommon, 3 = rare, 4 = other), type: (0 = atk, 1 = skill, 2 = power, 3 = status, 4 = curse), cost: #, card text: "Card_effect", exhaust, retain, ethereal, effect)
#If mana cost is "U", its unplayable
# Cost: # OR ('C', Original Cost, +/-, Condition) OR 'x'
#Debuffs: 0 = Vulnerable, 1 = Weak, 2 = Negative Strength, 3 = Lose strength at the end of turn, 4 = No Draw, 5 = poison, 6 = lose dex at the end of turn
#Buffs: 0 = strength, 1 = dexterity, 2 = vigour, 3 = blur, 4 = Metalicize, 5 = double tap, 6 = plated armour, 7 = thorns, 8 = regen, 9 = flurry (Play the next card twice), 10 = artifact, 11 = Ritual
#tagets:  Self: 0, target: 1, random: 2, all: 3
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

#Note: When 'exhaust' is put in place for a #, that means # of cards exhausted

# innate, exhaust, retain, ethereal

card_info = {
    0: ('Unfocused', 4, 4, 'U', None, True, False, False, True, None, 0),
    1: ('Clumsy', 4, 4, 'U', None, False, False, False, True, None, 0),
    2: ('Writhe', 4, 4, 'U', None, True, False, False, False, None, 0),
    3: ('Cluttered', 4, 4, 'U', None, False, False, True, False, None, 0),
    4: ('Injury', 4, 4, 'U', None, False, False, False, False, None, 0),
    5: ('Doubt', 4, 4, 'U', 'At the end of your turn, gain 1 Weak', False, False, False, False, {'Turn End': {effects.apply_debuff: (['Weak'], [1])}}, 0),
    6: ('Corroded', 4, 4, 'U', 'At the end of your turn, gain 1 Frail', False, False, False, False, {'Turn End': {effects.apply_debuff: (['Frail'], [1])}}, 0),
    7: ('Shame', 4, 4, 'U', 'At the end of your turn, gain 1 Vulnerable', False, False, False, False, {'Turn End': {effects.apply_debuff: (['Vulnerable'], [1])}}, 0),
    8: ('Decay', 4, 4, 'U', 'At the end of your turn, take 2 damage', False, False, False, False, {'Turn End': {effects.deal_damage: (2, )}}, 0),
    9: ('Regret', 4, 4, 'U', 'At the end of your turn, lose 1 Hp for each card in your hand', False, False, False, False, {'Turn End': {effects.lose_hp: ('hand', )}}, 0),
    10: ('Pain', 4, 4, 'U', 'While in hand, lose 1 Hp when other cards are played', False, False, False, False, {'Card Played': {effects.lose_hp: (1, )}}, 0),
    11: ('Normality', 4, 4, 'U', 'You cannot play more than 3 cards this turn', False, False, False, False, {'Drawn': {effects.card_play_limit: (3, )}, 'Discarded': {effects.card_play_limit: (False, )}, 'Exhausted': {effects.card_play_limit: (False, )}, 'Card Played': {effects.card_play_limit: (3, )}}, 0),
    12: ('Icky', 4, 4, 1, 'Add a Slimed to your hand', False, True, False, False, {effects.add_card_to_pile: ('hand', 50, 1, 'na')}, 0),
    20: ('Curse of the Blade', 4, 4, 'U', 'When drawn, lose 4, At the end of the turn, lose 2 HP', False, False, True, False, {'Drawn': {effects.lose_hp: (4, )}, 'Turn End': {effects.lose_hp: (2, )}}, 0),
    21: ('Curse of the Talisman', 4, 4, 'U', None, False, False, False, False, None, 0, False),
    22: ('Necronomicurse', 4, 4, 'U', 'You cannot escape from this Curse. ', False, False, False, False, {'Exhausted': {effects.add_card_to_pile: ('hand', 22, 1, 'na')}}, 0),
    50: ('Slimed', 4, 3, 1, None, False, True, False, False, None, 0),
    51: ('Burned', 4, 3, 'U', 'At the end of your turn, take 2 damage', False, False, False, False, {'Turn End': {effects.deal_attack_damage: (2, 1)}}, 0),
    52: ('Wound', 4, 3, 'U', None, False, False, False, False, None, 0),
    53: ('Dazed', 4, 3, 'U', None, False, False, False, True, None, 0),
    54: ('Void', 4, 3, 'U', 'When drawn, lose 1 Energy', False, False, False, True, {'Drawn': {effects.energy_manip: (-1, )}}, 0),
    1000: ('Slash', 0, 0, 1, 'Deal 6 damage', False, False, False, False, {effects.deal_attack_damage: (6, 1)}, 1),
    1001: ('Bash', 0, 0, 2, 'Deal 8 damage. Apply 2 Vulnerable', False, False, False, False, {effects.deal_attack_damage: (8, 1), effects.apply_debuff: (['Vulnerable'], [2])}, 1),
    1002: ('Block', 0, 1, 1, 'Gain 5 block', False, False, False, False, {effects.block_gain_card: (5, 1)}, 0),
    1003: ('Inflict Wounds', 1, 0, 0, 'Deal 3 damage. Apply 1 Vulnerable', False, False, False, False, {effects.deal_attack_damage: (3, 1), effects.apply_debuff: (['Vulnerable'], [1])}, 1),
    1004: ("Rampage", 1, 0, 0, 'Deal 6 damage. Add a copy of this card to your discard pile', False, False, False, False, {effects.deal_attack_damage: (6, 1), effects.add_card_to_pile: ('discard', 1004, 1, 'na')}, 1), # 0 = hand, 1 = draw pile, 2 = discard pile. 3 = exhaust pile
    1005: ("Covet", 1, 1, 0, 'Draw 1 card. Discard 1 card, if the card discarded was a Curse, Exhaust it instead', False, False, False, False, {effects.draw_cards: (1, ), effects.exhaust_discard_curse: (1, )}, 0),
    1006: ("Empower", 1, 1, 0, 'Gain 2 Temporary Strength', False, False, False, False, {effects.apply_buff: (['Strength'], [2]), effects.apply_debuff: (['Chained'], [2])}, 0),
    1007: ("War Cry", 1, 1, 0, 'Draw 1 card, place 1 card on top of the draw pile, gain 3 Vigour', False, False, False, False, {effects.draw_cards: (1, ), effects.place_card_in_loction: ('hand', 1, 'draw', 'na')}, 0),
    1008: ("To Basics", 1, 1, 0, 'Add 1 Common card from your draw pile into your hand', False, False, False, False, {effects.card_search: ('common', 1)}, 0),
    1009: ("Sword beam", 1, 0, 1, 'Deal 9 damage to all enemies', False, False, False, False, {effects.deal_attack_damage: (9, 1)}, 3),
    1010: ("Grudge", 1, 0, 1, 'Exhaust a random card in your hand, deal 9 damage', False, False, False, False, {effects.exhaust_random_from_hand: (1, ), effects.deal_attack_damage: (9, 1)}, 1),
    1011: ("Pummel Strike", 1, 0, 1, 'Deal 9 damage. Draw 1 card', False, False, False, False, {effects.deal_attack_damage: (9, 1), effects.draw_cards: (1, )}, 1),
    1012: ("Twin Slash", 1, 0, 1, 'Deal 5 damage twice', False, False, False, False, {effects.deal_attack_damage: (5, 2)}, 1),
    1013: ("Reckless Charge", 1, 0, 1, 'Deal 11 damage. Add a Curse your draw pile', False, False, False, False, {effects.deal_attack_damage: (11, 1), effects.add_card_to_pile: ('draw', 'weak curse', 1, 'na')}, 1),
    1014: ("Sword Boomerang", 1, 0, 1, 'Deal 3 damage 3 times to a random enemy', False, False, False, False, {effects.deal_attack_damage: (3, 3)}, 2),
    1015: ("Careful Strike", 1, 0, 1, 'Careful Strike', False, False, False, False, {effects.deal_attack_damage: (5, 1), effects.block_gain_card: (5, 1)}, 1),
    1016: ("Headbutt", 1, 0, 1, 'Deal 9 damage. Place a card from discard pile to top of the draw pile', False, False, False, False, {effects.deal_attack_damage: (9, 1), effects.place_card_in_loction: ('discard', 1, 'draw', 'na')}, 1),
    1017: ("Shrug it off", 1, 1, 1, 'Gain 8 block. Draw 1 card', False, False, False, False, {effects.block_gain_card: (8, 1), effects.draw_cards: (1, )}, 0),
    1018: ("Grit", 1, 1, 1, 'Gain 5 block. Exhaust a random card in your hand', False, False, False, False, {effects.block_gain_card: (5, 1), effects.exhaust_random_from_hand: (1, )}, 0),
    1019: ("Feint", 1, 1, 1, 'Apply 1 Weak. Gain 5 block', False, False, False, False, {effects.apply_debuff: (['Weak'], [1]), effects.block_gain_card: (5, 1)}, 1),
    1020: ("Preperations", 1, 1, 1, 'Gain 6 block. Choose up to 2 cards to Retain this turn', False, False, False, False, {effects.block_gain_card: (6, 1), effects.retain_cards: (2, )}, 0),
    1021: ("Havoc", 1, 1, 1, 'Play the top card of your draw pile and Exhaust it', False, False, False, False, {effects.havoc: (1, True)}, 2),
    1022: ("Crushing blow", 1, 0, 2, 'Deal 12 damage. Apply 2 Weak', False, False, False, False, {effects.deal_attack_damage: (12, 1), effects.apply_debuff: (['Weak'], [2])}, 1),
    1023: ("Body charge", 1, 0, 1, 'Deal damage equal to your block', False, False, False, False, {effects.deal_attack_damage: ('block', 1)}, 1),
    1024: ("Desperato", 1, 1, 1, 'Gain 8 Vigour, lose 1 Strength', False, False, False, False, {effects.apply_buff: (['Vigour'], [8]), effects.apply_debuff: (['-Strength'], [1])}, 0),
    1025: ("Flurry of beams", 2, 0, "X", 'Deal 5 damage to all enemies X times', False, False, False, False, {effects.deal_attack_damage: (5, 'X')}, 3),
    1026: ("Cursed Blade", 2, 0, 1, 'Lose 3 HP. Deal 20 damage. Shuffle a Curse of the Blade into the draw pile', False, False, False, False, {effects.hp_cost: (3, ), effects.deal_attack_damage: (20, 1), effects.add_card_to_pile: ('draw', 20, 1, 'na')}, 1),
    1027: ("Glooming blade", 2, 0, 'c', 'Deal 20 damage. Cost 1 less Energy for every Curse in the draw pile, discard pile, exhaust pile and hand', False, False, False, False, {effects.deal_attack_damage: (20, 1)}, 1),
    1028: ("Multi-Slash", 2, 0, 1, 'Deal 2 damage 4 times', False, False, False, False, {effects.deal_attack_damage: (2, 4)}, 1),
    1029: ("Aim for the eyes", 2, 0, 2, 'Deal 13 damage. Apply 1 Weak and 1 Vulnerable', False, False, False, False, {effects.deal_attack_damage: (13, 1), effects.apply_debuff: (['Weak', 'Vulnerable'], [1, 1])}, 1),
    1030: ("Uncontrolled slash", 2, 0, 0, 'Deal 8 damage. Shuffle a Curse into the draw pile', False, False, False, False, {effects.deal_attack_damage: (8, 1), effects.add_card_to_pile: ('draw', 'weak curse', 1, 'na')}, 1),
    1031: ("Consumed", 2, 0, 1, 'Deal 8 damage. This card deals 5 more damage this combat', False, False, False, False, {effects.deal_attack_damage: (8, 1), effects.modify_effect: (effects.deal_attack_damage, 5)}, 1),
    1032: ("Flaming Strike", 2, 0, 2, 'Deal 12 damage. Can be Upgraded up to 9 times', False, False, False, False, {effects.deal_attack_damage: (12, 1)}, 1),
    1033: ("Purgatory", 2, 0, 3, 'Deal 26 damage to all enemies', False, False, False, False, {effects.deal_attack_damage: (26, 1)}, 3),
    1034: ("Parry", 2, 1, 2, 'Gain 12 block. Whenever you are attacked this turn, apply 2 Vulnerable to the attacker', False, False, False, False, {effects.block_gain_card: (12, 1), effects.apply_buff: (['Parry'], [2])}, 0),
    1035: ("Deflect", 2, 1, 2, 'Gain 12 block. Whenever you are attacked this turn, deal 4 damage back', False, False, False, False, {effects.block_gain_card: (12, 1), effects.apply_buff: (['Deflect'], [4])}, 0),
    1036: ("Sever Soul", 2, 1, 1, 'Exhaust all non-attack cards in hand. For every curse exhausted, gain 1 Strength and draw 2 card', False, False, False, False, {effects.hand_for_card_exhausted: ({1, 2, 3, 4}, {4}, [effects.apply_buff, effects.draw_cards], [(['Strength'], [1]), (2, )])}, 0),
    1037: ("Cursed Pact", 2, 1, 1, 'Exhaust 1 card in your hand. Draw 2 cards', False, False, False, False, {effects.exhaust_from_hand: (1, ), effects.draw_cards: (2, )}, 0),
    1038: ("Power Through", 2, 1, 0, 'Lose 3 HP. Gain 15 block, shuffle 1 Curse into the draw pile', False, False, False, False, {effects.hp_cost: (3, ), effects.block_gain_card: (15, 1), effects.add_card_to_pile: ('draw', 'weak curse', 1, 'na')}, 0),
    1039: ("Second wind", 2, 1, 1, 'Exhaust all non-attack cards and gain 5 block for each card exhausted', False, False, False, False, {effects.hand_for_card_exhausted: ({1, 2, 3, 4}, {0, 1, 2, 3, 4}, [effects.block_gain_card], [(5, 1)])}, 0),
    1040: ("Conjour blade", 2, 1, 0, 'Add a random attack card to your hand. It costs 0 this turn', False, True, False, False, {effects.add_card_to_pile: ('hand', 'atk', 1, (0, 'Turn'))}, 0),
    1041: ("Sinister appearance", 2, 1, 0, 'Apply 1 Weak to all enemies', False, True, False, False, {effects.apply_debuff: (['Weak'], [1])}, 3),
    1042: ("Sentenal", 2, 1, 1, 'Gain 5 block. If this card is exhausted, gain 2 Energy', False, False, False, False, {effects.block_gain_card: (5, 1), 'Exhausted': {effects.energy_manip: (2, )}}, 0),
    1043: ("Bloodletting", 2, 1, 0, 'Lose 3 HP. Gain 2 Energy', False, False, False, False, {effects.hp_cost: (3, ), effects.energy_manip: (2, )}, 0),
    1044: ("Cursed Shield", 2, 1, 1, 'Gain 15 block. Add 2 Curses to your hand', False, False, False, False, {effects.block_gain_card: (15, 1), effects.add_card_to_pile: ('hand', 'weak curse', 2, 'na')}, 0),
    1045: ("Cursed Aura", 2, 1, 2, 'Apply 3 Weak and 3 Vulnerable to all enemies', False, True, False, False, {effects.apply_debuff: (['Weak', 'Vulnerable'], [3, 3])}, 3),
    1046: ("Disarm", 2, 1, 1, 'Enemy loses 2 Strength', False, True, False, False, {effects.apply_debuff: (['-Strength'], [2])}, 1),
    1047: ("Entrench", 2, 1, 2, 'Double the amount of block you have', False, False, False, False, {effects.double_block: (1, )}, 0),
    1048: ("Defensive Positioning", 2, 1, 1, 'Gain 2 Blur', False, False, False, False, {effects.apply_buff: (['Blur'], [2])}, 0),
    1049: ("Battle Trance", 2, 1, 0, 'Draw 3 cards. You can no longer draw cards this turn', False, False, False, False, {effects.draw_cards: (3, ), effects.apply_debuff: (['No Draw'], [1])}, 0),
    1050: ("Defensive Stance", 2, 2, 1, 'Gain 3 Metalicize', False, False, False, False, {effects.apply_buff: (['Metalicize'], [3])}, 0),
    1051: ("Inflame", 2, 2, 1, 'Gain 2 Strength', False, False, False, False, {effects.apply_buff: (['Strength'], [2])}, 0),
    1052: ("Curse Ward", 2, 2, 2, 'Whenever you draw a Curse, gain 2 block', False, False, False, False, {'Power': {'Draw Curse': {effects.block_gain_power: (2, )}}}, 0),
    1053: ("Feel no pain", 2, 2, 1, 'Whenever you Exhaust a card, gain 3 block', False, False, False, False, {'Power': {'Exhaust': {effects.block_gain_power: (3, )}}}, 0),
    1054: ("Evolve", 2, 2, 1, 'Whenever you draw a Status, draw 1 card', False, False, False, False, {'Power': {'Draw Status': {effects.draw_cards: (1, )}}}, 0),
    1055: ("Transfer pain", 2, 2, 1, 'Whenever you draw a Curse or Status, deal 6 damage to all enemies', False, False, False, False, {'Power': {'Draw Negative': {effects.deal_damage: (6, )}}}, 3),
    1056: ("Dark Embrace", 2, 2, 2, 'Whenever a card is exhausted, draw 1 card', False, False, False, False, {'Power': {'Exhaust': {effects.draw_cards: (1, )}}}, 0),
    1057: ("Devouring Blade", 3, 0, 1, 'Deal 10 damage. If Fatal, increase your Max Hp by 3', False, True, False, False, {effects.feed: (10, 3)}, 1),
    1058: ("Void Strike", 3, 0, 0, 'Deal 3 damage. Apply 2 Vulnerable. 2 Weak and 2 Poison', False, True, False, False, {effects.deal_attack_damage: (3, 1), effects.apply_debuff: (['Vulnerable', 'Weak', 'Poison'], [2, 2, 2])}, 1),
    1059: ("Cursed flames", 3, 0, 2, 'Deal 21 to all enemies. Shuffle 2 Curses into the discard pile', False, False, False, False, {effects.deal_attack_damage: (21, 1), effects.add_card_to_pile: ('discard', 'weak curse', 2, 'na')}, 3),
    1060: ("Bloodlust", 3, 0, 2, 'Deal 4 damage to all enemies. Heal HP equal to the unblocked damage dealt', False, True, False, False, {effects.reap: (4, )}, 3),
    1061: ("Black Wind", 3, 0, 0, 'Deal 10 damage for each Curse in your hand', False, False, True, False, {effects.for_card_type_in_hand: (effects.deal_attack_damage, (10, 1), {4})}, 1),
    1062: ("Demonic Fire", 3, 0, 2, 'Exhaust your hand. Deal 7 damage for each card exhausted', False, True, False, False, {effects.hand_for_card_exhausted: ({0, 1, 2, 3, 4}, {0, 1, 2, 3, 4}, [effects.deal_attack_damage], [(7, 1)])}, 1),
    1063: ("Generational Skill", 3, 1, 1, 'Exhaust all cards in your hand, shuffle a Curse into the draw pile and draw 2 for each card exhausted. gain 1 Energy', False, True, False, False, {effects.hand_for_card_exhausted: ({0, 1, 2, 3, 4}, {0, 1, 2, 3, 4}, [effects.add_card_to_pile, effects.draw_cards], [('draw', 'weak curse', 1, 'na'), (2, )]), effects.energy_manip: (1, )}, 0),
    1064: ("Fey's Offering", 3, 1, 0, 'Lose 6 HP. Draw 3 cards. Gain 2 Energy', False, True, False, False, {effects.hp_cost: (6, ), effects.draw_cards: (3, ), effects.energy_manip: (2, )}, 0),
    1065: ("Mirror image", 3, 1, 1, 'Your next attack is played twice', False, False, False, False, {effects.apply_buff: (['Double Tap'], [1])}, 0),
    1066: ("Hallucinations", 3, 1, 1, 'Add 1 card from your exhaust pile to your hand', False, True, False, False, {effects.place_card_in_loction: ('exhaust', 1, 'hand', 'na')}, 0),
    1067: ("Final Gambit", 3, 1, "X", 'Exhaust EVERYTHING. Add X + 1 cards from your exhaust pile to your hand, they cost 0 this turn, You cannot play Final Gambit until the start of your next turn. At the end of your turn, Exhaust EVERYTHING', False, True, False, False, {effects.final_gambit: ('X', 1)}, 0),
    1068: ("Impervious", 3, 1, 2, 'Gain 30 block', False, True, False, False, {effects.block_gain_card: (30, 1)}, 0),
    1069: ("Corruption Form", 3, 2, 3, 'At the start of your turn, lose 1 HP and gain 3 Strength', False, False, False, False, {'Power': {'Turn Start': {effects.hp_cost: (1, ), effects.apply_buff: (['Strength'], [3])}}}, 0),
    1070: ("Phantom blades", 3, 2, 2, 'At the start of your turn, gain 6 Vigour', False, False, False, False, {'Power': {'Turn Start': {effects.apply_buff: (['Vigour'], [6])}}}, 0),
    1071: ("Seeing red", 3, 2, 1, 'Draw 2 cards at the start of turn and add a Curse to hand', False, False, False, False, {'Power': {'Turn Start': {effects.draw_cards: (2, ), effects.add_card_to_pile: ('hand', 'weak curse', 1, 'na')}}}, 0),
    1072: ("Clear mind", 3, 2, 3, 'At the start of turn, you can exhaust a card from your hand to gain 8 block', False, False, False, False, {'Power': {'Turn Start': {effects.adapt: (1, )}}}, 0),
    1073: ("Corruption", 3, 2, 2, 'Curses no longer have negative effects', False, False, False, False, {effects.remove_effect_from_type: (4, ), 'Power': None}, 0),
    1074: ("Eternal flames", 3, 2, 0, 'Gain 3 Energy, Draw 3 cards. At the end of the turn, lose 3 Hp', False, False, False, False, {effects.energy_manip: (3, ), effects.draw_cards: (3, ), 'Power': {'Turn End': {effects.lose_hp: (3, )}}}, 0),
    #below are upgrades
    1100: ('Slash+', 0, 0, 1, 'Deal 9 damage', False, False, False, False, {effects.deal_attack_damage: (9, 1)}, 1),
    1101: ('Bash+', 0, 0, 2, 'Deal 12 damage. Apply 3 Vulnerable', False, False, False, False, {effects.deal_attack_damage: (12, 1), effects.apply_debuff: (['Vulnerable'], [3])}, 1),
    1102: ('Block+', 0, 1, 1, 'Gain 8 block', False, False, False, False, {effects.block_gain_card: (8, 1)}, 0),
    1103: ('Inflict Wounds+', 1, 0, 0, 'Deal 4 damage. Apply 2 Vulnerable', False, False, False, False, {effects.deal_attack_damage: (4, 1), effects.apply_debuff: (['Vulnerable'], [2])}, 1),
    1104: ("Rampage+", 1, 0, 0, 'Deal 8 damage. Add a copy of this card to your discard pile', False, False, False, False, {effects.deal_attack_damage: (8, 1), effects.add_card_to_pile: ('discard', 1104, 1, 'na')}, 1),
    1105: ("Covet+", 1, 1, 0, 'Draw 2 card. Discard 2 card, if the card discarded was a Curse, Exhaust it instead', False, False, False, False, {effects.draw_cards: (2, ), effects.exhaust_discard_curse: (2, )}, 0),
    1106: ("Empower+", 1, 1, 0, 'Gain 4 Temporary Strength', False, False, False, False, {effects.apply_buff: (['Strength'], [4]), effects.apply_debuff: (['Chained'], [4])}, 0),
    1107: ("War cry+", 1, 1, 0, 'Draw 2 card, place 1 card on top of the draw pile, gain 3 Vigour', False, False, False, False, {effects.draw_cards: (2, ), effects.place_card_in_loction: ('hand', 1, 'draw', 'na')}, 0),
    1108: ("To Basics+", 1, 1, 0, 'Add 2 Common card from your draw pile into your hand', False, False, False, False, {effects.card_search: ('common', 2)}, 0),
    1109: ("Sword beam+", 1, 0, 1, 'Deal 11 damage to all enemies', False, False, False, False, {effects.deal_attack_damage: (11, 1)}, 3),
    1110: ("Grudge+", 1, 0, 1, 'Exhaust a card in your hand, deal 11 damage', False, False, False, False, {effects.exhaust_from_hand: (1, ), effects.deal_attack_damage: (11, 1)}, 1),
    1111: ("Pummel Strike+", 1, 0, 1, 'Deal 12 damage. Draw 2 card', False, False, False, False, {effects.deal_attack_damage: (12, 1), effects.draw_cards: (2, )}, 1),
    1112: ("Twin Slash+", 1, 0, 1, 'Deal 7 damage twice', False, False, False, False, {effects.deal_attack_damage: (7, 2)}, 1),
    1113: ("Reckless Charge+", 1, 0, 1, 'Deal 15 damage. Add a Curse your draw pile', False, False, False, False, {effects.deal_attack_damage: (15, 1), effects.add_card_to_pile: ('draw', 'weak curse', 1, 'na')}, 1),
    1114: ("Sword Boomerang+", 1, 0, 1, 'Deal 3 damage to a random enemy 4 times', False, False, False, False, {effects.deal_attack_damage: (3, 4)}, 2),
    1115: ("Careful Strike+", 1, 0, 1, 'Deal 7 damage. Gain 7 block', False, False, False, False, {effects.deal_attack_damage: (7, 1), effects.block_gain_card: (7, 1)}, 1),
    1116: ("Headbutt+", 1, 0, 1, 'Deal 11 damage. Place a card from discard pile to top of the draw pile', False, False, False, False, {effects.deal_attack_damage: (11, 1), effects.place_card_in_loction: ('discard', 1, 'draw', 'na')}, 1),
    1117: ("Shrug it off+", 1, 1, 1, 'Gain 11 block. Draw 1 card', False, False, False, False, {effects.block_gain_card: (11, 1), effects.draw_cards: (1, )}, 0),
    1118: ("Grit+", 1, 1, 1, 'Gain 8 block. Exhaust a card in your hand', False, False, False, False, {effects.block_gain_card: (8, 1), effects.exhaust_from_hand: (1, )}, 0),
    1119: ("Feint+", 1, 1, 1, 'Apply 1 Weak. Gain 7 block', False, False, False, False, {effects.apply_debuff: (['Weak'], [1]), effects.block_gain_card: (7, 1)}, 1),
    1120: ("Preperations+", 1, 1, 1, 'Gain 8 block. Choose up to 3 cards to Retain this turn', False, False, False, False, {effects.block_gain_card: (8, 1), effects.retain_cards: (3, )}, 0),
    1121: ("Havoc+", 1, 1, 1, 'Play the top 2 cards of your draw pile and Exhaust it', False, False, False, False, {effects.havoc: (2, True)}, 2),
    1122: ("Crushing blow+", 1, 0, 2, 'Deal 14 damage. Apply 3 Weak', False, False, False, False, {effects.deal_attack_damage: (14, 1), effects.apply_debuff: (['Weak'], [3])}, 1),
    1123: ("Body charge+", 1, 0, 0, 'Deal damage equal to your block', False, False, False, False, {effects.deal_attack_damage: ('block', 1)}, 1),
    1124: ("Desperato+", 1, 1, 0, 'Gain 8 Vigour, lose 1 Strength', False, False, False, False, {effects.apply_buff: (['Vigour'], [8]), effects.apply_debuff: (['-Strength'], [1])}, 0),
    1125: ("Flurry of beams+", 2, 0, "X", 'Deal 8 damage to all enemies X times', False, False, False, False, {effects.deal_attack_damage: (8, 'X')}, 3),
    1126: ("Cursed Blade+", 2, 0, 1, 'Lose 2 HP. Deal 26 damage. Shuffle a Curse of the Blade into the draw pile', False, False, False, False, {effects.hp_cost: (2, ), effects.deal_attack_damage: (26, 1), effects.add_card_to_pile: ('draw', 20, 1, 'na')}, 1),
    1127: ("Glooming blade+", 2, 0, 'c', 'Deal 26 damage. Cost 1 less Energy for every Curse in the draw pile, discard pile, exhaust pile and hand', False, False, False, False, {effects.deal_attack_damage: (26, 1)}, 1),
    1128: ("Multi-Slash+", 2, 0, 1, 'Deal 2 damage 5 times', False, False, False, False, {effects.deal_attack_damage: (2, 5)}, 1),
    1129: ("Aim for the eyes+", 2, 0, 2, 'Deal 13 damage. Apply 2 Weak and 2 Vulnerable', False, False, False, False, {effects.deal_attack_damage: (13, 1), effects.apply_debuff: (['Weal', 'Vulnerable'], [2, 2])}, 1),
    1130: ("Uncontrolled slash+", 2, 0, 0, 'Deal 11 damage. Shuffle a Curse into the draw pile', False, False, False, False, {effects.deal_attack_damage: (11, 1), effects.add_card_to_pile: ('draw', 'weak curse', 1, 'na')}, 1),
    1131: ("Consumed+", 2, 0, 1, 'Deal 8 damage. This card deals 8 more damage this combat', False, False, False, False, {effects.deal_attack_damage: (8, 1), effects.modify_effect: (effects.deal_attack_damage, 8)}, 1),
    1132: ("Flaming Strike+", 2, 0, 2, 'Deal 16 damage. Can be Upgraded up to 8 times', False, False, False, False, {effects.deal_attack_damage: (16, 1)}, 1),
    1133: ("Purgatory+", 2, 0, 3, 'Deal 30 damage to all enemies', False, False, False, False, {effects.deal_attack_damage: (30, 1)}, 3),
    1134: ("Parry+", 2, 1, 2, 'Gain 16 block. Whenever you are attacked this turn, apply 2 Vulnerable to the attacker', False, False, False, False, {effects.block_gain_card: (16, 1), effects.apply_buff: (['Parry'], [2])}, 0),
    1135: ("Deflect+", 2, 1, 2, 'Gain 16 block. Whenever you are attacked this turn, deal 6 damage back', False, False, False, False, {effects.block_gain_card: (16, 1), effects.apply_debuff: (['Deflect'], [6])}, 0),
    1136: ("Sever Soul+", 2, 1, 1, 'Exhaust all Ailments in hand. For every curse exhausted, gain 1 Strength and draw 2 card', False, False, False, False, {effects.hand_for_card_exhausted: ({3, 4}, {4}, [effects.apply_buff, effects.draw_cards], [(['Strength'], [1]), (2, )])}, 0),
    1137: ("Cursed Pact+", 2, 1, 1, 'Exhaust 1 card in your hand. Draw 3 cards', False, False, False, False, {effects.exhaust_from_hand: (1, ), effects.draw_cards: (3, )}, 0),
    1138: ("Power Through+", 2, 1, 0, 'Lose 3 HP. Gain 18 block, Add 1 Curse into the hand', False, False, False, False, {effects.hp_cost: (3, ), effects.block_gain_card: (18, 1), effects.add_card_to_pile: ('hand', 'weak curse', 1, 'na')}, 0),
    1139: ("Second wind+", 2, 1, 1, 'Exhaust all non-attack cards and gain 7 block for each card exhausted', False, False, False, False, {effects.hand_for_card_exhausted: ({1, 2, 3, 4}, {0, 1, 2, 3, 4}, [effects.block_gain_card], [(7, 1)])}, 0),
    1140: ("Conjour blade+", 2, 1, 0, 'Add a random attack card to your hand. It costs 0 this turn', False, False, False, False, {effects.add_card_to_pile: ('hand', 'atk', 1, (0, 'Turn'))}, 0),
    1141: ("Sinister appearance+", 2, 1, 0, 'Apply 2 Weak to all enemies', False, True, False, False, {effects.apply_debuff: (['Weak'], [2])}, 3),
    1142: ("Sentenal+", 2, 1, 1, 'Gain 8 block. If this card is exhausted, gain 3 Energy', False, False, False, False, {effects.block_gain_card: (8, 1), 'Exhausted': {effects.energy_manip: (3, )}}, 0),
    1143: ("Bloodletting+", 2, 1, 0, 'Lose 3 HP. Gain 3 Energy', False, False, False, False, {effects.hp_cost: (3, ), effects.energy_manip: (3, )}, 0),
    1144: ("Cursed Shield+", 2, 1, 1, 'Gain 20 block. Add 2 Curses to your hand', False, False, False, False, {effects.block_gain_card: (20, 1), effects.add_card_to_pile: ('hand', 'weak curse', 2, 'na')}, 0),
    1145: ("Cursed Aura+", 2, 1, 2, 'Apply 5 Weak and 5 Vulnerable to all enemies', False, True, False, False, {effects.apply_debuff: (['Weak', 'Vulnerable'], [5, 5])}, 3),
    1146: ("Disarm+", 2, 1, 1, 'Enemy loses 3 Strength', False, True, False, False, {effects.apply_debuff: (['-Strength'], [3])}, 1),
    1147: ("Entrench+", 2, 1, 1, 'Double the amount of block you have', False, False, False, False, {effects.double_block: (1, )}, 0),
    1148: ("Defensive Positioning+", 2, 1, 0, 'Gain 3 Blur', False, False, False, False, {effects.apply_buff: (['Blur'], [3])}, 0),
    1149: ("Battle Trance+", 2, 1, 0, 'Draw 4 cards. You can no longer draw cards this turn', False, False, False, False, {effects.draw_cards: (4, ), effects.apply_debuff: (['No Draw'], [1])}, 0),
    1150: ("Defensive Stance+", 2, 2, 1, 'Gain 4 Metalicize', False, False, False, False, {effects.apply_buff: (['Metalicize'], [4])}, 0),
    1151: ("Inflame+", 2, 2, 1, 'Gain 3 Strength', False, False, False, False, {effects.apply_buff: (['Strength'], [3])}, 0),
    1152: ("Curse Ward+", 2, 2, 2, 'Whenever you draw a Curse, gain 2 block and draw 1 card', False, False, False, False, {'Power': {'Draw Curse': {effects.block_gain_power: (2, ), effects.draw_cards: (1, )}}}, 0),
    1153: ("Feel no pain+", 2, 2, 1, 'Whenever you Exhaust a card, gain 4 block', False, False, False, False, {'Power': {'Exhaust': {effects.block_gain_power: (4, )}}}, 0),
    1154: ("Evolve+", 2, 2, 1, 'Whenever you draw an Ailment, draw 2 card', False, False, False, False, {'Power': {'Draw Negative': {effects.draw_cards: (2, )}}}, 0),
    1155: ("Transfer pain+", 2, 2, 1, 'Whenever you draw a Curse or Status, deal 8 damage to all enemies', False, False, False, False, {'Power': {'Draw Negative': {effects.deal_damage: (8, )}}}, 3),
    1156: ("Dark Embrace+", 2, 2, 1, 'Whenever a card is exhausted, draw 1 card', False, False, False, False, {'Power': {'Exhaust': {effects.draw_cards: (1, )}}}),
    1157: ("Devouring Blade+", 3, 0, 1, 'Deal 12 damage. If Fatal, Incrase your Max Hp by 4', False, True, False, False, {effects.feed: (12, 4)}, 1),
    1158: ("Void Strike+", 3, 0, 0, 'Deal 4 damage. Apply 4 Vulnerable. 4 Weak and 4 Poison', False, True, False, False, {effects.deal_attack_damage: (4, 1), effects.apply_debuff: (['Vulnerable', 'Weak', 'Poison'], [4, 4, 4])}, 1),
    1159: ("Cursed flames+", 3, 0, 2, 'Deal 28 to all enemies. Shuffle 2 Curses into the discard pile', False, False, False, False, {effects.deal_attack_damage: (28, 1), effects.add_card_to_pile: ('discard', 'weak curse', 2, 'na')}, 3),
    1160: ("Bloodlust+", 3, 0, 2, 'Deal 5 damage to all enemies. Heal HP equal to the unblocked damage dealt', False, True, False, False, {effects.reap: (5, )}, 3),
    1161: ("Black Wind+", 3, 0, 0, 'Deal 12 damage for each Curse in your hand. Retain', False, False, True, False, {effects.for_card_type_in_hand: (effects.deal_attack_damage, (12, 1), {4})}, 1),
    1162: ("Demonic Fire+", 3, 0, 2, 'Exhaust your hand. Deal 10 damage for each card exhausted', False, True, False, False, {effects.hand_for_card_exhausted: ({0, 1, 2, 3, 4}, {0, 1, 2, 3, 4}, [effects.deal_attack_damage], [(10, 1)])}, 1),
    1163: ("Generational Skill+", 3, 1, 0, 'Exhaust all cards in your hand, shuffle a Curse into the draw pile and draw 2 for each card exhausted. gain 1 Energy', False, True, False, False, {effects.hand_for_card_exhausted: ({0, 1, 2, 3, 4}, {0, 1, 2, 3, 4}, [effects.add_card_to_pile, effects.draw_cards], [('draw', 'weak curse', 1, 'na'), (2, )]), effects.energy_manip: (1, )}, 0),
    1164: ("Fey's Offering+", 3, 1, 0, 'Lose 6 HP. Draw 5 cards. Gain 2 Energy', False, True, False, False, {effects.hp_cost: (6, ), effects.draw_cards: (5, ), effects.energy_manip: (2, )}, 0),
    1165: ("Mirror image+", 3, 1, 1, 'Your next 2 attacks are played twice', False, False, False, False, {effects.apply_buff: (['Double Tap'], [2])}, 0),
    1166: ("Hallucinations+", 3, 1, 0, 'Add 1 card from your exhaust pile to your hand', False, True, False, False, {effects.place_card_in_loction: ('exhaust', 1, 'hand', 'na')}, 0),
    1167: ("Final Gambit+", 3, 1, "X", 'Exhaust EVERYTHING. Add X + 2 cards from your exhaust pile to your hand, they cost 0 this turn, You cannot play Final Gambit until the start of your next turn. At the end of your turn, Exhaust EVERYTHING. Exhaust', False, True, False, False, {effects.final_gambit: ('X', 2)}, 0),
    1168: ("Impervious+", 3, 1, 2, 'Gain 40 block. Exhaust', False, True, False, False, {effects.block_gain_card: (40, 1)}, 0),
    1169: ("Corruption Form+", 3, 2, 3, 'At the start of your turn, lose 1 HP and gain 4 Strength', False, False, False, False, {'Power': {'Turn Start': {effects.hp_cost: (1, ), effects.apply_buff: (['Strength'], [4])}}}, 0),
    1170: ("Phantom blades+", 3, 2, 1, 'At the start of your turn, gain 7 Vigour', False, False, False, False, {'Power': {'Turn Start': {effects.apply_buff: (['Vigour'], [7])}}}, 0),
    1171: ("Seeing red+", 3, 2, 1, 'Draw 2 cards at the start of turn and add a Curse to hand', True, False, False, False, {'Power': {'Turn Start': {effects.draw_cards: (2, ), effects.add_card_to_pile: ('hand', 'weak curse', 1, 'na')}}}, 0),
    1172: ("Clear mind+", 3, 2, 2, 'At the start of turn, you can exhaust a card from your hand to gain 8 block', False, False, False, False, {'Power': {'Turn Start': {effects.adapt: (1, )}}}, 0),
    1173: ("Corruption+", 3, 2, 2, 'Curses no longer have negative effects', True, False, False, False, {effects.remove_effect_from_type: (4, ), 'Power': None}, 0),
    1174: ("Eternal flames+", 3, 2, 0, 'Gain 3 Energy, Draw 4 cards. At the end of your turn, lose 2 HP', False, False, False, False, {effects.energy_manip: (3, ), effects.draw_cards: (4, ), 'Power': {'Turn End': {effects.lose_hp: (2, )}}}, 0),

    1232: ("Flaming Strike+2", 2, 0, 2, 'Deal 21 damage. Can be Upgraded up to 7 more times', False, False, False, False, {effects.deal_attack_damage: (21, 1)}, 1),
    1332: ("Flaming Strike+3", 2, 0, 2, 'Deal 27 damage. Can be Upgraded up to 6 more times', False, False, False, False, {effects.deal_attack_damage: (27, 1)}, 1),
    1432: ("Flaming Strike+4", 2, 0, 2, 'Deal 34 damage. Can be Upgraded up to 5 more time', False, False, False, False, {effects.deal_attack_damage: (34, 1)}, 1),
    1532: ("Flaming Strike+5", 2, 0, 2, 'Deal 42 damage. Can be Upgraded up to 4 more time', False, False, False, False, {effects.deal_attack_damage: (42, 1)}, 1),
    1632: ("Flaming Strike+6", 2, 0, 2, 'Deal 51 damage. Can be Upgraded up to 3 more time', False, False, False, False, {effects.deal_attack_damage: (51, 1)}, 1),
    1732: ("Flaming Strike+7", 2, 0, 2, 'Deal 61 damage. Can be Upgraded up to 2 more time', False, False, False, False, {effects.deal_attack_damage: (61, 1)}, 1),
    1832: ("Flaming Strike+8", 2, 0, 2, 'Deal 72 damage. Can be Upgraded up to 1 more time', False, False, False, False, {effects.deal_attack_damage: (72, 1)}, 1),
    1932: ("Flaming Strike+9", 2, 0, 2, 'Deal 84 damage', False, False, False, False, {effects.deal_attack_damage: (84, 1)}, 1),
}


