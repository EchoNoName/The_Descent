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
        self.upgradable_cards = []
        self.confirm_button_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
        self.back_button_sprite = pygame.image.load(os.path.join("assets", "ui", "back_button.png"))
        self.skip_button_sprite = pygame.image.load(os.path.join("assets", "ui", "skip_button.png"))
        self.fertilize_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "fertilize.png"))
        self.dig_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "dig.png"))
        self.shred_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "shred.png"))
        self.rest_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "rest.png"))
        self.smith_button_sprite = pygame.image.load(os.path.join("assets", "icons", "campfires", "smith.png"))
        self.campfire_background_sprite = pygame.image.load(os.path.join("assets", "ui", "campfire_background.png"))
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 24)
        self.options = run.campfire
        self.completed = False

    def run_campfire(self):
        campfire = True
        confirm_button = pygame.Rect(1600 - self.confirm_button_sprite.get_width(), 650, self.confirm_button_sprite.get_width(), self.confirm_button_sprite.get_height())
        skip_button = pygame.Rect(1600 - self.skip_button_sprite.get_width(), 650, self.skip_button_sprite.get_width(), self.skip_button_sprite.get_height())
        if self.options['Rest']:
            rest_button = pygame.Rect(400, 250, self.rest_button_sprite.get_width(), self.rest_button_sprite.get_height())
        if self.options['Smith']:
            smith_button = pygame.Rect(900, 250, self.smith_button_sprite.get_width(), self.smith_button_sprite.get_height())
        if self.options['Fertilize']:
            fertilize_button = pygame.Rect(250, 520, self.fertilize_button_sprite.get_width(), self.fertilize_button_sprite.get_height())
        if self.options['Dig']:
            dig_button = pygame.Rect(1050, 520, self.dig_button_sprite.get_width(), self.dig_button_sprite.get_height())
        if self.options['Shred']:
            shred_button = pygame.Rect(650, 520, self.shred_button_sprite.get_width(), self.shred_button_sprite.get_height())
        
        rest_hover = False
        smith_hover = False
        fertilize_hover = False
        dig_hover = False
        shred_hover = False
        exit = None

        while campfire:
            selection_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)

            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.potion_events(mouse_pos, events)
            self.run.handle_deck_view(events, mouse_pos)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                campfire = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    campfire = False
                    self.run.exit_game()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if confirm_button.collidepoint(mouse_pos):
                        campfire = False
                        break
                    elif skip_button.collidepoint(mouse_pos):
                        campfire = False
                        break
                
                    elif self.options['Rest'] and rest_button.collidepoint(mouse_pos):
                        self.rest()
                        break
                    elif self.options['Smith'] and smith_button.collidepoint(mouse_pos):
                        text = self.font.render(f"Upgrade a card.", True, (255, 255, 255))
                        selection_surface.blit(text, (skip_button.centerx - text.get_width()//2, skip_button.top - 30))
                        self.smith()
                        break
                    elif self.options['Fertilize'] and fertilize_button.collidepoint(mouse_pos):
                        self.fertilize()
                        break
                    elif self.options['Dig'] and dig_button.collidepoint(mouse_pos):
                        self.dig()
                        break
                    elif self.options['Shred'] and shred_button.collidepoint(mouse_pos):
                        self.shred()
                        break
            
                if self.options['Rest']:
                    if rest_button.collidepoint(mouse_pos):
                        rest_hover = True
                    else:
                        rest_hover = False

                if self.options['Smith']:
                    if smith_button.collidepoint(mouse_pos):
                        smith_hover = True
                    else:
                        smith_hover = False
                
                if self.options['Fertilize']:
                    if fertilize_button.collidepoint(mouse_pos):
                        fertilize_hover = True
                    else:
                        fertilize_hover = False

                if self.options['Dig']:
                    if dig_button.collidepoint(mouse_pos):
                        dig_hover = True
                    else:
                        dig_hover = False

                if self.options['Shred']:
                    if shred_button.collidepoint(mouse_pos):
                        shred_hover = True
                    else:
                        shred_hover = False

            if self.completed:
                # Draw "Confirm" text above button
                selection_surface.blit(self.confirm_button_sprite, confirm_button)
            else:
                selection_surface.blit(self.skip_button_sprite, skip_button)
                if self.options['Rest']:
                    # Draw "Rest" text above button
                    text = self.font.render("Rest", True, (255, 255, 255))
                    selection_surface.blit(text, (rest_button.centerx - text.get_width()//2, rest_button.top - 30))
                    selection_surface.blit(self.rest_button_sprite, rest_button)

                    if rest_hover:
                        # If hovering over rest button, display what the action does
                        text = self.font.render(f"Heal for 30% of Max HP. ({int(self.run.player.maxHp * 0.3)})", True, (255, 255, 255))
                        selection_surface.blit(text, (800 - text.get_width()//2, 445))

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
        for card in self.run.player.deck:
            if card.id + 100 in card_data.card_info:
                self.upgradable_cards.append(card)

    def rest(self):
        self.run.player.heal(int(self.run.player.maxHp * 0.3))
        self.run.bonusEff('Rest')
        self.completed = True

    def smith(self):
        self.get_upgradable_cards()
        upgrade_pile = combat.Pile(self.upgradable_cards, 'upgrade')
        upgrading = True            
        
        upgrade_pile.scroll_offset = 0

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
                    for card in upgrade_pile.cards:
                        if card.rect.collidepoint(mouse_pos):
                            card.inspecting = True
                            inspecting = True
                            upgraded_card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
                            upgraded_card.inspecting = True
                            while inspecting:
                                inspect_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
                                inspect_surface.fill((0, 0, 0, 0))  # Completely transparent background   
                                
                                events = pygame.event.get()
                                mouse_pos = pygame.mouse.get_pos()
                                self.run.handle_deck_view(events, mouse_pos)
                                self.run.potion_events(mouse_pos, events)
                                exit = self.run.handle_save_and_exit_input(events)
                                if exit == 'Main Menu':
                                    inspecting = False
                                    upgrading = False
                                    break
                                

                                for event in events:
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                                        inspecting = False
                                        upgrading = False
                                        self.run.exit_game()
                                        break
                                        
                                    if event.type == pygame.QUIT:
                                        inspecting = False
                                        upgrading = False
                                        self.run.exit_game()
                                        break

                                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                        if back_button.collidepoint(mouse_pos):
                                            inspecting = False
                                            break
                                        elif confirm_button.collidepoint(mouse_pos):
                                            inspecting = False
                                            upgrading = False
                                            self.upgrade_card(card)
                                            self.completed = True
                                            break
                                    
                                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                                        inspecting = False
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
        self.run.player.increase_max_hp(5)
        self.options['Fertilize'] = False
    
    def dig(self):
        while True:
            relic = relic_data.spawnRelic()
            if relic.name not in [relic.name for relic in self.run.player.relics]:
                break
        self.run.relic_pickup(relic)
        self.completed = True
    
    def shred(self):
        removable_cards = [card for card in self.run.player.deck if card.removable]
        removal_pile = combat.Pile(removable_cards, 'remove')
        removing = True            

        
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
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.potion_events(mouse_pos, events)
            self.run.handle_deck_view(events, mouse_pos)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                removing = False
                break

            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                    removing = False
                    self.run.exit_game()
                    break
                
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    
                    if back_button.collidepoint(mouse_pos):
                        removing = False
                        break
                    
                    if confirm_button.collidepoint(mouse_pos):
                        if selected_card:
                            self.run.player.deck.remove(selected_card)
                            removing = False
                            self.completed = True
                            break
                    
                    # Check if card clicked
                    for card in removal_pile.cards:
                        if card.rect.collidepoint(mouse_pos):
                            if card != selected_card:
                                selected_card = card
                            else:
                                selected_card = None
                            break
                            
                
                elif event.type == pygame.QUIT:
                    self.quit_game()

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



