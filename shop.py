import random
import card_constructor
import card_data
import relic_data
import potion_data
import effects
import random

class Shop:
    def __init__(self, run):
        self.run = run
        self.wares = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: True
        }
        self.generated = False

    def generate_wares(self):
        if self.run.player.character_class == 1:
            if self.generated == False:
                card1 = random.choice(card_constructor.attack_card_1)
                card2 = random.choice(card_constructor.attack_card_1)
                card3 = random.choice(card_constructor.skill_card_1)
                card4 = random.choice(card_constructor.skill_card_1)
                card5 = random.choice(card_constructor.power_card_1)
                card1 = card_constructor.create_card(card1, card_data.card_info[card1])
                card2 = card_constructor.create_card(card2, card_data.card_info[card2])
                card3 = card_constructor.create_card(card3, card_data.card_info[card3])
                card4 = card_constructor.create_card(card4, card_data.card_info[card4])
                card5 = card_constructor.create_card(card5, card_data.card_info[card5])
                self.wares[0] = card1
                self.wares[1] = card2
                self.wares[2] = card3
                self.wares[3] = card4
                self.wares[4] = card5
                for i in range(0, 5):
                    if self.wares[i].rarity == 1:
                        self.wares[i] =[self.wares[i], random.randint(45, 55)]
                    elif self.wares[i].rarity == 2:
                        self.wares[i] = [self.wares[i], random.randint(68, 82)]
                    elif self.wares[i].rarity == 3:
                        self.wares[i] = [self.wares[i], random.randint(135, 165)]
                while True:
                    combined_list = card_constructor.attack_card_1
                    combined_list.extend(card_constructor.skill_card_1)
                    combined_list.extend(card_constructor.power_card_1)
                    card6 = random.choice(combined_list)
                    if card_data.card_info[card6][1] == 2:
                        card6 = card_constructor.create_card(card6, card_data.card_info[card6])
                        self.wares[5] = [card6, random.randint(81, 99)]
                        break
                    else:
                        continue
                while True:
                    card7 = random.choice(combined_list)
                    if card_data.card_info[card7][1] == 3:
                        card7 = card_constructor.create_card(card7, card_data.card_info[card7])
                        self.wares[6] = [card7, random.randint(162, 198)]
                        break
                    else:
                        continue
                self.wares[7] = [potion_data.randomPotion(), random.randint(48, 105)]
                self.wares[8] = [potion_data.randomPotion(), random.randint(48, 105)]
                self.wares[9] = [potion_data.randomPotion(), random.randint(48, 105)]
                relic1 = relic_data.spawnRelic()
                if relic1.rarity == 4:
                    self.wares[10] = [relic1, random.randint(143, 157)]
                elif relic1.rarity == 3:
                    self.wares[10] = [relic1, random.randint(238, 262)]
                elif relic1.rarity == 2:
                    self.wares[10] = [relic1, random.randint(285, 315)]
                relic2 = relic_data.spawnRelic()
                if relic1.rarity == 4:
                    self.wares[11] = [relic2, random.randint(143, 157)]
                elif relic1.rarity == 3:
                    self.wares[11] = [relic2, random.randint(238, 262)]
                elif relic1.rarity == 2:
                    self.wares[11] = [relic2, random.randint(285, 315)]
                shopRelic = random.choice(list(relic_data.shopRelics.keys()))
                shopRelic = relic_data.createRelic(shopRelic, relic_data.shopRelics[shopRelic])
                self.wares[12] = [shopRelic, random.randint(143, 157)]
                removalCost = 75 + self.run.removals * 25
                self.wares[13] = ['Remove', removalCost]

    def interact(self):
        for i in range(0, 14):
            if self.wares[i][0] != None:
                print(f'{i}: {self.wares[i][0]}, costs: {self.wares[i][1]}')
        action = input('Type index to buy and Leave to go to map')
        if action == 'Leave':
            self.run.mapNav()
        else:
            action = int(action)
            if self.wares[action][1] <= self.run.player.gold:
                self.run.gold_modification(-self.wares[action][1])
                item = self.wares[action][0]
                self.wares[action][0] = None
                if item == 'Remove':
                    effects.card_select(1, {}, self.run)
                    self.run.player.remove_card()
                elif isinstance(item, card_constructor.Card):
                    self.run.card_pickup(item)
                elif isinstance(item, potion_data.Potion):
                    self.run.potion_pickup(item)
                elif isinstance(item, relic_data.Relics):
                    self.run.relic_pickup(item)
                else:
                    raise TypeError(f'Unkown item bought {item}')
            else:
                print('Too Expensive')
            self.interact()