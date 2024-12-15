import card_constructor
import card_data
import relic_data
import potion_data
import random

class RewardScreen: # Class for any reward screed
    def __init__(self, run, character_class, rareChanceOffset, potionChance, cardRewardOptions, reward_type, set_reward = False, additonal_rewards = {'Gold': 0, 'Cards': 0, 'Potions': 0, 'Relic': 0}):
        self.run = run
        self.character_class = character_class
        self.rareChanceOffset = rareChanceOffset
        self.potionChance = potionChance
        self.cardRewardOptions = cardRewardOptions
        self.reward_type = reward_type
        self.set_reward = set_reward
        self.rewards = {
            'Gold': 0,
            'Cards': [],
            'Potions': [],
            'Relics': []
        }
        self.additional_rewards = additonal_rewards
    
    def isEmpty(self):
        '''Method for checking if there are still items left'''
        for items in self.rewards.values():
            if items == True:
                return False
        return True

    def generate_rewards(self):
        if not self.set_reward:
            if self.reward_type == 0: 
                # Normal combat
                self.rewards['Gold'] = random.randint(10, 20)
                # Gold amount
                cards = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
                # Generate random card rewards
            elif self.reward_type == 1: 
                # Elite combat
                self.rewards['Gold'] = random.randint(25, 35)
                # Gold amount
                cards = card_constructor.generate_card_reward('elite', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
                # Generate random card rewards
                relic = relic_data.spawnRelic()
                self.rewards['Relics'].append(relic)
                # Generate relic
            elif self.reward_type == 2: 
                # Boss encounter
                self.rewards['Gold'] = random.randint(95, 105)
                # Gold amount
                cards = card_constructor.generate_card_reward('boss', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
                # Generate random card rewards
            elif self.reward_type == 3: 
                # Small chest
                self.rewards['Gold'] = random.randint(23, 27)
                # Gold amount
                relic = relic_data.spawnRelic(75, 25)
                self.rewards['Relics'].append(relic)
                # Generate relic
            elif self.reward_type == 4: 
                # Medium chest
                self.rewards['Gold'] = random.randint(45, 55)
                # Gold amount
                relic = relic_data.spawnRelic(35, 50)
                self.rewards['Relics'].append(relic)
                # Generate relic
            elif self.reward_type == 5: 
                # Large chest
                self.rewards['Gold'] = random.randint(68, 82)
                # Gold amount
                relic = relic_data.spawnRelic(0, 75)
                self.rewards['Relics'].append(relic)
                # Generate relic
            else:
                raise TypeError(f'Invalid reward type: {self.reward_type}')
        else:
            if self.set_reward == 'Bell':
                self.rewards['Relics'].append(relic_data.createCommon)
                self.rewards['Relics'].append(relic_data.createUncommon)
                self.rewards['Relics'].append(relic_data.createRare)
            elif self.set_reward == 'Booster Pack':
                for k in range(0, 5):
                    cards = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                    for i in range(0, len(cards)):
                        card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                        cards[i] = card_option
                    self.rewards['Cards'].append(cards)
            elif self.set_reward == 'Caldron':
                for i in range(0, 5):
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
            elif self.set_reward == 'Tiny House':
                self.rewards['Gold'] = 100
                for i in range(0, 2):
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
                cards = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
            else:
                self.rewards = self.set_reward

        if self.additional_rewards:
            if self.additional_rewards['Gold'] > 0:
                self.rewards['Gold'] += self.rewards['Gold']
            if self.additional_rewards['Card'] > 0:
                for k in range(0, self.additional_rewards['Card']):
                    cards = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                    for i in range(0, len(cards)):
                        card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                        cards[i] = card_option
                    self.rewards['Cards'].append(cards)
            if self.additional_rewards['Potion'] > 0:
                for i in range(0, self.additional_rewards['Potion']):
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
            if self.additional_rewards['Relic'] > 0:
                for i in range(0, self.additional_rewards['Potion']):
                    relic = relic_data.spawnRelic()
                    self.rewards['Relics'].append(relic)
        
    def listRewards(self):
        i = 0
        reward_picks = {
            'gold': 0,
            'card': 0,
            'potion': 0,
            'relic': 0
        }
        while True:
            for type, amount in self.rewards.items():
                if amount != False:
                    if type == 'Gold':
                        print(f'{i}: {amount}')
                        i += 1
                    elif type in {'Potions', 'Relics'}:
                        for item in amount:
                            print(f'{i}: {item}')
                            i += 1
                            if type == 'Potions':
                                reward_picks['potion'] += 1
                            else:
                                reward_picks['relic'] += 1
                    else:
                        for option in amount:
                            print(f'{i}: Add a Card to your deck')
                            i += 1
                            reward_picks['card'] += 1
            i = 0
            player_action = input('Enter a index or Skip: ')
            if player_action == 'Skip':
                break
            else:
                player_action = int(player_action)
                if player_action < reward_picks['gold']:
                    self.run.gold_modification(self.rewards['Gold'])
                elif player_action - reward_picks['gold'] < reward_picks['card']:
                    player_action -= reward_picks['gold']
                    j = 0
                    for card in self.rewards['Cards'][player_action]:
                        print(f'{j}: {card}')
                        j += 1
                    card_choice = input('Enter a index or Skip: ')
                    if card_choice != 'Skip':
                        self.run.card_pickup(self.rewards['Cards'][player_action][int(card_choice)])
                elif player_action - reward_picks['gold'] - reward_picks['card'] < reward_picks['potion']:
                    player_action = player_action - reward_picks['gold'] - reward_picks['card']
                    self.run.potion_pickup(self.rewards['Potions'][player_action])
                else:
                    player_action = player_action - reward_picks['gold'] - reward_picks['card'] - reward_picks['potion']
                    self.run.relic_pickup(self.rewards['Relics'][player_action])

