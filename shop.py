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
            13: 'Remove'
        }
        self.generated = False
        self.discounted = False
        gold_sprite = pygame.image.load(os.path.join("assets", "icons", "gold.png"))
        self.gold_icon_sprite = pygame.transform.scale(gold_sprite, (gold_sprite.get_width()//11, gold_sprite.get_height()//11))
        pygame.font.init()
        self.font = pygame.font.Font('assets/fonts/Kreon-Bold.ttf', 36)
        self.removal_sprite = pygame.image.load(os.path.join("assets", "icons", "pile_icon.png"))
        self.removal_sprite = pygame.transform.scale(self.removal_sprite, (self.removal_sprite.get_width()//2, self.removal_sprite.get_height()//2))
        self.removal_rect = self.removal_sprite.get_rect()
        self.confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
        self.confirm_rect = self.confirm_sprite.get_rect()
        self.background_sprite = pygame.image.load(os.path.join("assets", "ui", "shop_background.png"))
        self.close = False

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
                relic1 = None
                while True:
                    relic1 = relic_data.spawnRelic()
                    for owned_relic in self.run.player.relics:
                        if owned_relic.name == relic1.name:
                            continue
                    break
                if relic1.rarity == 4:
                    self.wares[10] = [relic1, random.randint(143, 157)]
                elif relic1.rarity == 3:
                    self.wares[10] = [relic1, random.randint(238, 262)]
                elif relic1.rarity == 2:
                    self.wares[10] = [relic1, random.randint(285, 315)]
                relic2 = None
                while True:
                    relic2 = relic_data.spawnRelic()
                    for owned_relic in self.run.player.relics:
                        if owned_relic.name == relic2.name:
                            continue
                    break
                if relic2.rarity == 4:
                    self.wares[11] = [relic2, random.randint(143, 157)]
                elif relic1.rarity == 3:
                    self.wares[11] = [relic2, random.randint(238, 262)]
                elif relic1.rarity == 2:
                    self.wares[11] = [relic2, random.randint(285, 315)]
                shopRelic = None
                while True:
                    shopRelic = random.choice(list(relic_data.shopRelics.keys()))
                    shopRelic = relic_data.createRelic(shopRelic, relic_data.shopRelics[shopRelic])
                    for owned_relic in self.run.player.relics:
                        if owned_relic.name == shopRelic.name:
                            continue
                    break
                self.wares[12] = [shopRelic, random.randint(143, 157)]
                removalCost = 75 + self.run.removals * 25
                for relic in self.run.player.relics:
                    if relic.name == 'Coupon':
                        removalCost = 50
                self.wares[13] = ['Remove', removalCost]
        for relic in self.run.player.relics:
            if relic.name == 'Costco\'s Membership Card':
                for ware in self.wares.values():
                    if ware and ware[0]:
                        ware[1] = int(ware[1] * 0.5)
                self.discounted = True

    def interact(self):
        self.close = False
        exit = None
        screen = pygame.display.get_surface()
        shop_surface = pygame.Surface((1600, 900))
        shop_rect = shop_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

        while not self.close:
            screen.fill((0, 0, 0))
            shop_surface.blit(self.background_sprite, (0, 0))
            
            # Display cards 0-4 in top row
            for i in range(5):
                if self.wares[i] and self.wares[i][0]:
                    card_x = 200 + i * 250
                    card_y = 150
                    self.wares[i][0].current_pos = (card_x, card_y)
                    self.wares[i][0].update_rect()
                    self.wares[i][0].draw(shop_surface)
                    
                    # Draw gold cost below
                    shop_surface.blit(self.gold_icon_sprite, (card_x, card_y + 250))
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0))
                    shop_surface.blit(cost_text, (card_x + 80, card_y + 250))

            self.run.player.draw_ui(shop_surface)

            # Display cards 5-6 below cards 0-1
            for i in range(5, 7):
                if self.wares[i] and self.wares[i][0]:
                    card_x = 200 + (i-5) * 250  
                    card_y = 500
                    self.wares[i][0].current_pos = (card_x, card_y)
                    self.wares[i][0].draw(shop_surface)
                    self.wares[i][0].update_rect()

                    shop_surface.blit(self.gold_icon_sprite, (card_x, card_y + 250))
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0))
                    shop_surface.blit(cost_text, (card_x + 80, card_y + 250))

            # Display relics row below cards 2-3
            for i in range(10, 13):
                if self.wares[i] and self.wares[i][0]:
                    relic_x = 720 + (i-10) * 165
                    relic_y = 500
                    self.wares[i][0].draw(shop_surface, relic_x, relic_y)
                    self.wares[i][0].rect.topleft = (relic_x, relic_y)
                    
                    shop_surface.blit(self.gold_icon_sprite, (relic_x - 50, relic_y + 75))
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0))
                    shop_surface.blit(cost_text, (relic_x + 10, relic_y + 75))

            # Display potions row below cards 2-3
            for i in range(7, 10):
                if self.wares[i] and self.wares[i][0]:
                    potion_x = 720 + (i-7) * 165
                    potion_y = 700
                    self.wares[i][0].draw(shop_surface, potion_x, potion_y)
                    self.wares[i][0].rect.topleft = (potion_x, potion_y)
                    shop_surface.blit(self.gold_icon_sprite, (potion_x - 50, potion_y + 50))
                    cost_text = self.font.render(str(self.wares[i][1]), True, (255, 215, 0))
                    shop_surface.blit(cost_text, (potion_x + 10, potion_y + 50))

            # Display card removal box below card 4
            if self.wares[13] and self.wares[13][0]:
                removal_x = 1200
                removal_y = 500
                shop_surface.blit(self.removal_sprite, (removal_x, removal_y))
                self.removal_rect.topleft = (removal_x, removal_y)
                
                shop_surface.blit(self.gold_icon_sprite, (removal_x, removal_y + 250))
                cost_text = self.font.render(str(self.wares[13][1]), True, (255, 215, 0))
                shop_surface.blit(cost_text, (removal_x + 80, removal_y + 250))

            # Draw confirm button in bottom right
            confirm_x = shop_surface.get_width() - self.confirm_sprite.get_width()
            confirm_y = shop_surface.get_height() - 200
            shop_surface.blit(self.confirm_sprite, (confirm_x, confirm_y))
            self.confirm_rect = self.confirm_sprite.get_rect(topleft=(confirm_x, confirm_y))

            # Blit shop surface to screen
            screen.blit(shop_surface, shop_rect)

            # Handle mouse hover for tooltips
            mouse_pos = pygame.mouse.get_pos()
            shop_mouse_pos = (mouse_pos[0] - shop_rect.left, mouse_pos[1] - shop_rect.top)
            hover_name = None
            hover_text = None

            for ware in self.wares.values():
                if ware and ware[0]:
                    if ware[0] != 'Remove':
                        if ware[0].rect.collidepoint(shop_mouse_pos) and not isinstance(ware[0], card_constructor.Card):
                            hover_text = str(ware[0].description)
                            hover_name = ware[0].name
                    else:
                        if self.removal_rect.collidepoint(shop_mouse_pos):
                            hover_text = "Remove a card from your deck"


            if self.run.player.deck_button_rect.collidepoint(mouse_pos):
                deck_hovering = True
            else:
                deck_hovering = False
            
            if deck_hovering:
                deck_text_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 16)
                # Create background surface
                deck_text = deck_text_font.render("View Deck", True, (255, 255, 255))
                bg_surface = pygame.Surface((deck_text.get_width() + 10, deck_text.get_height() + 6))
                bg_surface.fill((0, 0, 0))
                text_x = self.run.player.deck_button_rect.centerx - deck_text.get_width() // 2
                text_y = self.run.player.deck_button_rect.bottom + 35  # Changed from +10 to +30
                # Draw background then text
                shop_surface.blit(bg_surface, (text_x - 5, text_y - 3))
                shop_surface.blit(deck_text, (text_x, text_y))

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
                    test_text = test_font.render(' '.join(current_line), True, (255, 255, 255))
                    if test_text.get_width() > screen.get_width() - 40:  # Leave some margin
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))
                
                desc_texts = [desc_font.render(line, True, (255, 255, 255)) for line in lines]
                
                if hover_name:
                    name_text = self.font.render(hover_name, True, (255, 255, 255))
                    total_height = sum(text.get_height() for text in desc_texts) + name_text.get_height() + 25
                    max_width = max(max(text.get_width() for text in desc_texts), name_text.get_width())
                    desc_bg = pygame.Surface((max_width + 20, total_height))
                    desc_bg.fill((50, 50, 50))
                    desc_bg.blit(name_text, (10, 10))
                    
                    y_offset = name_text.get_height() + 15
                    for text in desc_texts:
                        desc_bg.blit(text, (10, y_offset))
                        y_offset += text.get_height()
                else:
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
            self.run.handle_deck_view(events, mouse_pos)
            self.run.potion_events(mouse_pos, events)
            exit = self.run.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                self.close = True
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.confirm_rect.collidepoint(mouse_pos):
                        self.close = True
                        break

                    if deck_hovering:
                        self.run.player.view_deck()
                    
                    for ware in self.wares.values():
                        if ware and ware[0]:
                            if ware[0] != 'Remove':
                                if ware[0].rect.collidepoint(mouse_pos):
                                    if ware[1] <= self.run.player.gold:
                                        self.run.gold_modification(-ware[1])
                                        self.break_piggy_bank()
                                        item = ware[0]
                                        ware[0] = None
                                        if isinstance(item, card_constructor.Card):
                                            self.run.card_pickup(item)
                                        elif isinstance(item, potion_data.Potion):
                                            self.run.potion_pickup(item)
                                        elif isinstance(item, relic_data.Relics):
                                            self.run.relic_pickup(item)
                                            if item.name == 'Costco\'s Membership Card':
                                                for ware in self.wares.values():
                                                    if ware and ware[0]:
                                                        ware[1] = int(ware[1] * 0.5)
                                                self.discounted = True
                    
                    if self.removal_rect.collidepoint(mouse_pos) and self.wares[13] and self.wares[13][0]:
                        if self.run.player.deck and self.run.player.gold >= self.wares[13][1]:
                            effects.card_select(1, {}, self.run)
                            self.run.player.remove_card()
                            self.run.removals += 1
                            self.run.gold_modification(-self.wares[13][1])
                            self.wares[13] = [None, None]
                            self.break_piggy_bank()
        
        if exit == 'Main Menu':
            self.run.main_menu.main_menu()

    def break_piggy_bank(self):
        if self.run.player.relics:
            for relic in self.run.player.relics:
                if relic.name == 'Piggy Bank':
                    self.run.player.relics.remove(relic)
                    break
