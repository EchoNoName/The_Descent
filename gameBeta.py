import random
import card_data
import card_constructor
import effects
import combat_beta
import potion_data
import enemy_data
import map_generation
import events
import shop
import treasure
import copy

Instances = []

class Character:
    def __init__(self, name, maxHp, character_class):
        self.name = name
        self.maxHp = maxHp
        self.hp = maxHp
        self.character_class = character_class
        self.block = 0
        self.deck = []
        self.selected_cards = []
        self.gold = 100
        self.thieved = 0
        self.potions = [None, None, None]
        self.relics = []
        self.buffs = {'Strength': 0, 'Dexterity': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Double Tap': 0, 'Duplicate': 0, 'Draw Card': 0, 'Energized': 0, 'Next Turn Block': 0, 'Parry': 0, 'Deflect': 0}
        #Debuffs: Atrophy = lose dex at the end of turn
        self.debuffs = {'Vulnerable': 0, 'Weak': 0, 'Frail': 0, '-Strength': 0, '-Dexterity': 0, 'Atrophy': 0, 'Chained': 0, 'Poison': 0, 'No Draw': 0, 'Chaotic': 0, 'Last Chance': 0, 'Draw Reduction': 0, 'Parry': 0, 'Deflect': 0}
        self.bottled = []
    
    def __str__(self):
        '''Override for String representation'''
        return f'{self.name}   HP: {self.hp}/{self.maxHp}   Block: {self.block}   Gold: {self.gold}   Potions: {self.potions}   Relics: {self.relics}'

    def __repr__(self):
        return self.__str__()

    def combat_info(self):
        buffs = []
        for buff, amount in self.buffs.items():
            if amount > 0:
                buffs.append(f'{buff}: {amount}')
        buffs = str(', '.join(buffs))
        debuffs = []
        for debuff, amount in self.debuffs.items():
            if amount > 0:
                debuffs.append(f'{debuff}: {amount}')
        debuffs = str(', '.join(debuffs))
        return self.__repr__() + f'   Buffs: {buffs}   Debuffs: {debuffs}'

    def gold_modification(self, amount):
        '''Method to change amount of gold the player has
        
        ### args:
            amount: amount of gold gained or lost'''
        self.gold += amount
        # Add amount

    def relic_pickup(self, relic):
        self.relics.append(relic)
        relic.applyEff('pickup', None)
    
    def potion_pickup(self, potion):
        if self.potions.count(None) > 0:
            self.potions[self.potions.index(None)] = potion
    
    def gain_rand_potion(self):
        '''Method for filling a empty slot with a random potion
        '''
        potion_name, potion_details = random.choice(list(potion_data.potions.items()))
        potion = potion_data.Potion(potion_name, *potion_details)
        self.potion_pickup(potion)
        # Fill the an empty potion slot with a random potion if there is one
    
    def use_potion(self, potion):
        '''Method to use non combat based potions
        
        ### args:
            potion: The potion to be used
        '''
        i = 1
        for relic in self.relics:
            if relic.effect_type == 'Sacred Bark':
                i = 2
                break
        for times in range(0, i):
            for effect, details in potion.effect.items():
                    effect(*details, self)
                # Execute effects
        self.potions.remove(potion)
    
    def upgrade_card(self, cards = 'Selected'):
        '''Method to upgrading cards
        
        ### args:
            cards: cards being upgraded'''
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            if isinstance(card, str):
                # If a random card of a type is being upgraded
                if card == 'Card':
                    # Random card
                    validUpgrades = False
                    for player_card in self.deck:
                        if player_card.id + 100 in card_data.card_info:
                            validUpgrades = True
                            break
                    # Check if there is a card that has an upgrade
                    while validUpgrades:
                        # If there is
                        upgrade = random.choice(self.deck)
                        # Randomly pick one
                        if upgrade.id + 100 in card_data.card_info:
                            upgrade.upgrade_self()
                            validUpgrades -= 1
                            # If it can be upgraded, upgrade it and end the loop
                            break
                elif card == 'Attack':
                    # Random Attack
                    validUpgrades = False
                    for player_card in self.deck:
                        if player_card.type == 0 and player_card.id + 100 in card_data.card_info:
                            validUpgrades = True
                            break
                    # Check if there is an attack card avalible to upgrade
                    while validUpgrades:
                        upgrade = random.choice(self.deck)
                        if upgrade.type == 0:
                            # Picks a random card and checks if its the right type
                            if upgrade.id + 100 in card_data.card_info:
                                upgrade.upgrade_self()
                                validUpgrades -= 1
                                # If it can be upgraded, upgrade it and end the loop
                                break
                elif card == 'Skill':
                    # Random Skill
                    validUpgrades = False
                    for player_card in self.deck:
                        if player_card.type == 1 and player_card.id + 100 in card_data.card_info:
                            validUpgrades = True
                            break
                    # Check if there is a valid skill to be upgraded
                    while validUpgrades:
                        upgrade = random.choice(self.deck)
                        if upgrade.type == 1:
                            if upgrade.id + 100 in card_data.card_info:
                                upgrade.upgrade_self()
                                break
                    # If there is a upgrade, random;y pick cards until a valid card is upgraded
                else:
                    raise TypeError(f'Unknown Card Type: {card}')
            else:
                if card.id + 100 in card_data.card_info:
                    card.upgrade_self()
                    # If the card is referanced as an obj, upgrade it
                else:
                    raise KeyError(f'Card has no upgrade: {card.name}')
                    # Invalid upgrade
    
    def transform(self, cards = 'Selected'):
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            # for every card that needs to be transformed
            if card.type == 4:
                # If the card is a curse
                transform_id = random.choice(card_constructor.weak_curse + card_constructor.medium_curse + card_constructor.strong_curse)
                card = card_constructor.create_card(transform_id, card_data.card_info[transform_id])
                # Transform into a random non special curse
            else:
                if self.character_class == 1:
                    transform_id = random.choice(card_constructor.attack_card_1 + card_constructor.skill_card_1 + card_constructor.power_card_1)
                    card = card_constructor.create_card(transform_id, card_data.card_info[transform_id])
                    # Tranfrom into a card of the character class
                else:
                    return TypeError(f'Unknown card transform: {card}')

    def heal(self, amount):
        '''Method to heal the player by an amount or percentage
        
        ### args:
            amount: Int for a fixed value, string for percentage'''
        if isinstance(amount, str):
            # If its a string
            percentage = int(amount)
            percentage = percentage / 100
            self.hp = min(self.maxHp, self.hp + int(self.maxHp * percentage))
            # Add a percentage of of max hp to your own hp
        else:
            self.hp = min(self.maxHp, self.hp + amount)
            # Add fixed amount of hp up to max hp
    
    def increase_max_hp(self, amount):
        '''Method for increasing max hp from effects
        
        ### args:
            amount = Amount to increase by'''
        self.maxHp += amount
        self.hp += amount
        # Increase max hp by amount, when max hp is gained the equal amount of hp is gained

    def gain_block_card(self, amount):
        '''Getting block from playing cards
        
        ### args:
            amount: amount gained'''
        self.block += amount + self.buffs['Dexterity']
        # add more block and adding the dexterity bonus
    
    def gain_block_power(self, amount):
        '''gaining block from powers or some other passive effects
        
        ### args: 
            amount: amount gained'''
        self.block += amount
        # Add more block
    
    def gain_buff(self, buff_type, amount):
        '''Method for gaining buffs
        
        ### args:
            buff_type: The type of buff being gained
            amount: amount being gained
        '''
        if buff_type not in {'Strength', 'Dexterity'}:
            # If its not Str or Dex
            self.buffs[buff_type] += amount
            # Just add the amount
        else:
            # If it is
            if self.debuffs['-' + buff_type] > 0:
                self.debuffs['-' + buff_type] -= amount
                if self.debuffs['-' + buff_type] < 0:
                    self.buffs[buff_type] = -self.debuffs['-' + buff_type]
                    self.debuffs['-' + buff_type] = 0
            else:
                self.buffs[buff_type] += amount
            # Accounts for negative Str or Dex when adding the buffs
        # Add amount to corresponding buff
    
    def lose_buff(self, buff_type, amount):
        '''Method for losing buffs
        
        ### args:
            buff_type: type of buff being lost
            amount: amount being lost
        '''
        self.buffs[buff_type] -= amount
        # Subtract the amount
        if self.buffs[buff_type] < 0:
            # if it goes below 0
            if '-' + buff_type in self.debuffs:
                # check if can be negative
                self.debuffs['-' + buff_type] = self.buffs[buff_type]
                # Apply the negative debuff
            self.buffs[buff_type] = 0
            # Set amount of buffs to 0
    
    def gain_debuff(self, debuff_type, amount):
        '''Method for gaining debuffs
        
        ### args:
            buff_type: The type of debuff being gained
            amount: amount being gained
        '''
        if self.buffs['Artifact'] > 0:
            # If player has artifact
            self.buffs['ArtiFact'] -= 1
            # Lose 1 artifact and negate the debuff
        elif debuff_type == "No Draw" or debuff_type == "Chaotic" or debuff_type == 'Last Chance':
            # If its non stackable
            self.debuffs[debuff_type] = 1
            # Make the debuff 1
        elif debuff_type in {'-Strength', '-Dexterity'}:
            # If its Str and Dex where the player can have positive values in buffs
            self.lose_buff(debuff_type[1:], amount)
            # use the lose buff method instead
        else:
            self.debuffs[debuff_type] += amount
            # Add the amount to debuff
    
    def lose_buff(self, buff_type, amount):
        '''Method for losing buffs
        
        ### args:
            buff_type: type of buff being lost
            amount: amount being lost
        '''
        self.buffs[buff_type] -= amount
        # Subtract the amount
        if self.buffs[buff_type] < 0:
            # if it goes below 0
            if '-' + buff_type in self.debuffs:
                # check if can be negative
                self.debuffs['-' + buff_type] = -self.buffs[buff_type]
                # Apply the negative debuff
            self.buffs[buff_type] = 0
            # Set amount of buffs to 0

    def hp_loss(self, amount):
        for relic in self.relics:
            amount = relic.applyEff('HpLoss', amount)
        self.hp -= amount
        if amount > 0:
            if self.died == True:
                return 'GG' # Placeholder
            return True
        else:
            return False
    
    def hp_recovery(self, amount):
        self.hp = min(self.hp + amount, self.maxHp)

    def damage_taken(self, damage):
        '''
        Handles damage taken by the character, applying block reduction and relic effects.
        '''
        damage = damage
        # Applies relic effects that reduce damage taken
        for relic in self.relics:
            damage = relic.applyEff('damageTaken', damage)
        self.block -= damage
        if self.block >= 0:
            return 0
        else:
            if self.buffs['Plated Armour'] > 0:
                self.buffs['Plated Armour'] -= 1
            # Remove 1 plated armour for taking damage
            damage = -self.block
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            return self.hp_loss(damage)
        
    def true_damage_taken(self, damage):
        '''
        Handles taking true damage that is uneffected by debuffs
        '''
        damage = damage
        self.block -= damage
        # Deal damage to block first
        if self.block < 0:
            # If block wasn't enough
            damage = -self.block
            # Update damage to only amount unblocked
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            # Update entity status
            self.hp_loss(damage)
            # Hp loss
    
    def died(self):
        if self.hp <= 0:
            for relic in self.relics:
                if relic.condition == 'dead' and relic.used == False:
                    self.hp = relic.applyEff('dead', self.maxHp)
                    relic.used = True
                    return False
            return True
        else:
            return False
        
classes = {
    1: ('Wandering Samerai', 80, 1)
}

def main_menu():
    main = True
    while main:
        print('Selected any of the below options')
        print('1: New Run')
        print('2: Card Library')
        # Other options to be added
        input = int(input(''))
        if input == 1:
            return 'Run'
        elif input == 2:
            return 'Cards'
        else:
            print('Invalid Menu Option')
        # To be continued

class Run:
    def __init__(self, player, ascsension = 0, map_info = None, act = 1, act_name = 'The Forest', room = [0, 0], roomInfo = None, easyPool = [], normalPool = [], elitePool = [], boss = [], eventList = [], shrineList = [], rareChanceOffset = -5, newRun = True, turtorial = True):
        self.player = player
        if map_info != None:
            self.map, self.path, self.map_display = map_info
        else:
            self.map, self.path, self.map_display = map_generation.createMap(ascsension)
        self.act = act
        self.act_name = act_name
        self.room = room
        self.roomInfo = roomInfo
        self.newRun = newRun
        self.turtorial = turtorial
        if not self.newRun:
            self.easyPool = easyPool
            self.normalPool = normalPool
            self.elitePool = elitePool
            self.boss = boss
            self.eventList = eventList
            self.shrineList = shrineList
            self.rareChanceOffset = rareChanceOffset
        else:
            self.easyPool = enemy_data.act_1_easy_pool()
            self.normalPool = enemy_data.act_1_pool()
            self.elitePool = enemy_data.act_1_elite()
            self.boss = enemy_data.act_1_boss()
            # ADDED EVENTS AND SHRINES
            self.rareChanceOffset = rareChanceOffset
            # More to be added
        self.event = None
        self.combat = None
        self.shop = None
        self.treasure = None
        self.instances = [self.shop, self.combat, self.event, self.treasure]
    
    def runStart(self):
        if self.newRun == True:
            self.neowBlessing()
        else:
            return # placeholder

    def neowBlessing(self):
        return # Placeholder

    def mapNav(self):
        return # Placeholder
    

#while combat.combat_active == True:
#    if combat.combat_active == True:
#        combat.player_turn_start()
#    if combat.combat_active == True:
#        combat.player_turn()
#    if combat.combat_active == True:
#        combat.player_turn_end()
#    if combat.combat_active == True:
#        combat.enemy_turn_start()
#    if combat.combat_active == True:
#        combat.enemy_action()
#    if combat.combat_active == True:
#        combat.enemy_turn_end()



