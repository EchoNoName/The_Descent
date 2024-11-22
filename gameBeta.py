import effects
class Relics: # Relic Object Class
    def __init__(self, name, effect, condition, consumable, magnitude = 1):
        self.name = name # Name
        self.effect = effect # Effect represented by a function
        self.condition = condition # Condition for the effect
        self.consumable = consumable # If the relic is one time use
        self.used = None
        if consumable == True:
            self.used = False
        self.magnitude = magnitude

    def applyEff(self, event, context): # Method to apply the effect
        if event == self.condition: # Check if the condition is met
            return self.effect(context, self.magnitude) # Apply the effect
        return context # Nothing Happens

class Character:
    def __init__(self, name, maxHp):
        self.name = name
        self.maxHp = maxHp
        self.Hp = maxHp
        self.block = 0
        self.potion = [None, None, None]
        self.relics = []
        self.buff = {'Strength': 0, 'Dexterity': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Throns': 0, 'Regen': 0, 'Artifact': 0, 'Double Tap': 0, 'Flurry': 0}
        #Debuffs: Atrophy = lose dex at the end of turn
        self.debuff = {'Vulerable': 0, 'Weak': 0, 'Frail': 0, '-Strength': 0, '-Dexterity': 0, 'Atrophy': 0, 'Chained': 0, 'Poison': 0, 'No Draw': 0}
        self.powers = {'Parry': 0, 'Deflect': 0, 'Cursed Ward': 0, 'Feel No Pain': 0, 'Evolve': 0, 'Transfer Pain': 0, 'Dark Embrace': 0, 'Corruption Form': 0, 'Spectral Blades': 0, 'Seeing Red': 0, 'Corruption': 0, 'Clear Mind': 0}
    
    def relic_pickup(self, relic):
        self.relics.append(relic)

    def gain_block(self, amount):
        self.block += amount + self.buff['Dexterity']

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

