import card_constructor
import card_data
import relic_data
import potion_data
import random
import pygame
import os

class RewardScreen: # Class for any reward screed
    def __init__(self, run, character_class, rareChanceMult, rareChanceOffset, potionChance, cardRewardOptions, reward_type, set_reward = False, additonal_rewards = {'Gold': 0, 'Cards': 0, 'Potions': 0, 'Relic': 0}):
        self.run = run # Set the run to the run
        self.character_class = character_class # Set the character class to the character class
        self.rareChanceOffset = rareChanceOffset # Set the rare chance offset to the rare chance offset
        self.potionChance = potionChance # Set the potion chance to the potion chance
        self.cardRewardOptions = cardRewardOptions # Set the card reward options to the card reward options
        self.reward_type = reward_type # Set the reward type to the reward type
        self.set_reward = set_reward # Set the set reward to the set reward
        self.close = False # Set the close to False
        self.generated = False # Set the generated to False
        self.rewards = { # Initialize the rewards dictionary
            'Gold': 0, # Set the gold to 0
            'Cards': [], # Set the cards to an empty list
            'Potions': [], # Set the potions to an empty list
            'Relics': [] # Set the relics to an empty list
        }
        self.additional_rewards = additonal_rewards # Set the additional rewards to the additional rewards
        self.rareChanceMult = rareChanceMult # Set the rare chance mult to the rare chance mult
        gold_sprite = pygame.image.load(os.path.join("assets", "icons", "gold.png")) # Load the gold sprite
        self.gold_sprite = pygame.transform.scale(gold_sprite, (gold_sprite.get_width()//11, gold_sprite.get_height()//11)) # Scale the gold sprite
        self.deck_button_sprite = pygame.image.load(os.path.join("assets", "icons", "pile_icon.png")) # Load the deck button sprite
        self.deck_button_sprite = pygame.transform.scale(self.deck_button_sprite, (self.deck_button_sprite.get_width()//10, self.deck_button_sprite.get_height()//10)) # Scale the deck button sprite
        pygame.font.init() # Initialize the font
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 24) # Set the font to the font
        self.skip_button_sprite = pygame.image.load(os.path.join("assets", "ui", "skip_button.png")) # Load the skip button sprite

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
                self.additional_rewards = {'Gold': 0, 'Card': 0, 'Potion': 0, 'Relic': 0}
                for relic in self.run.player.relics:
                    relic.additionalRewards(self.reward_type, self.additional_rewards)
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
                common_relic = None # Set the common relic to None
                uncommon_relic = None # Set the uncommon relic to None
                rare_relic = None # Set the rare relic to None
                while True:
                    common_relic = relic_data.createCommon() # Create a common relic
                    for relic in self.run.player.relics: # For each relic in the player's relics
                        if relic.name == common_relic.name: # If the relic is the same as the common relic
                            continue # Continue the loop
                    break
                while True:
                    uncommon_relic = relic_data.createUncommon() # Create an uncommon relic
                    for relic in self.run.player.relics: # For each relic in the player's relics
                        if relic.name == uncommon_relic.name: # If the relic is the same as the uncommon relic
                            continue
                    break
                while True:
                    rare_relic = relic_data.createRare() # Create a rare relic
                    for relic in self.run.player.relics: # For each relic in the player's relics
                        if relic.name == rare_relic.name: # If the relic is the same as the rare relic
                            continue # Continue the loop
                    break
                self.rewards['Relics'].append(common_relic) # Add the common relic to the rewards
                self.rewards['Relics'].append(uncommon_relic) # Add the uncommon relic to the rewards
                self.rewards['Relics'].append(rare_relic) # Add the rare relic to the rewards
            elif self.set_reward == 'Booster Pack':
                # Booster pack reward
                for k in range(0, 5): # For 5 cards
                    cards, self.rareChanceOffset = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class) # Generate a card reward
                    for i in range(0, len(cards)): # For each card in the cards
                        card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]]) # Create a card option
                        cards[i] = card_option # Set the card to the card option
                    self.rewards['Cards'].append(cards) # Add the cards to the rewards
            elif self.set_reward == 'Cauldron':
                # Cauldron reward
                for i in range(0, 5): # For 5 potions
                    potion = potion_data.randomPotion() # Generate a random potion
                    self.rewards['Potions'].append(potion)
            elif self.set_reward == 'Tiny House':
                # Tiny house reward - House Deed relic
                self.rewards['Gold'] = 100
                for i in range(0, 2):
                    potion = potion_data.randomPotion()
                    self.rewards['Potions'].append(potion) # Add the potion to the rewards
                cards, self.rareChanceOffset = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class) # Generate a card reward
                for i in range(0, len(cards)): # For each card in the cards
                    card_option = card_constructor.create_card(cards[i], card_data.card_info[cards[i]]) # Create a card option
                    cards[i] = card_option # Set the card to the card option
                self.rewards['Cards'].append(cards)
            elif self.set_reward == 'Brewing Stand':
                # Brewing stand reward - Potion
                self.rewards['Potions'].append(potion_data.randomPotion()) # Add a random potion to the rewards
            else:
                # set reward
                self.rewards = self.set_reward # Set the rewards to the set reward
                if 'Gold' not in self.rewards: # If the gold is not in the rewards
                    self.rewards['Gold'] = 0 # Set the gold to 0
                if 'Cards' not in self.rewards: # If the cards are not in the rewards
                    self.rewards['Cards'] = [] # Set the cards to an empty list
                if 'Potions' not in self.rewards: # If the potions are not in the rewards
                    self.rewards['Potions'] = [] # Set the potions to an empty list
                if 'Relics' not in self.rewards: # If the relics are not in the rewards
                    self.rewards['Relics'] = [] # Set the relics to an empty list
            
        if self.additional_rewards: # If there are additional rewards, apply them
            if self.additional_rewards['Gold'] > 0: # Additional gold
                self.rewards['Gold'] += self.rewards['Gold']
            if self.additional_rewards['Card'] > 0: # Additional cards
                for k in range(0, self.additional_rewards['Card']): # For the number of cards
                    cards, self.rareChanceOffset = card_constructor.generate_card_reward('normal', self.rareChanceOffset, self.cardRewardOptions, self.character_class) # Generate a card reward
                    for i in range(0, len(cards)): # For each card in the cards
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

        exit = None

        # Main loop
        while not self.close:
            reward_box.fill((50, 50, 50)) # Fill the reward box with gray
            reward_y = 20 # Reset the reward y position

            if known_screen:
                self.run.screen.blit(screen, (0, 0))
            else:
                screen.fill((0, 0, 0, 25))
                self.run.screen.blit(screen, (0, 0))

            mouse_pos = pygame.mouse.get_pos() # Get the mouse position
            events = pygame.event.get() # Get the events
            self.run.potion_events(mouse_pos, events) # Handle the potion events
            self.run.handle_deck_view(events, mouse_pos) # Handle the deck view
            exit = self.run.handle_save_and_exit_input(events) # Handle the save and exit input
            if exit == 'Main Menu': # If the exit is the main menu
                self.close = True
                break

            # Draw rewards on reward_box
            if self.rewards['Gold']:
                gold_rect = pygame.Rect(30, reward_y, 460, reward_height) # Create a gold rectangle
                pygame.draw.rect(reward_box, (70, 70, 70), gold_rect) # Draw the gold rectangle
                reward_box.blit(self.gold_sprite, (gold_rect.left + 10, gold_rect.centery - self.gold_sprite.get_height()//2)) # Draw the gold sprite
                font = pygame.font.Font(None, 36) # Create a font
                text = font.render(f"{self.rewards['Gold']}", True, (255, 255, 255)) # Render the text
                reward_box.blit(text, (gold_rect.left + 70, gold_rect.centery - text.get_height()//2)) # Draw the text
                reward_y += reward_height + reward_spacing # Add the reward height and spacing to the reward y position

            for card_options in self.rewards['Cards']: # For each card in the cards
                card_rect = pygame.Rect(30, reward_y, 460, reward_height) # Create a card rectangle
                pygame.draw.rect(reward_box, (70, 70, 70), card_rect) # Draw the card rectangle
                reward_box.blit(self.deck_button_sprite, (card_rect.left + 10, card_rect.centery - self.deck_button_sprite.get_height()//2)) # Draw the deck button sprite
                font = pygame.font.Font(None, 36) # Create a font
                text = font.render("Add a card to your deck", True, (255, 255, 255)) # Render the text
                reward_box.blit(text, (card_rect.left + 70, card_rect.centery - text.get_height()//2)) # Draw the text
                reward_y += reward_height + reward_spacing # Add the reward height and spacing to the reward y position

            # Track if mouse is hovering over any item
            mouse_pos = pygame.mouse.get_pos()
            box_mouse_pos = (mouse_pos[0] - reward_box_rect.left, mouse_pos[1] - reward_box_rect.top)
            hover_text = None
            
            # Draw potions
            for potion in self.rewards['Potions']: # For each potion in the potions
                potion_rect = pygame.Rect(30, reward_y, 460, reward_height) # Create a potion rectangle
                pygame.draw.rect(reward_box, (70, 70, 70), potion_rect) # Draw the potion rectangle
                reward_box.blit(potion.sprite, (potion_rect.left + 10, potion_rect.centery - potion.sprite.get_height()//2)) # Draw the potion sprite
                font = pygame.font.Font(None, 36) # Create a font
                text = font.render(potion.name, True, (255, 255, 255)) # Render the text
                reward_box.blit(text, (potion_rect.left + 70, potion_rect.centery - text.get_height()//2))
                
                if potion_rect.collidepoint(box_mouse_pos): # If the potion rectangle collides with the box mouse position
                    hover_text = potion.description # Set the hover text to the potion description
                
                reward_y += reward_height + reward_spacing # Add the reward height and spacing to the reward y position

            # Draw relics
            for relic in self.rewards['Relics']: # For each relic in the relics
                relic_rect = pygame.Rect(30, reward_y, 460, reward_height)
                pygame.draw.rect(reward_box, (70, 70, 70), relic_rect) # Draw the relic rectangle
                reward_box.blit(relic.sprite, (relic_rect.left + 10, relic_rect.centery - relic.sprite.get_height()//2)) # Draw the relic sprite
                font = pygame.font.Font(None, 36) # Create a font
                text = font.render(relic.name, True, (255, 255, 255))
                reward_box.blit(text, (relic_rect.left + 70, relic_rect.centery - text.get_height()//2))
                
                if relic_rect.collidepoint(box_mouse_pos): # If the relic rectangle collides with the box mouse position
                    hover_text = relic.description # Set the hover text to the relic description
                    
                reward_y += reward_height + reward_spacing # Add the reward height and spacing to the reward y position

            # Blit reward_box to screen
            self.run.screen.blit(reward_box, reward_box_rect)

            # Draw hover text if needed
            if hover_text:
                # Create text surface
                desc_font = pygame.font.Font(None, 24) # Create a font
                desc_text = desc_font.render(hover_text, True, (255, 255, 255)) # Render the text
                desc_bg = pygame.Surface((desc_text.get_width() + 20, desc_text.get_height() + 20)) # Create a background surface
                desc_bg.fill((50, 50, 50)) # Fill the background surface with gray
                desc_bg.blit(desc_text, (10, 10)) # Draw the text
                
                # Position near mouse but ensure on screen
                desc_x = min(mouse_pos[0], self.run.SCREEN_WIDTH - desc_bg.get_width())
                desc_y = min(mouse_pos[1] - desc_bg.get_height(), self.run.SCREEN_HEIGHT - desc_bg.get_height())
                self.run.screen.blit(desc_bg, (desc_x, desc_y))

            # Draw skip button directly on screen
            skip_rect = self.skip_button_sprite.get_rect() # Get the rect of the skip button sprite
            skip_rect.bottomright = (self.run.SCREEN_WIDTH, self.run.SCREEN_HEIGHT - 200) # Set the bottom right of the skip button rect to the screen width and 200 pixels from the bottom
            self.run.screen.blit(self.skip_button_sprite, skip_rect) # Draw the skip button sprite
            self.run.player.draw_ui(self.run.screen) # Draw the player ui
            pygame.display.flip() # Flip the display

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

                    if self.rewards['Gold']: # If the gold is in the rewards
                        gold_rect = pygame.Rect(30, reward_y, 460, reward_height) # Create a gold rectangle
                        if gold_rect.collidepoint(box_mouse_pos): # If the gold rectangle collides with the box mouse position
                            self.run.gold_modification(self.rewards['Gold']) # Modify the gold
                            self.rewards['Gold'] = 0 # Set the gold to 0
                        reward_y += reward_height + reward_spacing

                    for i, card_options in enumerate(self.rewards['Cards']): # For each card in the cards
                        card_rect = pygame.Rect(30, reward_y, 460, reward_height) # Create a card rectangle
                        if card_rect.collidepoint(box_mouse_pos): # If the card rectangle collides with the box mouse position
                            # Show card selection menu
                            card_menu = True
                            while card_menu:
                                # Create a transparent surface for the background
                                background = pygame.Surface(self.run.screen.get_size(), pygame.SRCALPHA) # Create a background surface
                                background.fill((0, 0, 0, 25)) # Fill the background surface with gray
                                self.run.screen.blit(background, (0, 0)) # Draw the background surface
                                events = pygame.event.get() # Get the events
                                mouse_pos = pygame.mouse.get_pos() # Get the mouse position
                                self.run.potion_events(mouse_pos, events)
                                self.run.handle_deck_view(events, mouse_pos)
                                
                                # Draw cards
                                card_x = self.run.SCREEN_WIDTH//4 # Set the card x position to the screen width divided by 4
                                for j, card in enumerate(card_options): # For each card in the card options
                                    card.rect.center = (card_x, self.run.SCREEN_HEIGHT//2) # Set the card rect center to the screen height divided by 2
                                    self.run.screen.blit(card.sprite, card.rect) # Draw the card sprite
                                    card.current_pos = (card.rect.x, card.rect.y) # Set the card current position to the card rect x and y
                                    card.draw_energy_cost(self.run.screen) # Draw the card energy cost
                                    card_x += self.run.SCREEN_WIDTH//4 # Add the screen width divided by 4 to the card x position

                                # Draw skip button
                                skip_rect = self.skip_button_sprite.get_rect() # Get the rect of the skip button sprite
                                skip_rect.bottomright = (self.run.SCREEN_WIDTH, self.run.SCREEN_HEIGHT - 200) # Set the bottom right of the skip button rect to the screen width and 200 pixels from the bottom
                                self.run.screen.blit(self.skip_button_sprite, skip_rect) # Draw the skip button sprite

                                for card_event in pygame.event.get(): # For each card event
                                    if card_event.type == pygame.QUIT or (card_event.type == pygame.KEYDOWN and card_event.key == pygame.K_F4 and (pygame.key.get_mods() & pygame.KMOD_ALT)): # If the card event is the quit event or the F4 key is pressed with the alt key
                                        pygame.quit() # Quit the game
                                        
                                    if card_event.type == pygame.MOUSEBUTTONUP and card_event.button == 1: # If the card event is the mouse button up event and the button is 1
                                        card_mouse_pos = pygame.mouse.get_pos() # Get the mouse position
                                        if skip_rect.collidepoint(card_mouse_pos): # If the skip button rect collides with the card mouse position
                                            card_menu = False # Set the card menu to False
                                        else:
                                            for j, card in enumerate(card_options): # For each card in the card options
                                                if card.rect.collidepoint(card_mouse_pos): # If the card rect collides with the card mouse position
                                                    self.run.card_pickup(card) # Pickup the card
                                                    self.rewards['Cards'].pop(i) # Pop the card from the cards
                                                    card_menu = False # Set the card menu to False
                                                    break # Break the loop
                                                
                                pygame.display.flip() # Flip the display

                                

                        reward_y += reward_height + reward_spacing

                    for i, potion in enumerate(self.rewards['Potions']): # For each potion in the potions
                        potion_rect = pygame.Rect(30, reward_y, 460, reward_height) # Create a potion rectangle
                        if potion_rect.collidepoint(box_mouse_pos): # If the potion rectangle collides with the box mouse position
                            if self.run.potion_pickup(potion): # If the potion pickup is successful
                                self.rewards['Potions'].pop(i) # Pop the potion from the potions
                        reward_y += reward_height + reward_spacing

                    for i, relic in enumerate(self.rewards['Relics']):
                        relic_rect = pygame.Rect(30, reward_y, 460, reward_height) # Create a relic rectangle
                        if relic_rect.collidepoint(box_mouse_pos): # If the relic rectangle collides with the box mouse position
                            print(self.run.player.relics)
                            self.rewards['Relics'].pop(i) # Pop the relic from the relics
                        reward_y += reward_height + reward_spacing

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # If the event is the key down event and the key is the escape key
                    self.close = True # Set the close to True

            if not any([self.rewards['Gold'], self.rewards['Cards'], self.rewards['Potions'], self.rewards['Relics']]):
                self.close = True # Set the close to True
        
        if exit == 'Main Menu': # If the exit is the main menu
            self.run.main_menu.main_menu() # Main menu
