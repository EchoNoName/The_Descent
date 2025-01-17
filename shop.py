import random
import card_constructor
import card_data
import relic_data
import potion_data
import effects
import random
import pygame
import os

class Shop:
    def __init__(self, run):
        self.run = run
        self.wares = { # Initialize the wares to a dictionary with the keys 0-13 and the values None
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
            13: 'Remove'
        }
        self.generated = False # Initialize the generated to False
        self.discounted = False # Initialize the discounted to False
        gold_sprite = pygame.image.load(os.path.join("assets", "icons", "gold.png")) # Load the gold sprite
        self.gold_icon_sprite = pygame.transform.scale(gold_sprite, (gold_sprite.get_width()//11, gold_sprite.get_height()//11)) # Scale the gold sprite
        pygame.font.init() # Initialize the font
        self.font = pygame.font.Font('assets/fonts/Kreon-Bold.ttf', 36) # Load the font
        self.removal_sprite = pygame.image.load(os.path.join("assets", "icons", "pile_icon.png"))
        self.removal_sprite = pygame.transform.scale(self.removal_sprite, (self.removal_sprite.get_width()//2, self.removal_sprite.get_height()//2)) # Scale the removal sprite
        self.removal_rect = self.removal_sprite.get_rect() # Get the rect of the removal sprite
        self.confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png")) # Load the confirm sprite
        self.confirm_rect = self.confirm_sprite.get_rect() # Get the rect of the confirm sprite
        self.background_sprite = pygame.image.load(os.path.join("assets", "ui", "shop_background.png")) # Load the background sprite
        self.close = False # Initialize the close to False

    def generate_wares(self):
        if self.run.player.character_class == 1: # If the character class is 1
            if self.generated == False: # If the generated is False
                card1 = random.choice(card_constructor.attack_card_1) # Choose a random card from the attack card 1 list
                card2 = random.choice(card_constructor.attack_card_1) # Choose a random card from the attack card 1 list
                card3 = random.choice(card_constructor.skill_card_1) # Choose a random card from the skill card 1 list
                card4 = random.choice(card_constructor.skill_card_1) # Choose a random card from the skill card 1 list
                card5 = random.choice(card_constructor.power_card_1)
                card1 = card_constructor.create_card(card1, card_data.card_info[card1]) # Create a card from the card 1
                card2 = card_constructor.create_card(card2, card_data.card_info[card2]) # Create a card from the card 2
                card3 = card_constructor.create_card(card3, card_data.card_info[card3]) # Create a card from the card 3
                card4 = card_constructor.create_card(card4, card_data.card_info[card4]) # Create a card from the card 4
                card5 = card_constructor.create_card(card5, card_data.card_info[card5]) # Create a card from the card 5
                self.wares[0] = card1 # Set the ware 0 to the card 1
                self.wares[1] = card2 # Set the ware 1 to the card 2
                self.wares[2] = card3 # Set the ware 2 to the card 3
                self.wares[3] = card4 # Set the ware 3 to the card 4
                self.wares[4] = card5
                for i in range(0, 5):
                    if self.wares[i].rarity == 1: # If the rarity of the ware is 1
                        self.wares[i] =[self.wares[i], random.randint(45, 55)] # Set the ware to the card and the cost to a random number between 45 and 55
                    elif self.wares[i].rarity == 2: # If the rarity of the ware is 2
                        self.wares[i] = [self.wares[i], random.randint(68, 82)] # Set the ware to the card and the cost to a random number between 68 and 82
                    elif self.wares[i].rarity == 3: # If the rarity of the ware is 3
                        self.wares[i] = [self.wares[i], random.randint(135, 165)] # Set the ware to the card and the cost to a random number between 135 and 165
                while True: # While True
                    combined_list = card_constructor.attack_card_1 # Combine the attack card 1 list
                    combined_list.extend(card_constructor.skill_card_1) # Extend the combined list with the skill card 1 list
                    combined_list.extend(card_constructor.power_card_1) # Extend the combined list with the power card 1 list
                    card6 = random.choice(combined_list) # Choose a random card from the combined list
                    if card_data.card_info[card6][1] == 2: # If the rarity of the card is 2
                        card6 = card_constructor.create_card(card6, card_data.card_info[card6]) # Create a card from the card
                        self.wares[5] = [card6, random.randint(81, 99)] # Set the ware 5 to the card and the cost to a random number between 81 and 99
                        break # Break the loop
                    else: # Else
                        continue # Continue the loop
                while True: # While True
                    card7 = random.choice(combined_list) # Choose a random card from the combined list
                    if card_data.card_info[card7][1] == 3: # If the rarity of the card is 3
                        card7 = card_constructor.create_card(card7, card_data.card_info[card7]) # Create a card from the card
                        self.wares[6] = [card7, random.randint(162, 198)] # Set the ware 6 to the card and the cost to a random number between 162 and 198
                        break # Break the loop
                    else: # Else
                        continue # Continue the loop
                self.wares[7] = [potion_data.randomPotion(), random.randint(48, 105)] # Set the ware 7 to a random potion and the cost to a random number between 48 and 105    
                self.wares[8] = [potion_data.randomPotion(), random.randint(48, 105)] # Set the ware 8 to a random potion and the cost to a random number between 48 and 105
                self.wares[9] = [potion_data.randomPotion(), random.randint(48, 105)] # Set the ware 9 to a random potion and the cost to a random number between 48 and 105
                relic1 = None # Initialize the relic 1 to None
                while True: # While True
                    relic1 = relic_data.spawnRelic() # Spawn a random relic
                    for owned_relic in self.run.player.relics: # For each owned relic
                        if owned_relic.name == relic1.name: # If the name of the owned relic is the same as the name of the relic
                            continue # Continue the loop
                    break # Break the loop
                if relic1.rarity == 4:
                    self.wares[10] = [relic1, random.randint(143, 157)] # Set the ware 10 to the relic and the cost to a random number between 143 and 157
                elif relic1.rarity == 3: # If the rarity of the relic is 3
                    self.wares[10] = [relic1, random.randint(238, 262)] # Set the ware 10 to the relic and the cost to a random number between 238 and 262
                elif relic1.rarity == 2: # If the rarity of the relic is 2
                    self.wares[10] = [relic1, random.randint(285, 315)] # Set the ware 10 to the relic and the cost to a random number between 285 and 315
                relic2 = None # Initialize the relic 2 to None
                while True: # While True
                    relic2 = relic_data.spawnRelic() # Spawn a random relic
                    for owned_relic in self.run.player.relics: # For each owned relic
                        if owned_relic.name == relic2.name: # If the name of the owned relic is the same as the name of the relic
                            continue # Continue the loop
                    break # Break the loop
                if relic2.rarity == 4: # If the rarity of the relic is 4    
                    self.wares[11] = [relic2, random.randint(143, 157)] # Set the ware 11 to the relic and the cost to a random number between 143 and 157
                elif relic2.rarity == 3: # If the rarity of the relic is 3
                    self.wares[11] = [relic2, random.randint(238, 262)] # Set the ware 11 to the relic and the cost to a random number between 238 and 262
                elif relic2.rarity == 2: # If the rarity of the relic is 2  
                    self.wares[11] = [relic2, random.randint(285, 315)] # Set the ware 11 to the relic and the cost to a random number between 285 and 315
                shopRelic = None # Initialize the shop relic to None
                while True: # While True
                    shopRelic = random.choice(list(relic_data.shopRelics.keys())) # Choose a random relic from the shop relics
                    shopRelic = relic_data.createRelic(shopRelic, relic_data.shopRelics[shopRelic]) # Create a relic from the shop relic
                    for owned_relic in self.run.player.relics: # For each owned relic
                        if owned_relic.name == shopRelic.name: # If the name of the owned relic is the same as the name of the relic
                            continue # Continue the loop
                    break # Break the loop
                self.wares[12] = [shopRelic, random.randint(143, 157)] # Set the ware 12 to the relic and the cost to a random number between 143 and 157
                removalCost = 75 + self.run.removals * 25 # Set the removal cost to 75 plus the number of removals times 25
                for relic in self.run.player.relics: # For each relic in the player's relics
                    if relic.name == 'Coupon': # If the name of the relic is 'Coupon'
                        removalCost = 50 # Set the removal cost to 50
                self.wares[13] = ['Remove', removalCost] # Set the ware 13 to 'Remove' and the cost to the removal cost
        for relic in self.run.player.relics: # For each relic in the player's relics
            if relic.name == 'Costco\'s Membership Card': # If the name of the relic is 'Costco\'s Membership Card'
                for ware in self.wares.values(): # For each ware in the wares   
                    if ware and ware[0]: # If the ware is not None and the ware is not 'Remove'
                        ware[1] = int(ware[1] * 0.5) # Set the cost of the ware to the cost times 0.5
                self.discounted = True # Set the discounted to True

    def interact(self):
        self.close = False # Set the close to False
        exit = None # Initialize the exit to None
        screen = pygame.display.get_surface() # Get the screen
        shop_surface = pygame.Surface((1600, 900)) # Create a shop surface
        shop_rect = shop_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2)) # Get the rect of the shop surface

        while not self.close:
            screen.fill((0, 0, 0))
            shop_surface.blit(self.background_sprite, (0, 0))
            
            # Display cards 0-4 in top row
            for i in range(5):
                if self.wares[i] and self.wares[i][0]:
                    card_x = 200 + i * 250 # Set the x position of the card to 200 plus the index times 250
                    card_y = 150 # Set the y position of the card to 150
                    self.wares[i][0].current_pos = (card_x, card_y) # Set the current position of the card to the card x and y
                    self.wares[i][0].update_rect() # Update the rect of the card
                    self.wares[i][0].draw(shop_surface) # Draw the card
                    
                    # Draw gold cost below
                    shop_surface.blit(self.gold_icon_sprite, (card_x, card_y + 250))
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0))
                    shop_surface.blit(cost_text, (card_x + 80, card_y + 250))

            self.run.player.draw_ui(shop_surface)

            # Display cards 5-6 below cards 0-1
            for i in range(5, 7): # For each card in the range 5 to 7
                if self.wares[i] and self.wares[i][0]: # If the ware is not None and the ware is not 'Remove'
                    card_x = 200 + (i-5) * 250 # Set the x position of the card to 200 plus the index minus 5 times 250
                    card_y = 500 # Set the y position of the card to 500
                    self.wares[i][0].current_pos = (card_x, card_y) # Set the current position of the card to the card x and y
                    self.wares[i][0].draw(shop_surface) # Draw the card
                    self.wares[i][0].update_rect() # Update the rect of the card

                    shop_surface.blit(self.gold_icon_sprite, (card_x, card_y + 250)) # Draw the gold icon
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0)) # Render the cost text
                    shop_surface.blit(cost_text, (card_x + 80, card_y + 250))

            # Display relics row below cards 2-3
            for i in range(10, 13):
                if self.wares[i] and self.wares[i][0]:
                    relic_x = 720 + (i-10) * 165
                    relic_y = 500 # Set the y position of the relic to 500
                    self.wares[i][0].draw(shop_surface, relic_x, relic_y) # Draw the relic
                    self.wares[i][0].rect.topleft = (relic_x, relic_y) # Set the rect of the relic to the relic x and y
                    
                    shop_surface.blit(self.gold_icon_sprite, (relic_x - 50, relic_y + 75))
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0))
                    shop_surface.blit(cost_text, (relic_x + 10, relic_y + 75))

            # Display potions row below cards 2-3
            for i in range(7, 10):
                if self.wares[i] and self.wares[i][0]:
                    potion_x = 720 + (i-7) * 165
                    potion_y = 700 # Set the y position of the potion to 700
                    self.wares[i][0].draw(shop_surface, potion_x, potion_y) # Draw the potion
                    self.wares[i][0].rect.topleft = (potion_x, potion_y) # Set the rect of the potion to the potion x and y
                    shop_surface.blit(self.gold_icon_sprite, (potion_x - 50, potion_y + 50)) # Draw the gold icon
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0))
                    shop_surface.blit(cost_text, (potion_x + 10, potion_y + 50))

            # Display card removal box below card 4
            if self.wares[13] and self.wares[13][0]: # If the ware is not None and the ware is not 'Remove'
                removal_x = 1200 # Set the x position of the removal to 1200
                removal_y = 500 # Set the y position of the removal to 500
                shop_surface.blit(self.removal_sprite, (removal_x, removal_y)) # Draw the removal sprite
                self.removal_rect.topleft = (removal_x, removal_y) # Set the rect of the removal to the removal x and y
                
                shop_surface.blit(self.gold_icon_sprite, (removal_x, removal_y + 250))
                cost_text = self.font.render(str(self.wares[13][1]), True, (255, 215, 0))
                shop_surface.blit(cost_text, (removal_x + 80, removal_y + 250)) # Draw the cost text

            # Draw confirm button in bottom right
            confirm_x = shop_surface.get_width() - self.confirm_sprite.get_width() # Set the x position of the confirm to the width of the shop surface minus the width of the confirm sprite
            confirm_y = shop_surface.get_height() - 200 # Set the y position of the confirm to the height of the shop surface minus 200
            shop_surface.blit(self.confirm_sprite, (confirm_x, confirm_y))
            self.confirm_rect = self.confirm_sprite.get_rect(topleft=(confirm_x, confirm_y))

            # Blit shop surface to screen
            screen.blit(shop_surface, shop_rect)

            # Handle mouse hover for tooltips
            mouse_pos = pygame.mouse.get_pos()
            shop_mouse_pos = (mouse_pos[0] - shop_rect.left, mouse_pos[1] - shop_rect.top)
            hover_name = None
            hover_text = None

            for ware in self.wares.values(): # For each ware in the wares
                if ware and ware[0]: # If the ware is not None and the ware is not 'Remove'
                    if ware[0] != 'Remove': # If the ware is not 'Remove'
                        if ware[0].rect.collidepoint(shop_mouse_pos) and not isinstance(ware[0], card_constructor.Card): # If the rect of the ware collides with the shop mouse position and the ware is not a card
                            hover_text = str(ware[0].description) # Set the hover text to the description of the ware
                            hover_name = ware[0].name # Set the hover name to the name of the ware
                    else: # If the ware is 'Remove'
                        if self.removal_rect.collidepoint(shop_mouse_pos): # If the removal rect collides with the shop mouse position
                            hover_text = "Remove a card from your deck"


            if self.run.player.deck_button_rect.collidepoint(mouse_pos): # If the deck button rect collides with the mouse position
                deck_hovering = True # Set the deck hovering to True
            else: # If the deck button rect does not collide with the mouse position
                deck_hovering = False # Set the deck hovering to False
            
            if deck_hovering: # If the deck hovering is True
                deck_text_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 16) # Set the deck text font to the Kreon-Bold font at size 16
                # Create background surface
                deck_text = deck_text_font.render("View Deck", True, (255, 255, 255)) # Render the deck text
                bg_surface = pygame.Surface((deck_text.get_width() + 10, deck_text.get_height() + 6))
                bg_surface.fill((0, 0, 0))
                text_x = self.run.player.deck_button_rect.centerx - deck_text.get_width() // 2
                text_y = self.run.player.deck_button_rect.bottom + 35  # Changed from +10 to +30
                # Draw background then text
                shop_surface.blit(bg_surface, (text_x - 5, text_y - 3)) # Draw the background
                shop_surface.blit(deck_text, (text_x, text_y)) # Draw the deck text

            # Draw hover text if needed
            if hover_text:
                desc_font = pygame.font.Font(None, 24)
                
                # Split text into lines if it's too long
                words = hover_text.split()
                lines = []
                current_line = []
                test_font = pygame.font.Font(None, 24)
                
                for word in words:
                    current_line.append(word)
                    test_text = test_font.render(' '.join(current_line), True, (255, 255, 255)) # Render the test text
                    if test_text.get_width() > screen.get_width() - 40:  # Leave some margin
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line)) # Add the current line to the lines
                
                desc_texts = [desc_font.render(line, True, (255, 255, 255)) for line in lines] # Render the description texts
                
                if hover_name:
                    name_text = self.font.render(hover_name, True, (255, 255, 255))
                    total_height = sum(text.get_height() for text in desc_texts) + name_text.get_height() + 25 # Set the total height to the sum of the height of the description texts plus the height of the name text plus 25
                    max_width = max(max(text.get_width() for text in desc_texts), name_text.get_width()) # Set the max width to the maximum of the width of the description texts and the width of the name text
                    desc_bg = pygame.Surface((max_width + 20, total_height)) # Create a surface with the max width plus 20 and the total height
                    desc_bg.fill((50, 50, 50)) # Fill the surface with the color (50, 50, 50)
                    desc_bg.blit(name_text, (10, 10))
                    
                    y_offset = name_text.get_height() + 15 # Set the y offset to the height of the name text plus 15
                    for text in desc_texts: # For each text in the description texts
                        desc_bg.blit(text, (10, y_offset)) # Draw the text
                        y_offset += text.get_height() # Add the height of the text to the y offset
                else: # If the hover name is not None
                    total_height = sum(text.get_height() for text in desc_texts) + 20
                    max_width = max(text.get_width() for text in desc_texts)
                    desc_bg = pygame.Surface((max_width + 20, total_height))
                    desc_bg.fill((50, 50, 50))

                    y_offset = 10
                    for text in desc_texts:
                        desc_bg.blit(text, (10, y_offset))
                        y_offset += text.get_height()
                
                desc_x = min(mouse_pos[0], screen.get_width() - desc_bg.get_width())
                desc_y = min(mouse_pos[1] - desc_bg.get_height(), screen.get_height() - desc_bg.get_height())
                screen.blit(desc_bg, (desc_x, desc_y))

            # Draw debug rect boxes for testing
            # for ware in self.wares.values():
            #     if ware and ware[0] and ware[0] != 'Remove':
            #         pygame.draw.rect(screen, (255, 0, 0), ware[0].rect, 2)  # Red outline for items
            
            # Draw card removal service rect
            # pygame.draw.rect(screen, (0, 255, 0), self.removal_rect, 2)  # Green outline for removal service

            pygame.display.flip()
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos) # Handle the deck view
            self.run.potion_events(mouse_pos, events) # Handle the potion events
            exit = self.run.handle_save_and_exit_input(events) # Handle the save and exit input
            if exit == 'Main Menu': # If the exit is the main menu
                self.close = True
                break

            for event in events: # For each event in the events
                if event.type == pygame.QUIT: # If the event is the quit event
                    pygame.quit() # Quit the game
                    
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.confirm_rect.collidepoint(mouse_pos):
                        self.close = True
                        break

                    if deck_hovering: # If the deck hovering is True
                        self.run.player.view_deck() # View the deck
                    
                    for ware in self.wares.values():
                        if ware and ware[0]:
                            if ware[0] != 'Remove': # If the ware is not 'Remove'
                                if ware[0].rect.collidepoint(mouse_pos): # If the rect of the ware collides with the mouse position
                                    if ware[1] <= self.run.player.gold: # If the cost of the ware is less than or equal to the player's gold
                                        self.run.gold_modification(-ware[1]) # Modify the player's gold by the cost of the ware
                                        self.break_piggy_bank() # Break the piggy bank
                                        item = ware[0] # Set the item to the ware
                                        ware[0] = None # Set the ware to None
                                        if isinstance(item, card_constructor.Card): # If the item is a card
                                            self.run.card_pickup(item) # Pickup the card
                                        elif isinstance(item, potion_data.Potion): # If the item is a potion
                                            if None in self.run.player.potions: # If the player's potions is None
                                                self.run.potion_pickup(item) # Pickup the potion
                                            else: # If the player's potions is not None
                                                self.run.gold += -ware[1] # Modify the player's gold by the cost of the ware
                                                ware[0] = item # Set the ware to the item
                                        elif isinstance(item, relic_data.Relics): # If the item is a relic
                                            self.run.relic_pickup(item)
                                            if item.name == 'Costco\'s Membership Card':
                                                for ware in self.wares.values():
                                                    if ware and ware[0]:
                                                        ware[1] = int(ware[1] * 0.5) # Modify the cost of the ware by 50%
                                                self.discounted = True # Set the discounted to True
                    
                    if self.removal_rect.collidepoint(mouse_pos) and self.wares[13] and self.wares[13][0]: # If the removal rect collides with the mouse position and the ware is not None and the ware is not 'Remove'
                        if self.run.player.deck and self.run.player.gold >= self.wares[13][1]: # If the player's deck is not None and the player's gold is greater than or equal to the cost of the ware
                            effects.card_select(1, {}, self.run) # Select the card
                            self.run.player.remove_card() # Remove the card
                            self.run.removals += 1 # Add 1 to the removals
                            self.run.gold_modification(-self.wares[13][1]) # Modify the player's gold by the cost of the ware
                            self.wares[13] = [None, None] # Set the ware to None
                            self.break_piggy_bank() # Break the piggy bank
        
        if exit == 'Main Menu':
            self.run.main_menu.main_menu()

    def break_piggy_bank(self):
        if self.run.player.relics: # If the player's relics is not None
            for relic in self.run.player.relics: # For each relic in the player's relics
                if relic.name == 'Piggy Bank': # If the relic's name is 'Piggy Bank'
                    self.run.player.relics.remove(relic) # Remove the relic
                    break # Break the loop

