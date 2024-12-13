import card_constructor
import relic_data
import potion_data

class RewardScreen: # Class for any reward screed
    def __init__(self, rareChanceOffset, potionChance, combat_type, set_reward = False):
        self.rareChanceOffset = rareChanceOffset
        self.potionChance = potionChance
        self.combat_type = combat_type
        self.set_reward = set_reward
        self.rewards = {
            'Gold': None,
            'Cards': [],
            'Potions': [],
            'Relics': []
        }
    
    def generate_rewards(self):
        if not self.set_reward:
