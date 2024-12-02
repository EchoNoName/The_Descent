import card_data
import card_constructor
import effects
import combat_beta

Instances = []

class Character:
    def __init__(self, name, maxHp, character_class):
        self.name = name
        self.maxHp = maxHp
        self.Hp = maxHp
        self.character_class = character_class
        self.block = 0
        self.deck = []
        self.potions = [None, None, None]
        self.relics = []
        self.buffs = {'Strength': 0, 'Dexterity': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Double Tap': 0, 'Duplicate': 0, 'Draw Card': 0, 'Energized': 0, 'Next Turn Block': 0}
        #Debuffs: Atrophy = lose dex at the end of turn
        self.debuffs = {'Vulerable': 0, 'Weak': 0, 'Frail': 0, '-Strength': 0, '-Dexterity': 0, 'Atrophy': 0, 'Chained': 0, 'Poison': 0, 'No Draw': 0, 'Chaotic': 0, 'Last Chance': 0, 'Draw Reduction': 0, 'Parry': 0, 'Deflect': 0}
        # self.powers = {'Cursed Ward': 0, 'Feel No Pain': 0, 'Evolve': 0, 'Transfer Pain': 0, 'Dark Embrace': 0, 'Corruption Form': 0, 'Spectral Blades': 0, 'Seeing Red': 0, 'Corruption': 0, 'Clear Mind': 0}
    
    def relic_pickup(self, relic):
        self.relics.append(relic)
        relic.applyEff('pickup', None)
    
    def potion_pickup(self, potion):
        if self.potions.count(None) > 0:
            self.potions[self.potions.index(None)] = potion

    def gain_block_card(self, amount):
        '''Getting block from playing cards
        
        ### args:
            amount: amount gained'''
        self.block += amount + self.buff['Dexterity']
        # add more block and adding the dexterity bonus
    
    def gain_block_power(self, amount):
        '''gaining block from powers or some other passive effects
        
        ### args: 
            amount: amount gained'''
        self.block += amount
        # Add more block
    
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
            # If player has artifact
            self.buffs['ArtiFact'] -= 1
            # Lose 1 artifact and negate the debuff
        elif debuff_type == "No Draw" or debuff_type == "Chaotic" or debuff_type == 'Last Chance':
            # If its non stackable
            self.debuffs[debuff_type] = 1
            # Make the debuff 1
        elif debuff_type in {'-Strength', '-Dexterity'}:
            # If its Str and Dex where the player can have positive values in buffs
            self.lose_buff(debuff_type, amount)
            # use the lose buff function instead
        else:
            self.debuffs[debuff_type] += amount
            # Add the amount to debuff
    
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

    def hp_loss(self, amount):
        for relic in self.relics:
            amount = relic.applyEff('HpLoss', amount)
        self.Hp -= amount
        if amount > 0:
            if self.died == True:
                return 'GG' # Placeholder
            return True
        else:
            return False
    
    def hp_recovery(self, amount):
        self.Hp = min(self.Hp + amount, self.maxHp)

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
            damage = -self.block
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            return self.hp_loss(damage)
    
    def died(self):
        if self.Hp <= 0:
            for relic in self.relics:
                if relic.condition == 'dead' and relic.used == False:
                    self.Hp = relic.applyEff('dead', self.maxHp)
                    relic.used = True
                    return False
            return False
        else:
            return True

