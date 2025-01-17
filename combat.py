import enemy_data
import card_data
import card_constructor
import effects
import random
import pygame
import os
import sys
import reward_screen

class Combat:
    def __init__(self, player, deck, enemies, combat_type, run, screen):
        self.run = run # The current run
        self.player = player # The Player, can also be accessed through run but this is here for ease of use
        self.enemies = Enemies(enemies) # The Enemies in a combat encounter
        self.deck = deck # The player's deck
        self.combat_type = combat_type # The Type of combat, (Normal, Elite, Boss)
        self.turn = 0 # Turn counter
        self.start_of_combat = True # Whether its the start of combat
        self.draw_pile = Pile(deck, "draw") # Draw pile
        self.cards_played = 0 # num of cards played
        self.hand = Hand([], center_pos=(1600 // 2 - 100, 900 - 200), spread= 130 ) # Cards in hand
        self.selected = [] # Selected cards
        self.discard_pile = Pile([], "discard") # Discard pile
        self.exhaust_pile = Pile([], "exhaust") # Exhaust pile
        self.playing = None # The card being played
        self.energy_cap = 3 # Energy gained at the start of the turn
        self.energy = 0 # Current energy
        self.retain = 0 # num of cards to keep at the end of the turn
        self.can_play_card = True # If the player can play cards
        self.combat_active = True # Whether the player is in this combat
        self.powers = Pile([], "powers") # The powers the player has gained
        self.card_type_played = {} # The type of cards played
        self.enemy_turn = False # Whether the enemy is taking their turn
        self.escaped = False # Whether the player has escaped
        self.necroed = True # Whether the player has necroed
        self.clock = pygame.time.Clock() # The clock
        self.current_phase = 'player_turn_start'
        self.turn_phases = {
            'player_turn_start': self.player_turn_start, # The start of the player's turn
            'player_turn': self.player_turn, # The player's turn
            'player_turn_end': self.player_turn_end, # The end of the player's turn
            'enemy_turn_start': self.enemy_turn_start, # The start of the enemy's turn
            'enemy_actions': self.enemy_action, # The enemy's actions
            'enemy_turn_end': self.enemy_turn_end # The end of the enemy's turn
        }
        self.dragged_card = None # The card being dragged
        self.targetting_potion = None # The targetting potion
        self.clicked_potion = None # The clicked potion
        pygame.init() # Initialize pygame
        self.SCREEN_WIDTH = 1600 # The width of the screen
        self.SCREEN_HEIGHT = 900 # The height of the screen
        self.screen = screen # The screen
        self.combat_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA) # The combat surface
        self.end_turn_button = pygame.image.load("assets/ui/end_turn.png") # The end turn button
        # Scale down end turn button
        self.background_sprite = pygame.image.load(os.path.join("assets", "ui", "forest.png")) # The background sprite
        scaled_size = (int(self.end_turn_button.get_width() * 0.8), int(self.end_turn_button.get_height() * 0.8)) # The scaled size of the end turn button
        self.end_turn_button = pygame.transform.scale(self.end_turn_button, scaled_size) # The scaled end turn button
        self.energy_sprite = pygame.image.load(os.path.join("assets", "ui", "energy.png")) # The energy sprite
        scaled_size = (int(self.energy_sprite.get_width() // 6.5), int(self.energy_sprite.get_height() // 6.5)) # The scaled size of the energy sprite
        self.energy_sprite = pygame.transform.scale(self.energy_sprite, scaled_size) # The scaled energy sprite
        self.energy_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 48) # The font of the energy
        self.action_time_start = 0
        self.error_message = None # The error message
        self.last_time = 0
    
    def run_combat(self):
        """Main combat loop"""
        running = True # Whether the combat is running
        exit = None # Whether the player wants to exit to the main menu
        self.combat_start() # Start the combat
        self.clock = pygame.time.Clock() # The clock
        while running and self.combat_active:
            self.clock.tick(60) # The clock tick
            self.last_time = pygame.time.get_ticks() # The last time
            
            # Clear screen and get mouse position
            self.combat_surface.fill((30, 30, 30)) # Clear the combat surface
            self.combat_surface.blit(self.background_sprite, (0, 0)) # Draw the background sprite
            mouse_pos = pygame.mouse.get_pos() # Get the mouse position

            # Execute current phase
            if self.current_phase:
                phase_result = self.turn_phases[self.current_phase]() # Execute the current phase
                
                # Handle phase transitions
                if phase_result == 'next':
                    self.advance_phase() # Advance to the next phase
                elif phase_result == 'end_combat':
                    break # End the combat
            
            events = pygame.event.get() # Get the events
            # Event handling
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game() # Quit the game
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                    self.quit_game() # Quit the game
                
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.player.deck_button_rect.collidepoint(mouse_pos):
                    self.player.view_deck() # View the deck

                # Only handle card and potion events during player turn
                if self.current_phase == 'player_turn':
                    self.handle_card_events(event, mouse_pos) # Handle card events
                    self.handle_potion_events(event, mouse_pos) # Handle potion events
                    
            # Update and draw game state
            self.run.handle_deck_view(events, mouse_pos) # Handle deck view
            self.run.potion_events(mouse_pos, events) # Handle potion events
            exit = self.run.handle_save_and_exit_input(events) # Handle save and exit input
            if exit == 'Main Menu':
                running = False
                break
            self.handle_enemy_events(mouse_pos) # Handle enemy events
            self.handle_pile_events(events, mouse_pos) # Handle pile events
            self.handle_character_events(mouse_pos) # Handle character events
            self.update_game_state(mouse_pos) # Update the game state
            self.draw_game_state(mouse_pos) # Draw the game state
            if self.error_message:
                self.draw_error_message()
            self.screen.blit(self.combat_surface, (0, 0)) # Draw the combat surface
            pygame.display.flip() # Update the display

        if exit == 'Main Menu':
            self.run.main_menu.main_menu() # Return to the main menu
        else:
            pygame.time.wait(1000)
            return self.combat_result(), self.combat_surface # Return the combat result and the combat surface

    def draw_error_message(self):
        """Draw the error message"""
        if pygame.time.get_ticks() - self.error_message['start_time'] < self.error_message['duration']:
            # Create semi-transparent black background surface
            background = pygame.Surface((self.error_message['text'].get_width(), self.error_message['text'].get_height()))
            background.fill((0, 0, 0))
            background.set_alpha(128)  # 50% opacity
            
            # Draw background then text
            self.combat_surface.blit(background, self.error_message['rect'])
            self.combat_surface.blit(self.error_message['text'], self.error_message['rect'])
        else:
            self.error_message = None # Clear the error message

    def combat_result(self):
        """Determine the result of the combat"""
        if self.player.hp <= 0:
            return 'defeat' # Defeat
        elif self.enemies.is_empty():
            return 'victory' # Victory
        else:
            return 'escape' # Escape

    def advance_phase(self):
        """Advance to the next combat phase"""
        phase_order = [ # The order of the phases
            'player_turn_start',
            'player_turn',
            'player_turn_end',
            'enemy_turn_start',
            'enemy_actions',
            'enemy_turn_end'
        ]
        current_index = phase_order.index(self.current_phase) # Get the current phase index
        next_index = (current_index + 1) % len(phase_order) # Get the next phase index
        self.current_phase = phase_order[next_index] # Set the current phase to the next phase

    def handle_enemy_events(self, mouse_pos):
        """Handle enemy-related events"""
        if not self.targetting_potion and not self.dragged_card: # If the player is not targeting a potion and not dragging a card
            for enemy in self.enemies.enemy_list:
                if enemy is not None:
                    if enemy.rect.collidepoint(mouse_pos):
                        enemy.hover() # Hover the enemy
                    else:
                        enemy.unhover() # Unhover the enemy

    def handle_pile_events(self, events, mouse_pos):
        """Handle pile-related events"""
        # Handle hovering
        if self.draw_pile.rect.collidepoint(mouse_pos):
            self.draw_pile.hover()
        else:
            self.draw_pile.unhover()
            
        if self.discard_pile.rect.collidepoint(mouse_pos):
            self.discard_pile.hover() # Hover the discard pile
        else:
            self.discard_pile.unhover() # Unhover the discard pile
            
        if self.exhaust_pile.rect.collidepoint(mouse_pos):
            self.exhaust_pile.hover() # Hover the exhaust pile
        else:
            self.exhaust_pile.unhover() # Unhover the exhaust pile
            
        if self.powers.rect.collidepoint(mouse_pos):
            self.powers.hover() # Hover the powers pile
        else:
            self.powers.unhover() # Unhover the powers pile
            
        # Handle clicking
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.draw_pile.rect.collidepoint(mouse_pos):
                    self.view_pile(self.draw_pile) # View the draw pile
                elif self.discard_pile.rect.collidepoint(mouse_pos):
                    self.view_pile(self.discard_pile) # View the discard pile
                elif self.exhaust_pile.rect.collidepoint(mouse_pos):
                    self.view_pile(self.exhaust_pile) # View the exhaust pile   
                elif self.powers.rect.collidepoint(mouse_pos):
                    self.view_pile(self.powers) # View the powers pile


    def handle_character_events(self, mouse_pos):
        """Handle character-related events"""
        if self.player.rect.collidepoint(mouse_pos):
            self.player.hover() # Hover the player
        else:
            self.player.unhover() # Unhover the player

    def handle_card_events(self, event, mouse_pos):
        """Handle card-related events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in reversed(self.hand.cards):
                if card.rect.collidepoint(mouse_pos):
                    if card.target == 1:
                        card.start_targeting(mouse_pos) # Start targeting the card
                        self.dragged_card = card
                    else:
                        card.start_dragging(mouse_pos) # Start dragging the card
                        self.dragged_card = card
                    break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragged_card:
                cost = self.dragged_card.get_cost(self) # Get the cost of the card
                
                def show_error_message(message):
                    """Helper function to show temporary error message that fades after 2 seconds"""
                    font = pygame.font.Font("assets/fonts/Kreon-Bold.ttf", 24)
                    text = font.render(message, True, (255, 0, 0))
                    text_rect = text.get_rect(center=(self.player.rect.right + 150, self.player.rect.centery))
                    # Store message text, position, start time, and duration in seconds
                    self.error_message = {
                        'text': text,
                        'rect': text_rect, 
                        'start_time': pygame.time.get_ticks(),
                        'duration': 2000 # 2 seconds in milliseconds
                    }

                if self.player.debuffs['Entangle'] > 0 and self.dragged_card.type == 0:
                    show_error_message("Can't play Attack cards while Entangled") # Show the error message
                elif self.dragged_card.cost == 'U' and mouse_pos[1] <= 550: # If the card is a curse and the mouse is in the player's area
                    if (self.run.mechanics['Playable_Curse'] == True and self.dragged_card.type == 4) or (self.run.mechanics['Playable_Status'] == True and self.dragged_card.type == 3):
                        if self.can_play_card and self.energy >= cost:
                            self.playing = self.dragged_card # Set the playing card
                            self.hand.remove_card(self.dragged_card) # Remove the card from the hand
                            self.play_card(self.player_targeting(0, self.dragged_card.target)) # Play the card
                            self.energy -= cost # Subtract the cost from the energy
                        elif self.energy < cost:
                            show_error_message("Not enough energy") # Show the error message
                        else:
                            show_error_message("Can't play more cards this turn") # Show the error message
                    else:
                        show_error_message("Can't play this card") # Show the error message
                elif self.dragged_card.target == 1:
                    for enemy in self.enemies.enemy_list:
                        if enemy and enemy.rect.collidepoint(mouse_pos):
                            if self.can_play_card and self.energy >= cost:
                                self.playing = self.dragged_card # Set the playing card
                                self.hand.remove_card(self.dragged_card) # Remove the card from the hand
                                self.play_card([enemy]) # Play the card
                                self.energy -= cost # Subtract the cost from the energy
                            elif self.energy < cost:
                                show_error_message("Not enough energy")
                            else:
                                show_error_message("Can't play more cards this turn") # Show the error message
                else:
                    if mouse_pos[1] <= 550:
                        if self.can_play_card and self.energy >= cost:
                            self.playing = self.dragged_card # Set the playing card
                            self.hand.remove_card(self.dragged_card) # Remove the card from the hand
                            self.play_card(self.player_targeting(0, self.dragged_card.target)) # Play the card
                            self.energy -= cost # Subtract the cost from the energy
                        elif self.energy < cost:
                            show_error_message("Not enough energy")
                        else:
                            show_error_message("Can't play more cards this turn") # Show the error message
                self.dragged_card.stop_targeting() # Card stops targeting
                self.dragged_card.stop_dragging() # Stop dragging the card
                self.dragged_card = None # Clear the dragged card

    def handle_potion_events(self, event, mouse_pos):
        """Handle potion-related events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # If the right mouse button is clicked
            if self.targetting_potion:
                self.targetting_potion.stop_targeting() # Potion stops targeting
                self.targetting_potion = None # Clear the targetting potion
            if self.clicked_potion:
                self.clicked_potion.unclick() # Unclick the potion
                self.clicked_potion = None # Clear the clicked potion

        elif self.clicked_potion and not self.targetting_potion:
            self.clicked_potion.unhover() # Unhover the potion
            box_width = 100
            box_height = 40
            box_x = self.clicked_potion.rect.x + (self.clicked_potion.sprite.get_width() - box_width) // 2
            box_y = self.clicked_potion.rect.y + self.clicked_potion.sprite.get_height() + 10
            use_rect = pygame.Rect(box_x, box_y, box_width, box_height) # Create a rect for the use button
            discard_rect = pygame.Rect(box_x, box_y + 45, 100, 40) # Create a rect for the discard button
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if use_rect.collidepoint(mouse_pos):
                    if self.clicked_potion.time_of_use in ['combat']:
                        if self.clicked_potion.target == 1:
                            self.clicked_potion.start_targeting() # Start targeting the potion
                            self.clicked_potion.unclick() # Unclick the potion
                            self.targetting_potion = self.clicked_potion # Set the targetting potion
                            self.dragged_card = None  # Clear any dragged card
                        else:
                            self.use_potion(self.clicked_potion) # Use the potion
                            self.clicked_potion.unclick() # Unclick the potion
                            self.clicked_potion = None # Clear the clicked potion
                    else:
                        self.clicked_potion.unclick() # Unclick the potion
                        self.clicked_potion = None
                elif discard_rect.collidepoint(mouse_pos):
                    self.run.discard_potion(self.clicked_potion) # Discard the potion
                    self.clicked_potion.unclick() # Unclick the potion
                    self.clicked_potion = None # Clear the clicked potion
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                self.clicked_potion.unclick() # Unclick the potion
                self.clicked_potion = None # Clear the clicked potion

        elif self.targetting_potion:
            self.targetting_potion.unhover() # Unhover the potion
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for enemy in self.enemies.enemy_list:
                    if enemy and enemy.rect.collidepoint(mouse_pos):
                        self.use_potion(self.targetting_potion, [enemy]) # Use the potion
                        self.targetting_potion = None # Clear the targetting potion
                        self.clicked_potion = None # Clear the clicked potion
                        break

        else:
            for potion in self.player.potions:
                if potion:
                    if potion.rect.collidepoint(mouse_pos):
                        potion.hover()
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            potion.click() # Click the potion
                            self.clicked_potion = potion # Set the clicked potion
                            potion.unhover() # Unhover the potion
                    else:
                        potion.unhover() # Unhover the potion
        
    def update_game_state(self, mouse_pos):
        """Update all game objects"""
        for card in self.hand.cards:
            card.update() # Update the card
            card.check_hover(mouse_pos) # Check if the card is being hovered
        
        self.hand.update_positions(self.dragged_card) # Update the positions of the cards in the hand

    def view_pile(self, pile):
        '''View a pile'''
        if pile.is_empty():
            # If the pile to select from is empty
            return None
        else:
            # Create a new surface for viewing the cards
            viewing_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
            viewing_surface.fill((0, 0, 0, 0))  # Completely transparent background
            
            # Create a Pile object to handle drawing the cards in a grid
            pile.scroll_offset = 0  # Initialize scroll position
            
            # Create a confirm button in bottom right
            confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
            confirm_button = pygame.Rect(1600 - confirm_sprite.get_width(), 520, confirm_sprite.get_width(), confirm_sprite.get_height())
            
            viewing = True
            while viewing:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Check if confirm button clicked
                        if confirm_button.collidepoint(mouse_pos):
                            viewing = False
                            break
                    
                    elif event.type == pygame.QUIT:
                        self.quit_game()
                
                # Draw cards
                pile.draw(viewing_surface, pygame.event.get())
                
                # Draw confirm button
                viewing_surface.blit(confirm_sprite, confirm_button)
                
                # Update display
                # Create a transparent surface for the background
                background = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
                background.fill((50, 50, 50))  # Semi-transparent dark gray
                background.set_alpha(200)
                pygame.display.get_surface().blit(background, (0, 0))
                pygame.display.get_surface().blit(viewing_surface, (0, 0))
                pygame.display.flip()

    def draw_game_state(self, mouse_pos):
        """Draw all game objects"""
        
        player_x, player_y = 300, self.SCREEN_HEIGHT//2.9

        # Draw power cards in a row above player, scaled down
        spacing = 50  # Space between cards
        start_x = player_x - (len(self.powers.cards) * spacing) / 2  # Center the row above player
        for i, card in enumerate(self.powers.cards):
            card.draw_as_power(self.combat_surface, x=start_x + (i * spacing), y=player_y - 100)


        # Draw enemies
        self.enemies.draw(self.combat_surface, self.run.mechanics['Intent'])
        
        # Draw energy
        self.draw_energy(self.combat_surface)

        # Only draw targeting effects if card is being dragged
        if self.dragged_card:
            self.dragged_card.draw_targeting_arrow(self.combat_surface, mouse_pos) # Draw the targeting arrow
            if self.dragged_card.target in [1, 2, 3]:
                for enemy in self.enemies.enemy_list:
                    if enemy:
                        enemy.draw_collision_box(self.combat_surface) # Draw the collision box for the enemy
            else:
                self.player.rect.x = player_x
                self.player.rect.y = player_y
                self.player.draw_collision_box(self.combat_surface) # Draw the collision box for the player

        # Draw hand
        self.hand.draw(self.combat_surface, self.dragged_card) # Draw the hand
        
        # Draw potion targeting effects
        if self.targetting_potion:
            self.targetting_potion.start_targeting() # Potions can target enemies
            self.targetting_potion.draw_targeting_arrow(self.combat_surface, mouse_pos) # Draw the targeting arrow
            for enemy in self.enemies.enemy_list:
                if enemy:
                    enemy.draw_collision_box(self.combat_surface) # Draw the collision box for the enemy
        
        self.draw_pile.draw_icon(self.combat_surface) # Draw the draw pile
        self.discard_pile.draw_icon(self.combat_surface) # Draw the discard pile
        self.exhaust_pile.draw_icon(self.combat_surface) # Draw the exhaust pile
        self.powers.draw_icon(self.combat_surface) # Draw the powers
        # Draw player
        
        self.player.draw(self.combat_surface, x=player_x, y=player_y)
        self.player.draw_ui(self.combat_surface)

    def draw_energy(self, surface):
        """Draw energy counter in bottom left"""
        # Load and scale energy orb sprite
        scaled_width = int(self.energy_sprite.get_width() * 0.75)
        scaled_height = int(self.energy_sprite.get_height() * 0.75)
        
        # Position in bottom left with some padding
        x = 100
        y = self.SCREEN_HEIGHT - scaled_height - 250
        
        # Draw energy orb
        surface.blit(self.energy_sprite, (x, y))

        # Draw energy text
        energy_text = f"{self.energy}/{self.energy_cap}"
        # Draw black outline by rendering text in black and offsetting slightly
        outline_color = (0, 0, 0)
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
            outline = self.energy_font.render(energy_text, True, outline_color)
            text_x = x + (scaled_width - outline.get_width()) // 2 + 20 + dx
            text_y = y + (scaled_height - outline.get_height()) // 2 + 15 + dy
            surface.blit(outline, (text_x, text_y))
        
        # Draw main white text on top
        text = self.energy_font.render(energy_text, True, (255, 255, 255))
        text_x = x + (scaled_width - text.get_width()) // 2 + 20
        text_y = y + (scaled_height - text.get_height()) // 2 + 18
        surface.blit(text, (text_x, text_y))
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
                
        # Create rect for collision detection
        energy_rect = pygame.Rect(x, y, scaled_width, scaled_height)
        
        # Check if mouse is hovering over energy orb
        if energy_rect.collidepoint(mouse_pos):
            # Create tooltip text
            tooltip_text = "Energy"
            tooltip_surface = self.energy_font.render(tooltip_text, True, (255, 255, 255))
            
            # Create background box
            padding = 10
            box_width = tooltip_surface.get_width() + padding * 2
            box_height = tooltip_surface.get_height() + padding * 2
            box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            box.fill((0, 0, 0))
            box.set_alpha(100)
            
            # Position tooltip to right of energy orb
            box_x = x + scaled_width + 10
            box_y = y + (scaled_height - box_height) // 2
            
            # Draw tooltip
            surface.blit(box, (box_x, box_y))
            surface.blit(tooltip_surface, (box_x + padding, box_y + padding))

    def combat_start(self):
        '''Method for starting combat'''
        self.get_energy_cap() # Get the energy cap
        for buff in self.player.buffs.keys():
            self.player.buffs[buff] = 0 # Reset buffs
        for debuff in self.player.debuffs.keys():
            self.player.debuffs[debuff] = 0 # Reset debuffs
        if self.combat_type == 'Elite':
            if self.player.relics:
                for relic in self.player.relics:
                    relic.combatActionEff('Elite Start', self) # Execute relic effects
        if self.run.mechanics['Insect'] == True and self.combat_type == 'Elite':
            for enemy in self.enemies.enemy_list:
                if enemy != None:
                    enemy.hp = int(enemy.hp * 0.75) # Reduce enemy hp by 75%
        # check for preserved insect condition
        innate_or_bottled = []
        for card in reversed(self.draw_pile):
            if card.innate == True or card.bottled == True:
                innate_or_bottled.append(card)
                self.draw_pile.remove_card(card)
        self.draw_pile.shuffle()
        random.shuffle(innate_or_bottled)
        for card in innate_or_bottled:
            self.draw_pile.add_top(card)
        innate_or_bottled = []
        # put all innate and bottled cards at the top of the draw pile

    def counter_reset(self):
        '''Method for resetting turn counters'''
        if self.player.relics:
            for relic in self.player.relics:
                if relic.counter != None:
                    if relic.counter_type != 'global':
                        relic.counter = 0 # Reset turn counters

    def bonusEff(self, event):
        if self.player.relics:
            for relic in self.player.relics:
                # Go through all relics
                relic.eventBonus(event, self.run) # Execute relic effects

    def passive_check_and_exe(self, cond: str):
        '''Method to check if a power's condition or relic's condition is met and activates its effect if it is

        ### args:
            cond (string): The event that is occuring
        '''
        if not self.powers.is_empty(): # If there are powers played
            for card in self.powers.cards: # For all powers
                context = {
                    # Basic info to be passed on for executing effects
                    'user': self.player,
                    'enemies': self.enemies,
                    'draw': self.draw_pile,
                    'discard': self.discard_pile,
                    'hand': self.hand,
                    'exhaust': self.exhaust_pile,
                    'target': card.target
                }
                context['target'] = self.player_targeting(context, card.target) # Get the target of the card
                if 'Power' in card.effect and card.effect['Power'] != None:
                    # The power effect in a card
                    for power_cond, effect in card.effect['Power'].items():
                        # for every condition and effect
                        if cond == power_cond: # If the condition is met
                            for effects, effect_details in effect.items():
                                effects(*effect_details, context, self) # Execute the power's effect
        if self.player.relics:
            for relic in self.player.relics:
                # Go through all relics
                relic.combatActionEff(cond, self)
                # Execute condisional effects of relics

    def get_energy_cap(self):
        '''Gets the energy cap of the player
        '''
        for relic in self.player.relics:
            # Goes throught every relic
            if relic.energy_relic == True:
                # If its an energy relic
                if relic.energy_relic != 'Elite':
                    self.energy_cap += 1
                else:
                    if self.combat_type == 'Elite':
                        self.energy_cap += 1
                # Add 1 energy to the cap if its a normal energy relic and add 1 for slavers collar in elites

    def curse_count(self):
        '''Counts the number of curses in play'''
        curse = 0
        if self.draw_pile:
            curse += self.draw_pile.curse_count()
        if self.discard_pile:
            curse += self.discard_pile.curse_count()
        if self.hand:
            curse += self.hand.curse_count()
        if self.exhaust_pile:
            curse += self.exhaust_pile.curse_count()
        return curse
        # counts the number of curses in play
    
    def enemy_targeting(self, context, target_code):
        '''Retrieves the target of a enemies based on the target code

        ### args:
            target_code (int): An int corresponding to a specific target or targets
        '''
        if target_code == None:
            return None
        if target_code == 0:
            # If its 0
            return [context['user']]
            # Returns the player
        elif target_code == 1:
            # If its 1
            return [self.player]
            # returns that player
        elif target_code == 2:
            # if its 2
            return [self.enemies.random_enemy()]
            # Returns a random enemy
        elif target_code == 3:
            # if its 3
            enemies = []
            for enemy in self.enemies.enemy_list:
                if enemy != None:
                    enemies.append(enemy)
            return enemies
            # Returns all the enemies
        else:
            raise ValueError(f"Unknown target code: {target_code}")
            # Errors

    def player_targeting(self, context, target_code):
        '''Retrieves the target of a card based on the cards target code

        ### args:
            target_code (int): An int corresponding to a specific target or targets
        '''
        if target_code == None:
            return None
        if target_code == 0:
            # If its 0
            return [self.player]
            # Returns the player
        elif target_code == 1:
            raise ValueError('Should not have accessed this method')
        elif target_code == 2:
            # if its 2
            return [self.enemies.random_enemy()]
            # Returns a random enemy
        elif target_code == 3:
            # if its 3
            return self.enemies
            # Returns all the enemies
        else:
            raise ValueError(f"Unknown target code: {target_code}")
            # Errors

    def add_card_to_pile(self, location, card_id, location_name, cost):
        '''adds a certain card to a certain pile

        ### args: 
            loctaion (int): represents which pile to add the card, 0 = hand, 1 = draw pile, 2 = discard pile. 3 = exhaust pile
            card (object): An object that represents the card
        '''
        card = card_constructor.create_card(card_id, card_data.card_info[card_id])
        # Creates a card object using methods in card_constructor and data in card_data
        if cost != 'na':
            # If a cost change is needed
            card.cost_change(*cost)
            # Modifies the cards cost
        if location.type == 'hand':
            if self.hand.cards_in_hand() == 10:
                self.discard_pile.add_card(card)
            else:
                location.add_card(card)
        elif location.type == 'draw':
            location.insert_card(card)
        else:
            location.add_card(card)
            

    def shuffle(self):
        '''
        Method for shuffling the discard pile into the draw pile and shuffling the order of the draw pile
        '''
        if not self.draw_pile.is_empty():
            # If the draw pile is not empty
            if not self.discard_pile.is_empty():
                # If the discard pile is not empty
                for card in self.discard_pile.cards:
                    self.draw_pile.add_card(card)
                # Add the discard pile to the draw pile
            self.draw_pile.shuffle()
            # Shuffle the draw pile
            self.discard_pile.empty()
            # Empty the discard pile
        else:
            if not self.discard_pile.is_empty():
                # If the discard pile is not empty
                for card in self.discard_pile.cards:
                    self.draw_pile.add_card(card)
                # Make the draw pile the discard pile
                self.draw_pile.shuffle()
                # Shuffle the draw pile
                self.discard_pile.empty()
                # Empty the discard pile
        self.passive_check_and_exe('Shuffle')
            # Active the relic effects with the event being shuffling

    def draw(self, num: int):
        '''Method for drawing cards during combat
        
        ### args:
            num (int): The number of cards that needs to be drawn
        '''
        while num > 0: # While drawing still needs to be done
            if self.hand.cards_in_hand() == 10:
                # If the hand is full 
                num -= 1
                # One less card to draw
                continue
                # To the next iteration
            elif self.draw_pile.is_empty():
                # If the draw pile is empty
                self.shuffle()
                # shuffle the draw pile
                if self.draw_pile.is_empty():
                    # If the draw pile is still empty
                    num -= 1
                    # One less card to draw
                    continue
                    # To the next iteration
            else:
                drawn_card = self.draw_pile.remove_top()
                # "draw" a card from top of draw pile
                if self.player.debuffs['Chaotic'] > 0:
                    drawn_card.chaos()
                # If the player is chaotic, randomize the cost of drawn cards
                if drawn_card.effect:
                    if 'Drawn' in drawn_card.effect:
                        # If the card has a when drawn effect
                        for effect, details in drawn_card.effect['Drawn'].items():
                            context = {
                                # Basic info to be passed on for executing effects
                                'user': self.player,
                                'enemies': self.enemies,
                                'draw': self.draw_pile,
                                'discard': self.discard_pile,
                                'hand': self.hand,
                                'exhaust': self.exhaust_pile,
                                'target': drawn_card.target
                            }
                            effect(*details, context, self)
                            # Execute the drawn effect
                self.hand.add_card(drawn_card)
                # Add card to hand
                if drawn_card.type in {3, 4}:
                    # If the card drawn is a negative card
                    self.passive_check_and_exe('Draw Negative')
                    # Check for effects
                    if drawn_card.type == 3:
                        self.passive_check_and_exe('Draw Status')
                    elif drawn_card.type == 4:
                        self.passive_check_and_exe('Draw Curse')
                    # If they drew a status or a curse and check for effects
                num -= 1
                # One less card to draw
    
    def quit_game(self):
        '''Method for quitting the game'''
        pygame.quit()
        sys.exit()

    def view_pile(self, pile):
        '''Method for viewing a pile of cards

        ### args:
            pile (list): The pile of cards to view
        '''                
        card_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
        card_surface.fill((0, 0, 0, 0))  # Completely transparent background
        confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
        confirm_button = pygame.Rect(1600 - confirm_sprite.get_width(), 520, confirm_sprite.get_width(), confirm_sprite.get_height())
        viewing = True

        # If it's the draw pile and ordered_draw is False, randomize display order
        if pile.type == 'draw' and not self.run.mechanics['Ordered_Draw_Pile']:
            display_pile = Pile(random.sample(pile.cards, len(pile.cards)), pile.type) # Randomize the display order of the cards
        else:
            display_pile = pile # If ordered draw is true, display the cards in order

        while viewing:
            card_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
            card_surface.fill((0, 0, 0, 0))  # Completely transparent background
            events = pygame.event.get() 
            for event in events: # Handle events
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                    self.quit_game() # Quit the game
                
                if event.type == pygame.QUIT:
                    self.quit_game() # Quit the game

                if event.type == pygame.MOUSEBUTTONDOWN: # If a mouse button is clicked
                    mouse_pos = pygame.mouse.get_pos() # Get the mouse position
                    if confirm_button.collidepoint(mouse_pos): # If the confirm button is clicked
                        viewing = False # Stop viewing the pile
                        break
            
            display_pile.draw(card_surface, events)
            card_surface.blit(confirm_sprite, confirm_button)
            background = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
            background.fill((50, 50, 50))  # Semi-transparent dark gray
            pygame.display.get_surface().blit(background, (0, 0))
            pygame.display.get_surface().blit(card_surface, (0, 0))
            pygame.display.flip()

    def soft_card_select(self, num : int, pile : list): # Needs to be changed to match hard card select
        '''A soft card select refers to when the game needs the player to select up to x amount of cards but can choose to select below x amount of cards or none at all
        
        ### args:
            num (int): Number of cards that needs to be selected
            pile (list): The place the player needs to select from

        ### Returns:
            Number of cards selected (If more than 1) or the type of card selected (If 1 card was selected) or None (No cards were selected)
            '''
        if not pile:
            # If the pile to select from is empty
            return None
        else:
            # Create a new surface for the card selection screen
            selection_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
            selection_surface.fill((0, 0, 0, 0))  # Completely transparent background
            
            # Create a Pile object to handle drawing the cards in a grid
            selection_pile = Pile(pile.cards, "selection")
            selection_pile.scroll_offset = 0  # Initialize scroll position
            
            # Create a confirm button in bottom right
            confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
            confirm_button = pygame.Rect(1600 - confirm_sprite.get_width(), 520, confirm_sprite.get_width(), confirm_sprite.get_height())
            
            selecting = True
            while selecting:
                selection_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
                selection_surface.fill((0, 0, 0, 0))  # Completely transparent background
                events = pygame.event.get()
                # Handle events
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                        self.quit_game()
                
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Check if confirm button clicked
                        if confirm_button.collidepoint(mouse_pos):
                            selecting = False
                            break
                            
                        # Check if card clicked
                        for card in pile:
                            if card.rect.collidepoint(mouse_pos):
                                if card in self.selected:
                                    # Unselect card if already selected
                                    self.selected.remove(card)
                                elif len(self.selected) < num:
                                    # Select card if under max selections
                                    self.selected.append(card)
                                break

                    elif event.type == pygame.QUIT:
                        self.quit_game()
                
                # Draw cards
                selection_pile.draw(selection_surface, events)
                
                # Draw highlights around selected cards
                for card in self.selected:
                    card.draw_highlight(selection_surface)
                    
                # Draw confirm button
                selection_surface.blit(confirm_sprite, confirm_button)
                
                # Update display
                # Create a transparent surface for the background
                background = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
                background.fill((50, 50, 50))  # Semi-transparent dark gray
                pygame.display.get_surface().blit(background, (0, 0))
                pygame.display.get_surface().blit(selection_surface, (0, 0))
                pygame.display.flip()
            
            # Return results
            if len(self.selected) == 1:
                if pile == self.draw_pile:
                    random.shuffle(self.draw_pile)
                pile.remove_card(self.selected[0])
                return self.selected[0].type
            else:
                if pile == self.draw_pile:
                    random.shuffle(self.draw_pile)
                for card in self.selected:
                    pile.remove_card(card)
                return len(self.selected)

    def hard_card_select(self, num, pile):
        '''A hard card select refers to when the game needs the player to select x amount of cards and they must choose the maximum amount of cards to select
        
        ### args:
            num (int): Number of cards that needs to be selected
            pile (list): The place the player needs to select from

        ### Returns:
            Number of cards selected (If more than 1) or the type of card selected (If 1 card was selected) or None (No cards were selected)
        '''
        if pile.is_empty():
            return None
            
        if len(pile.cards) <= num:
            self.selected.extend(pile.cards)
            pile.empty()
            if num == 1:
                return self.selected[0].type
            else:
                return len(self.selected)
                
        # Create selection surface and pile
        selection_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
        selection_surface.fill((0, 0, 0, 0))  # Completely transparent background
        
        # Create a Pile object to handle drawing the cards in a grid
        selection_pile = Pile(pile.cards, "selection")
        selection_pile.scroll_offset = 0  # Initialize scroll position
        
        # Create a confirm button in bottom right
        confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
        confirm_button = pygame.Rect(1600 - confirm_sprite.get_width(), 520, confirm_sprite.get_width(), confirm_sprite.get_height())
        
        selecting = True
        while selecting:
            selection_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
            selection_surface.fill((0, 0, 0, 0))  # Completely transparent background   
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                    selecting = False
                    break
                
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if confirm button clicked
                    if confirm_button.collidepoint(mouse_pos):
                        if len(self.selected) == num:
                            selecting = False
                            break
                            
                    # Check if card clicked
                    for card in pile:
                        if card.rect.collidepoint(mouse_pos):
                            if card in self.selected:
                                # Unselect card if already selected
                                self.selected.remove(card)
                            elif len(self.selected) < num:
                                # Select card if under max selections
                                self.selected.append(card)
                            break
                
                elif event.type == pygame.QUIT:
                    self.quit_game()
            
            # Draw cards
            selection_pile.draw(selection_surface, events)
            
            # Draw highlights around selected cards
            for card in self.selected:
                card.draw_highlight(selection_surface)
                
            # Draw confirm button
            confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
            selection_surface.blit(confirm_sprite, confirm_button)
            
            # Update display
            # Create a transparent surface for the background
            background = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
            background.fill((50, 50, 50))  # Semi-transparent dark gray
            pygame.display.get_surface().blit(background, (0, 0))
            pygame.display.get_surface().blit(selection_surface, (0, 0))
            pygame.display.flip()
        
        # Return results
        if len(self.selected) == 1:
            if pile == self.draw_pile:
                random.shuffle(self.draw_pile)
            pile.remove_card(self.selected[0])
            return self.selected[0].type
        else:
            if pile == self.draw_pile:
                random.shuffle(self.draw_pile)
            for card in self.selected:
                pile.remove_card(card)
            return len(self.selected)

    def place_selected_cards(self, end_pile, cost):
        '''Method for placing a selected card into a specific pile

        ### args: 
            end_pile: The location the selected cards end up
            cost: Any cost modifcations to the cards, na for no modifications
        '''
        if self.selected:
            # If there are cards selected
            for card in self.selected:
                if cost != 'na':
                    # If there is a cost change needed
                    card.cost_change(*cost)
                    # Change the cost for everycard in selected
                if end_pile.type == 'hand':
                    if self.hand.cards_in_hand() == 10:
                        self.discard_pile.add_card(card)
                    else:
                        self.hand.add_card(card)
                else:
                    end_pile.add_card(card)
                # Adds all selected cards to the top of the end pile
            self.selected[:] = []
            # Empty selected cards
    
    def search(self, num, type = 'all'):
        ''' Add a card from the draw pile to the hand (Searching)

        ### args: 
            num: Number of cards you can add from the draw pile to the hand
            type: The type of cards that you can search, all by default
        '''
        if not self.draw_pile:
            # If there are no cards in the draw pile
            return None
            # Returns nothing
        eligible_cards = []
        # Initialize eligible_cards
        if type == 'all':
            # If all cards can be searched
            eligible_cards.extend(self.draw_pile)
            # Make eligible_cards the entire draw pile
        elif type in {'common', 'uncommon', 'rare'}:
            # If searching based on rarity
            rarity = {
                'common': 1,
                'uncommon': 2,
                'rare': 3
            }
            for card in reversed(self.draw_pile):
                # Go through every card in the draw pile
                if card.rarity == rarity[type]:
                    # If the rarity matches the search type
                    eligible_cards.append(card)
                    # Add it to eligible cards
            if eligible_cards:
                # If there are eligible cards
                eligible_cards = Pile(eligible_cards, 'selection')
                self.hard_card_select(num, eligible_cards)
                # Select from the cards
                for card in reversed(self.selected):
                    # Loop through every card in selected
                    if len(self.hand) < 10:
                        # While the hand is below the hand size limit
                        self.hand.add_card(card)
                        # Add the selected card to hand
                        self.selected.remove(card)
                        # Remove it from selected
                        self.draw_pile.remove_card(card)
                        # Remove the cards from the draw pile
                    else:
                        self.discard_pile.add_cards(self.selected)
                        # Add remaining cards to the discard pile
                        self.selected.remove(card)
                        # Remove it from selected
                        self.draw_pile.remove_card(card)
                        # Remove the cards from the draw pile
                        break
                        # Exit the loop
                self.draw_pile.shuffle()
                # Shuffle the draw pile

        elif type in {'atk', 'skill', 'power'}:
            return None
        # Placeholder
        
    def exhaust_discard_curse(self, num):
        '''Discard X amounts of cards from hand and exhaust all discarded curses
        
        ### args: 
            num: Number of cards that needs to be discarded
        '''
        self.hard_card_select(num, self.hand)
        # Select cards from hand
        if self.selected:
            # If there were cards selected
            for card in reversed(self.selected):
                # Loop through cards selected
                if card.type == 4:
                    # If the card is a curse
                    self.exhaust_pile.add_card(card)
                    # add the card to the exhaust pile
                    self.if_card_cond(card, 'Exhausted')
                    # Executes exhausted effects
                    self.selected.remove(card)
                    # Remove the card from selected
                    self.passive_check_and_exe('Exhaust')
                else:
                    self.discard_pile.add_card(card)
                    # Add the card to the discard pile
                    self.if_card_cond(card, 'Discarded')
                    # Executes Discarded effects
                    self.selected.remove(card)
                    # Discards the card instead

    def random_discard(self, num: int):
        '''Randomly discards cards from the hand
        
        ### args:
            num: The Number of cards to randomly discard'''
        if not self.hand.is_empty():
            # If there are cards in hand
            if len(self.hand.cards) > num:
                # There are more cards in hand than the amount needed to be discarded
                for i in range(0, num):
                    # Iterate num amount of times
                    card = random.choice(self.hand.cards)
                    # Choose a random card
                    if card.effect:
                        self.if_card_cond(card, 'Discarded')
                        # Execute the discarded effect
                    self.discard_pile.add_card(card)
                    # Add the card to the discard pile
                    self.hand.remove_card(card)
                    # Remove the card from hand
            else:
                for card in reversed(self.hand.cards):
                    # Go through every card
                    if card.effect:
                        self.if_card_cond(card, 'Discarded')
                        # Execute the discarded effect
                    self.discard_pile.add_card(card)
                    # Add the card to the discard pile
                    self.hand.remove_card(card)
                    # Remove the card from hand

    def choose_discard(self, num: int):
        '''Selected a number of cards to discard from the hand
        
        ### args:
            num: The number of cards that needs to be discarded
        '''
        self.hard_card_select(num, self.hand)
        # Selected a certain amount of cards from the hand
        if self.selected:
            # If there were cards selected
            for card in reversed(self.selected):
                # Go through every selected card
                if card.effect:
                    self.if_card_cond(card, 'Discarded')
                    # Executes all if Discarded effects
                self.discard_pile.add_card(card)
                # Add the card to the discard pile
                self.hand.remove_card(card)
                # Remove card from hand
                self.selected.remove(card)
                # remove the card from selected

    def exhaust_random_hand(self, num: int):
        '''Exhausts a number of random cards from the hand
        
        ### args:
            num: The number of cards that needs to be exhausted'''
        if not self.hand.is_empty():
            # If there are cards in hand
            if len(self.hand.cards) > num:
                # There are more cards in hand than the amount needed to be Exhausted
                for i in range(0, num):
                    # Iterate num amount of times
                    card = random.choice(self.hand.cards)
                    # Choose a random card
                    if card.effect:
                        # If that card has a effect when exhausted
                        self.if_card_cond(card, 'Exhausted')
                    self.exhaust_pile.add_card(card)
                    # Add the card to the Exhausted pile
                    self.hand.remove_card(card)
                    # Remove the card from hand
                    self.passive_check_and_exe('Exhaust')
            else:
                for card in reversed(self.hand.cards):
                    # Go through every card
                    if card.effect:
                        self.if_card_cond(card, 'Exhausted')
                        # Execute the Exhausted effect
                    self.exhaust_pile.add_card(card)
                    # Add the card to the Exhausted pile
                    self.hand.remove_card(card)
                    # Remove the card from hand
                    self.passive_check_and_exe('Exhaust')
    
    def exhaust_choose_hand(self, num : int):
        '''Exhaust a number choosen cards from hand
        
        ### args: 
            num: Number of cards that needs to be exhausted'''
        self.hard_card_select(num, self.hand)
        # Select a number of cards
        self.exhaust_selected()

    def exhaust_selected(self):
        '''Exhausts selected cards
        
        ### Returns: 
            True or False depending on if a card was exhausted'''
        if self.selected:
            # If there are selected cards
            for card in reversed(self.selected):
                # Go through every selected card
                self.if_card_cond(card, 'Exhausted')
                self.exhaust_pile.add_card(card)
                self.selected.remove(card)
                # Exhaust all selected cards
                self.passive_check_and_exe('Exhaust')
                # check for effects
            return True
        return False
    
    def if_card_cond(self, card : card_constructor.Card, cond : str, override = None):
        '''Executes card effects that happens when something happens to a card (IE: Discarded, Exhausted, etc)
        
        ### args:
            card: The card being exhausted
            cond: The condition that is happening
            override: Info override for certain situations
        '''
        context = {
            # Info to be passed on in effect execution
            'user': self.player,
            'enemies': self.enemies,
            'draw': self.draw_pile,
            'discard': self.discard_pile,
            'hand': self.hand,
            'exhaust': self.exhaust_pile,
            'target': card.target
        }
        if override:
            context = override
        # uses override context if there is one
        if card.effect:
            # If the cards have effects
            if cond in card.effect:
                # If the cards have an conditional effect
                for effect, details in card.effect[cond].items():
                    effect(*details, context, self)
                    # Executing effects

    def retain_cards(self, num: int):
        '''Increase the amount of cards you can keep at the end of the turn

        ### args:
            num: The amount to increase by
        '''
        self.retain += num

    def energy_change(self, amount: int):
        '''Updates the amount of energy the player has
        
        ### args:
            amount: The number to change the energu by, can be positive or negative'''
        self.energy = max(0, self.energy + amount)
        # Adds amount to energy, if energy becomes negative, becomes 0 instead

    def gold_gain(self, amount: int):
        '''Method for player gaining gold in the middle of combat
        
        ### args:
            amount: amount of gold gained'''
        self.run.gold_modification(amount)

    def card_limit(self, limit = False):
        '''Checks for if the player can play anymore cards
        
        ### args:
            limit: The Number of cards you can play per turn, False if there is none given'''
        if limit:
            # If limit is not false
            if self.cards_played >= limit:
                # If the number of cards played is above or equal to the limit
                self.can_play_card = False
                # Disable the ability to play cards
            else:
                if self.run.mechanics['Cards_per_Turn'] != False:
                    # Checks for if there is a cards per turn limit set
                    if self.cards_played < self.run.mechanics['Cards_per_Turn']:
                        # If its below the amount
                        self.can_play_card = True
                        # can play cards
                    else:
                        self.can_play_card = False
                        # Disable the ability to play cards
                else: 
                    self.can_play_card = True
                    # No Limit set

    def resolve_action(self):
        '''Resolves an action done by the player, mainly just checks for deaths of enemies and if a end of combat condition is met'''
        for enemy in reversed(self.enemies.enemy_list):
            # Goes throught every enemy
            if enemy != None:
                if enemy.died(self) == True:
                    # If they're dead
                    if enemy.buffs['Thievery'] > 0:
                        if enemy.buffs['Stolen'] > 0:
                            self.player.gold += enemy.buffs['Stolen']
                    self.enemies.remove_enemy(enemy)
                    # Remove them from the enemy list
                    self.passive_check_and_exe('Lethal')
        if self.hand.is_empty():
            self.passive_check_and_exe('Empty Hand')
        if self.enemies.is_empty():
            # If there are no more enemies
            self.combat_active = False
            # End the combat
        if self.player.died() == True:
            self.combat_active = False
        # Checks if the player has died and end sthe combat if so

    def havoc(self, num: int, special: bool):
        '''Havoc referrs to playing the top card of the draw pile, this Method will do that action a number of times
        
        ### args:
            num: Number of times to havoc
            special: true or false to represent whether to exhaust the card played this way'''
        for i in range(0, num):
            # Iterate a certain amount of times
            if not self.draw_pile.is_empty():
                # If there are cards in the draw pile
                holding = None
                # Initialize holding
                if self.playing:
                    holding = self.playing
                # temporily holds the current playing card
                self.playing = self.draw_pile.top_card()
                # Make the top card the card being played
                self.draw_pile.remove_card(self.playing)
                # Remove the top card of the draw pile
                if special == True:
                    # If the played card needs to be exhausted
                    self.playing.exhaust = True
                    # Make the card exhaust
                context = {
                    # Info to be passed on for executing effects
                    'user': self.player,
                    'enemies': self.enemies,
                    'draw': self.draw_pile,
                    'discard': self.discard_pile,
                    'hand': self.hand,
                    'exhaust': self.exhaust_pile,
                    'target': 2
                }
                if self.playing.target == 1:
                    context['target'] = self.player_targeting(context, 2)
                else:
                    context['target'] = self.player_targeting(context, self.playing.target)
                self.play_card(context['target'])
                # Play the card
                if holding:
                    self.playing = holding
            else:
                break
                # end the loop
    
    def sever(self, card_type: set) -> list:
        ''' Sever refers to exhausting all cards of certain types from hand
        
        ### args:
            card_type (set): Contains all the card type ids of the cards that needs to be exhausted'''
        cards_exhausted_type = []
        # Initialize a list for storing the types of all cards exhausted
        if self.hand:
            # If the hand is not empty
            for card in reversed(self.hand):
                # Go through all cards in the hand
                if card.type in card_type:
                    # If the card type is a type that needs to be exhausted
                    cards_exhausted_type.append(card.type)
                    # Save the type of the card exhausted to the list
                    self.exhaust_pile.add_card(card)
                    # Add the card to the exhaust pile
                    self.hand.remove_card(card)
                    # remove the card from hand
                    self.passive_check_and_exe('Exhaust')
        return cards_exhausted_type
        # Returns the list of types of all the cards exhausted, used for executing conditional effects on certain cards
    
    def escape(self):
        '''Method for ending combat without killing all enemies'''
        if self.combat_type != 'Boss':
            self.player.thieved = 0
            self.escaped = True
            self.combat_active = False
        # Escape from non boss combats

    def mulligan(self):
        '''Method for performing a mulligan which refers to discarding any number of cards from the hand and drawing that many back
        '''
        if self.hand:
            # If the player even has cards in the hand
            self.soft_card_select(len(self.hand), self.hand)
            # Selected as many cards in hand as the player wants
            if self.selected:
                # If there were cards selected
                amount = len(self.selected)
                # Save amount of cards selected
                for card in reversed(self.selected):
                    self.discard_pile.add_card(card)
                    self.selected.remove(card)
                # Add cards to discard pile
                self.draw(amount)
                # Draw same amount back

    def exhaust_entire_pile(self, pile):
        '''Exhausts an entire pile
        
        ### args:
            pile: The pile that needs to be exhausted'''
        if pile:
            # if the pile is not empty
            for card in reversed(pile):
                # Goes through every card in the pile
                self.exhaust_pile.add_card(card)
                # Add the card to the exhaust pile
                pile.remove_card(card)
                # remove the card from the pile
                self.passive_check_and_exe('Exhaust')
                # Check for effects

    def play_card(self, target = None):
        '''Method used for playing cards in combat

        ### args:
            target: The target of the card, only inputted if some info needs to be overrided to not be the default or if the card targets a specific enemy
            overide: A dictionary of information that is passed on to execute effects, only inputted if some info needs to be overrided to not be the default
        '''
        context = {
            # Default info to pass on for executing effects
            'user': self.player, # The player is playing the card
            'enemies': self.enemies, # List of enemies
            'draw': self.draw_pile, # The draw pile
            'discard': self.discard_pile, # The discard pile
            'hand': self.hand, # the hand
            'exhaust': self.exhaust_pile, # The exhaust pile
            'target': target # the target of the card, This is mainly the one that gets overrided
        }
        # Queue effects with delay to start after animation
        if self.can_play_card == False:
            self.discard_pile.add_card(self.playing)
            # Add the card to the discard pile
        elif self.playing.cost == 'U':
            # If the card being played is Unplayable
            if self.playing.type == 3 and self.run.mechanics['Playable_Status']:
                # If the type of card is a status and the mechanic Playable_Status is activated
                self.exhaust_pile.add_card(self.playing)
                # Add the card to the exhaust pile
                self.playing = None
                # Empty the playing card
                self.passive_check_and_exe('Exhaust')
                # Check for effects
            elif self.playing.type == 4 and self.run.mechanics['Playable_Curse']:
                # If the type of card is a Curse and the mechanic Playable_Curse is activated
                effects.lose_hp(1, context, self)
                # Execute the effect for playing a curse
                self.exhaust_pile.add_card(self.playing)
                # Add the card to the exhaust pile
                self.passive_check_and_exe('Exhaust')
                # Check for effects
            else:
                self.discard_pile.add_card(self.playing)
                # Does nothing
        elif self.playing.cost == 'X':
            # If you are playing an X cost card (A card that spends all you energy and has effects scale off of energy spent)
            self.playing.play_x_cost(self.energy + self.run.mechanics['X_Bonus'])
            # Aquire the complete details of the effect being executed
            times = 1
            if self.necroed == True and self.run.mechanics['Necro'] == True and self.playing.type == 0 and self.playing.get_cost() >= 2:
                self.necroed = False
                times = 2
            if self.player.buffs['Duplicate'] > 0:
                times += 1
                self.player.buffs['Duplicate'] -= 1
            if self.player.buffs['Double Tap'] > 0 and self.playing.type == 0:
                times += 1
                self.player.buffs['Double Tap'] -= 1
            for i in range(0, times):
                for effect, details in self.playing.x_cost_effect.items():
                    effect(*details, context, self)
                # Execute the X cost effect
            if self.playing.exhaust == True:
                rng = random.randint(1, 100)
                if rng <= self.run.mechanics['Exhaust_Chance']:
                    # If the card exhausts
                    self.exhaust_pile.add_card(self.playing)
                    # Add the card to the exhaust pile 
                    self.if_card_cond(self.playing, 'Exhausted')
                    # Execute Exhausted effects
                    self.passive_check_and_exe('Exhaust')
                    # Check for effects
                else:
                    self.discard_pile.add_card(self.playing)
                    # Discard instead
            else:
                self.discard_pile.add_card(self.playing)
                # Add the card to the discard pile
        else: 
            if self.playing.effect:
                # If the card has an effect
                times = 1
                if self.necroed == True and self.run.mechanics['Necro'] == True and self.playing.type == 0 and self.playing.get_cost() >= 2:
                    self.necroed = False
                    times = 2
                if self.player.buffs['Duplicate'] > 0:
                    times += 1
                    self.player.buffs['Duplicate'] -= 1
                if self.player.buffs['Double Tap'] > 0 and self.playing.type == 0:
                    times += 1
                    self.player.buffs['Double Tap'] -= 1
                for i in range(0, times):
                    for effect, details in self.playing.effect.items():
                        # Iterates through every effect
                        if not isinstance(effect, str):
                            effect(*details, context, self)
                            #  Performs the effects if its not a conditional
            if self.playing.type == 2:
                # If the card played was a power
                if 'Power' in self.playing.effect:
                    # If the power card played has an actual effect that isn't just giving an normal buff
                    self.powers.add_card(self.playing)
                    # Add the card played to the player powers
            elif self.playing.exhaust == True:
                rng = random.randint(1, 100)
                if rng <= self.run.mechanics['Exhaust_Chance']:
                    # If the card exhausts
                    self.exhaust_pile.add_card(self.playing)
                    # Add the card to the exhaust pile 
                    self.if_card_cond(self.playing, 'Exhausted')
                    # Execute Exhausted effects
                    self.passive_check_and_exe('Exhaust')
                    # Check for effects
                else:
                    self.discard_pile.add_card(self.playing)
                    # Discard instead
            else:
                self.discard_pile.add_card(self.playing)
                # Add the card to the discard pile
        if self.playing.combat_cost[1] == 'Played':
            self.playing.combat_cost = (None, None)
        # Update cost of cards after being played
        self.resolve_action()
        if self.playing.type == 0:
            self.passive_check_and_exe('Attack Played')
        elif self.playing.type == 1:
            self.passive_check_and_exe('Skill Played')
            if self.enemies.is_empty() == False:
                for enemy in self.enemies.enemy_list:
                    if enemy != None:
                        if 'Enraged' in enemy.buffs:
                            enemy.gain_buff('Strength', enemy.buffs['Enraged'])
        elif self.playing.type == 2:
            self.passive_check_and_exe('Power Played')
        elif self.playing.type == 3:
            self.passive_check_and_exe('Status Played')
        elif self.playing.type == 4:
            self.passive_check_and_exe('Curse Played')
        else:
            raise TypeError(f'Card type not found: {self.playing.type}')
        # Check for effects that occur when certain types of cards are played
        self.playing = None
        # Empty the currently playing card
        self.cards_played += 1
        # Increase the amount of cards played by 1
        self.passive_check_and_exe('Card Played')
        if self.hand:
            # if there are cards in hand
            for card in self.hand:
                # for all cards in hand
                self.if_card_cond(card, 'Card Played')
                # Execute effects for if a card is played
                self.resolve_action()
                # Resolve effects
    
    def use_potion(self, potion, targets = None):
        '''Method used for using potions in combat

        ### args:
            Potion: The potion that is being used
        '''
        context = {
            # Info for executing effects
            'user': self.player,
            'enemies': self.enemies,
            'draw': self.draw_pile,
            'discard': self.discard_pile,
            'hand': self.hand,
            'exhaust': self.exhaust_pile,
            'target': targets
        }
        if targets == None or isinstance(targets, int):
            context['target'] = self.player_targeting(context, potion.target)
        if potion.time_of_use == 'combat':
            # If the potion that is being used can be used during combat
            i = 1
            if self.player.relics:
                for relic in self.player.relics:
                    if relic.effect_type == 'Sacred Bark':
                        i = 2
                        break
            for times in range(0, i):
                for effect, details in potion.effect.items():
                    effect(*details, context, self)
                # Execute effects
            self.bonusEff('Used Potion')
            self.player.potions[self.player.potions.index(potion)] = None
            # Remove the potion from combat and the player object
        elif potion.time_of_use == 'all':
            self.run.use_potion(potion)
            # Use potion using player method
        self.resolve_action()

    def player_turn_start(self):
        '''Method for doing everything that needs to be done at the start of combat'''
        self.necroed = True
        self.enemy_turn = False
        # Player turn starts
        self.can_play_card = True
        # Set the ability to play cards to be true
        self.card_type_played = {}
        # Reset the card types that were played
        self.energy = 0
        # Set energy to 0
        self.turn += 1
        # Increase turn counter
        self.player.buffs['Parry'] = 0
        self.player.buffs['Deflect'] = 0
        if self.player.relics:
            for relic in self.player.relics:
                relic.turnEff(self)
        # Execute effects for specific turns
        self.cards_played = 0
        # Set cards played to 0
        if not self.run.mechanics['Block_Loss']:
            self.player.block = 0
        else:
            self.player.block = max(0, self.player.block - self.run.mechanics['Block_Loss'])
        # Lose all block at the start of turn
        if self.start_of_combat == True:
            # Retrieve the enery cap for this combat
            self.passive_check_and_exe('Combat Start')
            # Execute start of combat effects of passives
            self.start_of_combat = False
        self.energy += self.energy_cap
        # Add energy cap to energy
        self.energy += self.player.buffs['Energized']
        self.player.buffs['Energized'] = 0
        # Add extra energy equal to energized
        self.draw(5 + self.player.buffs['Draw Card'] - self.player.debuffs['Draw Reduction'])
        # Draw 5 cards for the start of turn, modified depending on buffs and debuffs that affect draw
        self.player.buffs['Draw Card'] = 0
        # Said buff resets
        self.player.debuffs['Draw Reduction'] = 0
        # Said debuff resets
        self.passive_check_and_exe('Turn Start')
        # Check for powers that activate at the start of a turn
        self.get_intent()
        return 'next'

    def get_intent(self):
        '''Method for getting the intent of the enemies'''
        for enemy in self.enemies.enemy_list:
            if enemy != None:
                if enemy.intent == None:
                    enemy.intent_get(self)

    def player_turn(self):
        '''Execute actions the player does during their turn'''
        # Draw end turn button
        end_turn_rect = pygame.Rect(self.SCREEN_WIDTH - 250, self.SCREEN_HEIGHT - 250, 150, 50)
        self.combat_surface.blit(self.end_turn_button, end_turn_rect)

        # Check for end turn button click
        mouse_pos = pygame.mouse.get_pos()
        if end_turn_rect.collidepoint(mouse_pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    return 'next'
        return None

    def player_turn_end(self):
        '''Executes actions of the player's turn ending'''
        
        if self.player.debuffs['Vulnerable'] > 0:
            self.player.debuffs['Vulnerable'] -= 1
        if self.player.debuffs['Weak'] > 0:
            self.player.debuffs['Weak'] -= 1
        if self.player.debuffs['Frail'] > 0:
            self.player.debuffs['Frail'] -= 1
        # Lower some debuff counters by 1
        if self.player.buffs['Ritual'] > 0:
            self.player.gain_buff('Strength', self.player.buffs['Ritual'])
        self.player.debuffs['No Draw'] = 0
        if self.player.debuffs['Last Chance'] > 0:
            self.exhaust_entire_pile(self.hand)
            self.exhaust_entire_pile(self.discard_pile)
            self.exhaust_entire_pile(self.draw_pile)
            self.player.debuffs['Last Chance'] = 0
        # Execute all end of turn passives
        self.passive_check_and_exe('Turn End')
        if not self.discard_pile.is_empty():
            for card in self.discard_pile:
                if card.combat_cost[1] == 'Turn':
                    card.combat_cost = (None, None)
        if not self.draw_pile.is_empty():
            for card in self.draw_pile:
                if card.combat_cost[1] == 'Turn':
                    card.combat_cost = (None, None)
        if not self.exhaust_pile.is_empty():
            for card in self.exhaust_pile:
                if card.combat_cost[1] == 'Turn':
                    card.combat_cost = (None, None)
        if not self.hand.is_empty():
            # If the hand isn't empty
            for card in reversed(self.hand):
                # Go through every card
                self.if_card_cond(card, 'Turn End')
                # Execute turn end effects
                if card.combat_cost[1] == 'Turn':
                    card.combat_cost == (None, None)
                # update card costs
            if self.run.mechanics['Turn_End_Discard']:
                # Check if the player needs to discard their hand
                if self.retain > 0:
                    self.soft_card_select(self.retain, self.hand)
                self.retain = 0
                # Select a number of cards to keep
                for card in reversed(self.hand):
                    # goes through everycard in hand
                    if card.retain:
                        # If its retain
                        continue
                        # skip over
                    elif card.ethereal:
                        # if its ethereal
                        self.exhaust_pile.add_card(card)
                        # Exhaust the card
                        self.if_card_cond(card, 'Exhaust')
                        # Activate Exhausted effects
                        self.passive_check_and_exe('Exhaust')
                        # Check for effects
                    else:
                        self.discard_pile.add_card(card)
                        # Discard the card
                    self.hand.remove_card(card)
                    # removes the card from hand
                if self.selected:
                    # If cards were selected to be retained
                    self.hand.extend(self.selected)
                    # Add them back to hand
                    self.selected[:] = []
                    # empty selected
        if self.player.debuffs['Chained'] > 0:
            self.player.lose_buff('Strength', self.player.debuffs['Chained'])
            self.player.debuffs['Chained'] = 0
        # Chained effect
        if self.player.debuffs['Atrophy'] > 0:
            self.player.lose_buff('Dexterity', self.player.debuffs['Atrophy'])
            self.player.debuffs['Atrophy'] = 0
        self.player.debuffs['Entangled'] = 0
        self.counter_reset()
        return 'next'
        
    def discover(self, cards, cost):
        '''Ask user to add to hand one of the 3 cards given
        
        ### args:
            cards: A list of 3 cards to choose from
            cost: cost modifications to the cards
        '''
        for i in range(0, 3):
            cards[i] = card_constructor.create_card(cards[i], card_data.card_info[cards[i]])
        cards = Pile(cards, 'discover')
        self.hard_card_select(1, cards)
        # Select 1 card from the list
        if not self.hand.is_empty():
            if len(self.hand) == 10:
                # If the player is at hand size
                self.discard_pile.add_card(self.selected[-1])
                self.selected[:] = []
                # Add to discard pile
            else:
                self.hand.add_card(self.selected[-1])
                self.selected[:] = []
                # Add to hand instead
        else:
            self.hand.add_card(self.selected[-1])
            self.selected[:] = []
            # Add to hand instead
        if cost != 'na':
            # If the cost needs to be modified
            self.hand.cards[-1].cost_change(cost, 'Played')
            # Change the cost until end of turn

    def upgrade(self, cards):
        '''Method to upgrade cards temporily for the combat
        
        ### args:
            cards: a list of cards to upgrade
        '''
        if cards:
            # If there are cards to be upgraded
            for card in cards:
                # go through every card
                if card.id + 100 in card_data.card_info:
                    # If a card can be upgraded
                    upgraded_card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
                    if cards == self.hand:
                        current_pos = self.hand[self.hand.index(card)].current_pos
                        self.hand[self.hand.index(card)] = upgraded_card
                        self.hand[self.hand.index(upgraded_card)].current_pos = current_pos
                    elif cards == self.draw_pile:
                        self.draw_pile[self.draw_pile.index(card)] = upgraded_card
                    elif cards == self.discard_pile:
                        self.discard_pile[self.discard_pile.index(card)] = upgraded_card
                    else:
                        cards[cards.index(card)] = upgraded_card
                # upgrade the card by making its id and effects of the card 100 higher

    def enemy_turn_start(self):
        '''Method for the enemy turn starting'''
        self.enemy_turn = True
        for enemy in self.enemies.enemy_list:
            # For every enemy
            if enemy != None:
                enemy.turn_start()
                # Execute the start of turn method
        return 'next'

    def enemy_turn_end(self):
        '''Method for ending enemy's turn'''
        for enemy in self.enemies.enemy_list:
            # For every enemy
            if enemy != None:
                enemy.turn_end()
                # Execute the end of turn method
        return 'next'

    def enemy_action(self):
        '''Execute all enemy actions
        '''
        for enemy in self.enemies.enemy_list:
            # Go through every enemy
            if enemy != None:
                pygame.time.wait(500)
                if enemy.intent == None:
                    continue
                if enemy.intent[0]:
                    # If the enemy has an intent
                    context = {
                        # Default info to pass on for executing effects
                        'user': enemy, # The enemy doing the action
                        'enemies': self.enemies, # List of enemies
                        'target': enemy.intent[1], # the target of the card, This is mainly the one that gets overrided
                        'draw': self.draw_pile,
                        'discard': self.discard_pile,
                        'hand': self.hand,
                        'exhaust': self.exhaust_pile
                    }
                    if enemy.intent[0] != None or enemy.intent[2] != 'Special':
                        for effect, details in enemy.intent[0].items():
                            effect(*details, context, self)
                    # Execute the ffects
                    self.resolve_action()
                    self.combat_surface.fill((30, 30, 30))
                    self.combat_surface.blit(self.background_sprite, (0, 0))
                    mouse_pos = pygame.mouse.get_pos()
                    enemy.intent = None
                    self.update_game_state(mouse_pos)
                    self.draw_game_state(mouse_pos)
                    self.screen.blit(self.combat_surface, (0, 0))
                    pygame.display.flip()
                enemy.intent = None

            # Clear intent
        self.resolve_action()
        # Resolves action
        return 'next'

    def bandit_run(self, context):
        '''Method for a bandit escape
        
        ### args:
        context: info related to the user and state of game'''
        self.player.thieved -= context['user'].buffs['Stolen']
        self.enemies.remove_enemy(context['user'])
        # Update info related to stolen gold and remove the escaping enemy

    def summon_enemies(self, enemies: list):
        '''Method for adding more enemies to the combat session
        
        ### args:
            enemies: A list of new enemy objects to be added
        '''
        return # Placeholder

    def split(self, slime_type, hp):
        '''Method for larger slimes splitting when they hit half health
        
        ### args: 
            slime_type: the type of slime that is splitting
            hp: health of the slimes the bigger slime split into
        '''
        if slime_type == 'Slime Boss':
            # if the slime boss is splitting
            enemies = [enemy_data.LargeBlueSlime(hp), enemy_data.LargeGreenSlime(hp)]
            for enemy in enemies:
                self.enemies.add_enemy(enemy)
            # Add 2 smaller slimes of the each type with the current hp of the bigger slime
        elif slime_type == 'Blue':
            # If a large Blue slime is splitting
            enemies = [enemy_data.MediumBlueSlime(hp), enemy_data.MediumBlueSlime(hp)]
            for enemy in enemies:
                self.enemies.add_enemy(enemy)
            # Add 2 smaller slimes of the same type with the current hp of the bigger slime
        elif slime_type == 'Green':
            # If a large green slime is splitting
            enemies = [enemy_data.MediumGreenSlime(hp), enemy_data.MediumGreenSlime(hp)]
            for enemy in enemies:
                self.enemies.add_enemy(enemy)
            # Add 2 smaller slimes of the same type with the current hp of the bigger slime
        else:
            raise ValueError(f'Unknown slime type {slime_type}')
        


class Pile:
    def __init__(self, cards, type):
        self.cards = cards
        self.type = type
        self.is_hover = False
        self.is_clicked = False
        self.scroll_offset = 0
        self.icon_sprite = pygame.image.load(os.path.join("assets", "icons", "pile_icon.png"))
        # Scale down the pile icon sprite
        scaled_width = int(self.icon_sprite.get_width() / 10)
        scaled_height = int(self.icon_sprite.get_height() / 10)
        self.icon_sprite = pygame.transform.scale(self.icon_sprite, (scaled_width, scaled_height))
        self.rect = self.icon_sprite.get_rect()
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 30)
    
    def index(self, card):
        """Return the index of a card in the pile"""
        return self.cards.index(card)

    def __setitem__(self, index, card):
        """Allow setting cards by index"""
        self.cards[index] = card

    def __len__(self):
        """Return the number of cards in the pile"""
        return len(self.cards)

    def __iter__(self):
        """Make pile iterable by returning iterator of self.cards"""
        return iter(self.cards)
        
    def __reversed__(self):
        """Make pile reversible by returning reversed iterator of self.cards"""
        return reversed(self.cards)

    def is_empty(self):
        """Check if the pile is empty"""
        return len(self.cards) == 0

    def curse_count(self):
        """Count the number of curse cards in the hand"""
        return sum(1 for card in self.cards if card.type == 4)

    def top_card(self):
        """Return the top card of the pile"""
        return self.cards[-1]
    
    def add_top(self, card):
        """Add a card to the top of the pile"""
        self.cards.append(card)

    def add_card(self, card):
        """Add a card to the pile"""
        if not self.type == 'draw' or self.is_empty():
            self.cards.append(card)
        else:
            self.cards.insert(random.randint(0, len(self.cards) - 1), card)

    def insert_card(self, card):
        """Insert a card into the pile at a random index"""
        self.cards.insert(random.randint(0, len(self.cards) - 1), card)

    def shuffle(self):
        """Shuffle the cards in the pile"""
        random.shuffle(self.cards)
    
    def empty(self):
        """Empty the pile"""
        self.cards = []

    def remove_card(self, card):
        """Remove a card from the pile"""
        self.cards.remove(card)

    def remove_top(self):
        """Remove the top card from the pile"""
        return self.cards.pop()

    def hover(self):
        self.is_hover = True

    def unhover(self):
        self.is_hover = False

    def click(self):
        self.is_clicked = True
    
    def unclick(self):
        self.is_clicked = False

    def draw_icon(self, surface):
        """Draw the icon of the pile"""
        if self.type == 'draw':
            # Draw pile icon in bottom right
            icon_x = surface.get_width() - self.icon_sprite.get_width() - 20  # 20px padding from right
            icon_y = surface.get_height() - self.icon_sprite.get_height() - 20  # 20px padding from bottom
            surface.blit(self.icon_sprite, (icon_x, icon_y))
            # Update collision box to match icon position
            self.rect = pygame.Rect(icon_x, icon_y, self.icon_sprite.get_width(), self.icon_sprite.get_height())
            
        elif self.type == 'discard':
            # Discard pile icon in bottom left
            icon_x = 20  # 20px padding from left
            icon_y = surface.get_height() - self.icon_sprite.get_height() - 20  # 20px padding from bottom
            surface.blit(self.icon_sprite, (icon_x, icon_y))
            # Update collision box to match icon position
            self.rect = pygame.Rect(icon_x, icon_y, self.icon_sprite.get_width(), self.icon_sprite.get_height())
        elif self.type == 'exhaust':
            # Exhaust pile icon in bottom right above draw pile
            icon_x = surface.get_width() - self.icon_sprite.get_width() - 20  # 20px padding from right
            icon_y = surface.get_height() - self.icon_sprite.get_height() - 100  # 100px above draw pile
            surface.blit(self.icon_sprite, (icon_x, icon_y))
            # Update collision box to match icon position
            self.rect = pygame.Rect(icon_x, icon_y, self.icon_sprite.get_width(), self.icon_sprite.get_height())
            
            # Draw number of exhausted cards
            # Black outline
            outline = self.font.render(str(len(self.cards)), True, (0, 0, 0))
            # Purple text
            text = self.font.render(str(len(self.cards)), True, (128, 0, 128))
            
            # Position text centered above icon
            text_x = icon_x + (self.icon_sprite.get_width() - text.get_width()) // 2
            text_y = icon_y + 5
            
            # Draw outline by offsetting in all directions
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                surface.blit(outline, (text_x + dx, text_y + dy))
            # Draw main text
            surface.blit(text, (text_x, text_y))
        elif self.type == 'powers':
            # Exhaust pile icon in bottom right above draw pile
            icon_x =  20  # 20px padding from left
            icon_y = surface.get_height() - self.icon_sprite.get_height() - 100  # 100px above draw pile
            surface.blit(self.icon_sprite, (icon_x, icon_y))
            # Update collision box to match icon position
            self.rect = pygame.Rect(icon_x, icon_y, self.icon_sprite.get_width(), self.icon_sprite.get_height())
            
            # Draw number of exhausted cards
            # Black outline
            outline = self.font.render(str(len(self.cards)), True, (0, 0, 0))
            # Purple text
            text = self.font.render(str(len(self.cards)), True, (128, 0, 128))
            
            # Position text centered above icon
            text_x = icon_x + (self.icon_sprite.get_width() - text.get_width()) // 2
            text_y = icon_y + 5
            
            # Draw outline by offsetting in all directions
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                surface.blit(outline, (text_x + dx, text_y + dy))
            # Draw main text
            surface.blit(text, (text_x, text_y))
        
        if self.is_hover:
            # Draw textbox showing pile name
            if self.type != 'powers':
                text = self.font.render(self.type.capitalize() + " Pile", True, (255, 255, 255))
            else:
                text = self.font.render("Active Powers", True, (255, 255, 255))
            padding = 10
            box_width = text.get_width() + padding * 2
            box_height = text.get_height() + padding * 2
            
            # Position box to left or right of icon based on pile type
            if self.type == 'discard' or self.type == 'powers':
                # Position to right of discard pile
                box_x = self.rect.right + 10
            else:
                # Position to left of draw/exhaust piles
                box_x = self.rect.left - box_width - 10
            box_y = self.rect.centery - box_height//2
            
            # Draw semi-transparent black background
            box_surface = pygame.Surface((box_width, box_height))
            box_surface.fill((0, 0, 0))
            box_surface.set_alpha(200)
            surface.blit(box_surface, (box_x, box_y))
            
            # Draw text centered in box
            text_x = box_x + padding
            text_y = box_y + padding 
            surface.blit(text, (text_x, text_y))

    def draw(self, surface, events):
        """Draw all cards in the pile in a scrollable grid formation"""
        CARDS_PER_ROW = 5
        CARD_SPACING = 50  # Pixels between cards
        SCROLL_SPEED = 30
        
        # Get scaled card dimensions (assuming all cards have same size)
        if self.cards:
            card_width = self.cards[0].sprite.get_width() // 2  # Using scaled width
            card_height = self.cards[0].sprite.get_height() // 2  # Using scaled height
        else:
            return
            
        # Calculate grid dimensions
        row_width = (card_width * CARDS_PER_ROW) + (CARD_SPACING * (CARDS_PER_ROW - 1))
        num_rows = (len(self.cards) + CARDS_PER_ROW - 1) // CARDS_PER_ROW
        total_height = (card_height * num_rows) + (CARD_SPACING * (num_rows - 1))
        
        # Calculate starting x position to center the grid
        start_x = (surface.get_width() - row_width) // 2
        
        # Handle scrolling with mouse wheel
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset = max(min(self.scroll_offset + event.y * SCROLL_SPEED, 0), -max(0, total_height - surface.get_height()))
                
        # Draw each card in grid
        for i, card in enumerate(self.cards):
            row = i // CARDS_PER_ROW
            col = i % CARDS_PER_ROW
            
            x = start_x + (col * (card_width + CARD_SPACING))
            y = (row * (card_height + CARD_SPACING)) + CARD_SPACING + self.scroll_offset
            
            # Only draw if any part of the card would be visible on screen
            if y + card_height >= 0 and y <= surface.get_height() + 300:
                card.current_pos = (x, y)
                card.draw(surface)
                # Update cards collision rect
                card.rect = pygame.Rect(x, y, card_width, card_height)

class Hand:
    def __init__(self, cards, center_pos, spread):
        self.cards = cards
        self.type = 'hand'
        self.center_pos = center_pos  # Center position of the hand
        self.spread = spread  # Spread angle or linear spread
        self.hover_spread = spread * 1.3  # Increased spread when hovering

    def index(self, card):
        """Return the index of a card in the pile"""
        return self.cards.index(card)

    def __getitem__(self, index):
        """Allow getting cards by index"""
        return self.cards[index]

    def __setitem__(self, index, card):
        """Allow setting cards by index"""
        self.cards[index] = card

    def __len__(self):
        """Return the number of cards in the hand"""
        return len(self.cards)

    def __reversed__(self):
        """Make pile reversible by returning reversed iterator of self.cards"""
        return reversed(self.cards)

    def __iter__(self):
        """Make Hand iterable by returning iterator of self.cards"""
        return iter(self.cards)

    def is_empty(self):
        """Check if the hand is empty"""
        return len(self.cards) == 0

    def cards_in_hand(self):
        """Return the number of cards in the hand"""
        return len(self.cards)

    def curse_count(self):
        """Count the number of curse cards in the hand"""
        return sum(1 for card in self.cards if card.type == 4)

    def add_card(self, card):
        """Add a card to the hand and position it in the bottom right corner"""
        card.current_pos = (1600, 900)
        self.cards.append(card)
    
    def insert_card(self, card):
        """Insert a card into the hand at a specific index"""
        index = random.randint(0, len(self.cards))
        self.cards.insert(index, card)

    def remove_card(self, card):
        """Remove a card from the hand"""
        self.cards.remove(card)

    def update_positions(self, dragged_card):
        """Update the positions of the cards in the hand."""
        num_cards = len(self.cards)
        if num_cards == 0:
            return

        # Find hovered card index
        hovered_index = -1
        # Only check for hover on the topmost card at each x position
        mouse_pos = pygame.mouse.get_pos()
        for i, card in enumerate(reversed(self.cards)):  # Check cards from top to bottom
            if card != dragged_card and card.rect.collidepoint(mouse_pos):
                hovered_index = len(self.cards) - 1 - i  # Convert reversed index to normal index
                # Set this card as hovered and ensure all others are not
                for j, other_card in enumerate(self.cards):
                    other_card.is_hovered = (j == hovered_index)
                break
        else:  # No card was hovered
            for card in self.cards:
                card.is_hovered = False

        # Calculate total width needed
        total_width = (num_cards - 1) * self.spread
        start_x = self.center_pos[0] - total_width // 2

        for i, card in enumerate(self.cards):
            if card == dragged_card:
                continue

            target_x = start_x + i * self.spread
            target_y = self.center_pos[1]

            # If there's a hovered card, adjust positions
            if hovered_index != -1:
                if i < hovered_index:
                    # Cards before hovered card move left
                    target_x -= self.hover_spread/2
                elif i > hovered_index:
                    # Cards after hovered card move right
                    target_x += self.hover_spread/2
                
                if i == hovered_index:
                    # Move hovered card down instead of up
                    target_y -= card.hover_y_offset

            # Set the target position for each card
            card.target_pos = pygame.Vector2(target_x, target_y)

    def draw(self, surface, dragged_card):
        """Draw all the cards in the hand."""
        for card in self.cards:
            if card != dragged_card:  # Skip the dragged card
                card.draw(surface)
        # Draw the dragged card last for visibility
        if dragged_card:
            dragged_card.draw(surface)

    def bring_to_top(self, card):
        """Bring the specified card to the top of the hand."""
        if card in self.cards:
            self.cards.remove(card)
            self.cards.append(card)

class Enemies:
    def __init__(self, enemies):
        self.enemies = enemies
        self.enemy_list = [None, None, None, None, None]
        for enemy in self.enemies:
            if self.enemy_list[3] == None:
                self.enemy_list[3] = enemy
            elif self.enemy_list[2] == None:
                self.enemy_list[2] = enemy
            elif self.enemy_list[1] == None:
                self.enemy_list[1] = enemy
            elif self.enemy_list[0] == None:
                self.enemy_list[0] = enemy
            elif self.enemy_list[4] == None:
                self.enemy_list[4] = enemy

    def random_enemy(self):
        """Return a random enemy from the list"""
        return random.choice([enemy for enemy in self.enemy_list if enemy is not None])

    def __iter__(self):
        """Make Enemies iterable by returning iterator of self.enemy_list"""
        return (enemy for enemy in self.enemy_list if enemy is not None)

    def __len__(self):
        """Return the number of enemies in the list"""
        i = 0
        for enemy in self.enemy_list:
            if enemy is not None:
                i += 1
        return i

    def is_empty(self):
        if self.enemy_list == [None, None, None, None, None]:
            return True
        else:
            return False

    def draw(self, surface, intent):
        screen_width = surface.get_width()
        mid_x = screen_width // 2
        base_y = 500  # Base y position where enemies will line up
        
        # Start drawing from slightly right of middle
        current_x = mid_x + 50
        
        for i, enemy in enumerate(self.enemy_list):
            if enemy is not None:
                sprite_width = enemy.sprite.get_width()
                sprite_height = enemy.sprite.get_height()
                
                # Get current enemy spacing
                if hasattr(enemy, 'size'):
                    if enemy.size == 'small':
                        current_spacing = 90
                    elif enemy.size == 'medium':
                        current_spacing = 140
                    else:  # large or default
                        current_spacing = 275
                else:
                    current_spacing = 200  # Default spacing
                
                # Look ahead to next enemy's spacing
                next_spacing = current_spacing
                if i < len(self.enemy_list)-1 and self.enemy_list[i+1] is not None:
                    next_enemy = self.enemy_list[i+1]
                    if hasattr(next_enemy, 'size'):
                        if next_enemy.size == 'small':
                            next_spacing = 90
                        elif next_enemy.size == 'medium':
                            next_spacing = 140
                        else:
                            next_spacing = 275
                    else:
                        next_spacing = 200
                
                # Use average of current and next spacing
                spacing = (current_spacing + next_spacing) // 2
                
                # Calculate y position by subtracting sprite height from base_y
                y_pos = base_y - sprite_height
                
                # Update collision rect position to match sprite position
                enemy.rect.bottomleft = (current_x - (sprite_width // 2), base_y)
                
                # Draw sprite
                enemy.draw(surface, current_x - (sprite_width // 2), y_pos)
                if intent:
                    enemy.draw_intent(surface, current_x - (sprite_width // 2), y_pos)
                
                # Move x position for next enemy
                current_x += spacing
            else:
                current_x += 100

    def add_enemy(self, enemy):
        if self.enemy_list[3] == None:
            self.enemy_list[3] = enemy
        elif self.enemy_list[2] == None:
            self.enemy_list[2] = enemy
        elif self.enemy_list[1] == None:
            self.enemy_list[1] = enemy
        elif self.enemy_list[0] == None:
            self.enemy_list[0] = enemy
        elif self.enemy_list[4] == None:
            self.enemy_list[4] = enemy
        else:
            raise ValueError('Too many enemies')

    def remove_enemy(self, enemy):
        if enemy in self.enemy_list:
            self.enemy_list[self.enemy_list.index(enemy)] = None
        else:
            raise ValueError('Enemy not found in list')
    
    def is_empty(self):
        if self.enemy_list[0] != None:
            return False
        elif self.enemy_list[1] != None:
            return False
        elif self.enemy_list[2] != None:
            return False
        elif self.enemy_list[3] != None:
            return False
        elif self.enemy_list[4] != None:
            return False
        else:
            return True
