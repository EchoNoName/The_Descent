import combat
import card_data
import potion_data
import pygame
import os
import card_constructor
import relic_data

class Campfire:
    def __init__(self, run):
        self.run = run
        self.upgradable_cards = [] # List of upgradable cards
        self.confirm_button_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png")) # Load the confirm button sprite
        self.back_button_sprite = pygame.image.load(os.path.join("assets", "ui", "back_button.png")) # Load the back button sprite  
        self.skip_button_sprite = pygame.image.load(os.path.join("assets", "ui", "skip_button.png")) # Load the skip button sprite
        self.fertilize_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "fertilize.png")) # Load the fertilize button sprite
        self.dig_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "dig.png")) # Load the dig button sprite
        self.shred_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "shred.png")) # Load the shred button sprite
        self.rest_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "rest.png")) # Load the rest button sprite
        self.smith_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "smith.png")) # Load the smith button sprite
        self.campfire_background_sprite = pygame.image.load(os.path.join("assets", "ui", "campfire_background.png")) # Load the campfire background sprite
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 24)
        self.options = run.campfire # Dictionary of options
        self.completed = False # Boolean to check if the campfire is completed

    def run_campfire(self):
        '''Method to run the campfire'''
        campfire = True # Boolean to check if the campfire is active
        confirm_button = pygame.Rect(1600 - self.confirm_button_sprite.get_width(), 650, self.confirm_button_sprite.get_width(), self.confirm_button_sprite.get_height()) # Create the confirm button
        skip_button = pygame.Rect(1600 - self.skip_button_sprite.get_width(), 650, self.skip_button_sprite.get_width(), self.skip_button_sprite.get_height()) # Create the skip button
        if self.options['Rest']: # If the rest option is available
            rest_button = pygame.Rect(400, 250, self.rest_button_sprite.get_width(), self.rest_button_sprite.get_height()) # Create the rest button
        if self.options['Smith']: # If the smith option is available
            smith_button = pygame.Rect(900, 250, self.smith_button_sprite.get_width(), self.smith_button_sprite.get_height()) # Create the smith button
        if self.options['Fertilize']: # If the fertilize option is available
            fertilize_button = pygame.Rect(250, 520, self.fertilize_button_sprite.get_width(), self.fertilize_button_sprite.get_height()) # Create the fertilize button
        if self.options['Dig']: # If the dig option is available
            dig_button = pygame.Rect(1050, 520, self.dig_button_sprite.get_width(), self.dig_button_sprite.get_height()) # Create the dig button
        if self.options['Shred']: # If the shred option is available
            shred_button = pygame.Rect(650, 520, self.shred_button_sprite.get_width(), self.shred_button_sprite.get_height()) # Create the shred button
        
        rest_hover = False # Boolean to check if the rest button is hovered over
        smith_hover = False # Boolean to check if the smith button is hovered over
        fertilize_hover = False # Boolean to check if the fertilize button is hovered over
        dig_hover = False # Boolean to check if the dig button is hovered over
        shred_hover = False # Boolean to check if the shred button is hovered over
        exit = None # Variable to check if the game is exited

        while campfire: # While the campfire is active
            selection_surface = pygame.Surface((1600, 900), pygame.SRCALPHA) # Create a transparent surface

            events = pygame.event.get() # Get the events
            mouse_pos = pygame.mouse.get_pos() # Get the mouse position
            self.run.potion_events(mouse_pos, events) # Handle potion events
            self.run.handle_deck_view(events, mouse_pos) # Handle deck view events
            exit = self.run.handle_save_and_exit_input(events) # Handle save and exit input
            if exit == 'Main Menu': # If the game is exited
                campfire = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    campfire = False
                    self.run.exit_game()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # If the mouse button is clicked
                    if confirm_button.collidepoint(mouse_pos): # If the confirm button is clicked
                        campfire = False # Set the campfire to inactive
                        break
                    elif skip_button.collidepoint(mouse_pos): # If the skip button is clicked
                        campfire = False # Set the campfire to inactive
                        break
                
                    elif self.options['Rest'] and rest_button.collidepoint(mouse_pos): # If the rest button is clicked and the rest option is available
                        self.rest() # Rest
                        break
                    elif self.options['Smith'] and smith_button.collidepoint(mouse_pos): # If the smith button is clicked and the smith option is available
                        self.smith() # Smith
                        break
                    elif self.options['Fertilize'] and fertilize_button.collidepoint(mouse_pos): # If the fertilize button is clicked and the fertilize option is available
                        self.fertilize() # Fertilize
                        break
                    elif self.options['Dig'] and dig_button.collidepoint(mouse_pos): # If the dig button is clicked and the dig option is available
                        self.dig() # Dig
                        break
                    elif self.options['Shred'] and shred_button.collidepoint(mouse_pos): # If the shred button is clicked and the shred option is available
                        self.shred() # Shred
                        break
            
                if self.options['Rest']: # If the rest option is available
                    if rest_button.collidepoint(mouse_pos): # If the rest button is hovered over
                        rest_hover = True # Set the rest hover to True
                    else:
                        rest_hover = False # Set the rest hover to False

                if self.options['Smith']:
                    if smith_button.collidepoint(mouse_pos): # If the smith button is hovered over
                        smith_hover = True # Set the smith hover to True
                    else:
                        smith_hover = False # Set the smith hover to False
                
                if self.options['Fertilize']:
                    if fertilize_button.collidepoint(mouse_pos):
                        fertilize_hover = True # Set the fertilize hover to True
                    else:
                        fertilize_hover = False # Set the fertilize hover to False

                if self.options['Dig']:
                    if dig_button.collidepoint(mouse_pos):
                        dig_hover = True # Set the dig hover to True
                    else:
                        dig_hover = False # Set the dig hover to False

                if self.options['Shred']:
                    if shred_button.collidepoint(mouse_pos):
                        shred_hover = True # Set the shred hover to True
                    else:
                        shred_hover = False # Set the shred hover to False

            if self.completed:
                # Draw "Confirm" text above button
                selection_surface.blit(self.confirm_button_sprite, confirm_button) # Draw the confirm button
            else:
                selection_surface.blit(self.skip_button_sprite, skip_button) # Draw the skip button
                if self.options['Rest']:
                    # Draw "Rest" text above button
                    text = self.font.render("Rest", True, (255, 255, 255))
                    selection_surface.blit(text, (rest_button.centerx - text.get_width()//2, rest_button.top - 30))
                    selection_surface.blit(self.rest_button_sprite, rest_button)

                    if rest_hover:
                        # If hovering over rest button, display what the action does
                        text = self.font.render(f"Heal for 30% of Max HP. ({int(self.run.player.maxHp * 0.3)})", True, (255, 255, 255))
                        selection_surface.blit(text, (800 - text.get_width()//2, 445)) # Draw the text

                if self.options['Smith']:
                    # Draw "Smith" text above button
                    text = self.font.render("Smith", True, (255, 255, 255))
                    selection_surface.blit(text, (smith_button.centerx - text.get_width()//2, smith_button.top - 30))
                    selection_surface.blit(self.smith_button_sprite, smith_button)

                    if smith_hover:
                        # If hovering over smith button, display what the action does
                        text = self.font.render(f"Upgrade a card.", True, (255, 255, 255))
                        selection_surface.blit(text, (800 - text.get_width()//2, 445))

                if self.options['Fertilize']:
                    # Draw "Fertilize" text above button
                    text = self.font.render("Fertilize", True, (255, 255, 255))
                    selection_surface.blit(text, (fertilize_button.centerx - text.get_width()//2, fertilize_button.top - 30))
                    selection_surface.blit(self.fertilize_button_sprite, fertilize_button)

                    if fertilize_hover:
                        # If hovering over fertilize button, display what the action does
                        text = self.font.render(f"Increase Max HP by 5. (Free Action)", True, (255, 255, 255))
                        selection_surface.blit(text, (800 - text.get_width()//2, 445))

                if self.options['Dig']:
                    # Draw "Dig" text above button
                    text = self.font.render("Dig", True, (255, 255, 255))
                    selection_surface.blit(text, (dig_button.centerx - text.get_width()//2, dig_button.top - 30))
                    selection_surface.blit(self.dig_button_sprite, dig_button)

                    if dig_hover:
                        # If hovering over dig button, display what the action does
                        text = self.font.render(f"Find a relic.", True, (255, 255, 255))
                        selection_surface.blit(text, (800 - text.get_width()//2, 445))

                if self.options['Shred']:
                    # Draw "Shred" text above button
                    text = self.font.render("Shred", True, (255, 255, 255))
                    selection_surface.blit(text, (shred_button.centerx - text.get_width()//2, shred_button.top - 30))
                    selection_surface.blit(self.shred_button_sprite, shred_button)

                    if shred_hover:
                        # If hovering over shred button, display what the action does
                        text = self.font.render(f"Remove a card from your deck.", True, (255, 255, 255))
                        selection_surface.blit(text, (800 - text.get_width()//2, 445))
            
            # Use campfire background

            pygame.display.get_surface().blit(self.campfire_background_sprite, (0, 0))
            pygame.display.get_surface().blit(selection_surface, (0, 0))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()


    def get_upgradable_cards(self):
        for card in self.run.player.deck: # For each card in the player's deck
            if card.id + 100 in card_data.card_info: # If the card is upgradable
                self.upgradable_cards.append(card) # Add the card to the upgradable cards list

    def rest(self):
        self.run.player.heal(int(self.run.player.maxHp * 0.3))
        self.run.bonusEff('Rest')
        self.completed = True

    def smith(self):
        self.get_upgradable_cards()
        upgrade_pile = combat.Pile(self.upgradable_cards, 'upgrade') # Create a pile of upgradable cards
        upgrading = True # Set the upgrading to True
        
        upgrade_pile.scroll_offset = 0 # Set the scroll offset to 0

        # Create a confirm button in bottom right
        confirm_button = pygame.Rect(1600 - self.confirm_button_sprite.get_width(), 650, self.confirm_button_sprite.get_width(), self.confirm_button_sprite.get_height())
        # Create a back button in bottom left
        back_button = pygame.Rect(0 , 650, self.back_button_sprite.get_width(), self.back_button_sprite.get_height())
        exit = None

        while upgrading:
            upgrade_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
            upgrade_surface.fill((0, 0, 0, 0))  # Completely transparent background   
            # Handle events
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()

            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                upgrading = False
                break

            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                    upgrading = False
                    break
                

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    
                    if back_button.collidepoint(mouse_pos):
                        upgrading = False
                        break
                    
                    # Check if card clicked
                    for card in upgrade_pile.cards: # For each card in the upgrade pile
                        if card.rect.collidepoint(mouse_pos): # If the card is clicked
                            card.inspecting = True # Set the card to inspecting
                            inspecting = True # Set the inspecting to True
                            upgraded_card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100]) # Create an upgraded card
                            upgraded_card.inspecting = True # Set the upgraded card to inspecting
                            while inspecting: # While inspecting
                                inspect_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
                                inspect_surface.fill((0, 0, 0, 0))  # Completely transparent background   
                                
                                events = pygame.event.get() # Get the events
                                mouse_pos = pygame.mouse.get_pos() # Get the mouse position
                                self.run.handle_deck_view(events, mouse_pos) # Handle the deck view
                                self.run.potion_events(mouse_pos, events) # Handle the potion events
                                exit = self.run.handle_save_and_exit_input(events) # Handle the save and exit input
                                if exit == 'Main Menu': # If the exit is the main menu
                                    inspecting = False # Set the inspecting to False
                                    upgrading = False # Set the upgrading to False
                                    break
                                

                                for event in events:
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT): # If the F4 key is pressed with the alt key
                                        inspecting = False # Set the inspecting to False
                                        upgrading = False # Set the upgrading to False
                                        self.run.exit_game() # Exit the game
                                        break
                                        
                                    if event.type == pygame.QUIT:
                                        inspecting = False # Set the inspecting to False
                                        upgrading = False # Set the upgrading to False
                                        self.run.exit_game() # Exit the game
                                        break

                                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                        if back_button.collidepoint(mouse_pos): # If the back button is clicked
                                            inspecting = False # Set the inspecting to False
                                            break
                                        elif confirm_button.collidepoint(mouse_pos): # If the confirm button is clicked
                                            inspecting = False # Set the inspecting to False
                                            upgrading = False # Set the upgrading to False
                                            self.upgrade_card(card) # Upgrade the card
                                            self.completed = True # Set the completed to True
                                            break
                                    
                                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                                        inspecting = False # Set the inspecting to False
                                        break

                                # draw unupgraded card on the left side of the middle of the screen
                                card.current_pos = (400, 300)
                                card.draw(inspect_surface)
                                # draw upgraded card on the right side of the middle of the screen
                                upgraded_card.current_pos = (900, 300)
                                upgraded_card.draw(inspect_surface)
                                # draw confirm button
                                inspect_surface.blit(self.confirm_button_sprite, confirm_button)
                                # draw back button
                                inspect_surface.blit(self.back_button_sprite, back_button)
                                pygame.display.get_surface().blit(self.campfire_background_sprite, (0, 0))
                                pygame.display.get_surface().blit(inspect_surface, (0, 0))
                                pygame.display.flip()
                            
                            card.inspecting = False
                            break
                
                elif event.type == pygame.QUIT:
                    self.quit_game()

            if not self.completed:
                # Draw cards
                upgrade_pile.draw(upgrade_surface, events)
                
                # Draw back button
                upgrade_surface.blit(self.back_button_sprite, back_button)
                
                # Update display
                # Use campfire background
                pygame.display.get_surface().blit(self.campfire_background_sprite, (0, 0))
                pygame.display.get_surface().blit(upgrade_surface, (0, 0))
                pygame.display.flip()
        
        if exit == 'Main Menu':
            self.run.main_menu.main_menu()

    def fertilize(self):
        self.run.player.increase_max_hp(5) # Increase the player's max HP by 5
        self.options['Fertilize'] = False # Set the fertilize option to False
    
    def dig(self):
        while True:
            relic = relic_data.spawnRelic() # Spawn a relic
            if relic.name not in [relic.name for relic in self.run.player.relics]: # If the relic is not already in the player's relics
                break # Break the loop
        self.run.relic_pickup(relic) # Pick up the relic
        self.completed = True
    
    def shred(self):
        removable_cards = [card for card in self.run.player.deck if card.removable] # Get the removable cards
        removal_pile = combat.Pile(removable_cards, 'remove') # Create a pile of removable cards
        removing = True # Set the removing to True

        
        removal_pile.scroll_offset = 0

        # Create a confirm button in bottom right
        confirm_button = pygame.Rect(1600 - self.confirm_button_sprite.get_width(), 650, self.confirm_button_sprite.get_width(), self.confirm_button_sprite.get_height())
        # Create a back button in bottom left
        back_button = pygame.Rect(0 , 650, self.back_button_sprite.get_width(), self.back_button_sprite.get_height())
        # Create a selected card holder
        selected_card = None
        exit = None
        while removing:
            removal_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
            removal_surface.fill((0, 0, 0, 0))  # Completely transparent background   
            # Handle events
            events = pygame.event.get() # Get the events
            mouse_pos = pygame.mouse.get_pos() # Get the mouse position
            self.run.potion_events(mouse_pos, events) # Handle the potion events
            self.run.handle_deck_view(events, mouse_pos) # Handle the deck view
            exit = self.run.handle_save_and_exit_input(events) # Handle the save and exit input
            if exit == 'Main Menu': # If the exit is the main menu
                removing = False # Set the removing to False
                break

            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT): # If the F4 key is pressed with the alt key
                    removing = False # Set the removing to False
                    self.run.exit_game() # Exit the game
                    break
                
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    
                    if back_button.collidepoint(mouse_pos): # If the back button is clicked
                        removing = False # Set the removing to False
                        break
                    
                    if confirm_button.collidepoint(mouse_pos):
                        if selected_card:
                            self.run.player.deck.remove(selected_card) # Remove the selected card
                            removing = False # Set the removing to False
                            self.completed = True # Set the completed to True
                            break
                    
                    # Check if card clicked
                    for card in removal_pile.cards: # For each card in the removal pile
                        if card.rect.collidepoint(mouse_pos): # If the card is clicked
                            if card != selected_card: # If the card is not the selected card
                                selected_card = card # Set the selected card to the card
                            else:
                                selected_card = None # Set the selected card to None
                            break
                            
                
                elif event.type == pygame.QUIT: # If the quit event is triggered
                    self.quit_game() # Quit the game

            if not self.completed:
                # Draw cards
                removal_pile.draw(removal_surface, events)

                # Draw back button
                removal_surface.blit(self.back_button_sprite, back_button)

                if selected_card:
                    selected_card.draw_highlight(removal_surface)
                    removal_surface.blit(self.confirm_button_sprite, confirm_button)
                
                # Update display
                # Create a transparent surface for the background
                pygame.display.get_surface().blit(self.campfire_background_sprite, (0, 0))
                pygame.display.get_surface().blit(removal_surface, (0, 0))
                pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()

    def upgrade_card(self, card):
        upgraded_card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
        upgraded_card.bottled = card.bottled
        self.run.player.deck.remove(card)
        self.run.player.deck.append(upgraded_card)

    def is_completed(self):
        return self.completed



