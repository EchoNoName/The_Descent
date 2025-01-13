import card_constructor
import card_data
import relic_data
import potion_data
import random
import pygame
import os

class RewardScreen: # Class for any reward screed
    def __init__(self, run, character_class, rareChanceMult, rareChanceOffset, potionChance, cardRewardOptions, reward_type, set_reward = False, additonal_rewards = {'Gold': 0, 'Cards': 0, 'Potions': 0, 'Relic': 0}):
        self.run = run
        self.character_class = character_class
        self.rareChanceOffset = rareChanceOffset
        self.potionChance = potionChance
        self.cardRewardOptions = cardRewardOptions
        self.reward_type = reward_type
        self.set_reward = set_reward
        self.close = False
        self.generated = False
        self.rewards = {
            'Gold': 0,
            'Cards': [],
            'Potions': [],
            'Relics': []
        }
        self.additional_rewards = additonal_rewards
        self.rareChanceMult = rareChanceMult
        gold_sprite = pygame.image.load(os.path.join("assets", "icons", "gold.png"))
        self.gold_sprite = pygame.transform.scale(gold_sprite, (gold_sprite.get_width()//11, gold_sprite.get_height()//11))
        self.deck_button_sprite = pygame.image.load(os.path.join("assets", "icons", "pile_icon.png"))
        self.deck_button_sprite = pygame.transform.scale(self.deck_button_sprite, (self.deck_button_sprite.get_width()//10, self.deck_button_sprite.get_height()//10))
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 24)
        self.skip_button_sprite = pygame.image.load(os.path.join("assets", "ui", "skip_button.png"))

    def isEmpty(self):
        '''Method for checking if there are still items left'''
        for items in self.rewards.values():
            if items == True:
                return False
        self.run.reward = None
        return True

    def generate_rewards(self):
        if not self.set_reward: # If the reward is not set, generate rewards
            if self.run.player.relics: # If the player has relic relating to rewards, apply the relic effects
                for relic in self.run.player.relics:
                    relic.rewardModification(self.reward_type, self.additional_rewards)
            # Apply relic effects
            if self.reward_type == 0: 
                # Normal combat
                self.rewards['Gold'] = random.randint(10, 20)
                # Gold amount
                cards, self.rareChanceOffset = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
                # Generate random card rewards
                rng = random.randint(1, 100)
                # Check if the player rolls a potion
                if rng <= self.potionChance:
                    # If the player rolls a potion, add it to the rewards
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
                    self.potionChance -= 10
                else:
                    # If the player does not roll a potion, increase the chance of rolling a potion
                    self.potionChance += 20
            elif self.reward_type == 1: 
                # Elite combat
                self.rewards['Gold'] = random.randint(25, 35)
                # Gold amount
                cards, self.rareChanceOffset = card_constructor.generate_card_reward('elite', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
                # Generate random card rewards
                relic = None
                while True:
                    relic = relic_data.spawnRelic()
                    for owned_relic in self.run.player.relics:
                        if owned_relic.name == relic.name:
                            continue
                    break
                self.rewards['Relics'].append(relic)
                # Generate relic
                rng = random.randint(1, 100)
                if rng <= self.potionChance:
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
                    self.potionChance -= 10
                else:
                    self.potionChance += 20
            elif self.reward_type == 2: 
                # Boss encounter
                self.rewards['Gold'] = random.randint(95, 105)
                # Gold amount
                cards, self.rareChanceOffset = card_constructor.generate_card_reward('boss', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
                # Generate random card rewards
                rng = random.randint(1, 100)
                if rng <= self.potionChance:
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
                    self.potionChance -= 10
                else:
                    self.potionChance += 20
            elif self.reward_type == 3: 
                # Small chest
                self.rewards['Gold'] = random.randint(23, 27)
                # Gold amount
                relic = None
                while True:
                    relic = relic_data.spawnRelic(75, 25)
                    for owned_relic in self.run.player.relics:
                        if owned_relic.name == relic.name:
                            continue
                    break
                self.rewards['Relics'].append(relic)
                # Generate relic
            elif self.reward_type == 4: 
                # Medium chest
                self.rewards['Gold'] = random.randint(45, 55)
                # Gold amount
                relic = None
                while True:
                    relic = relic_data.spawnRelic(35, 50)
                    for owned_relic in self.run.player.relics:
                        if owned_relic.name == relic.name:
                            continue
                    break
                self.rewards['Relics'].append(relic)
                # Generate relic
            elif self.reward_type == 5: 
                # Large chest
                self.rewards['Gold'] = random.randint(68, 82)
                # Gold amount
                relic = None
                while True:
                    relic = relic_data.spawnRelic(0, 75)
                    for owned_relic in self.run.player.relics:
                        if owned_relic.name == relic.name:
                            continue
                    break
                self.rewards['Relics'].append(relic)
                # Generate relic
            else:
                raise TypeError(f'Invalid reward type: {self.reward_type}')
        else: # If the reward is set, apply the set reward
            if self.set_reward == 'Bell':
                # Bell reward
                common_relic = None
                uncommon_relic = None
                rare_relic = None
                while True:
                    common_relic = relic_data.createCommon()
                    for relic in self.run.player.relics:
                        if relic.name == common_relic.name:
                            continue
                    break
                while True:
                    uncommon_relic = relic_data.createUncommon()
                    for relic in self.run.player.relics:
                        if relic.name == uncommon_relic.name:
                            continue
                    break
                while True:
                    rare_relic = relic_data.createRare()
                    for relic in self.run.player.relics:
                        if relic.name == rare_relic.name:
                            continue
                    break
                self.rewards['Relics'].append(common_relic)
                self.rewards['Relics'].append(uncommon_relic)
                self.rewards['Relics'].append(rare_relic)
            elif self.set_reward == 'Booster Pack':
                # Booster pack reward
                for k in range(0, 5):
                    cards, self.rareChanceOffset = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                    for i in range(0, len(cards)):
                        card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                        cards[i] = card_option
                    self.rewards['Cards'].append(cards)
            elif self.set_reward == 'Cauldron':
                # Cauldron reward
                for i in range(0, 5):
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
            elif self.set_reward == 'Tiny House':
                # Tiny house reward - House Deed relic
                self.rewards['Gold'] = 100
                for i in range(0, 2):
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
                cards, self.rareChanceOffset = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                for i in range(0, len(cards)):
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                    cards[i] = card_option
                self.rewards['Cards'].append(cards)
            elif self.set_reward == 'Brewing Stand':
                # Brewing stand reward - Potion
                self.rewards['Potions'].append(potion_data.randomPotion())
            else:
                # set reward
                self.rewards = self.set_reward

        if self.additional_rewards: # If there are additional rewards, apply them
            if self.additional_rewards['Gold'] > 0: # Additional gold
                self.rewards['Gold'] += self.rewards['Gold']
            if self.additional_rewards['Card'] > 0: # Additional cards
                for k in range(0, self.additional_rewards['Card']):
                    cards, self.rareChanceOffset = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class)
                    for i in range(0, len(cards)):
                        card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
                        cards[i] = card_option
                    self.rewards['Cards'].append(cards)
            if self.additional_rewards['Potion'] > 0: # Additional potions
                for i in range(0, self.additional_rewards['Potion']):
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion)
            if self.additional_rewards['Relic'] > 0: # Additional relics
                for i in range(0, self.additional_rewards['Relic']):
                    relic = None
                    while True:
                        relic = relic_data.spawnRelic()
                        for owned_relic in self.run.player.relics:
                            if owned_relic.name == relic.name:
                                continue
                        break
                    self.rewards['Relics'].append(relic)
        self.run.rareChanceOffset = self.rareChanceOffset # Update the rare chance offset
        self.run.potionChance = self.potionChance # Update the potion chance

    def listRewards(self, screen = None):
        if self.generated == False: # If the rewards have not been generated, generate them
            self.generate_rewards()
            self.generated = True

        self.close = False

        # Create main reward box surface
        reward_box = pygame.Surface((500, 600))
        reward_box.fill((50, 50, 50))
        reward_box_rect = reward_box.get_rect(center=(self.run.SCREEN_WIDTH//2, self.run.SCREEN_HEIGHT//2))

        # Track reward positions
        reward_y = 20
        reward_height = 60
        reward_spacing = 10

        known_screen = True
        if screen is None:
            screen = pygame.Surface((1600, 900))
            known_screen = False


        # Main loop
        while not self.close:
            reward_box.fill((50, 50, 50)) # Fill the reward box with gray
            reward_y = 20 # Reset the reward y position

            if known_screen:
                self.run.screen.blit(screen, (0, 0))
            else:
                screen.fill((0, 0, 0, 25))
                self.run.screen.blit(screen, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            self.run.potion_events(mouse_pos, events)
            self.run.handle_deck_view(events, mouse_pos)

            # Draw rewards on reward_box
            if self.rewards['Gold']:
                gold_rect = pygame.Rect(30, reward_y, 460, reward_height)
                pygame.draw.rect(reward_box, (70, 70, 70), gold_rect)
                reward_box.blit(self.gold_sprite, (gold_rect.left + 10, gold_rect.centery - self.gold_sprite.get_height()//2))
                font = pygame.font.Font(None, 36)
                text = font.render(f"{self.rewards['Gold']}", True, (255, 255, 255))
                reward_box.blit(text, (gold_rect.left + 70, gold_rect.centery - text.get_height()//2))
                reward_y += reward_height + reward_spacing

            for card_options in self.rewards['Cards']:
                card_rect = pygame.Rect(30, reward_y, 460, reward_height)
                pygame.draw.rect(reward_box, (70, 70, 70), card_rect)
                reward_box.blit(self.deck_button_sprite, (card_rect.left + 10, card_rect.centery - self.deck_button_sprite.get_height()//2))
                font = pygame.font.Font(None, 36)
                text = font.render("Add a card to your deck", True, (255, 255, 255))
                reward_box.blit(text, (card_rect.left + 70, card_rect.centery - text.get_height()//2))
                reward_y += reward_height + reward_spacing

            # Track if mouse is hovering over any item
            mouse_pos = pygame.mouse.get_pos()
            box_mouse_pos = (mouse_pos[0] - reward_box_rect.left, mouse_pos[1] - reward_box_rect.top)
            hover_text = None
            
            # Draw potions
            for potion in self.rewards['Potions']:
                potion_rect = pygame.Rect(30, reward_y, 460, reward_height)
                pygame.draw.rect(reward_box, (70, 70, 70), potion_rect)
                reward_box.blit(potion.sprite, (potion_rect.left + 10, potion_rect.centery - potion.sprite.get_height()//2))
                font = pygame.font.Font(None, 36)
                text = font.render(potion.name, True, (255, 255, 255))
                reward_box.blit(text, (potion_rect.left + 70, potion_rect.centery - text.get_height()//2))
                
                if potion_rect.collidepoint(box_mouse_pos):
                    hover_text = potion.description
                
                reward_y += reward_height + reward_spacing

            # Draw relics
            for relic in self.rewards['Relics']:
                relic_rect = pygame.Rect(30, reward_y, 460, reward_height)
                pygame.draw.rect(reward_box, (70, 70, 70), relic_rect)
                reward_box.blit(relic.sprite, (relic_rect.left + 10, relic_rect.centery - relic.sprite.get_height()//2))
                font = pygame.font.Font(None, 36)
                text = font.render(relic.name, True, (255, 255, 255))
                reward_box.blit(text, (relic_rect.left + 70, relic_rect.centery - text.get_height()//2))
                
                if relic_rect.collidepoint(box_mouse_pos):
                    hover_text = relic.description
                    
                reward_y += reward_height + reward_spacing

            # Blit reward_box to screen
            self.run.screen.blit(reward_box, reward_box_rect)

            # Draw hover text if needed
            if hover_text:
                # Create text surface
                desc_font = pygame.font.Font(None, 24)
                desc_text = desc_font.render(hover_text, True, (255, 255, 255))
                desc_bg = pygame.Surface((desc_text.get_width() + 20, desc_text.get_height() + 20))
                desc_bg.fill((50, 50, 50))
                desc_bg.blit(desc_text, (10, 10))
                
                # Position near mouse but ensure on screen
                desc_x = min(mouse_pos[0], self.run.SCREEN_WIDTH - desc_bg.get_width())
                desc_y = min(mouse_pos[1] - desc_bg.get_height(), self.run.SCREEN_HEIGHT - desc_bg.get_height())
                self.run.screen.blit(desc_bg, (desc_x, desc_y))

            # Draw skip button directly on screen
            skip_rect = self.skip_button_sprite.get_rect()
            skip_rect.bottomright = (self.run.SCREEN_WIDTH, self.run.SCREEN_HEIGHT - 200)
            self.run.screen.blit(self.skip_button_sprite, skip_rect)
            self.run.player.draw_ui(self.run.screen)
            pygame.display.flip()

            # Event loop
            for event in events :
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (pygame.key.get_mods() & pygame.KMOD_ALT)):
                    pygame.quit()
                    
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # If the mouse is clicked
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check skip button click
                    if skip_rect.collidepoint(mouse_pos):
                        self.close = True
                        break
                        
                    # Adjust mouse position relative to reward_box
                    box_mouse_pos = (mouse_pos[0] - reward_box_rect.left, mouse_pos[1] - reward_box_rect.top)
                    reward_y = 20

                    if self.rewards['Gold']:
                        gold_rect = pygame.Rect(30, reward_y, 460, reward_height)
                        if gold_rect.collidepoint(box_mouse_pos):
                            self.run.gold_modification(self.rewards['Gold'])
                            self.rewards['Gold'] = 0
                        reward_y += reward_height + reward_spacing

                    for i, card_options in enumerate(self.rewards['Cards']):
                        card_rect = pygame.Rect(30, reward_y, 460, reward_height)
                        if card_rect.collidepoint(box_mouse_pos):
                            # Show card selection menu
                            card_menu = True
                            while card_menu:
                                # Create a transparent surface for the background
                                background = pygame.Surface(self.run.screen.get_size(), pygame.SRCALPHA)
                                background.fill((0, 0, 0, 25))
                                self.run.screen.blit(background, (0, 0))
                                events = pygame.event.get()
                                mouse_pos = pygame.mouse.get_pos()
                                self.run.potion_events(mouse_pos, events)
                                self.run.handle_deck_view(events, mouse_pos)
                                
                                # Draw cards
                                card_x = self.run.SCREEN_WIDTH//4
                                for j, card in enumerate(card_options):
                                    card.rect.center = (card_x, self.run.SCREEN_HEIGHT//2)
                                    self.run.screen.blit(card.sprite, card.rect)
                                    card_x += self.run.SCREEN_WIDTH//4

                                # Draw skip button
                                skip_rect = self.skip_button_sprite.get_rect()
                                skip_rect.bottomright = (self.run.SCREEN_WIDTH, self.run.SCREEN_HEIGHT - 200)
                                self.run.screen.blit(self.skip_button_sprite, skip_rect)

                                pygame.display.flip()

                                for card_event in pygame.event.get():
                                    if card_event.type == pygame.QUIT or (card_event.type == pygame.KEYDOWN and card_event.key == pygame.K_F4 and (pygame.key.get_mods() & pygame.KMOD_ALT)):
                                        pygame.quit()
                                        
                                    if card_event.type == pygame.MOUSEBUTTONUP and card_event.button == 1:
                                        card_mouse_pos = pygame.mouse.get_pos()
                                        if skip_rect.collidepoint(card_mouse_pos):
                                            card_menu = False
                                        else:
                                            for j, card in enumerate(card_options):
                                                if card.rect.collidepoint(card_mouse_pos):
                                                    self.run.card_pickup(card)
                                                    self.rewards['Cards'].pop(i)
                                                    card_menu = False

                        reward_y += reward_height + reward_spacing

                    for i, potion in enumerate(self.rewards['Potions']):
                        potion_rect = pygame.Rect(30, reward_y, 460, reward_height)
                        if potion_rect.collidepoint(box_mouse_pos):
                            if self.run.potion_pickup(potion):
                                self.rewards['Potions'].pop(i)
                        reward_y += reward_height + reward_spacing

                    for i, relic in enumerate(self.rewards['Relics']):
                        relic_rect = pygame.Rect(30, reward_y, 460, reward_height)
                        if relic_rect.collidepoint(box_mouse_pos):
                            self.run.relic_pickup(relic)
                            self.rewards['Relics'].pop(i)
                        reward_y += reward_height + reward_spacing

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.close = True

            if not any([self.rewards['Gold'], self.rewards['Cards'], self.rewards['Potions'], self.rewards['Relics']]):
                self.close = True