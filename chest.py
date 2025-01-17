import random
import pygame
import os

class Treasure:
    def __init__(self, run):
        '''Method to initialize the treasure event
        
        ### args:
            run: the run instance'''
        self.run = run
        self.rewards = None
        self.empty = False
        self.type = None
        self.opened = False
        self.background_sprite = pygame.image.load(os.path.join("assets", "ui", "forest.png"))
        self.chest_sprite = pygame.image.load(os.path.join("assets", "sprites", "chest.png"))
        self.chest_rect = self.chest_sprite.get_rect()
        self.confirm_button_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))

    def start_event(self):
        '''Method to start the treasure event'''
        rng = random.randint(1, 100)
        if self.type == None:
            if rng <= 50:
                self.type = 3
            elif rng <= 83:
                self.type = 4
            else:
                self.type = 5
        self.interact()

    def interact(self):
        '''Method to interact with the treasure event'''
        # Initialize the event loop
        running = True
        # Calculate the position of the chest
        chest_x = (1600 - self.chest_sprite.get_width()) // 2
        chest_y = (900 - self.chest_sprite.get_height()) // 2
        self.chest_rect.x = chest_x
        self.chest_rect.y = chest_y
        # Initialize the exit variable
        exit = None
        # Start the event loop
        while running:
            # Get the events
            events = pygame.event.get()
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()
            # Handle potion events
            self.run.potion_events(mouse_pos, events)
            # Handle deck view
            self.run.handle_deck_view(events, mouse_pos)
            # Handle save and exit input
            exit = self.run.handle_save_and_exit_input(events)

            for event in events:
                # Handle quit event
                if event.type == pygame.QUIT:   
                    running = False
                    self.run.exit_game()
                # Handle mouse button up event
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Check if the chest is clicked
                    if self.chest_rect.collidepoint(mouse_pos):
                        # Check if the chest is not opened
                        if not self.opened:
                            self.opened = True
                            self.run.eventMod('Open Chest')
                            self.run.generate_reward_screen_instance(self.type, False, {})
                            self.run.reward.listRewards()
                            if self.run.reward.isEmpty():
                                self.empty = True
                        elif not self.empty:
                            self.run.reward.listRewards()
                            if self.run.reward.isEmpty():
                                self.empty = True
                    # Check if the confirm button is clicked
                    elif self.opened and confirm_button.collidepoint(mouse_pos):
                        running = False
                    # Check if the escape key is pressed
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

            # Draw
            self.run.screen.blit(self.background_sprite, (0, 0))
            self.run.screen.blit(self.chest_sprite, (chest_x, chest_y))
            
            # Draw the confirm button if the chest is opened
            if self.opened:
                confirm_button = pygame.Rect(1600 - self.confirm_button_sprite.get_width(), 650, self.confirm_button_sprite.get_width(), self.confirm_button_sprite.get_height())
                self.run.screen.blit(self.confirm_button_sprite, confirm_button)
                
            # Draw the player ui
            self.run.player.draw_ui(self.run.screen)
            # Update the display
            pygame.display.flip()

        # Check if the player wants to exit to the main menu
        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.run.mapNav()