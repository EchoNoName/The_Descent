import random
import pygame
import os

class Treasure:
    def __init__(self, run):
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
        running = True
        chest_x = (1600 - self.chest_sprite.get_width()) // 2
        chest_y = (900 - self.chest_sprite.get_height()) // 2
        self.chest_rect.x = chest_x
        self.chest_rect.y = chest_y

        while running:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.potion_events(mouse_pos, events)
            self.run.handle_deck_view(events, mouse_pos)

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    self.run.exit_game()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.chest_rect.collidepoint(mouse_pos):
                        if not self.opened:
                            self.opened = True
                            self.run.generate_reward_screen_instance(self.type, False, {})
                            self.run.reward.listRewards()
                            if self.run.reward.isEmpty():
                                self.empty = True
                        elif not self.empty:
                            self.run.reward.listRewards()
                            if self.run.reward.isEmpty():
                                self.empty = True
                    elif self.opened and confirm_button.collidepoint(mouse_pos):
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                        self.run.mapNav()

            # Draw
            self.run.screen.blit(self.background_sprite, (0, 0))
            self.run.screen.blit(self.chest_sprite, (chest_x, chest_y))
            
            if self.opened:
                confirm_button = pygame.Rect(1600 - self.confirm_button_sprite.get_width(), 650, self.confirm_button_sprite.get_width(), self.confirm_button_sprite.get_height())
                self.run.screen.blit(self.confirm_button_sprite, confirm_button)
                
            self.run.player.draw_ui(self.run.screen)
            pygame.display.flip()

        self.run.mapNav()