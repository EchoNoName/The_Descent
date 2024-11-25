import card_data
import card_constructor
import effects
import combat_beta

Instances = []

class Relics: # Relic Object Class
    def __init__(self, name, effect_type, effect_class, condition, consumable, effect_details, targets):
        self.name = name # Name
        self.effect_type = effect_type # Effect represented by a function
        self.effect_class = effect_class # Type of effect represented by a string
        self.condition = condition # Condition for the effect
        self.consumable = consumable # If the relic is one time use
        self.used = None
        if consumable == True:
            self.used = False
        self.effect_details = effect_details # The details of the effect, depends on the arguments of the effect_type
        self.targets = targets # Targets of the relic's effect, only applies to combat relics that effect entities, other relics will have None

    def applyEff(self, event, context): # Method to apply the effect
        if event == self.condition: # Check if the condition is met
            if context != None:    
                return self.effect_type(context, *self.effect_details) # Apply the effect
            else:
                return self.effect_type(*self.effect_details) # Apply the effect
        return context # Nothing Happens
    # The above is a place holder, code needs to be changed once things get added
    def valueModificationEff(self, event, context): # Method to apply the effect
        if event == self.condition and self.effect_class == 'valueMod': # Check if the condition is met 
            return self.effect_type(context, *self.effect_details) # Apply the effect
        return context # Nothing Happens
    
    def combatActionEff(self, event, combat):
        '''Handles relic effects that does an action in combat

        args: 
            event: The event occuring represented by a string
            combat: the combat object that holds all data related to a combat instance
        '''
        if event == self.condition and self.effect_class == 'combatAct': # Check if the condition is met 
            target = combat.get_targets(self.targets)
            self.effect_type(*self.effect_details, target)


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
        self.buffs = {'Strength': 0, 'Dexterity': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Throns': 0, 'Regen': 0, 'Artifact': 0, 'Double Tap': 0, 'Flurry': 0}
        #Debuffs: Atrophy = lose dex at the end of turn
        self.debuffs = {'Vulerable': 0, 'Weak': 0, 'Frail': 0, '-Strength': 0, '-Dexterity': 0, 'Atrophy': 0, 'Chained': 0, 'Poison': 0, 'No Draw': 0, 'Chaotic': 0, 'Last Chance': 0}
        self.powers = {'Parry': 0, 'Deflect': 0, 'Cursed Ward': 0, 'Feel No Pain': 0, 'Evolve': 0, 'Transfer Pain': 0, 'Dark Embrace': 0, 'Corruption Form': 0, 'Spectral Blades': 0, 'Seeing Red': 0, 'Corruption': 0, 'Clear Mind': 0}
    
    def relic_pickup(self, relic):
        self.relics.append(relic)
        relic.applyEff('pickup', None)
    
    def potion_pickup(self, potion):
        if self.potions.count(None) > 0:
            self.potions[self.potions.index(None)] = potion

    def gain_block_card(self, amount):
        self.block += amount + self.buff['Dexterity']
    
    def gain_block_power(self, amount):
        self.block += amount
    
    def gain_buff(self, buff_type, amount):
        self.buff[buff_type] += amount
    
    def lose_buff(self, buff_type, amount):
        self.buffs[buff_type] -= amount
        if self.buffs[buff_type] < 0:
            self.debuffs['-' + buff_type] = self.buffs[buff_type]
            self.buffs[buff_type] = 0
    
    def gain_debuff(self, debuff_type, amount):
        self.debuffs[debuff_type] += amount
    
    def lose_debuff(self, debuff_type, amount):
        self.debuffs[debuff_type] -= amount

    def gain_power(self, power, amount):
        self.powers[power] += amount

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
            return False
        else:
            damage = -self.block
            self.block = 0
            # Applies relic effects that reduce Hp Loss
            for relic in self.relics:
                damage = relic.applyEff('HpLoss', damage)
            self.Hp -= damage
        if damage > 0:
            return True
    
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

