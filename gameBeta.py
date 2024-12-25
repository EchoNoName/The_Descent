import random
import card_data
import card_constructor
import effects
import combat_beta
import potion_data
import enemy_data
import map_generation
import reward_screen
import events
import math
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
        if character_class == 1:
            for i in range(5):
                self.deck.append(card_constructor.create_card(1000, card_data.card_info[1000]))
        if character_class == 1:
            for i in range(5):
                self.deck.append(card_constructor.create_card(1002, card_data.card_info[1002]))
        self.deck.append(card_constructor.create_card(1001, card_data.card_info[1001]))
        self.selected_cards = []
        self.gold = 100
        self.thieved = 0
        self.potions = [None, None, None]
        self.relics = []
        self.buffs = {'Strength': 0, 'Dexterity': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Double Tap': 0, 'Duplicate': 0, 'Draw Card': 0, 'Energized': 0, 'Next Turn Block': 0, 'Parry': 0, 'Deflect': 0}
        #Debuffs: Atrophy = lose dex at the end of turn
        self.debuffs = {'Vulnerable': 0, 'Weak': 0, 'Frail': 0, '-Strength': 0, '-Dexterity': 0, 'Atrophy': 0, 'Chained': 0, 'Poison': 0, 'No Draw': 0, 'Chaotic': 0, 'Last Chance': 0, 'Draw Reduction': 0, 'Parry': 0, 'Deflect': 0, 'Entangle': 0}
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
                            card_id = upgrade.id + 100
                            card_information = list(card_data.card_info[card_id])
                            card_information.extend([upgrade.bottled, upgrade.removable])
                            upgrade = card_constructor.create_card(card_id, card_information)
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
                                card_id = upgrade.id + 100
                                card_information = list(card_data.card_info[card_id])
                                card_information.extend([upgrade.bottled, upgrade.removable])
                                upgrade = card_constructor.create_card(card_id, card_information)
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
                                card_id = upgrade.id + 100
                                card_information = list(card_data.card_info[card_id])
                                card_information.extend([upgrade.bottled, upgrade.removable])
                                upgrade = card_constructor.create_card(card_id, card_information)
                                break
                    # If there is a upgrade, random;y pick cards until a valid card is upgraded
                else:
                    raise TypeError(f'Unknown Card Type: {card}')
            else:
                if card.id + 100 in card_data.card_info:
                    card_id = card.id + 100
                    card_information = list(card_data.card_info[card_id])
                    card_information.extend([card.bottled, card.removable])
                    card = card_constructor.create_card(card_id, card_information)
                    # If the card is referanced as an obj, upgrade it
                else:
                    raise KeyError(f'Card has no upgrade: {card.name}')
                    # Invalid upgrade
    
    def transform_card(self, cards = 'Selected'):
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            # for every card that needs to be transformed
            if card.type == 4:
                # If the card is a curse
                transform_id = random.choice(card_constructor.weak_curse + card_constructor.medium_curse + card_constructor.strong_curse)
                card_new = card_constructor.create_card(transform_id, card_data.card_info[transform_id])
                self.deck.remove(card)
                self.deck.append(card_new)
                # Transform into a random non special curse
            else:
                if self.character_class == 1:
                    transform_id = random.choice(card_constructor.attack_card_1 + card_constructor.skill_card_1 + card_constructor.power_card_1)
                    card_new = card_constructor.create_card(transform_id, card_data.card_info[transform_id])
                    self.deck.remove(card)
                    self.deck.append(card_new)
                    # Tranfrom into a card of the character class
                else:
                    return TypeError(f'Unknown card transform: {card}')
    
    def remove_card(self, cards = 'Selected'):
        '''Method for removing cards from the deck
        
        ### args:
            cards: the cards being removed, the selected cards by default'''
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            self.deck.remove(card)

    def duplicate_card(self, card = 'Selected'):
        '''Method for removing cards from the deck
        
        ### args:
            cards: the cards being removed, the selected cards by default'''
        if card == 'Selected':
            card = self.selected_cards
        new_card = copy.deepcopy(card)
        # Create a deep copy of the card being duplicated
        self.deck.append(new_card)
        # Add the copy to the deck

    def heal(self, amount):
        '''Method to heal the player by an amount or percentage
        
        ### args:
            amount: Int for a fixed value, string for percentage'''
        if isinstance(amount, str):
            # If its a string
            percentage = int(amount)
            percentage = percentage / 100
            healing_amount = math.floor(self.maxHp * percentage)
            if self.relics:
                for relic in self.relics:
                    healing_amount = relic.valueModificationEff('Healing', healing_amount)
            self.hp = min(self.maxHp, self.hp + healing_amount)
            # Add a percentage of of max hp to your own hp
        else:
            healing_amount = amount
            if self.relics:
                for relic in self.relics:
                    healing_amount = relic.valueModificationEff('Healing', healing_amount)
            self.hp = min(self.maxHp, self.hp + healing_amount)
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
        if self.relics:
            for relic in self.relics:
                amount = relic.valueModificationEff(debuff_type, amount)
        if amount == 0:
            return None
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
            amount = relic.valueModificationEff('HpLoss', amount)
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
            damage = relic.valueModificationEff('damageTaken', damage)
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
                    self.hp = relic.valueModificationEff('dead', self.maxHp)
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
    def __init__(self, player: Character, newRun = True, turtorial = True, ascsension = 0, map_info = None, act = 1, act_name = 'The Forest', room = [0, 0], roomInfo = None, combats_finished = 0, easyPool = [], normalPool = [], elitePool = [], boss = [], eventList = [], shrineList = [], rareChanceMult = 1, rareChanceOffset = -5, potionChance = 40, cardRewardOptions = 3, removals = 0, encounterChance = {'Combat': 10, 'Treasure': 2, 'Shop': 3}, mechanics = {'Intent': True, 'Ordered_Draw_Pile': False, 'Turn_End_Discard': True, 'Playable_Curse': False, 'Playable_Status': False, 'Exhaust_Chance': 100, 'Cards_per_Turn': False, 'Random_Combat': True, 'Insect': False, 'Block_Loss': False, 'X_Bonus': 0, 'Necro': False}, campfire = {'Rest': True, 'Smith': True}, eggs = {}):
        self.player = player
        if map_info != None:
            self.map, self.path, self.map_display = map_info
        else:
            self.map, self.path, self.map_display = map_generation.createMap(ascsension)
        self.act = act
        self.act_name = act_name
        self.room = room
        self.roomInfo = roomInfo
        self.combats_finished = combats_finished
        self.newRun = newRun
        self.turtorial = turtorial
        self.encounterChance = encounterChance
        self.mechanics = mechanics
        self.campfire = campfire
        if not self.newRun:
            self.easyPool = easyPool
            self.normalPool = normalPool
            self.elitePool = elitePool
            self.boss = boss
            self.eventList = eventList
            self.shrineList = shrineList
        else:
            self.easyPool = enemy_data.act_1_easy_pool()
            self.normalPool = enemy_data.act_1_normal_pool()
            self.elitePool = enemy_data.act_1_elite_pool()
            self.boss = enemy_data.act_1_boss_pool()
            self.eventList = self.generate_event_list
            # ADDED EVENTS AND SHRINES
            # More to be added
        self.combat_pool_details = {}
        if self.act == 1:
            self.combat_pool_details = enemy_data.generate_act1_pools()
        self.rareChanceMult = rareChanceMult
        self.rareChanceOffset = rareChanceOffset
        self.potionChance = potionChance
        self.cardRewardOptions = cardRewardOptions
        self.event = None
        self.combat = None
        self.shop = None
        self.treasure = None
        self.reward = None
        self.removals = removals
        self.lastInstance = None
        self.eggs = eggs
        self.instances = [self.shop, self.combat, self.event, self.treasure, self.reward]
    
    def runStart(self):
        if self.newRun == True:
            self.neowBlessing()
        else:
            return # placeholder

    def neowBlessing(self):
        self.eventList = self.generate_event_list()
        for ds in reversed(self.map_display):
            print(ds)
        print('    0 1 2 3 4 5 6')
        entrances = self.map[1]
        room_type = {
            1: 'Normal Combat',
            2: 'Occurance',
            3: 'Elite Combat',
            4: 'Shop',
            5: 'Treasure',
            6: 'Campfire'
        }
        for room, encounter_type in entrances.items():
            print(f'Floor 1, Room {room}: {room_type[encounter_type]}')
        room = int(input('Type the room number you wish to enter'))
        self.room = [1, room]
        room_entered = self.map[1][room]
        if room_entered == 1:
            enemies = self.get_enemies()
            self.generage_combat_instace(enemies, 'normal')
            self.start_combat()
        self.mapNav()

    def mapNav(self):
        room_type = {
            1: 'Normal Combat',
            2: 'Occurance',
            3: 'Elite Combat',
            4: 'Shop',
            5: 'Treasure',
            6: 'Campfire'
        }
        for ds in reversed(self.map_display):
            print(ds)
        print('    0 1 2 3 4 5 6')
        for room in self.path[(self.room[0], self.room[1])]:
            print(f'Floor {room[0]}, Room {room[1]}: {room_type[self.map[room[0]][room[1]]]}')
        room = input('Type the room number you wish to enter or Back')
        if room == 'Back':
            if self.lastInstance not in {'E', 'C'}:
                if self.lastInstance == 'S':
                    self.shop.interact()
                else:
                    self.treasure.interact()
            else:
                print('Invalid')
                self.mapNav()
        else:
            room = int(room)
            self.room = [self.room[0] + 1, room]
            room_entered = self.map[self.room[0]][room]
            if room_entered == 1:
                enemies = self.get_enemies()
                self.generage_combat_instace(enemies, 'normal')
                self.start_combat()
            elif room_entered == 2:
                self.unknown_location()
            elif room_entered == 3:
                enemies = self.get_enemies('elite')
                self.generage_combat_instace(enemies, 'Elite')
                self.start_combat()
            elif room_entered == 4:
                self.shop = shop.Shop(self)
                self.start_shop()
            elif room_entered == 5:
                self.treasure = treasure.Treasure(self)
                self.start_treasure()
            self.mapNav()
    
    def generate_reward_screen_instance(self, reward_type, set_reward = False, additonal_rewards = {}):
        '''Method to generate a reward screen instance
        
        ### args:
            reward_type: the type of event that this reward screen correspond to, Ex: normal combat, events
            set_reward: predetermained loot, used for events and special occasions
            additional_rewards: additive rewards from certain effects'''
        if self.player.relics:
            for relic in self.player.relics:
                additonal_rewards = relic.additionalRewards(reward_type, additonal_rewards)
        self.reward = reward_screen.RewardScreen(self, self.player.character_class, self.rareChanceMult, self.rareChanceOffset, self.potionChance, self.cardRewardOptions, reward_type, set_reward, additonal_rewards)
        self.reward.generate_rewards()

    def bonusEff(self, event):
        if self.player.relics:
            for relic in self.player.relics:
                # Go through all relics
                relic.eventBonus(event, self.run)
                # Execute condisional effects of relics

    def card_reward_option_mod(self, mod):
        '''Method to increase or decrease the amount of cards avalible at card rewards'''
        self.cardRewardOptions += mod

    def campfire_restrict(self, action):
        '''Method to Disable an action at campfires'''
        self.campfire[action] = False

    def campfire_add_action(self, action):
        '''Method to add an action to a campfire'''
        self.campfire[action] = True

    def potion_chance_change(self, mod):
        '''Method to change the potion chance'''
        self.potionChance += mod

    def mechanics_change(self, mechanic, details): 
        '''Method to modify core mechanics of the game that relates to combat
        
        ### args:
            mechanic: the mechanic that is being changed
            details: what the mechanic will be changed to'''
        self.mechanics[mechanic] = details
        # Change the mechanic

    def gold_modification(self, amount):
        '''Method to change amount of gold the player has
        
        ### args:
            amount: amount of gold gained or lost'''
        for relic in self.player.relics:
            amount = relic.valueModificationEff('gold', amount)
        self.player.gold += amount
        # Add amount

    def card_pickup_from_id(self, card_id: int):
        '''Method for adding a card directly to the deck
        
        ### args:
            card_id: the card id'''
        card = card_constructor.create_card(card_id, card_data.card_info[card_id])
        if card.type == 4:
            if self.player.relics:
                for relic in self.player.relics:
                    card = relic.valueModificationEff('curse', card)
        if card != None:
            self.card_pickup(card)

    def card_pickup(self, card: card_constructor.Card):
        '''Method for picking up card rewards
        
        ### args:
            card: the card object being added'''
        if card.type in self.eggs:
            if card.id + 100 in card_data.card_info:
                card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
        self.player.deck.append(card)

    def egg_relic(self, type: int):
        '''Method to add a type of card to egg stash
        
        ### args: 
            type: card type id for the eggs'''
        self.egg_relic.add(type)

    def relic_pickup(self, relic):
        self.player.relics.append(relic)
        relic.pickUp(self)
    
    def potion_pickup(self, potion):
        if self.player.potions.count(None) > 0:
            for relic in self.player.relics:
                potion = relic.valueModificationEff('potion', potion)
            self.player.potions[self.player.potions.index(None)] = potion
            return True
        else:
            print('Potion Slots Full!')
            return False

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
        self.bonusEff('Used Potion')
        self.player.potions.remove(potion)

    def bottle(self):
        '''Method to add bottled tag to selected cards'''
        if self.player.selected_cards:
            for card in self.player.selected_cards:
                card.bottled = True

    def get_enemies(self, combat = 'normal'):
        enemies_constructors = []
        cap = 0
        if self.act == 1:
            cap = 3
        if combat == 'elite':
            enemies_constructors = self.combat_pool_details['elite'][self.elitePool[-1]]
            self.elitePool.pop(-1)
        elif combat == 'boss':
            enemies_constructors = self.combat_pool_details['boss'][self.boss[-1]]
        elif self.combats_finished <= cap:
            enemies_constructors = self.combat_pool_details['easy'][self.easyPool[-1]]
            self.easyPool.pop(-1)
        else:
            enemies_constructors = self.combat_pool_details['normal'][self.normalPool[-1]]
            self.normalPool.pop(-1)
        enemies = []
        for enemy_class in enemies_constructors:
            enemies.append(enemy_class())
        return enemies

    def generage_combat_instace(self, enemies, combatType):
        self.combat = combat_beta.Combat(self, self.player, copy.deepcopy(self.player.deck), enemies, combatType)

    def start_combat(self, set_rewards = False):
        self.lastInstance = 'C'
        self.combat.combat_start()
        self.combats_finished += 1
        combat_type_conversion = {
            'normal': 0,
            'Normal': 0,
            'Elite': 1,
            'Boss': 2,
        }
        self.generate_reward_screen_instance(combat_type_conversion[self.combat.combat_type], set_rewards, {})
        self.reward.listRewards()

    def start_treasure(self):
        self.lastInstance = 'T'
        self.treasure.start_event()
    
    def start_shop(self):
        self.lastInstance = 'S'
        self.shop.generate_wares()
        self.shop.interact()

    def start_event(self):
        self.lastInstance = 'E'
        self.event.start_event()

    def generate_event_list(self):
        '''Method to generate the list of random events the player will encouter'''
        possible_events = list(events.events1.keys())
        encounter_list = []
        combat_chance = 10
        treasure_chance = 2
        shop_chance = 3
        while possible_events:
            rng = random.randint(1, 100)
            if rng <= combat_chance:
                encounter_list.append('combat')
                combat_chance = 10
                treasure_chance += 2
                shop_chance += 3
            elif rng <= combat_chance + treasure_chance:
                encounter_list.append('treasure')
                treasure_chance = 2
                combat_chance += 10
                shop_chance += 3
            elif rng <= combat_chance + treasure_chance + shop_chance:
                encounter_list.append('shop')
                combat_chance += 10
                treasure_chance += 2
                shop_chance = 3
            else:
                combat_chance += 10
                treasure_chance += 2
                shop_chance += 3
                rng = random.randint(1, 100)
                if rng <= 95:
                    event_pick = random.choice(possible_events)
                    encounter_list.append(event_pick)
                    possible_events.remove(event_pick)
                else:
                    event_pick = random.choice(possible_events)
                    encounter_list.append(event_pick)
                    possible_events.remove(event_pick)
                    # encounter_list.append('shrine') # Placeholder
        return encounter_list

    def unknown_location(self):
        event = self.eventList[-1]
        self.eventList.pop(-1)
        while event == 'combat' and self.mechanics['Random_Combat'] == False:
            self.eventList.pop(-1)
            event = self.eventList[-1]
        if event == 'combat':
            enemies = self.get_enemies()
            self.generage_combat_instace(enemies, 'normal')
            self.start_combat()
        elif event == 'treasure':
            self.treasure = treasure.Treasure(self) # placeHolder to be continued
            self.start_treasure()
        elif event == 'shop':
            self.shop = shop.Shop(self)
            self.start_shop()
        else:
            self.event = events.events1[event](self.player, self)
            self.start_event()