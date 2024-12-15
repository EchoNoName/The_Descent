import card_constructor
import relic_data
import potion_data
import random

class RewardScreen: # Class for any reward screed
    def __init__(self, rareChanceOffset, potionChance, reward_type, set_reward = False, additonal_rewards = None):
        self.rareChanceOffset = rareChanceOffset
        self.potionChance = potionChance
        self.reward_type = reward_type
        self.set_reward = set_reward
        self.rewards = {
            'Gold': None,
            'Cards': [],
            'Potions': [],
            'Relics': []
        }
        self.additional_rewards = additonal_rewards
    
    def generate_rewards(self):
        if not self.set_reward:
            if self.reward_type == 0: # Normal combat
                self.rewards['Gold'] = random.randint(10, 20)
            elif self.reward_type == 1: # Elite combat
                self.rewards['Gold'] = random.randint(25, 35)
            elif self.reward_type == 2: # Boss encounter
                self.rewards['Gold'] = random.randint(95, 105)
            elif self.reward_type == 3: # Small chest
                self.rewards['Gold'] = random.randint(23, 27)
            elif self.reward_type == 4: # Medium chest
                self.rewards['Gold'] = random.randint(45, 55)
            elif self.reward_type == 5: # Large chest
                self.rewards['Gold'] = random.randint(68, 82)
            else:
                raise TypeError(f'Invalid reward type: {self.reward_type}')