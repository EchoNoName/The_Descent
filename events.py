import relic_data
import enemy_data
import card_data
import card_constructor
import potion_data
import effects
import random
import pygame
import os

class ScorchedForest:
    def __init__(self, player, run):
        self.name = 'Scorched Forest'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False

    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("As you wander through the thick forest, the air suddenly grows hot, and", True, (255, 255, 255))
        text2 = self.dialogue_font.render("the scent of burning wood fills your nostrils. You come upon a clearing,", True, (255, 255, 255))
        text3 = self.dialogue_font.render("blackened by fire, where flames still dance hungrily on the remnants of trees.", True, (255, 255, 255))
        text4 = self.dialogue_font.render("In the center of the grove, a strange figure looms—an ember-wreathed dryad,", True, (255, 255, 255))
        text5 = self.dialogue_font.render("her fiery eyes watching you intently. She extends a charred hand toward you,", True, (255, 255, 255))
        text6 = self.dialogue_font.render("her voice crackling like the flames:", True, (255, 255, 255))
        text7 = self.dialogue_font.render("\"These flames cleanse and destroy... but they also forge and strengthen.", True, (255, 255, 255))
        text8 = self.dialogue_font.render("Will you step into the fire to claim its gifts, or will you turn away?\"", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("The flames lick at your skin as you reach into the inferno.", True, (255, 255, 255))
        result2 = self.dialogue_font.render("When you withdraw, your hands clutch a small pouch of seared coins.", True, (255, 255, 255))
        result3 = self.dialogue_font.render("You plunge your hand into the inferno and withdraw a small, smoking vial.", True, (255, 255, 255))
        result4 = self.dialogue_font.render("The liquid inside swirls with a fiery glow.", True, (255, 255, 255))
        result5 = self.dialogue_font.render("The fire engulfs you momentarily, and when it subsides, you find yourself", True, (255, 255, 255))
        result6 = self.dialogue_font.render("holding a scorched card pulsing with latent power.", True, (255, 255, 255))
        result7 = self.dialogue_font.render("The dryad watches silently as you turn away, her fiery gaze burning", True, (255, 255, 255))
        result8 = self.dialogue_font.render("into your back until you're out of sight.", True, (255, 255, 255))

        result_active = False
        result_dialogue = None

        # Create option buttons
        option1 = pygame.Rect(650, 480, 800, 40)
        option2 = pygame.Rect(650, 530, 800, 40)
        option3 = pygame.Rect(650, 580, 800, 40)
        option4 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)

        event_active = True
        exit = None

        while event_active:
            # Handle events
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Adjust mouse position to account for event_box position
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if option1.collidepoint(adjusted_pos) and not result_active:
                        self.player.hp_loss(8)
                        self.run.gold_modification(75)
                        result_dialogue = [result1, result2]
                        result_active = True
                        self.completed = True
                    elif option2.collidepoint(adjusted_pos) and not result_active:
                        self.player.hp_loss(8)
                        self.run.generate_reward_screen_instance(False, {'Potions': [potion_data.randomPotion()]})
                        result_dialogue = [result3, result4]
                        result_active = True
                        self.completed = True
                    elif option3.collidepoint(adjusted_pos) and not result_active:
                        self.player.hp_loss(8)
                        card_reward, self.run.rareChanceOffset = card_constructor.generate_card_reward('normal', self.run.rareChanceOffset, self.run.cardRewardOptions, self.player.character_class, self.run.rareChanceMult)
                        for i, card_id in enumerate(card_reward):
                            card_reward[i] = card_constructor.create_card(card_id, card_data.card_info[card_id])
                        self.run.generate_reward_screen_instance(False, {'Cards': [card_reward]})
                        self.run.reward.listRewards()
                        result_dialogue = [result5, result6]
                        result_active = True
                        self.completed = True
                    elif option4.collidepoint(adjusted_pos) and not result_active:
                        result_dialogue = [result7, result8]
                        result_active = True
                        self.completed = True
                    elif continue_button.collidepoint(adjusted_pos) and self.completed:
                        event_active = False
                        break

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            if not result_active:
                # Draw dialogue text
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 60))
                event_box.blit(text3, (650, 90))
                event_box.blit(text4, (650, 140))
                event_box.blit(text5, (650, 170))
                event_box.blit(text6, (650, 200))
                event_box.blit(text7, (650, 250))
                event_box.blit(text8, (650, 280))
            else:
                # Draw result dialogue text
                event_box.blit(result_dialogue[0], (650, 30))
                event_box.blit(result_dialogue[1], (650, 60))

            if not self.completed:
                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)
                pygame.draw.rect(event_box, (70, 70, 70), option3)
                pygame.draw.rect(event_box, (70, 70, 70), option4)

                # Draw option text
                option1_text = self.option_font.render("[Gold for the burning!] Lose 8 HP, gain 75 gold.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Brewed in flame!] Lose 8 HP, gain a random potion.", True, (255, 255, 255))
                option3_text = self.option_font.render("[Strength through suffering!] Lose 8 HP, gain a random card.", True, (255, 255, 255))
                option4_text = self.option_font.render("[This is not my path.] Nothing happens.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
                event_box.blit(option3_text, (option3.x + 10, option3.y + 8))
                event_box.blit(option4_text, (option4.x + 10, option4.y + 8))
            else:
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_button_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_button_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()
        
        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.end_event()

    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class EntangledTreasure:
    def __init__(self, player, run):
        self.name = 'Entangled Treasure'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False
    
    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("In the heart of the forest, you stumble upon a strange sight. Gnarled vines", True, (255, 255, 255))
        text2 = self.dialogue_font.render("twist and writhe unnaturally, encasing what appears to be a faintly glowing", True, (255, 255, 255))
        text3 = self.dialogue_font.render("object. The treasure's shape is obscured, but its allure is undeniable.", True, (255, 255, 255))
        text4 = self.dialogue_font.render("As you approach, the vines shift, tightening protectively around the prize.", True, (255, 255, 255))
        text5 = self.dialogue_font.render("A soft whisper echoes in your mind:", True, (255, 255, 255))
        text6 = self.dialogue_font.render("\"Do you desire what lies within? It will not yield easily... but perhaps", True, (255, 255, 255))
        text7 = self.dialogue_font.render("your persistence will prove worthy.\"", True, (255, 255, 255))
        text8 = self.dialogue_font.render("The vines seem alive, pulsing faintly as if waiting for your decision.", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("You plunge your hand into the writhing mass. The vines lash at you,", True, (255, 255, 255))
        result2 = self.dialogue_font.render("cutting into your skin as you grope blindly for the treasure...", True, (255, 255, 255))
        result3 = self.dialogue_font.render("The vines slap your hand away, leaving only pain for your effort.", True, (255, 255, 255))
        result4 = self.dialogue_font.render("The treasure remains tantalizingly out of reach.", True, (255, 255, 255))
        result5 = self.dialogue_font.render("Your fingers close around a cold, solid object, and with a sharp tug,", True, (255, 255, 255))
        result6 = self.dialogue_font.render("you wrench it free. The vines hiss angrily as the treasure is revealed:", True, (255, 255, 255))
        result7 = self.dialogue_font.render("a Relic of unmistakable power.", True, (255, 255, 255))
        result8 = self.dialogue_font.render("You turn away, leaving the mysterious treasure behind.", True, (255, 255, 255))
        result9 = self.dialogue_font.render("The whispers fade, and the vines settle back into stillness.", True, (255, 255, 255))

        result_active = False
        result_dialogue = None
        current_hp_loss = 3
        current_chance = 25
        attempts = 0

        # Create option buttons
        option1 = pygame.Rect(650, 580, 800, 40)
        option2 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)

        event_active = True
        exit = None
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if option1.collidepoint(adjusted_pos) and not self.completed:
                        self.player.hp_loss(current_hp_loss)
                        if self.player.hp <= 0:  # Check for death
                            self.run.death_screen()
                        else:
                            rng = random.randint(1, 100)
                            if rng <= current_chance:
                                relic = None
                                while True:
                                    relic = relic_data.spawnRelic()
                                    for owned_relic in self.player.relics:
                                        if owned_relic.name == relic.name:
                                            continue
                                    break   
                                self.run.relic_pickup(relic)
                                result_dialogue = [result1, result2, result5, result6, result7]
                                result_active = True
                                self.completed = True
                            else:
                                result_dialogue = [result1, result2, result3, result4]
                                result_active = True
                                attempts += 1
                                current_hp_loss += 1
                                current_chance += 10

                    elif option2.collidepoint(adjusted_pos) and not self.completed:
                        result_dialogue = [result8, result9]
                        result_active = True
                        self.completed = True
                    elif continue_button.collidepoint(adjusted_pos) and result_active:
                        if self.completed:
                            event_active = False
                        else:
                            result_active = False  # Reset to show options again

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            if not result_active:
                # Draw initial dialogue and options
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 60))
                event_box.blit(text3, (650, 90))
                event_box.blit(text4, (650, 140))
                event_box.blit(text5, (650, 190))
                event_box.blit(text6, (650, 220))
                event_box.blit(text7, (650, 250))
                event_box.blit(text8, (650, 300))

                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)

                # Draw option text with updated values
                option1_text = self.option_font.render(f"[Reach Inside] Lose {current_hp_loss} HP. {current_chance}% chance to find a Relic.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Leave] Nothing happens.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
            else:
                # Draw result dialogue
                y_offset = 30
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30

                # Only show continue button if event is completed
                if self.completed:
                    pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                    continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                    event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))
                else:
                    # Show options again after failed attempt
                    pygame.draw.rect(event_box, (70, 70, 70), option1)
                    pygame.draw.rect(event_box, (70, 70, 70), option2)
                    option1_text = self.option_font.render(f"[Try Again] Lose {current_hp_loss} HP. {current_chance}% chance to find a Relic.", True, (255, 255, 255))
                    option2_text = self.option_font.render("[Leave] Nothing happens.", True, (255, 255, 255))
                    event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                    event_box.blit(option2_text, (option2.x + 10, option2.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.end_event()

    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class TheCleric:
    def __init__(self, player, run):
        self.name = 'The Cleric'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False

    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("A strange blue humanoid with a golden helm(?) approaches you with a huge smile.", True, (255, 255, 255))
        text2 = self.dialogue_font.render("\"Hello friend! I am Cleric! Are you interested in my services?!\"", True, (255, 255, 255))
        text3 = self.dialogue_font.render("the creature shouts, loudly.", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("A warm golden light envelops your body and dissipates.", True, (255, 255, 255))
        result2 = self.dialogue_font.render("The creature grins.", True, (255, 255, 255))
        result3 = self.dialogue_font.render("Cleric: \"Cleric best healer. Have a good day!\"", True, (255, 255, 255))
        
        result4 = self.dialogue_font.render("A cold blue flame envelops your body and dissipates.", True, (255, 255, 255))
        result5 = self.dialogue_font.render("The creature grins.", True, (255, 255, 255))
        result6 = self.dialogue_font.render("Cleric: \"Cleric talented. Have a good day!\"", True, (255, 255, 255))
        
        result7 = self.dialogue_font.render("You don't trust this \"Cleric\", so you leave.", True, (255, 255, 255))

        result_active = False
        result_dialogue = None

        # Create option buttons
        option1 = pygame.Rect(650, 530, 800, 40)
        option2 = pygame.Rect(650, 580, 800, 40)
        option3 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)
        exit = None

        event_active = True
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if option1.collidepoint(adjusted_pos) and not result_active and self.player.gold >= 35:
                        self.run.gold_modification(-35)
                        effects.heal_player(int(self.player.maxHp * 0.25), self.run)
                        result_dialogue = [result1, result2, result3]
                        result_active = True
                        self.completed = True
                    elif option2.collidepoint(adjusted_pos) and not result_active and self.player.gold >= 50:
                        self.run.gold_modification(-50)
                        effects.card_select(1, {}, self.run)
                        self.player.remove_card(self.player.selected_cards)
                        result_dialogue = [result4, result5, result6]
                        result_active = True
                        self.completed = True
                    elif option3.collidepoint(adjusted_pos) and not result_active:
                        result_dialogue = [result7]
                        result_active = True
                        self.completed = True
                    elif continue_button.collidepoint(adjusted_pos) and result_active:
                        event_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            if not result_active:
                # Draw dialogue text
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 80))
                event_box.blit(text3, (650, 130))

                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)
                pygame.draw.rect(event_box, (70, 70, 70), option3)

                # Draw option text
                heal_color = (255, 255, 255) if self.player.gold >= 35 else (100, 100, 100)
                purify_color = (255, 255, 255) if self.player.gold >= 50 else (100, 100, 100)
                
                option1_text = self.option_font.render(f"[Heal] Lose 35 Gold. Heal 25% of your Max HP. ({int(self.player.maxHp * 0.25)})", True, heal_color)
                option2_text = self.option_font.render("[Purify] Lose 50 Gold. Remove a card from your deck.", True, purify_color)
                option3_text = self.option_font.render("[Leave] Nothing happens.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
                event_box.blit(option3_text, (option3.x + 10, option3.y + 8))
            else:
                # Draw result dialogue
                y_offset = 30
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30

                # Draw continue button
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.end_event()

    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class GoddessStatue:
    def __init__(self, player, run):
        self.name = 'Goddess Statue'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False
    
    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("As you wander deeper into the forest, the trees part to reveal a clearing", True, (255, 255, 255))
        text2 = self.dialogue_font.render("bathed in soft, ethereal light. In the center stands a towering statue of", True, (255, 255, 255))
        text3 = self.dialogue_font.render("a serene goddess, her expression calm and unjudging. Her hands are", True, (255, 255, 255))
        text4 = self.dialogue_font.render("clasped in prayer, and an ancient plaque at her feet reads:", True, (255, 255, 255))
        text5 = self.dialogue_font.render("\"Offer your burdens to the goddess, and she shall grant you freedom.\"", True, (255, 255, 255))
        text6 = self.dialogue_font.render("You feel an inexplicable pull toward the statue, though the air grows", True, (255, 255, 255))
        text7 = self.dialogue_font.render("heavy with the weight of what you might lose.", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("You kneel before the statue and press your hand to its cold,", True, (255, 255, 255))
        result2 = self.dialogue_font.render("weathered surface. A warmth spreads through your body as a", True, (255, 255, 255))
        result3 = self.dialogue_font.render("shimmering light envelops you. You feel a burden lift—", True, (255, 255, 255))
        result4 = self.dialogue_font.render("a card you no longer need is gone.", True, (255, 255, 255))
        
        result5 = self.dialogue_font.render("You bow respectfully to the statue and step away.", True, (255, 255, 255))
        result6 = self.dialogue_font.render("The clearing remains tranquil, the goddess watching silently as you depart.", True, (255, 255, 255))

        result_active = False
        result_dialogue = None

        # Create option buttons
        option1 = pygame.Rect(650, 580, 800, 40)
        option2 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)
        exit = None

        event_active = True
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if option1.collidepoint(adjusted_pos) and not result_active:
                        self.player.hp_loss(7)
                        effects.card_select(1, {}, self.run)
                        self.player.remove_card(self.player.selected_cards)
                        result_dialogue = [result1, result2, result3, result4]
                        result_active = True
                        self.completed = True
                    elif option2.collidepoint(adjusted_pos) and not result_active:
                        result_dialogue = [result5, result6]
                        result_active = True
                        self.completed = True
                    elif continue_button.collidepoint(adjusted_pos) and result_active:
                        event_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            if not result_active:
                # Draw dialogue text
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 60))
                event_box.blit(text3, (650, 90))
                event_box.blit(text4, (650, 120))
                event_box.blit(text5, (650, 170))
                event_box.blit(text6, (650, 220))
                event_box.blit(text7, (650, 250))

                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)

                # Draw option text
                option1_text = self.option_font.render("[Pray] Lose 7 HP. Remove a card from your deck.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Leave] Nothing happens.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
            else:
                # Draw result dialogue
                y_offset = 30
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30

                # Draw continue button
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.end_event()

    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class AbandonedMonument:
    def __init__(self, player, run):
        self.name = 'Abandoned Monument'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False

    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("You emerge into a secluded grove where an ancient monument stands,", True, (255, 255, 255))
        text2 = self.dialogue_font.render("weathered but still imposing. Vines creep along its crumbling stone base,", True, (255, 255, 255))
        text3 = self.dialogue_font.render("yet one feature remains untouched: a gleaming golden statue at its peak.", True, (255, 255, 255))
        text4 = self.dialogue_font.render("The figure shimmers unnaturally, as if resisting the ravages of time.", True, (255, 255, 255))
        text5 = self.dialogue_font.render("The air grows tense, and you can't shake the feeling that the", True, (255, 255, 255))
        text6 = self.dialogue_font.render("monument is watching you.", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("As you grab the statue and stow it away, a deep rumble shakes", True, (255, 255, 255))
        result2 = self.dialogue_font.render("the monument. Hidden mechanisms spring to life, and deadly", True, (255, 255, 255))
        result3 = self.dialogue_font.render("traps activate around you!", True, (255, 255, 255))
        
        result4 = self.dialogue_font.render("You barely leap into a side passageway, dodging the arrows", True, (255, 255, 255))
        result5 = self.dialogue_font.render("that fly all over the place. Unfortunately, it feels like", True, (255, 255, 255))
        result6 = self.dialogue_font.render("you sprained something however.", True, (255, 255, 255))
        
        result7 = self.dialogue_font.render("You brace for impact, and as the dust settles, you make", True, (255, 255, 255))
        result8 = self.dialogue_font.render("your way out of the monument, injured.", True, (255, 255, 255))
        
        result9 = self.dialogue_font.render("You look for the nearest cover and hide behind it,", True, (255, 255, 255))
        result10 = self.dialogue_font.render("managing to get away with minor injury.", True, (255, 255, 255))
        
        result11 = self.dialogue_font.render("You resist the lure of the golden statue, stepping back cautiously.", True, (255, 255, 255))
        result12 = self.dialogue_font.render("As you leave, the monument's warning lingers in your mind,", True, (255, 255, 255))
        result13 = self.dialogue_font.render("its gleaming treasure untouched.", True, (255, 255, 255))

        result_active = False
        result_dialogue = None
        trap_choice = False
        trap_dialogue = None

        # Create option buttons
        option1 = pygame.Rect(650, 580, 800, 40)
        option2 = pygame.Rect(650, 630, 800, 40)
        option3 = pygame.Rect(650, 530, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)

        event_active = True
        exit = None
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.run.exit_game()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if not trap_choice and not result_active:
                        if option1.collidepoint(adjusted_pos):
                            self.run.relic_pickup(relic_data.createRelic('Golden Statue', relic_data.eventRelics['Golden Statue']))
                            trap_dialogue = [result1, result2, result3]
                            trap_choice = True
                        elif option2.collidepoint(adjusted_pos):
                            result_dialogue = [result11, result12, result13]
                            result_active = True
                            self.completed = True
                    elif trap_choice and not self.completed:
                        if option1.collidepoint(adjusted_pos):
                            effects.max_hp_change(int(self.player.maxHp * -0.08), self.run)
                            result_dialogue = [result4, result5, result6]
                            result_active = True
                            self.completed = True
                        elif option2.collidepoint(adjusted_pos):
                            self.run.card_pickup_from_id(4)  # Injury curse
                            result_dialogue = [result7, result8]
                            result_active = True
                            self.completed = True
                        elif option3.collidepoint(adjusted_pos):
                            self.player.hp_loss(int(self.player.maxHp * 0.25))
                            result_dialogue = [result9, result10]
                            result_active = True
                            self.completed = True
                    elif continue_button.collidepoint(adjusted_pos) and result_active:
                        if self.completed:
                            event_active = False
                        else:
                            result_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            if not result_active:
                if not trap_choice:
                    # Draw initial dialogue
                    event_box.blit(text1, (650, 30))
                    event_box.blit(text2, (650, 60))
                    event_box.blit(text3, (650, 90))
                    event_box.blit(text4, (650, 120))
                    event_box.blit(text5, (650, 150))
                    event_box.blit(text6, (650, 180))

                    # Draw initial options
                    pygame.draw.rect(event_box, (70, 70, 70), option1)
                    pygame.draw.rect(event_box, (70, 70, 70), option2)

                    option1_text = self.option_font.render("[Take] Obtain Golden Statue. Trigger a trap.", True, (255, 255, 255))
                    option2_text = self.option_font.render("[Leave] Nothing happens.", True, (255, 255, 255))

                    event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                    event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
                else:
                    y_offset = 30
                    for line in trap_dialogue:
                        event_box.blit(line, (650, y_offset))
                        y_offset += 30

                    # Draw trap choice options
                    pygame.draw.rect(event_box, (70, 70, 70), option1)
                    pygame.draw.rect(event_box, (70, 70, 70), option2)
                    pygame.draw.rect(event_box, (70, 70, 70), option3)

                    option1_text = self.option_font.render(f"[Dodge] Lose {int(self.player.maxHp * 0.08)} Max HP.", True, (255, 255, 255))
                    option2_text = self.option_font.render("[Tank] Become Cursed - Injury.", True, (255, 255, 255))
                    option3_text = self.option_font.render(f"[Run] Take {int(self.player.maxHp * 0.25)} damage.", True, (255, 255, 255))

                    event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                    event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
                    event_box.blit(option3_text, (option3.x + 10, option3.y + 8))
            else:
                # Draw result dialogue
                y_offset = 30
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30

                if self.completed:
                    pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                    continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                    event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.end_event()

    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class DeadAdventurers:
    def __init__(self, player, run):
        self.name = 'Dead Adventurers'
        self.player = player
        self.run = run
        self.elite = None
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False
        self.elite = None
        self.loot = ['Gold', 'N']
        self.current_chance = 25
        
    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Randomly determine the elite type
        rng = random.randint(1, 3)
        if rng == 1:
            self.elite = [enemy_data.SentryA(), enemy_data.SentryB(), enemy_data.SentryA()]
            elite_text = 'Their pants has been stolen! '
            elite_text2 = 'Also, the armour and face appear to be scoured by flames.'
        elif rng == 2:
            self.elite = [enemy_data.GoblinGiant()]
            elite_text = 'Their pants has been stolen! '
            elite_text2 = 'Also, they look to have been eviscerated and chopped by giant blades.'
        else:
            self.elite = [enemy_data.GiantLouseAwake()]
            elite_text = 'Their pants has been stolen! '
            elite_text2 = 'Also, purple liquid leaks from giant bite marks on their bodies.'
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("As you walk on the path towards your destination, you come across a", True, (255, 255, 255))
        text2 = self.dialogue_font.render("group of dead adventurers on the side.", True, (255, 255, 255))
        text3 = self.dialogue_font.render(elite_text, True, (255, 255, 255))
        text4 = self.dialogue_font.render(elite_text2, True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("You found some gold!", True, (255, 255, 255))
        result2 = self.dialogue_font.render("Hmm, couldn't find anything...", True, (255, 255, 255))
        result3 = self.dialogue_font.render("You found a relic!", True, (255, 255, 255))
        result4 = self.dialogue_font.render("While searching the adventurer you are caught off guard!", True, (255, 255, 255))
        result5 = self.dialogue_font.render("You leave without a sound.", True, (255, 255, 255))

        result_dialogue = None
        combat_triggered = False

        # Create option buttons
        option1 = pygame.Rect(650, 580, 800, 40)
        option2 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)

        event_active = True
        exit = None
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if option1.collidepoint(adjusted_pos) and not self.completed:
                        rng = random.randint(1, 100)
                        if rng <= self.current_chance:
                            # Elite encounter
                            result_dialogue = [result4]
                            combat_triggered = True
                            self.completed = True
                        else:
                            # Found loot
                            if self.loot:
                                item = random.choice(self.loot)
                                self.loot.remove(item)
                                if item == 'Gold':
                                    self.run.gold_modification(30)
                                    result_dialogue = [result1]
                                elif item == 'N':
                                    result_dialogue = [result2]
                                if not self.loot:
                                    self.loot.append('Relic')
                                self.current_chance += 25
                            else:
                                # Found relic
                                relic = relic_data.spawnRelic()
                                self.run.relic_pickup(relic)
                                result_dialogue = [result3]
                                self.completed = True
                    elif option2.collidepoint(adjusted_pos) and not self.completed:
                        result_dialogue = [result5]
                        self.completed = True
                        event_active = False
                    elif continue_button.collidepoint(adjusted_pos) and combat_triggered:
                        event_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            # Draw dialogue text
            event_box.blit(text1, (650, 30))
            event_box.blit(text2, (650, 60))
            event_box.blit(text3, (650, 90))
            event_box.blit(text4, (650, 120))

            # Draw result dialogue if exists
            if result_dialogue:
                y_offset = 180  # Start results below initial dialogue
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30

            if not self.completed:
                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)

                # Draw option text
                option1_text = self.option_font.render(f"[Search] Find Loot. {self.current_chance}% that an Elite will return to fight you.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Leave] End the search and resume your journey.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
            elif combat_triggered:
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            if not combat_triggered:
                self.end_event()
            else:
                self.run_combat()

    def run_combat(self):
        self.run.generage_combat_instace(self.elite, 'Elite')
        self.run.start_combat()
        self.end_event()

    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class ColouredMushrooms:
    def __init__(self, player, run):
        self.name = 'Strange Mushrooms'
        self.player = player
        self.run = run
        self.combat_rewards = None
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False
    
    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("You enter an area full of brightly colored mushrooms.", True, (255, 255, 255))
        text2 = self.dialogue_font.render("Due to your lack of specialization in mycology you are unable", True, (255, 255, 255))
        text3 = self.dialogue_font.render("to identify the specimens.", True, (255, 255, 255))
        text4 = self.dialogue_font.render("You want to escape, but feel oddly compelled to eat a mushroom.", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("Ambushed!!", True, (255, 0, 0))  # Red text for emphasis
        result2 = self.dialogue_font.render("Corpses infested by the mushrooms appear out of nowhere!", True, (255, 255, 255))
        
        result3 = self.dialogue_font.render("You give in to the unnatural desire to eat. As you consume mushroom", True, (255, 255, 255))
        result4 = self.dialogue_font.render("after mushroom, you feel yourself entering into a daze and pass out.", True, (255, 255, 255))
        result5 = self.dialogue_font.render("As you awake, you feel very odd.", True, (255, 255, 255))
        result6 = self.dialogue_font.render("You Heal 25% of your HP, but you also get infected.", True, (255, 255, 255))

        result_dialogue = None
        combat_triggered = False
        show_continue = False
        enemies_ready = False

        # Create option buttons
        option1 = pygame.Rect(650, 580, 800, 40)
        option2 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)

        event_active = True
        exit = None
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if option1.collidepoint(adjusted_pos) and not self.completed:
                        result_dialogue = [result1, result2]
                        combat_triggered = True
                        self.completed = True
                        show_continue = True
                        enemies_ready = True
                        # Set up combat rewards
                        gold = random.randint(10, 20)
                        cards, self.run.rareChanceOffset = card_constructor.generate_card_reward('normal', self.run.rareChanceOffset, self.run.cardRewardOptions, self.player.character_class)
                        for i, card in enumerate(cards):
                            cards[i] = card_constructor.create_card(card, card_data.card_info[card])
                        potions = []
                        rng = random.randint(1, 100)
                        if rng <= self.run.potionChance:
                            potion = potion_data.randomPotion()
                            potions.append(potion)
                            self.run.potionChance -= 10
                        else:
                            self.run.potionChance += 20
                        self.combat_rewards = {'Gold': gold, 'Cards': [cards], 'Potions': potions, 'Relics': [relic_data.createRelic('Strange Mushroom', relic_data.eventRelics['Strange Mushroom'])]}
                    elif option2.collidepoint(adjusted_pos) and not self.completed:
                        self.player.hp_recovery(int(self.player.maxHp * 0.25))
                        card = card_constructor.create_card(6, card_data.card_info[6])
                        self.run.card_pickup(card)
                        result_dialogue = [result3, result4, result5, result6]
                        self.completed = True
                        show_continue = True
                    elif continue_button.collidepoint(adjusted_pos) and show_continue:
                        if combat_triggered and enemies_ready:
                            self.run.generage_combat_instace([enemy_data.InfestedCorpes(), enemy_data.InfestedCorpes(), enemy_data.InfestedCorpes()], 'normal')
                            event_active = False
                        else:
                            event_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            # Draw result dialogue if exists
            if result_dialogue:
                y_offset = 30  # Start results below initial dialogue
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30
            else:
                # Draw dialogue text
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 60))
                event_box.blit(text3, (650, 90))
                event_box.blit(text4, (650, 120))

            if not self.completed:
                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)

                # Draw option text
                option1_text = self.option_font.render("[Destroy] Anger the Mushrooms.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Eat] Heal 25% HP. Become Cursed: Corroded.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
            elif show_continue:
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            if not combat_triggered:
                self.end_event()
            else:
                self.run.generage_combat_instace([enemy_data.InfestedCorpes(), enemy_data.InfestedCorpes(), enemy_data.InfestedCorpes()], 'normal')
                self.run.start_combat(self.combat_rewards)
                self.end_event()

    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class HallucinationFog:
    def __init__(self, player, run):
        self.name = 'Hallucination Fog'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False
    
    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("As you tread deeper into the forest, a dense fog begins to roll in,", True, (255, 255, 255))
        text2 = self.dialogue_font.render("swirling around your feet and creeping into your lungs. The world", True, (255, 255, 255))
        text3 = self.dialogue_font.render("around you warps and twists—the trees seem to breathe, the ground", True, (255, 255, 255))
        text4 = self.dialogue_font.render("pulses like a heartbeat, and whispers echo from unseen figures.", True, (255, 255, 255))
        text5 = self.dialogue_font.render("A voice, soft and disorienting, speaks directly into your mind:", True, (255, 255, 255))
        text6 = self.dialogue_font.render("\"Lost traveler, the fog can reshape what is... if you dare to let", True, (255, 255, 255))
        text7 = self.dialogue_font.render("it touch you. Will you embrace the change, or will you turn away?\"", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("The fog envelops you, its edges blurring and shifting as it twists", True, (255, 255, 255))
        result2 = self.dialogue_font.render("into something new. The whispers in the mist grow louder before", True, (255, 255, 255))
        result3 = self.dialogue_font.render("abruptly ceasing, leaving behind an unfamiliar power in your hands.", True, (255, 255, 255))
        
        result4 = self.dialogue_font.render("The fog swirls around you, then turning it into nothingness.", True, (255, 255, 255))
        result5 = self.dialogue_font.render("A faint sense of relief washes over you, as though a burden", True, (255, 255, 255))
        result6 = self.dialogue_font.render("you didn't realize you carried has vanished.", True, (255, 255, 255))
        
        result7 = self.dialogue_font.render("The fog clings to one of your items, its energy intensifying", True, (255, 255, 255))
        result8 = self.dialogue_font.render("as it glows brighter and stronger. When the fog lifts,", True, (255, 255, 255))
        result9 = self.dialogue_font.render("the item gleams with newfound power.", True, (255, 255, 255))

        result_dialogue = None

        # Create option buttons
        option1 = pygame.Rect(650, 530, 800, 40)
        option2 = pygame.Rect(650, 580, 800, 40)
        option3 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)

        exit = None
        event_active = True
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if not self.completed:
                        if option1.collidepoint(adjusted_pos):
                            effects.card_select(1, {}, self.run)
                            self.player.transform_card()
                            result_dialogue = [result1, result2, result3]
                            self.completed = True
                        elif option2.collidepoint(adjusted_pos):
                            effects.card_select(1, {}, self.run)
                            self.player.remove_card()
                            result_dialogue = [result4, result5, result6]
                            self.completed = True
                        elif option3.collidepoint(adjusted_pos):
                            effects.card_select(1, {}, self.run)
                            self.player.upgrade_card()
                            result_dialogue = [result7, result8, result9]
                            self.completed = True
                    elif continue_button.collidepoint(adjusted_pos):
                        event_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))

            # Draw result dialogue if exists
            if result_dialogue:
                y_offset = 30  # Start results below initial dialogue
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30
            else:
                # Draw dialogue text
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 60))
                event_box.blit(text3, (650, 90))
                event_box.blit(text4, (650, 120))
                event_box.blit(text5, (650, 150))
                event_box.blit(text6, (650, 180))
                event_box.blit(text7, (650, 210))

            if not self.completed:
                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)
                pygame.draw.rect(event_box, (70, 70, 70), option3)

                # Draw option text
                option1_text = self.option_font.render("[Embrace Change] Transform a card.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Shed the Old] Remove a card.", True, (255, 255, 255))
                option3_text = self.option_font.render("[Forge Through] Upgrade a card.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
                event_box.blit(option3_text, (option3.x + 10, option3.y + 8))
            else:
                # Draw continue button
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.end_event()
    
    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class ShiningLight:
    def __init__(self, player, run):
        self.name = 'Shining Light'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False

    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("As you reach an enclosure in the forest, You find a shimmering mass", True, (255, 255, 255))
        text2 = self.dialogue_font.render("of light at the center of a circle of trees.", True, (255, 255, 255))
        text3 = self.dialogue_font.render("Its warm glow and enchanting patterns invite you in.", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("As you walk through the light, you notice that the light is", True, (255, 255, 255))
        result2 = self.dialogue_font.render("absorbed into you.", True, (255, 255, 255))
        result3 = self.dialogue_font.render("It's scorching hot!", True, (255, 0, 0))  # Red text for emphasis
        result4 = self.dialogue_font.render("However, the pain quickly recedes.", True, (255, 255, 255))
        result5 = self.dialogue_font.render("You feel invigorated, as though you received a well deserved slap.", True, (0, 191, 255))  # Blue text
        
        result6 = self.dialogue_font.render("You walk around it, wondering what could have been.", True, (255, 255, 255))

        result_dialogue = None

        # Create option buttons
        option1 = pygame.Rect(650, 580, 800, 40)
        option2 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)

        exit = None
        event_active = True
        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if not self.completed:
                        if option1.collidepoint(adjusted_pos):
                            self.player.hp_loss(int(self.player.maxHp * 0.2))
                            self.player.upgrade_card(['Card', 'Card'])
                            result_dialogue = [result1, result2, result3, result4, result5]
                            self.completed = True
                        elif option2.collidepoint(adjusted_pos):
                            result_dialogue = [result6]
                            self.completed = True
                    elif continue_button.collidepoint(adjusted_pos):
                        event_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            

            # Draw result dialogue if exists
            if result_dialogue:
                y_offset = 30  # Start results below initial dialogue
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30
            else:
                # Draw dialogue text
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 60))
                event_box.blit(text3, (650, 90))

            if not self.completed:
                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)

                # Draw option text
                option1_text = self.option_font.render(f"[Enter] Upgrade 2 random cards. Take {int(self.player.maxHp * 0.2)} damage.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Leave] Nothing happens.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
            else:
                # Draw continue button
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.end_event()
    
    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class SlimeGoop:
    def __init__(self, player, run):
        self.name = 'Slime Goop'
        self.player = player
        self.run = run
        self.event_active = True
        self.event_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'events', f'{self.name}.png'))
        self.event_sprite = pygame.transform.scale(self.event_sprite, (600, 640))
        self.background = pygame.image.load(os.path.join('assets', 'ui', 'event_background.png'))
        self.dialogue_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 26)
        self.option_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 20)
        self.completed = False
    
    def __str__(self):
        return self.name
    
    def run_event(self):
        event_box = pygame.Surface((1500, 700))
        event_box.fill((50, 50, 50))
        
        # Create text surfaces for initial dialogue
        text1 = self.dialogue_font.render("You come across a puddle of bright green slime.", True, (255, 255, 255))
        text2 = self.dialogue_font.render("You can see some gold coins floating within...", True, (255, 255, 255))
        text3 = self.dialogue_font.render("but the slime seems corrosive.", True, (255, 255, 255))

        # Create result dialogue surfaces
        result1 = self.dialogue_font.render("As you reach into the slime, you feel it burning your skin!", True, (255, 0, 0))  # Red for emphasis
        result2 = self.dialogue_font.render("However, you manage to grab some gold.", True, (255, 255, 255))
        
        result3 = self.dialogue_font.render("You decide it's not worth the risk.", True, (255, 255, 255))

        result_dialogue = None

        # Create option buttons
        option1 = pygame.Rect(650, 580, 800, 40)
        option2 = pygame.Rect(650, 630, 800, 40)
        continue_button = pygame.Rect(650, 630, 800, 40)
        exit = None
        event_active = True

        while event_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                event_active = False
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    adjusted_pos = (mouse_pos[0] - 50, mouse_pos[1] - 100)

                    if not self.completed:
                        if option1.collidepoint(adjusted_pos):
                            gold_amount = random.randint(45, 85)
                            self.run.gold_modification(gold_amount)
                            self.player.hp_loss(11)
                            result_dialogue = [result1, result2]
                            self.completed = True
                        elif option2.collidepoint(adjusted_pos):
                            result_dialogue = [result3]
                            self.completed = True
                    elif continue_button.collidepoint(adjusted_pos):
                        event_active = False

            # Draw everything
            event_box.fill((50, 50, 50))
            event_box.blit(self.event_sprite, (30, 30))
            
            
            # Draw result dialogue if exists
            if result_dialogue:
                y_offset = 30  # Start results below initial dialogue
                for line in result_dialogue:
                    event_box.blit(line, (650, y_offset))
                    y_offset += 30
            else:
                # Draw dialogue text
                event_box.blit(text1, (650, 30))
                event_box.blit(text2, (650, 60))
                event_box.blit(text3, (650, 90))


            if not self.completed:
                # Draw option buttons
                pygame.draw.rect(event_box, (70, 70, 70), option1)
                pygame.draw.rect(event_box, (70, 70, 70), option2)

                # Draw option text
                option1_text = self.option_font.render("[Reach Inside] Obtain 45-85 Gold. Take 11 damage.", True, (255, 255, 255))
                option2_text = self.option_font.render("[Leave] Nothing happens.", True, (255, 255, 255))

                event_box.blit(option1_text, (option1.x + 10, option1.y + 8))
                event_box.blit(option2_text, (option2.x + 10, option2.y + 8))
            else:
                # Draw continue button
                pygame.draw.rect(event_box, (70, 70, 70), continue_button)
                continue_text = self.option_font.render("[Continue]", True, (255, 255, 255))
                event_box.blit(continue_text, (continue_button.x + 10, continue_button.y + 8))

            pygame.display.get_surface().blit(self.background, (0, 0))
            self.run.screen.blit(event_box, (50, 100))
            self.run.player.draw_ui(pygame.display.get_surface())
            pygame.display.flip()

        if exit == 'Main Menu':
            self.run.main_menu.main_menu()
        else:
            self.run.mapNav()

    
    def end_event(self):
        self.event_active = False
        self.run.mapNav()

events1 = {
    'Scorched Forest': ScorchedForest,
    'Entangled Treasure': EntangledTreasure,
    'The Cleric': TheCleric,
    'Abandoned Monument': AbandonedMonument,
    'Goddess Statue': GoddessStatue,
    'Dead Adventurers': DeadAdventurers,
    'Coloured Mushrooms': ColouredMushrooms,
    'Hallucination Fog': HallucinationFog,
    'Shining Light': ShiningLight,
    'Slime Goop': SlimeGoop
}



