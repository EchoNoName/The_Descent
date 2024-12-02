import random
import effects

class Enemy():
    def __init__(self) -> None:
        pass

    def damage_taken(self, damage):
        '''
        Handles damage taken by the entity
        '''
        damage = damage
        self.block -= damage
        # Deal damage to block first
        if self.block >= 0:
            # If there is still block left or exacly enough block was spent
            return 0
            # return 0 for no attack damage dealt
        else:
            damage = -self.block
            # Update damage to only amount unblocked
            if self.buffs['Plated Armour'] > 0:
                self.buffs['Plated Armour'] -= 1
            # Remove 1 plated armour for taking damage 
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            # Update entity status
            return self.hp_loss(damage)
            # Hp loss
        
    def hp_loss(self, amount):
        '''Handles enemy losing Hp in anyway
        
        ### args: 
            amount: The amount of hp being lost
        
        ### returns: 
            the amount of hp lost, accounting for negatives'''
        self.hp -= amount
        # Subtract amount from hp
        if amount > 0:
            if self.died == True:
                return amount + self.hp
            else:
                return amount
        else:
            return 0
        # Returns actual amount of hp loss 

    def gain_block(self, block):
        '''Getting more block
        
        ### args:
            block: amount being gained'''
        self.block += block
        # Add to block

    def gain_buff(self, buff_type, amount):
        '''Function for gaining buffs
        
        ### args:
            buff_type: The type of buff being gained
            amount: amount being gained
        '''
        if buff_type not in {'Strength', 'Dexterity'}:
            # If its not Str or Dex
            self.buff[buff_type] += amount
            # Just add the amount
        else:
            # If it is
            if self.debuff['-' + buff_type] > 0:
                self.debuff['-' + buff_type] -= amount
                if self.debuff['-' + buff_type] < 0:
                    self.buff[buff_type] = -self.debuff['-' + buff_type]
                    self.debuff['-' + buff_type] = 0
            else:
                self.buff[buff_type] += amount
            # Accounts for negative Str or Dex when adding the buffs
        # Add amount to corresponding buff
    
    def lose_buff(self, buff_type, amount):
        '''Function for losing buffs
        
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
        '''Function for gaining debuffs
        
        ### args:
            buff_type: The type of debuff being gained
            amount: amount being gained
        '''
        if self.buffs['Artifact'] > 0:
            # If artifact is present
            self.buffs['ArtiFact'] -= 1
            # Subtrack 1 from artifact and negate the debuff
        elif debuff_type in {'-Strength', '-Dexterity'}:
            # If its Str or Dex
            self.lose_buff(debuff_type[1:], amount)
            # Use the lose_buff funtion instead
        else:
            self.debuffs[debuff_type] += amount
            # Add the amount to debuff
    
    def lose_debuff(self, debuff_type, amount):
        '''Function for Losing debuffs
        
        ### args:
            debuff_type: The type of debuff being lost
            amount: the amount being lost
        '''
        self.debuffs[debuff_type] -= amount
        # Subtract amount from debuff
        if self.debuffs[debuff_type] < 0:
            # if its below 0
            self.debuffs[debuff_type] = 0
            # Make it 0 instead

    def died(self, combat):
        '''Checks if entity is dead'''
        if self.hp <= 0:
            return True
        else:
            return False

class SmallGreenSlime(Enemy):
    def __init__(self, max_hp = random.randint(8, 12)):
        super().__init__()
        self.name = 'Small Green Slime'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (3, 1)}, 1, 'Attack'),
            'Lick': ({effects.apply_debuff: (['Weak'], [1])}, 1, 'Small Debuff')
        }
        self.intent = None
        self.actions_done = []
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if combat.turn == 1:
            # If its turn 1
            if random.randint(0, 1) == 0:
                self.intent = self.actions['Tackle']
                self.actions_done.append('Tackle')
            else:
                self.intent = self.actions['Lick']
                self.actions_done.append('Lick')
            # 50/50 Which move to use
        else:
            if self.actions_done[-1] == 'Tackle':
                self.intent = self.actions['Lick']
                self.actions_done.append('Lick')
            else:
                self.intent = self.actions['Tackle']
                self.actions_done.append('Tackle')
            # Alternates moves
        return self.intent

class MediumGreenSlime(Enemy):
    def __init__(self, max_hp = random.randint(28, 32)):
        super().__init__()
        self.name = 'Medium Green Slime'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (10, 1)}, 1, 'Attack'),
            'Lick': ({effects.apply_debuff: (['Weak'], [1])}, 1, 'Small Debuff'),
            'Corrosive Spit': ({effects.deal_attack_damage: (7, 1), effects.add_card_to_pile: ('draw', 50, 1, 'na')}, 1, 'Attack Debuff')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 40:
                # 40% Chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Tackle' == self.actions_done[-1] and 'Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Tackle'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            elif rng <= 70:
                # 30% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Corrosive Spit' == self.actions_done[-1] and 'Corrosive Spit' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Corrosive Spit'
                            self.actions_done.append(action)
                    else:
                        action = 'Corrosive Spit'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

class LargeGreenSlime(Enemy):
    def __init__(self, max_hp = random.randint(65, 69)):
        super().__init__()
        self.name = 'Large Green Slime'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (16, 1)}, 1, 'Attack'),
            'Lick': ({effects.apply_debuff: (['Weak'], [2])}, 1, 'Small Debuff'),
            'Corrosive Spit': ({effects.deal_attack_damage: (11, 1), effects.add_card_to_pile: ('draw', 50, 2, 'na')}, 1, 'Attack Debuff'),
            'Split': ({effects.split: ('Green', )}, 0, 'Special')
        }
        self.intent = None
        self.buffs = {'Split': 1, 'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 40:
                # 40% Chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Tackle' == self.actions_done[-1] and 'Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Tackle'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            elif rng <= 70:
                # 30% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Corrosive Spit' == self.actions_done[-1] and 'Corrosive Spit' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Corrosive Spit'
                            self.actions_done.append(action)
                    else:
                        action = 'Corrosive Spit'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def died(self, combat):
        '''Override function for the died function, used to determain if the slime will split'''
        if self.hp <= 0:
            # If the slime has no hp left
            return True
            # They have died
        elif self.hp <= self.max_hp // 2 and self.intent[2] != 'Special':
            # If the slime is below half HP and not splitting
            self.intent = self.actions['Split']
            # Slime intends splits
            return False
            # Not dead yet
        else:
            return False
            # Not dead yet

class SmallBlueSlime(Enemy):
    def __init__(self, max_hp = random.randint(10, 14)) -> None:
        super().__init__()
        self.name = 'Small Blue Slime'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (5, 1)}, 1, 'Attack'),
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Tackle']
        return self.intent

class MediumBlueSlime(Enemy):
    def __init__(self, max_hp = random.randint(28, 32)):
        super().__init__()
        self.name = 'Medium Blue Slime'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Lick': ({effects.apply_debuff: (['Frail'], [1])}, 1, 'Small Debuff'),
            'Flame Tackle': ({effects.deal_attack_damage: (8, 1), effects.add_card_to_pile: ('draw', 50, 1, 'na')}, 1, 'Attack Debuff')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 70:
                # 70% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Flame Tackle' == self.actions_done[-1] and 'Flame Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Flame Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Flame Tackle'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

class LargeBlueSlime(Enemy):
    def __init__(self, max_hp = random.randint(64, 70)):
        super().__init__()
        self.name = 'Large Blue Slime'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Lick': ({effects.apply_debuff: (['Frail'], [2])}, 1, 'Small Debuff'),
            'Flame Tackle': ({effects.deal_attack_damage: (16, 1), effects.add_card_to_pile: ('draw', 50, 2, 'na')}, 1, 'Attack Debuff'),
            'Split': ({effects.split: ('Blue', )}, 0, 'Special')
        }
        self.intent = None
        self.buffs = {'Split': 1, 'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 70:
                # 70% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Flame Tackle' == self.actions_done[-1] and 'Flame Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Flame Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Flame Tackle'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def died(self, combat):
        '''Override function for the died function, used to determain if the slime will split'''
        if self.hp <= 0:
            # If the slime has no hp left
            return True
            # They have died
        elif self.hp <= self.max_hp // 2 and self.intent[2] != 'Special':
            # If the slime is below half HP and not splitting
            self.intent = self.actions['Split']
            # Slime intends splits
            return False
            # Not dead yet
        else:
            return False
            # Not dead yet

class SneakyGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Sneaky Goblin'
        self.max_hp = random.randint(10, 14)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Puncture': ({effects.deal_attack_damage: (9, 1)}, 1, 'Attack'),
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Puncture']
        # Only has one move
        return self.intent

class FatGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Fat Goblin'
        self.max_hp = random.randint(13, 17)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Smash': ({effects.deal_attack_damage: (4, 1), effects.apply_debuff: (['Weak'], [1])}, 1, 'Debuff Attack'),
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Smash']
        # Only has one move
        return self.intent

class MadGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Mad Goblin'
        self.max_hp = random.randint(20, 24)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Scratch': ({effects.deal_attack_damage: (4, 1)}, 1, 'Attack'),
        }
        self.intent = None
        self.buffs = {'Anger': 1, 'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def hp_loss(self, amount):
        '''Handles enemy losing Hp in anyway
        
        ### args: 
            amount: The amount of hp being lost
        
        ### returns: 
            the amount of hp lost, accounting for negatives'''
        self.hp -= amount
        # Subtract amount from hp
        if amount > 0:
            self.gain_buff('Strength', 1)
            # From anger buff
            if self.died == True:
                return amount + self.hp
            else:
                return amount
        else:
            return 0
        # Returns actual amount of hp loss 
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Scratch']
        # Only has one move
        return self.intent

class ShieldGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Shield Goblin'
        self.max_hp = random.randint(12, 15)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Protect': ({effects.enemy_block_gain: (7, )}, 2, 'Block'),
            'Shield Bash': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if len(combat.enemies) > 1:
            self.intent = self.actions['Protect']
        else:
            self.intent = self.actions['Shield Bash']
        # Protect if there are other enemies, attack if there isn't
        return self.intent

class InfestedCorpes(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Infested Corpes'
        self.max_hp = random.randint(22, 28)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Grow': ({effects.apply_buff: (['Strength'], [3])}, 0, 'Buff')
        }
        self.intent = None
        self.buffs = {'Infestation': 2, 'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 60:
                # 60% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Bite' == self.actions_done[-1] and 'Bite' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Bite'
                            self.actions_done.append(action)
                    else:
                        action = 'Bite'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Grow' == self.actions_done[-1]:
                            continue
                        else:
                            action = 'Grow'
                            self.actions_done.append(action)
                    else:
                        action = 'Grow'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

    def died(self, combat):
        '''Override function for the died function, used to determain if the slime will split'''
        if self.hp <= 0:
            # If the enemy has no hp left
            combat.player.gain_debuff('Vulnerable', 2)
            return True
            # They have died
        else:
            return False
            # They alive

class Cultist(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Cultist'
        self.max_hp = random.randint(48, 54)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Dark Strike': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Incantation': ({effects.apply_buff: (['Ritual'], [3])}, 0, 'Buff')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if combat.turn == 1:
            # if its the first turn
            self.intent = self.actions['Incantation']
            # Use incantation
            return self.intent
        else:
            self.intent = self.actions['Dark Strike']
            # Use dark strike
            return self.intent

class RedArachnid(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Red Arachnid'
        self.max_hp = random.randint(46, 52)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Stab': ({effects.deal_attack_damage: (12, 1)}, 1, 'Attack'),
            'Scrape': ({effects.deal_attack_damage: (7, 1), effects.apply_debuff: (['Weak'], [1])}, 1, 'Debuff Attack')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 40:
                # 40% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Stab' == self.actions_done[-1] and 'Stab' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Stab'
                            self.actions_done.append(action)
                    else:
                        action = 'Stab'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Scrape' == self.actions_done[-1] and 'Scrape' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Scrape'
                            self.actions_done.append(action)
                    else:
                        action = 'Scrape'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
class BlueArachnid(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Blue Arachnid'
        self.max_hp = random.randint(46, 50)
        self.hp = self.max_hp
        self.block = 0
        self.special_done = False
        self.actions = {
            'Stab': ({effects.deal_attack_damage: (13, 1)}, 1, 'Attack'),
            'Scrape': ({effects.deal_attack_damage: (8, 1), effects.apply_debuff: (['Weak'], [1])}, 1, 'Debuff Attack'),
            'Entangle': ({effects.apply_debuff: (['Entangle'], [1])}, 1, 'Mega Debuff')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if self.special_done == False:
            # If entangle hasn't been used yet
            if combat.turn == 1:
                # if its the first turn
                self.intent = self.actions['Stab']
                # Use stab
                return self.intent
            elif combat.turn % 3 == 1:
                # follows a pattern
                if random.randint(1, 4) != 1:
                    # 25% percent chance
                    self.intent = self.actions['Entangle']
                    # Use Entangle
                    self.special_done = True
                    # Special move used
                    return self.intent
                else:
                    self.intent = self.actions['Stab']
                    # Use stab
                    return self.intent
            else:
                if random.randint(1, 4) != 1:
                    # 25% percent chance
                    self.intent = self.actions['Entangle']
                    # Use Entangle
                    self.special_done = True
                    # Special move used
                    return self.intent
                else: 
                    self.intent = self.actions['Scrape']
                    # Use Scrape
                    return self.intent
        else:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            action = ''
            # Initialize action variable
            while not action:
                # Loop until condition is met and the loop is broken
                if rng <= 45:
                    # 45% chance move
                    action = 'Stab'
                else: 
                    action = 'Scrape'
            self.intent = self.actions[action]
            # Update intent to correct move
            return self.intent

class GreenLouse(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Green Louse'
        self.max_hp = random.randint(10, 15)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Grow': ({effects.apply_buff: (['Strength'], [3])}, 0, 'Buff')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.buffs['Curl Up'] = random.randint(3, 7)
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 75:
                # 75% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Bite' == self.actions_done[-1] and 'Bite' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Bite'
                            self.actions_done.append(action)
                    else:
                        action = 'Bite'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Grow' == self.actions_done[-1] and 'Grow' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Grow'
                            self.actions_done.append(action)
                    else:
                        action = 'Grow'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def hp_loss(self, amount):
        '''Handles enemy losing Hp in anyway
        
        ### args: 
            amount: The amount of hp being lost
        
        ### returns: 
            the amount of hp lost, accounting for negatives'''
        self.hp -= amount
        # Subtract amount from hp
        if amount > 0:
            if self.died == True:
                return amount + self.hp
            else:
                self.block = self.buffs['Curl Up']
                self.buffs['Curl Up'] = 0
                # Consume curl up after taking damage to gain block
                return amount
        else:
            return 0
        # Returns actual amount of hp loss 

class RedLouse(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Red Louse'
        self.max_hp = random.randint(11, 17)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Spit Web': ({effects.apply_debuff: (['Weak'], [2])}, 1, 'Debuff')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.buffs['Curl Up'] = random.randint(3, 7)
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 75:
                # 75% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Bite' == self.actions_done[-1] and 'Bite' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Bite'
                            self.actions_done.append(action)
                    else:
                        action = 'Bite'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Spit Web' == self.actions_done[-1] and 'Spit Web' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Spit Web'
                            self.actions_done.append(action)
                    else:
                        action = 'Spit Web'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def hp_loss(self, amount):
        '''Handles enemy losing Hp in anyway
        
        ### args: 
            amount: The amount of hp being lost
        
        ### returns: 
            the amount of hp lost, accounting for negatives'''
        self.hp -= amount
        # Subtract amount from hp
        if amount > 0:
            if self.died == True:
                return amount + self.hp
            else:
                self.block = self.buffs['Curl Up']
                self.buffs['Curl Up'] = 0
                # Consume curl up after taking damage to gain block
                return amount
        else:
            return 0
        # Returns actual amount of hp loss 

class SentryA(Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Sentry'
        self.max_hp = random.randint(38, 42)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Beam': ({effects.deal_attack_damage: (8, 1)}, 1, 'Attack'),
            'Bolt': ({effects.add_card_to_pile: ('discard', 53, 2, 'na')}, 1, 'Small Debuff')
        }
        self.intent = None
        self.actions_done = []
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 1, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if combat.turn == 1:
            # If its turn 1
            self.intent = self.actions['Beam']
            self.actions_done.append('Beam')
            # Use beam
        else:
            if self.actions_done[-1] == 'Beam':
                self.intent = self.actions['Bolt']
                self.actions_done.append('Bolt')
            else:
                self.intent = self.actions['Beam']
                self.actions_done.append('Beam')
            # Alternates moves
        return self.intent

class SentryB(Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Sentry'
        self.max_hp = random.randint(38, 42)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Beam': ({effects.deal_attack_damage: (8, 1)}, 1, 'Attack'),
            'Bolt': ({effects.add_card_to_pile: ('discard', 53, 2, 'na')}, 1, 'Small Debuff')
        }
        self.intent = None
        self.actions_done = []
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 1, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if combat.turn == 1:
            # If its turn 1
            self.intent = self.actions['Bolt']
            self.actions_done.append('Bolt')
            # Use beam
        else:
            if self.actions_done[-1] == 'Beam':
                self.intent = self.actions['Bolt']
                self.actions_done.append('Bolt')
            else:
                self.intent = self.actions['Beam']
                self.actions_done.append('Beam')
            # Alternates moves
        return self.intent

class GiantLouse(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Giant Louse'
        self.max_hp = random.randint(109, 111)
        self.hp = self.max_hp
        self.block = 0
        self.special_done = False
        self.counter = 0
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (18, 1)}, 1, 'Attack'),
            'Asleep': (None, 1, 'Special'),
            'Web': ({effects.apply_debuff: (['-Dexterity', '-Strength'], [1, 1])}, 1, 'Mega Debuff'),
            'Stunned': (None, 1, 'Special')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 8, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0, 'Asleep': 1}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if self.special_done == False and combat.turn < 4:
            # If hasn't woke up yet
            self.intent = self.actions['Asleep']
            return self.intent
        else:
            if self.counter == 0 or self.counter == 1:
                # Pattern move
                self.intent = self.actions['Bite']
                self.counter += 1
                # Increase counter
            else:
                self.intent = self.actions['Web']
                self.counter = 0
                # Reset counter after webbing
            return self.intent
    
    def hp_loss(self, amount):
        '''Handles enemy losing Hp in anyway
        
        ### args: 
            amount: The amount of hp being lost
        
        ### returns: 
            the amount of hp lost, accounting for negatives'''
        self.hp -= amount
        # Subtract amount from hp
        if amount > 0:
            # Toke damage, wakes up
            self.buffs['Metalicize'] -= 8
            self.debuffs['Asleep'] = 0
            # Change buffs and debuffs
            self.intent = self.actions['Stunned']
            self.special_done = True
            # Awakens
            if self.died == True:
                return amount + self.hp
            else:
                return amount
        else:
            return 0
        # Returns actual amount of hp loss 

class GoblinGiant(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Goblin Giant'
        self.max_hp = random.randint(11, 17)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Skull Bash': ({effects.deal_attack_damage: (6, 1), effects.apply_debuff: (['Vulernable'], [2])}, 1, 'Debuff Attack'),
            'Rush': ({effects.deal_attack_damage: (14, 1)}, 1, 'Attack'),
            'Bellow': ({effects.apply_buff: (['Enraged'], [2])}, 0, 'Buff')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0, 'Enraged': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if combat.turn == 1:
            self.intent = self.actions['Bellow']
            # Always bellow on turn 1
            return self.intent
        rng = random.randint(1, 100)
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            # Loop until condition is met and the loop is broken
            if rng <= 67:
                # 67% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Rush' == self.actions_done[-1] and 'Rush' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Rush'
                            self.actions_done.append(action)
                    else:
                        action = 'Rush'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Skull Bash' == self.actions_done[-1] and 'Skull Bash' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Skull Bash'
                            self.actions_done.append(action)
                    else:
                        action = 'Skull Bash'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

class AncientMech(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Ancient Mech'
        self.max_hp = 250
        self.hp = self.max_hp
        self.block = 0
        self.counter = 0
        self.actions = {
            'Mode Shift: Initiate': (None, 0, 'Special'),
            'Laser Barrage': ({effects.deal_attack_damage: (5, 6)}, 1, 'Multi Attack'),
            'Sword Sweep': ({effects.deal_attack_damage: (6, 2)}, 1, 'Multi Attack'),
            'Mode Shift: Defense': ({effects.enemy_block_gain: (20, )}, 0, 'Special'),
            'Defensive Shock ': ({effects.enemy_block_gain: (15, ), effects.add_card_to_pile: ('discard', 53, 2, 'na')}, 0, 'Debuff Block'),
            'Sonic Pulse': ({effects.apply_debuff: (['Weak', 'Frail'], [3, 3])}, 1, 'Mega Debuff'),
            'Mode Shift: Offense': ({effects.apply_buff: (['Stength'], [3])}, 0, 'Special')
        }
        self.intent = None
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0}
        self.debuffs = {'Vulerable': 0, 'Weak': 0, '-Strength': 0, 'Chained': 0, 'Poison': 0}
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if combat.turn == 1:
            self.intent = self.actions['Mode Shift: Initiate']
            # Always initiates on turn 1
            return self.intent
        else:
            # Follows a set pattern
            if self.counter == 0:
                self.intent = self.actions['Laser Barrage']
                self.counter += 1
            elif self.counter == 1:
                self.intent = self.actions['Sword Sweep']
                self.counter += 1
            elif self.counter == 2:
                self.intent = self.actions['Mode Shift: Defense']
                self.counter += 1
            elif self.counter == 3:
                self.intent = self.actions['Defensive Shock']
                self.counter += 1
            elif self.counter == 4:
                self.intent = self.actions['Sonic Pulse']
                self.counter += 1
            else:
                self.intent = self.actions['Mode Shift: Offense']
                self.counter = 0
            return self.intent
        # Repeats this loop over and over