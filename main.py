import random
import card_data
import card_constructor
import combat
import potion_data
import enemy_data
import relic_data
import events
import rest_site
import map_generation
import reward_screen
import events
import math
import shop
import chest
import json
import pygame
import os  
import sys

class MainMenu:
    def __init__(self):
        # Initialize pygame and set up display window
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900))
        self.clock = pygame.time.Clock()
        
        # Initialize game state variables
        self.player = None  # Will hold the player character
        self.run = None    # Will hold the current game run
        self.save_data = {} # Dictionary to store save data
        self.running = True
        
        # Initialize fonts and load menu background image
        pygame.font.init()
        self.main_menu_sprite = pygame.image.load(os.path.join("assets", "menu", "main_menu.png"))
        self.menu_option_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 30)
        self.title_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 70)
        
        # Define menu options and track selected option
        self.menu_options = ['New Game', 'Load Game', 'Exit']
        self.menu_option_selected = 0
    
    def main_menu(self): 
        # Check if a save file exists and has content
        existing_save = False
        with open('assets/saves/save_data.txt', 'r') as file:
            save_content = file.read()
            if save_content and save_content.strip() != '{}':
                existing_save = True
                
        running = True
        while running:
            # Clear screen and draw background
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_menu_sprite, (0, 0))
            
            # Draw game title with outline effect
            title_outline = self.title_font.render("The Descent", True, (0, 0, 0))
            title_text = self.title_font.render("The Descent", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(800, 200))
            
            # Draw outline by offsetting text in 4 directions
            self.screen.blit(title_outline, (title_rect.x - 2, title_rect.y))
            self.screen.blit(title_outline, (title_rect.x + 2, title_rect.y))
            self.screen.blit(title_outline, (title_rect.x, title_rect.y - 2))
            self.screen.blit(title_outline, (title_rect.x, title_rect.y + 2))
            self.screen.blit(title_text, title_rect)
            
            # Draw menu options with outline effect
            for i, option in enumerate(self.menu_options):
                # Skip "Load Game" option if no save exists
                if option == 'Load Game' and not existing_save:
                    continue
                    
                outline = self.menu_option_font.render(option, True, (0, 0, 0))
                text = self.menu_option_font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(800, 400 + i * 80))
                
                # Draw outline by offsetting text in 4 directions
                self.screen.blit(outline, (text_rect.x - 2, text_rect.y))
                self.screen.blit(outline, (text_rect.x + 2, text_rect.y))
                self.screen.blit(outline, (text_rect.x, text_rect.y - 2))
                self.screen.blit(outline, (text_rect.x, text_rect.y + 2))
                self.screen.blit(text, text_rect)
                
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if any menu option was clicked
                    for i, option in enumerate(self.menu_options):
                        text_rect = self.menu_option_font.render(option, True, (255,255,255)).get_rect(center=(800, 400 + i * 80))
                        if text_rect.collidepoint(mouse_pos):
                            if i == 0:  # New Game
                                self.new_game()
                            elif i == 1 and existing_save:  # Load Game
                                self.load_save_data()
                            elif i == 2:  # Exit
                                self.exit()
    
    def new_game(self):
        # Create new player character and start a new run
        self.player = Character('Wandering Samerai', 80, 1)
        self.run = Run(self, self.screen, self.player)
        self.run.runStart()

    def load_save_data(self):
        # Load save data from file
        with open('assets/saves/save_data.txt', 'r') as file:
            self.save_data = json.load(file)
            
        # Reconstruct path data from save file
        reconstructed_path = {}
        for key, value in self.save_data['path'].items():
            floor, room = key.split(',')
            connections = []
            for conn in value:
                conn_floor, conn_room = conn.split(',')
                connections.append((int(conn_floor), int(conn_room)))
            reconstructed_path[int(floor), int(room)] = connections
        self.save_data['path'] = reconstructed_path
        player = Character(self.save_data['player name'], self.save_data['player maxHp'], self.save_data['player class'], False, self.save_data['player deck'], self.save_data['player potions'], self.save_data['player relics'], self.save_data['player hp'], self.save_data['player gold'])
        self.player = player
        
        # Reconstruct map info from save data
        map_info = self.save_data['map'], self.save_data['path'], self.save_data['mapDisplay'], self.save_data['entered_rooms']
        run = Run(self, self.screen, self.player, False, False, self.save_data['ascension'], map_info, self.save_data['act'], self.save_data['act_name'], self.save_data['room'], self.save_data['roomInfo'], self.save_data['combats_finished'], self.save_data['easyPool'], self.save_data['normalPool'], self.save_data['elitePool'], self.save_data['boss'], self.save_data['eventList'], self.save_data['rareChanceMult'], self.save_data['rareChanceOffset'], self.save_data['potionChance'], self.save_data['cardRewardOptions'], self.save_data['removals'], self.save_data['encounterChance'], self.save_data['mechanics'], self.save_data['campfire'], self.save_data['eggs'])
        self.run = run
        self.run.runStart()
    
    def exit(self):
        # Clean up pygame and exit program
        pygame.quit()
        sys.exit()

class Character:
    def __init__(self, name, maxHp, character_class, new_character = True, deck = [], potions = [], relics = [], current_hp = None, gold = 100):
        self.name = name
        self.maxHp = maxHp
        self.hp = maxHp
        self.character_class = character_class
        self.block = 0
        self.deck = []
        self.hp = maxHp
        self.gold = 100
        self.thieved = 0
        self.potions = [None, None, None]
        self.relics = []
        self.x = 0
        self.y = 0
        if new_character:
            # Create a new character with default deck and starter relics
            if character_class == 1:
                for i in range(5):
                    self.deck.append(card_constructor.create_card(1000, card_data.card_info[1000]))
            for i in range(5):
                self.deck.append(card_constructor.create_card(1002, card_data.card_info[1002]))
            self.deck.append(card_constructor.create_card(1001, card_data.card_info[1001]))
            self.relics.append(relic_data.createRelic('Purple Blood', relic_data.starterRelics['Purple Blood']))
        else:
            # Load existing character with saved deck, potions, and relics
            self.maxHp = maxHp
            self.gold = gold
            self.hp = current_hp
            for card in deck:
                self.deck.append(card_constructor.create_card(card, card_data.card_info[card]))
            for j, potion in enumerate(potions):
                if potion is not None:
                    self.potions[j] = potion_data.createPotion(potion, potion_data.potions[potion])
            for relic in relics:
                if relic in relic_data.commonRelics:
                    self.relics.append(relic_data.createRelic(relic, relic_data.commonRelics[relic]))
                elif relic in relic_data.rareRelics:
                    self.relics.append(relic_data.createRelic(relic, relic_data.rareRelics[relic]))
                elif relic in relic_data.UncommonRelics:
                    self.relics.append(relic_data.createRelic(relic, relic_data.UncommonRelics[relic]))
                elif relic in relic_data.shopRelics:
                    self.relics.append(relic_data.createRelic(relic, relic_data.shopRelics[relic]))
                elif relic in relic_data.bossRelics:
                    self.relics.append(relic_data.createRelic(relic, relic_data.bossRelics[relic]))
                elif relic in relic_data.eventRelics:
                    self.relics.append(relic_data.createRelic(relic, relic_data.eventRelics[relic]))
                elif relic in relic_data.starterRelics:
                    self.relics.append(relic_data.createRelic(relic, relic_data.starterRelics[relic]))
        sprite = pygame.image.load('assets/sprites/characters/swordsman.png')
        # Scale down the character sprite
        self.sprite = pygame.transform.scale(sprite, (sprite.get_width() // 2.75, sprite.get_height() // 2.75))
        self.rect = self.sprite.get_rect()
        self.selected_cards = []
        self.buffs = {'Strength': 0, 'Dexterity': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Double Tap': 0, 'Duplicate': 0, 'Draw Card': 0, 'Energized': 0, 'Next Turn Block': 0, 'Parry': 0, 'Deflect': 0, 'Intangible': 0}
        #Debuffs: Atrophy = lose dex at the end of turn
        self.debuffs = {'Vulnerable': 0, 'Weak': 0, 'Frail': 0, '-Strength': 0, '-Dexterity': 0, 'Atrophy': 0, 'Chained': 0, 'Poison': 0, 'No Draw': 0, 'Chaotic': 0, 'Last Chance': 0, 'Draw Reduction': 0, 'Entangle': 0}
        # Load buff and debuff icons
        self.attack_buff_sprite = pygame.image.load(os.path.join("assets", "icons", "attack_buff.png"))
        self.defense_buff_sprite = pygame.image.load(os.path.join("assets", "icons", "defense_buff.png"))
        self.misc_buff_sprite = pygame.image.load(os.path.join("assets", "icons", "misc_buff.png"))
        self.vulnerable_sprite = pygame.image.load(os.path.join("assets", "icons", "vulnerable.png"))
        self.weak_sprite = pygame.image.load(os.path.join("assets", "icons", "weak.png"))
        self.frail_sprite = pygame.image.load(os.path.join("assets", "icons", "frail.png"))
        self.debuff_sprite = pygame.image.load(os.path.join("assets", "icons", "debuff.png"))
        # Load block overlay and hp bar
        self.block_overlay_sprite = pygame.image.load(os.path.join("assets", "ui", "hp_bar", "block_overlay.png"))
        hp_bar_path = os.path.join("assets", "ui", "hp_bar", f"hp_bar_8_8.png")
        self.hp_bar_sprite = pygame.image.load(hp_bar_path)
        self.top_ui_sprite = pygame.image.load(os.path.join("assets", "ui", "ui_bar.png"))
        heart_sprite = pygame.image.load(os.path.join("assets", "icons", "hp.png"))
        gold_sprite = pygame.image.load(os.path.join("assets", "icons", "gold.png"))
        # Scale down heart and gold icons
        self.heart_sprite = pygame.transform.scale(heart_sprite, (heart_sprite.get_width()//2, heart_sprite.get_height()//2))
        self.gold_sprite = pygame.transform.scale(gold_sprite, (gold_sprite.get_width()//11, gold_sprite.get_height()//11))
        self.empty_potion_sprite = pygame.image.load(os.path.join("assets", "icons", "empty_potion_slot .png"))
        self.deck_button_sprite = pygame.image.load(os.path.join("assets", "icons", "pile_icon.png"))
        # Scale down deck button sprite
        self.deck_button_sprite = pygame.transform.scale(self.deck_button_sprite, (self.deck_button_sprite.get_width()//10, self.deck_button_sprite.get_height()//10))
        self.deck_button_rect = self.deck_button_sprite.get_rect()
        self.deck_button_hover = False
        # Pre-load fonts
        pygame.font.init()
        self.block_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 20)
        self.hp_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 24)
        # Pre-render block text surfaces
        self.block_text_surfaces = {}
        for i in range(1000):  # Pre-render numbers 0-999
            outline = self.block_font.render(str(i), True, (0, 0, 0))
            text = self.block_font.render(str(i), True, (255, 255, 255))
            self.block_text_surfaces[i] = (outline, text)
        self.buff_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 12)
        self.debuff_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 12)
        self.is_hover = False
        self.name_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 24)
        self.description_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 20)
    
    def hover(self):
        self.is_hover = True
    
    def unhover(self):
        self.is_hover = False

    def __str__(self):
        '''Override for String representation'''
        return f'{self.name}   HP: {self.hp}/{self.maxHp}   Block: {self.block}   Gold: {self.gold}   Potions: {self.potions}   Relics: {self.relics}'

    def __repr__(self):
        return self.__str__()

    def draw(self, surface, x = 0, y = 0):
        '''Method for drawing the character and health bar'''
        # Draw character sprite
        surface.blit(self.sprite, (x, y))
        
        # Update collision box position to match sprite position
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        # Scale up the health bar
        scaled_width = int(self.hp_bar_sprite.get_width() * 2.25)  
        scaled_height = int(self.hp_bar_sprite.get_height() * 2.25) 
        hp_bar = pygame.transform.scale(self.hp_bar_sprite, (scaled_width, scaled_height))
        
        # Position health bar below character, shifted left by 20 pixels
        bar_x = x + self.sprite.get_width()//2 - hp_bar.get_width()//2 - 20
        bar_y = y + self.sprite.get_height() + 10  # Moved below sprite with small gap
        surface.blit(hp_bar, (bar_x, bar_y))
        
        # Draw block overlay if character has block
        if self.block > 0:
            # Scale block overlay to match health bar size
            block_overlay = pygame.transform.scale(self.block_overlay_sprite, (scaled_width, scaled_height))
            surface.blit(block_overlay, (bar_x, bar_y))
            
            # Use pre-rendered block text surfaces
            block_outline, block_text = self.block_text_surfaces.get(self.block, 
                (self.block_font.render(str(self.block), True, (0, 0, 0)),
                self.block_font.render(str(self.block), True, (255, 255, 255))))
            
            text_x = bar_x + (scaled_width - block_outline.get_width()) // 2 - 63
            text_y = bar_y + (scaled_height - block_outline.get_height()) // 2
            
            # Draw black outline
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (1,-1), (-1,1), (1,1)]:
                surface.blit(block_outline, (text_x + dx, text_y + dy))
            
            # Draw white text
            surface.blit(block_text, (text_x, text_y))
        
        # Draw HP text overlapping the hp bar
        hp_text = f"{self.hp}/{self.maxHp}"
        hp_outline = self.hp_font.render(hp_text, True, (0, 0, 0))
        text_x = bar_x + (scaled_width - hp_outline.get_width()) // 2 + 17
        text_y = bar_y + (scaled_height - hp_outline.get_height()) // 2
        
        # Draw black outline in all 8 directions
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (1,-1), (-1,1), (1,1)]:
            surface.blit(hp_outline, (text_x + dx, text_y + dy))
            
        # Draw white HP text
        hp_text = self.hp_font.render(hp_text, True, (255, 255, 255))
        surface.blit(hp_text, (text_x, text_y))

        # Draw buffs and debuffs below character
        status_x = x  # Start from character's left edge
        status_y = bar_y + scaled_height + 10  # Position below health bar
        
        # Draw buffs
        for buff, amount in self.buffs.items():
            if amount > 0:
                # Choose correct buff sprite
                if buff == 'Strength' or buff == 'Vigour' or buff == 'Double Tap':
                    sprite = self.attack_buff_sprite
                elif buff == 'Dexterity' or buff == 'Plated Armour' or buff == 'Metalicize' or buff == 'Blur' or buff == 'Thorns' or buff == 'Regen' or buff == 'Artifact' or buff == 'Parry' or buff == 'Deflect':
                    sprite = self.defense_buff_sprite
                else:
                    sprite = self.misc_buff_sprite
                
                # Draw buff sprite
                surface.blit(sprite, (status_x, status_y))
                
                # Draw amount number in bottom right
                amount_text = self.buff_font.render(str(amount), True, (255, 255, 255))
                amount_x = status_x + sprite.get_width() - amount_text.get_width()
                amount_y = status_y + sprite.get_height() - amount_text.get_height()
                surface.blit(amount_text, (amount_x, amount_y))
                
                # If hovering over character, draw buff description box
                
                
                status_x += sprite.get_width() + 5  # Shift right for next icon

        if self.is_hover:
            # Combine active buffs and debuffs into one list
            active_effects = []
            active_effects.extend([(buff, amount, True) for buff, amount in self.buffs.items() if amount > 0])
            active_effects.extend([(debuff, amount, False) for debuff, amount in self.debuffs.items() if amount > 0])
            
            box_width = 300
            line_height = 25
            spacing = 20  # Space between boxes
            effects_per_column = 3
            previous_box_heights = []
            
            for i, (effect, amount, is_buff) in enumerate(active_effects):
                # Get effect description
                desc = self.get_buff_description(effect) if is_buff else self.get_debuff_description(effect)
                
                # Split description into 35 char lines
                desc_lines = []
                while len(desc) > 35:
                    split_index = desc.rfind(' ', 0, 35)
                    if split_index == -1:
                        split_index = 35
                    desc_lines.append(desc[:split_index])
                    desc = desc[split_index:].strip()
                desc_lines.append(desc)
                
                # Get correct sprite based on effect type
                if is_buff:
                    if effect == 'Strength' or effect == 'Vigour' or effect == 'Double Tap':
                        sprite = self.attack_buff_sprite
                    elif effect == 'Dexterity' or effect == 'Plated Armour' or effect == 'Metalicize' or effect == 'Blur' or effect == 'Thorns' or effect == 'Regen' or effect == 'Artifact' or effect == 'Parry' or effect == 'Deflect':
                        sprite = self.defense_buff_sprite
                    else:
                        sprite = self.misc_buff_sprite
                else:
                    if effect == 'Vulnerable':
                        sprite = self.vulnerable_sprite
                    elif effect == 'Weak':
                        sprite = self.weak_sprite
                    elif effect == 'Frail':
                        sprite = self.frail_sprite
                    elif effect == '-Strength':
                        sprite = self.attack_buff_sprite
                    elif effect == '-Dexterity':
                        sprite = self.defense_buff_sprite
                    else:
                        sprite = self.debuff_sprite

                # Calculate box dimensions
                box_height = (len(desc_lines) + 1) * line_height + 15
                previous_box_heights.append(box_height)
                
                # Calculate column and row position
                column = i // effects_per_column
                row = i % effects_per_column
                
                # Position box in grid layout, lowered by 50 pixels
                # Start at base x position (x)
                # Add smaller offset from left edge (50px instead of 100px)
                # For each column, add box_width + smaller spacing to position boxes horizontally
                box_x = x + 150 + (box_width + 10) * column  # Reduced left offset and column spacing
                # Calculate y position based on row number
                if row == 0:
                    box_y = y
                elif row == 1:
                    box_y = y + previous_box_heights[i-1]
                else:
                    box_y = y + previous_box_heights[i-2] + previous_box_heights[i-1]
                
                # Draw semi-transparent black background
                desc_box = pygame.Surface((box_width, box_height))
                desc_box.fill((0, 0, 0))
                surface.blit(desc_box, (box_x, box_y))
                
                # Draw effect name and icon
                name_text = self.name_font.render(effect, True, (255, 255, 255))
                surface.blit(sprite, (box_x + 5, box_y + 5))
                surface.blit(name_text, (box_x + sprite.get_width() + 10, box_y + 5))
                
                # Draw description lines
                for j, line in enumerate(desc_lines):
                    desc_text = self.description_font.render(line, True, (255, 255, 255))
                    surface.blit(desc_text, (box_x + 5, box_y + (j + 1) * line_height + 10))

        # Draw debuffs
        for debuff, amount in self.debuffs.items():
            text_colour = (255, 255, 255)
            if amount > 0:
                # Choose correct debuff sprite
                if debuff == 'Vulnerable':
                    sprite = self.vulnerable_sprite
                elif debuff == 'Weak':
                    sprite = self.weak_sprite
                elif debuff == 'Frail':
                    sprite = self.frail_sprite
                elif debuff == '-Strength':
                    sprite = self.attack_buff_sprite
                    text_colour = (255, 0, 0)
                elif debuff == '-Dexterity':
                    sprite = self.defense_buff_sprite
                    text_colour = (255, 0, 0)
                else:
                    sprite = self.debuff_sprite
                    
                # Draw debuff sprite
                surface.blit(sprite, (status_x, status_y))
                
                # Draw amount number in bottom right with black outline
                outline_text = self.debuff_font.render(str(amount), True, (0, 0, 0))
                amount_text = self.debuff_font.render(str(amount), True, text_colour)
                amount_x = status_x + sprite.get_width() - amount_text.get_width()
                amount_y = status_y + sprite.get_height() - amount_text.get_height()
                # Draw outline slightly offset in each direction
                surface.blit(outline_text, (amount_x - 1, amount_y - 1))
                surface.blit(outline_text, (amount_x + 1, amount_y - 1))
                surface.blit(outline_text, (amount_x - 1, amount_y + 1))
                surface.blit(outline_text, (amount_x + 1, amount_y + 1))
                # Draw main text
                surface.blit(amount_text, (amount_x, amount_y))
                
                status_x += sprite.get_width() + 5  # Shift right for next icon

    def get_buff_description(self, buff):
        desc = {
            'Strength': f'Increases attack damage by {self.buffs["Strength"]}. ',
            'Dexterity': f'Increases block gain from cards by {self.buffs["Dexterity"]}. ',
            'Vigour': f'Increases next attack damage by {self.buffs["Vigour"]}. ',
            'Ritual': f'At the start of your turn, gain {self.buffs["Ritual"]} Strength. ',
            'Plated Armour': f'At the end of your turn, gain {self.buffs["Plated Armour"]} Block, when you take unblocked attack damage, lose 1 Plated Armour. ',
            'Metalicize': f'At the end of your turn, gain {self.buffs["Metalicize"]} Block. ',
            'Blur': f'For the next {self.buffs["Blur"]} turns, retain all block. ',
            'Thorns': f'When you take unblocked attack damage, deal {self.buffs["Thorns"]} damage to the attacker. ',
            'Regen': f'At the start of your turn, heal {self.buffs["Regen"]} HP. ',
            'Artifact': f'Negate the next {self.buffs["Artifact"]} debuffs. ',
            'Double Tap': f'Your next {self.buffs["Double Tap"]} attack is played twice. ',
            'Duplicate': f'Your next {self.buffs["Duplicate"]} card is played twice. ',
            'Draw Card': f'At the start of your turn, draw {self.buffs["Draw Card"]} cards. ',
            'Energized': f'At the start of your turn, gain {self.buffs["Energized"]} energy. ',
            'Next Turn Block': f'At the start of your next turn, gain {self.buffs["Next Turn Block"]} Block. ',
            'Parry': f'When you take unblocked attack damage, Apply {self.buffs["Parry"]} Vulnerable to the attacker. ',
            'Deflect': f'When you take unblocked attack damage, deal {self.buffs["Deflect"]} damage to the attacker. ',
            'Intangible': f'All HP loss and attack damage is reduced to 1. ',
        }
        return desc[buff]

    def get_debuff_description(self, debuff):
        desc = {
            'Vulnerable': f'Take 50% more attack damage. ',
            'Weak': f'Deal 25% less attack damage. ',
            'Frail': f'Gain 25% less block from cards. ',
            '-Strength': f'Deal {self.debuffs["-Strength"]} less attack damage. ',
            '-Dexterity': f'Gain {self.debuffs["-Dexterity"]} less block from cards. ',
            'Atrophy': f'Lose {self.debuffs["Atrophy"]} Dexterity at the end of your turn. ',
            'Chained': f'Lose {self.debuffs["Chained"]} Strength at the end of your turn. ',
            'Poison': f'Lose {self.debuffs["Poison"]} HP at the start of your turn. ',
            'No Draw': f'You can no longer draw cards until the end of your turn. ',
            'Chaotic': f'Randomize the cost of all cards you draw. ',
            'Last Chance': f'At the end of your turn, Exhaust EVERY card in combat. ',
            'Draw Reduction': f'At the start of your turn, draw {self.debuffs["No Draw"]} less cards.  ',
            'Entangle': f'You cannot play any attack cards for the next {self.debuffs["Entangle"]} turns. ',
        }
        return desc[debuff]

    def update_relics(self):
        mouse_pos = pygame.mouse.get_pos()
        for relic in self.relics:
            if relic.rect.collidepoint(mouse_pos):
                relic.hover()
            else:
                relic.unhover()

    def draw_ui(self, surface):
        self.update_relics()
        # Draw the UI bar background
        ui_y = 0  # Place at top of screen
        surface.blit(self.top_ui_sprite, (0, ui_y))
        
        # Draw character name
        font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 36)
        name_text = font.render(self.name, True, (255, 255, 255))
        surface.blit(name_text, (20, ui_y + 15))
        
        # Draw heart icon and HP
        surface.blit(self.heart_sprite, (350, ui_y + 15))
        # Draw black outline for HP text
        hp_outline = font.render(f"{self.hp}/{self.maxHp}", True, (0, 0, 0))
        surface.blit(hp_outline, (428, ui_y + 13))
        surface.blit(hp_outline, (432, ui_y + 13))
        surface.blit(hp_outline, (430, ui_y + 11))
        surface.blit(hp_outline, (430, ui_y + 15))
        surface.blit(hp_outline, (429, ui_y + 14))
        surface.blit(hp_outline, (431, ui_y + 14))
        surface.blit(hp_outline, (430, ui_y + 13))
        surface.blit(hp_outline, (430, ui_y + 15))
        # Draw red HP text
        hp_text = font.render(f"{self.hp}/{self.maxHp}", True, (255, 0, 0))
        surface.blit(hp_text, (430, ui_y + 15))
        
        # Draw gold icon and amount
        surface.blit(self.gold_sprite, (600, ui_y + 15))
        # Draw black outline for gold text
        gold_outline = font.render(str(self.gold), True, (0, 0, 0))
        surface.blit(gold_outline, (668, ui_y + 13))
        surface.blit(gold_outline, (672, ui_y + 13))
        surface.blit(gold_outline, (670, ui_y + 11))
        surface.blit(gold_outline, (670, ui_y + 15))
        surface.blit(gold_outline, (669, ui_y + 14))
        surface.blit(gold_outline, (671, ui_y + 14))
        surface.blit(gold_outline, (670, ui_y + 13))
        surface.blit(gold_outline, (670, ui_y + 15))
        # Draw gold text
        gold_text = font.render(str(self.gold), True, (255, 215, 0))
        surface.blit(gold_text, (670, ui_y + 15))
        
        # Draw potion slots
        potion_x = 800
        for potion in self.potions:
            if potion is None:
                surface.blit(self.empty_potion_sprite, (potion_x, ui_y + 25))
            else:
                potion.draw(surface, potion_x, ui_y + 25)
            potion_x += 60
        
        # Draw deck button
        deck_button_x = surface.get_width() - 100 - self.deck_button_sprite.get_width()  # 100 pixels from right edge
        deck_button_y = ui_y + 15  # Align with other UI elements
        surface.blit(self.deck_button_sprite, (deck_button_x, deck_button_y))

        # Create collision box for deck button
        self.deck_button_rect = pygame.Rect(deck_button_x, deck_button_y,self.deck_button_sprite.get_width(), self.deck_button_sprite.get_height())

        # Draw relics
        relic_x = 20  # Start 20 pixels from left edge
        relic_y = ui_y + 80  # Position below UI bar
        for relic in self.relics:
            relic.draw(surface, relic_x, relic_y)
            relic_x += 60  # Shift right 60 pixels for next relic
        
        if self.deck_button_hover:
            deck_text_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 16)
            # Create background surface
            deck_text = deck_text_font.render("View Deck", True, (255, 255, 255))
            bg_surface = pygame.Surface((deck_text.get_width() + 10, deck_text.get_height() + 6))
            bg_surface.fill((0, 0, 0))
            text_x = self.deck_button_rect.centerx - deck_text.get_width() // 2
            text_y = self.deck_button_rect.bottom + 35  # Changed from +10 to +30
            surface.blit(bg_surface, (text_x - 5, text_y - 3))
            surface.blit(deck_text, (text_x, text_y))

    def draw_collision_box(self, surface):
        # Load and transform target corner sprite
        target_corner = pygame.image.load(os.path.join("assets", "ui", "target_corners.png"))
        
        # Get sprite rect and position
        sprite_rect = self.sprite.get_rect()
        sprite_rect.x = self.x
        sprite_rect.y = self.y
        self.rect = sprite_rect
        
        # Draw corners at each corner of the rectangle
        # Top left - no rotation needed
        surface.blit(target_corner, (sprite_rect.left, sprite_rect.top))
        
        # Top right - rotate 90 degrees clockwise
        rotated = pygame.transform.rotate(target_corner, -90)
        surface.blit(rotated, (sprite_rect.right - rotated.get_width(), sprite_rect.top))
        
        # Bottom right - rotate 180 degrees
        rotated = pygame.transform.rotate(target_corner, -180)
        surface.blit(rotated, (sprite_rect.right - rotated.get_width(), sprite_rect.bottom - rotated.get_height() + 10))
        
        # Bottom left - rotate 270 degrees clockwise
        rotated = pygame.transform.rotate(target_corner, -270)
        surface.blit(rotated, (sprite_rect.left, sprite_rect.bottom - rotated.get_height() + 10))

    def view_deck(self):
        '''Method for viewing a pile of cards

        ### args:
            pile (list): The pile of cards to view
        '''
        pile = combat.Pile(self.deck, 'Deck')
        card_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
        card_surface.fill((0, 0, 0, 0))  # Completely transparent background
        confirm_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
        confirm_button = pygame.Rect(1600 - confirm_sprite.get_width(), 520, confirm_sprite.get_width(), confirm_sprite.get_height())
        viewing = True
        while viewing:
            card_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
            card_surface.fill((0, 0, 0, 0))  # Completely transparent background
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if confirm_button.collidepoint(mouse_pos):
                        viewing = False
                        break
            
            pile.draw(card_surface, events)
            card_surface.blit(confirm_sprite, confirm_button)
            background = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
            background.fill((50, 50, 50))  # Semi-transparent dark gray
            pygame.display.get_surface().blit(background, (0, 0))
            pygame.display.get_surface().blit(card_surface, (0, 0))
            pygame.display.flip()

    def combat_info(self):
        buffs = []
        for buff, amount in self.buffs.items():
            if amount > 0:
                buffs.append(f'{buff}: {amount}')
        buffs = str(', '.join(buffs))
        debuffs = []
        for debuff, amount in self.debuffs.items():
            if amount > 0:
                debuffs.append(f'{debuff}: {amount}')
        debuffs = str(', '.join(debuffs))
        return self.__repr__() + f'   Buffs: {buffs}   Debuffs: {debuffs}'
    
    def upgrade_card(self, cards = 'Selected'):
        '''Method to upgrading cards
        
        ### args:
            cards: cards being upgraded'''
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            if isinstance(card, str):
                # If a random card of a type is being upgraded
                if card == 'Card':
                    # Random card
                    validUpgrades = False
                    for player_card in self.deck:
                        if player_card.id + 100 in card_data.card_info:
                            validUpgrades = True
                            break
                    # Check if there is a card that has an upgrade
                    while validUpgrades:
                        # If there is
                        upgrade = random.choice(self.deck)
                        # Randomly pick one
                        if upgrade.id + 100 in card_data.card_info:
                            upgraded_card = card_constructor.create_card(upgrade.id + 100, card_data.card_info[upgrade.id + 100])
                            upgraded_card.bottled = upgrade.bottled
                            self.deck.remove(upgrade)
                            self.deck.append(upgraded_card)
                            break
                elif card == 'Attack':
                    # Random Attack
                    validUpgrades = False
                    for player_card in self.deck:
                        if player_card.type == 0 and player_card.id + 100 in card_data.card_info:
                            validUpgrades = True
                            break
                    # Check if there is an attack card avalible to upgrade
                    while validUpgrades:
                        upgrade = random.choice(self.deck)
                        if upgrade.type == 0:
                            # Picks a random card and checks if its the right type
                            if upgrade.id + 100 in card_data.card_info:
                                upgraded_card = card_constructor.create_card(upgrade.id + 100, card_data.card_info[upgrade.id + 100])
                                upgraded_card.bottled = upgrade.bottled
                                self.deck.remove(upgrade)
                                self.deck.append(upgraded_card)
                                break
                elif card == 'Skill':
                    # Random Skill
                    validUpgrades = False
                    for player_card in self.deck:
                        if player_card.type == 1 and player_card.id + 100 in card_data.card_info:
                            validUpgrades = True
                            break
                    # Check if there is a valid skill to be upgraded
                    while validUpgrades:
                        upgrade = random.choice(self.deck)
                        if upgrade.type == 1:
                            if upgrade.id + 100 in card_data.card_info:
                                upgraded_card = card_constructor.create_card(upgrade.id + 100, card_data.card_info[upgrade.id + 100])
                                upgraded_card.bottled = upgrade.bottled
                                self.deck.remove(upgrade)
                                self.deck.append(upgraded_card)
                                break
                    # If there is a upgrade, random;y pick cards until a valid card is upgraded
                else:
                    raise TypeError(f'Unknown Card Type: {card}')
            else:
                if card.id + 100 in card_data.card_info:
                    upgraded_card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
                    upgraded_card.bottled = card.bottled
                    self.deck.remove(card)
                    self.deck.append(upgraded_card)
                else:
                    raise KeyError(f'Card has no upgrade: {card.name}')
                    # Invalid upgrade
    
    def transform_card(self, cards = 'Selected'):
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            # for every card that needs to be transformed
            if card.type == 4:
                # If the card is a curse
                transform_id = random.choice(card_constructor.weak_curse + card_constructor.medium_curse + card_constructor.strong_curse)
                card_new = card_constructor.create_card(transform_id, card_data.card_info[transform_id])
                self.deck.remove(card)
                self.deck.append(card_new)
                # Transform into a random non special curse
            else:
                if self.character_class == 1:
                    transform_id = random.choice(card_constructor.attack_card_1 + card_constructor.skill_card_1 + card_constructor.power_card_1)
                    card_new = card_constructor.create_card(transform_id, card_data.card_info[transform_id])
                    self.deck.remove(card)
                    self.deck.append(card_new)
                    # Tranfrom into a card of the character class
                else:
                    return TypeError(f'Unknown card transform: {card}')
    
    def transform_and_upgrade(self, cards = 'Selected'):
        new_cards = []
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            if self.character_class == 1:
                transform_id = random.choice(card_constructor.attack_card_1 + card_constructor.skill_card_1 + card_constructor.power_card_1)
                card_new = card_constructor.create_card(transform_id, card_data.card_info[transform_id])
                self.deck.remove(card)
                self.deck.append(card_new)
                new_cards.append(card_new)
                # Tranfrom into a card of the character class
        for card in new_cards:
            self.upgrade_card(card)


    def remove_card(self, cards = 'Selected'):
        '''Method for removing cards from the deck
        
        ### args:
            cards: the cards being removed, the selected cards by default'''
        if cards == 'Selected':
            cards = self.selected_cards
        for card in cards:
            self.deck.remove(card)

    def duplicate_card(self, card = 'Selected'):
        '''Method for removing cards from the deck
        
        ### args:
            cards: the cards being removed, the selected cards by default'''
        if card == 'Selected':
            card = self.selected_cards
        new_card = card_constructor.create_card(card.id, card_data.card_info[card.id])
        # Create a deep copy of the card being duplicated
        self.deck.append(new_card)
        # Add the copy to the deck

    def update_hp_bar(self):
        health_percent = self.hp / self.maxHp
        health_segment = 0
        if health_percent <= 0:
            health_segment = 0
        elif health_percent == 1:
            health_segment = 8
        elif health_percent <= 0.125:
            health_segment = 1
        elif health_percent <= 0.25:
            health_segment = 2
        elif health_percent <= 0.375:
            health_segment = 3
        elif health_percent <= 0.5:
            health_segment = 4
        elif health_percent <= 0.625:
            health_segment = 5
        elif health_percent <= 0.75:
            health_segment = 6
        else:
            health_segment = 7
        
        # Load health bar sprite
        self.hp_bar_sprite = pygame.image.load(os.path.join("assets", "ui", "hp_bar", f"hp_bar_{health_segment}_8.png"))

    def heal(self, amount):
        '''Method to heal the player by an amount or percentage
        
        ### args:
            amount: Int for a fixed value, string for percentage'''
        if isinstance(amount, str):
            # If its a string
            percentage = int(amount)
            percentage = percentage / 100
            healing_amount = math.floor(self.maxHp * percentage)
            if self.relics:
                for relic in self.relics:
                    healing_amount = relic.valueModificationEff('Healing', healing_amount)
            self.hp = min(self.maxHp, self.hp + healing_amount)
            # Add a percentage of of max hp to your own hp
        else:
            healing_amount = amount
            if self.relics:
                for relic in self.relics:
                    healing_amount = relic.valueModificationEff('Healing', healing_amount)
            self.hp = min(self.maxHp, self.hp + healing_amount)
            # Add fixed amount of hp up to max hp
            self.update_hp_bar()
    
    def increase_max_hp(self, amount):
        '''Method for increasing max hp from effects
        
        ### args:
            amount = Amount to increase by'''
        self.maxHp += amount
        self.hp += amount
        self.update_hp_bar()
        # Increase max hp by amount, when max hp is gained the equal amount of hp is gained

    def gain_block_card(self, amount):
        '''Getting block from playing cards
        
        ### args:
            amount: amount gained'''
        amount = amount + self.buffs['Dexterity']
        amount -= self.debuffs['-Dexterity']
        if self.debuffs['Frail'] > 0:
            amount = math.floor(amount * 0.75)
        amount = max(0, amount)
        self.block += amount 
        # add more block and adding the dexterity bonus
    
    def gain_block_power(self, amount):
        '''gaining block from powers or some other passive effects
        
        ### args: 
            amount: amount gained'''
        self.block += amount
        # Add more block
    
    def gain_buff(self, buff_type, amount):
        '''Method for gaining buffs
        
        ### args:
            buff_type: The type of buff being gained
            amount: amount being gained
        '''
        if buff_type not in {'Strength', 'Dexterity'}:
            # If its not Str or Dex
            self.buffs[buff_type] += amount
            # Just add the amount
        else:
            # If it is
            if self.debuffs['-' + buff_type] > 0:
                self.debuffs['-' + buff_type] -= amount
                if self.debuffs['-' + buff_type] < 0:
                    self.buffs[buff_type] = -self.debuffs['-' + buff_type]
                    self.debuffs['-' + buff_type] = 0
            else:
                self.buffs[buff_type] += amount
            # Accounts for negative Str or Dex when adding the buffs
        # Add amount to corresponding buff
    
    def lose_buff(self, buff_type, amount):
        '''Method for losing buffs
        
        ### args:
            buff_type: type of buff being lost
            amount: amount being lost
        '''
        if buff_type in {'-Strength', '-Dexterity'}:
            self.buffs[buff_type[1:]] -= amount
            if self.buffs['Strength'] < 0:
                self.debuffs['-Strength'] += self.buffs['Strength']
                self.buffs['Strength'] = 0
            if self.buffs['Dexterity'] < 0:
                self.debuffs['-Dexterity'] += self.buffs['Dexterity']
                self.buffs['Dexterity'] = 0
        else:
            self.buffs[buff_type] -= amount
    
    def gain_debuff(self, debuff_type, amount):
        '''Method for gaining debuffs
        
        ### args:
            buff_type: The type of debuff being gained
            amount: amount being gained
        '''
        if self.relics:
            for relic in self.relics:
                amount = relic.valueModificationEff(debuff_type, amount)
        if amount == 0:
            return None
        if self.buffs['Artifact'] > 0:
            # If player has artifact
            self.buffs['Artifact'] -= 1
            # Lose 1 artifact and negate the debuff
        elif debuff_type == "No Draw" or debuff_type == "Chaotic" or debuff_type == 'Last Chance':
            # If its non stackable
            self.debuffs[debuff_type] = 1
            # Make the debuff 1
        elif debuff_type in {'-Strength', '-Dexterity'}:
            # If its Str and Dex where the player can have positive values in buffs
            self.lose_buff(debuff_type[1:], amount)
            # use the lose buff method instead
        else:
            self.debuffs[debuff_type] += amount
            # Add the amount to debuff
    
    def lose_buff(self, buff_type, amount):
        '''Method for losing buffs
        
        ### args:
            buff_type: type of buff being lost
            amount: amount being lost
        '''
        self.buffs[buff_type] -= amount
        # Subtract the amount
        if self.buffs[buff_type] < 0:
            # if it goes below 0
            if '-' + buff_type in self.debuffs:
                # check if can be negative
                self.debuffs['-' + buff_type] = -self.buffs[buff_type]
                # Apply the negative debuff
            self.buffs[buff_type] = 0
            # Set amount of buffs to 0

    def hp_loss(self, amount):
        for relic in self.relics:
            amount = relic.valueModificationEff('HpLoss', amount)
        if self.buffs['Intangible'] > 0:
            amount = 1
        self.hp -= amount
        if amount > 0:
            if self.died == True:
                return 'GG' # Placeholder
            return True
        else:
            return False
    
    def hp_recovery(self, amount):
        self.hp = min(self.hp + amount, self.maxHp)

    def damage_taken(self, damage):
        '''
        Handles damage taken by the character, applying block reduction and relic effects.
        '''
        damage = damage
        # Applies relic effects that reduce damage taken
        for relic in self.relics:
            damage = relic.valueModificationEff('damageTaken', damage)
        if self.buffs['Intangible'] > 0:
            damage = 1
        self.block -= damage
        if self.block >= 0:
            return 0
        else:
            if self.buffs['Plated Armour'] > 0:
                self.buffs['Plated Armour'] -= 1
            # Remove 1 plated armour for taking damage
            damage = -self.block
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            return self.hp_loss(damage)
        
    def true_damage_taken(self, damage):
        '''
        Handles taking true damage that is uneffected by debuffs
        '''
        damage = damage
        self.block -= damage
        # Deal damage to block first
        if self.buffs['Intangible'] > 0:
            damage = 1
        if self.block < 0:
            # If block wasn't enough
            damage = -self.block
            # Update damage to only amount unblocked
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            # Update entity status
            self.hp_loss(damage)
            # Hp loss
    
    def died(self):
        if self.hp <= 0:
            for relic in self.relics:
                if relic.condition == 'dead' and relic.used == False:
                    self.hp = relic.valueModificationEff('dead', self.maxHp)
                    relic.used = True
                    return False
            return True
        else:
            return False
        
classes = {
    1: ('Wandering Samerai', 80, 1)
}

class Run:
    def __init__(self, main_menu: MainMenu, screen, player: Character, newRun = True, turtorial = True, ascsension = 0, map_info = None, act = 1, act_name = 'The Forest', room = [0, 0], roomInfo = None, combats_finished = 0, easyPool = [], normalPool = [], elitePool = [], boss = [], eventList = [], rareChanceMult = 1, rareChanceOffset = -5, potionChance = 40, cardRewardOptions = 3, removals = 0, encounterChance = {'Combat': 10, 'Treasure': 2, 'Shop': 3}, mechanics = {'Intent': True, 'Ordered_Draw_Pile': False, 'Turn_End_Discard': True, 'Playable_Curse': False, 'Playable_Status': False, 'Exhaust_Chance': 100, 'Cards_per_Turn': False, 'Random_Combat': True, 'Insect': False, 'Block_Loss': False, 'X_Bonus': 0, 'Necro': False}, campfire = {'Rest': True, 'Smith': True, 'Fertilize': False, 'Dig': False, 'Shred': False}, eggs = []):
        self.player = player
        self.main_menu = main_menu
        pygame.init()
        self.starting_blessing_background_spirte = pygame.image.load(os.path.join("assets", "ui", "forest.png"))
        self.screen = screen
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        pygame.display.set_caption("The Descent")
        self.combat_deck = None
        if map_info != None:
            self.map = map_generation.Map(ascsension, map_info)
            self.entered_rooms = map_info[3]
        else:
            self.map = map_generation.Map(ascsension)
        self.act = act
        self.act_name = act_name
        self.ascsension = ascsension
        self.room = room
        self.roomInfo = roomInfo
        self.combats_finished = combats_finished
        self.newRun = newRun
        self.turtorial = turtorial
        self.encounterChance = encounterChance
        self.mechanics = mechanics
        self.campfire = campfire
        self.entered_rooms = []
        if not self.newRun:
            self.easyPool = easyPool
            self.normalPool = normalPool
            self.elitePool = elitePool
            self.boss = boss
            self.eventList = eventList
            # self.shrineList = shrineList
        else:
            self.easyPool = enemy_data.act_1_easy_pool()
            self.normalPool = enemy_data.act_1_normal_pool()
            self.elitePool = enemy_data.act_1_elite_pool()
            self.boss = enemy_data.act_1_boss_pool()
            events = self.generate_event_list()
            self.eventList = list(events)
            # ADDED EVENTS AND SHRINES
            # More to be added
        self.combat_pool_details = {}
        if self.act == 1:
            self.combat_pool_details = enemy_data.generate_act1_pools()
        self.rareChanceMult = rareChanceMult
        self.rareChanceOffset = rareChanceOffset
        self.potionChance = potionChance
        self.cardRewardOptions = cardRewardOptions
        self.event = None
        self.combat = None
        self.shop = None
        self.treasure = None
        self.reward = None
        self.removals = removals
        self.lastInstance = None
        self.confirm_button_sprite = pygame.image.load(os.path.join("assets", "ui", "confirm_button.png"))
        self.eggs = eggs
        self.rest_site = None
        self.instances = [self.shop, self.combat, self.event, self.treasure, self.reward, self.rest_site]
        self.save_data = {}
        self.active_room = None
        self.clicked_potion = None
    
    def save_date(self):
        self.save_data['player name'] = self.player.name
        self.save_data['player maxHp'] = self.player.maxHp
        self.save_data['player hp'] = self.player.hp
        self.save_data['player class'] = self.player.character_class
        self.save_data['player deck'] = []
        for card in self.player.deck:
            self.save_data['player deck'].append(card.id)
        self.save_data['player potions'] = []
        for potion in self.player.potions:
            if potion:
                self.save_data['player potions'].append(potion.name)
            else:
                self.save_data['player potions'].append(None)
        self.save_data['player relics'] = []
        for relic in self.player.relics:
            self.save_data['player relics'].append(relic.name)
        self.save_data['player gold'] = self.player.gold
        self.save_data['ascsension'] = self.ascsension
        self.save_data['map'] = self.map.map
        # Convert path dictionary with tuple keys to serializable format
        path_data = {}
        for (floor, room), destinations in self.map.path.items():
            # Convert tuple key to string representation
            key = f"{floor},{room}"
            # Convert destination tuples to list of strings
            dest_list = [f"{d_floor},{d_room}" for d_floor, d_room in destinations]
            path_data[key] = dest_list
        self.save_data['path'] = path_data
        self.save_data['mapDisplay'] = self.map.mapDisplay
        self.save_data['entered_rooms'] = self.entered_rooms
        self.save_data['act'] = self.act
        self.save_data['act_name'] = self.act_name
        self.save_data['room'] = self.room
        self.save_data['roomInfo'] = self.roomInfo
        self.save_data['combats_finished'] = self.combats_finished
        self.save_data['ascension'] = self.ascsension
        self.save_data['easyPool'] = self.easyPool
        self.save_data['normalPool'] = self.normalPool
        self.save_data['elitePool'] = self.elitePool
        self.save_data['boss'] = self.boss
        self.save_data['eventList'] = self.eventList
        # self.save_data['shrineList'] = self.shrineList
        self.save_data['rareChanceMult'] = self.rareChanceMult
        self.save_data['rareChanceOffset'] = self.rareChanceOffset
        self.save_data['potionChance'] = self.potionChance
        self.save_data['cardRewardOptions'] = self.cardRewardOptions
        self.save_data['removals'] = self.removals
        self.save_data['encounterChance'] = self.encounterChance
        self.save_data['mechanics'] = self.mechanics
        self.save_data['campfire'] = self.campfire
        self.save_data['eggs'] = self.eggs
    
    def handle_save_and_exit_input(self, events):
        # If the player clicks on the 75 x 75 pixel area in the top right corner of the screen, open the save and exit menu
        if pygame.Rect(1525, 0, 75, 75).collidepoint(pygame.mouse.get_pos()):
            for event in events:    
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pause_menu = True
                    while pause_menu:
                        self.screen.fill((0, 0, 0))
                        
                        # Create font
                        font = pygame.font.Font(None, 36)
                        
                        # Draw menu text
                        menu_text = font.render("Do you wish to save and quit?", True, (255, 255, 255))
                        menu_rect = menu_text.get_rect(center=(800, 400))
                        self.screen.blit(menu_text, menu_rect)
                        
                        # Draw yes/no buttons
                        yes_text = font.render("Yes", True, (255, 255, 255))
                        no_text = font.render("No", True, (255, 255, 255))
                        
                        yes_rect = pygame.Rect(650, 500, 100, 50)
                        no_rect = pygame.Rect(850, 500, 100, 50)
                        
                        pygame.draw.rect(self.screen, (100, 100, 100), yes_rect)
                        pygame.draw.rect(self.screen, (100, 100, 100), no_rect)
                        
                        yes_text_rect = yes_text.get_rect(center=yes_rect.center)
                        no_text_rect = no_text.get_rect(center=no_rect.center)
                        
                        self.screen.blit(yes_text, yes_text_rect)
                        self.screen.blit(no_text, no_text_rect)
                        
                        pygame.display.flip()
                        
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                mouse_pos = pygame.mouse.get_pos()
                                if yes_rect.collidepoint(mouse_pos):
                                    pause_menu = False
                                    return self.save_and_return_to_main_menu()
                                elif no_rect.collidepoint(mouse_pos):
                                    pause_menu = False
            
    def save_and_return_to_main_menu(self):
        return 'Main Menu'

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def runStart(self):
        if self.newRun == True:
            self.neowBlessing()
        else:
            self.mapNav()

    def neowBlessing(self):
        self.eventList = self.generate_event_list()
        blessing_active = True
        font = pygame.font.Font(None, 36)
        self.room = [0, 0]
        # Create option text surfaces
        option1_text = font.render("Gain 100 Gold", True, (255, 255, 255))
        option2_text = font.render("Transform 1 Card", True, (255, 255, 255))
        option3_text = font.render("Lose all gold, gain a random rare card", True, (255, 255, 255))
        option4_text = font.render("Replace starting relic with random boss relic", True, (255, 255, 255))
        
        # Create option rects
        option1_rect = pygame.Rect(600, 200, 400, 50)
        option2_rect = pygame.Rect(600, 300, 400, 50)
        option3_rect = pygame.Rect(600, 400, 400, 50)
        option4_rect = pygame.Rect(600, 500, 400, 50)
        
        # Create confirm button rect
        confirm_rect = self.confirm_button_sprite.get_rect()
        confirm_rect.bottomright = (1500, 800)
        
        selected_option = None
        
        exit = None

        while blessing_active:
            self.screen.blit(self.starting_blessing_background_spirte, (0, 0))
            
            # Draw options only if not selected
            if selected_option is None:
                # Wider option boxes
                option1_rect = pygame.Rect(400, 200, 800, 50)
                option2_rect = pygame.Rect(400, 300, 800, 50)
                option3_rect = pygame.Rect(400, 400, 800, 50)
                option4_rect = pygame.Rect(400, 500, 800, 50)
                
                pygame.draw.rect(self.screen, (100, 100, 100), option1_rect)
                pygame.draw.rect(self.screen, (100, 100, 100), option2_rect)
                pygame.draw.rect(self.screen, (100, 100, 100), option3_rect)
                pygame.draw.rect(self.screen, (100, 100, 100), option4_rect)
                
                self.screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 10))
                self.screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 10))
                self.screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 10))
                self.screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 10))
            
            # Draw player UI
            self.player.draw_ui(self.screen)
            
            # Only show confirm button if option selected
            if selected_option is not None:
                self.screen.blit(self.confirm_button_sprite, confirm_rect)
            
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle UI events
            self.potion_events(mouse_pos, events)
            self.handle_deck_view(events, mouse_pos)
            exit = self.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                blessing_active = False
                break
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    if selected_option is None:  # Only check options if none selected
                        if option1_rect.collidepoint(mouse_pos):
                            self.player.gold += 100
                            selected_option = 1
                        elif option2_rect.collidepoint(mouse_pos):
                            # Transform random card in deck
                            self.card_select(1, {})
                            self.player.transform_card()
                            selected_option = 2
                        elif option3_rect.collidepoint(mouse_pos):
                            self.player.gold = 0
                            # Add random rare card to deck
                            while True:
                                rare_card = card_constructor.random_card('card', self.player)
                                rare_card = card_constructor.create_card(rare_card, card_data.card_info[rare_card])
                                if rare_card.rarity == 3:
                                    self.player.deck.append(rare_card)
                                    break
                            selected_option = 3
                        elif option4_rect.collidepoint(mouse_pos):
                            # Replace starting relic with random boss relic
                            if len(self.player.relics) > 0:
                                self.player.relics.pop(0)
                                boss_relic_name = random.choice(list(relic_data.bossRelics.keys()))
                                boss_relic = relic_data.createRelic(boss_relic_name, relic_data.bossRelics[boss_relic_name])
                                self.relic_pickup(boss_relic)
                            selected_option = 4
                        
                    if confirm_rect.collidepoint(mouse_pos) and selected_option is not None:
                        blessing_active = False
            
            pygame.display.flip()
            
        if exit == 'Main Menu':
            self.main_menu.main_menu()
        else:
            self.mapNav()

    def handle_deck_view(self, events, mouse_pos):

        if self.player.deck_button_rect.collidepoint(mouse_pos):
            self.player.deck_button_hover = True
        else:
            self.player.deck_button_hover = False

        for event in events:
            if self.player.deck_button_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.player.deck_button_hover = False
                self.player.view_deck()

    def mapNav(self):
        """Display the map and handle room navigation"""
        exit = None
        map_active = True
        scroll_y = 0
        scroll_speed = 50
        max_scroll = -900  # Half of map height (1800/2) as defined in Map.draw()
        if self.room != [0, 0]:
            self.entered_rooms.append(self.room)
        self.save_date()
        self.upload_save_data()
        if self.room == [16, 4]:
            return self.victory()

        room_entered = None

        while map_active:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.handle_deck_view(events, mouse_pos)
            self.potion_events(mouse_pos, events)
            exit = self.handle_save_and_exit_input(events)
            if exit == 'Main Menu':
                map_active = False
                break
            

            # Clear screen and draw map# Clear screen and draw map
            self.screen.fill((255, 255, 255))
            self.map.y = scroll_y
            self.map.draw(self.screen, 0, scroll_y)
            
            
            # Highlight available rooms
            x_spacing = 100
            y_spacing = 100
            map_width = 6 * x_spacing
            start_x = (1600 - map_width) // 2
            
            for next_floor, next_room in self.map.path[(self.room[0], self.room[1])]:
                room_x = start_x + (next_room - 1) * x_spacing
                room_y = next_floor * y_spacing + scroll_y + 50
                pygame.draw.circle(self.screen, (255, 255, 0), (room_x + 22, room_y + 22), 25, 2)  # Yellow circle around available rooms

            # Draw player UI
            self.player.draw_ui(self.screen)

            for event in events:
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEWHEEL:
                    scroll_y = min(0, max(max_scroll, scroll_y + event.y * scroll_speed))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Adjust mouse position for scroll
                    
                    # Check available paths from current room
                    available_rooms = []
                    connections = self.map.path[(self.room[0], self.room[1])]
                    for room in self.map.rooms:
                        for connection in connections:
                            if room.floor == connection[0] and room.room_num == connection[1]:
                                available_rooms.append(room)

                    
                    # Calculate room positions using same logic as map drawing
                    x_spacing = 100
                    y_spacing = 100
                    map_width = 6 * x_spacing
                    start_x = (1600 - map_width) // 2

                    # Check if clicked on an available room
                    for room in available_rooms:
                        # Adjust mouse position for scrolling when checking collisions
                        scrolled_mouse_pos = (mouse_pos[0], mouse_pos[1] - scroll_y)
                        
                        if room.rect.collidepoint(scrolled_mouse_pos):
                            self.room = [room.floor, room.room_num]
                            room_type = room.room_type
                            room.entered = True
                            # Check room type and generate appropriate instance
                            if room_type == 1:
                                enemies = self.get_enemies()
                                self.generage_combat_instace(enemies, 'normal')
                                room_entered = 1
                                map_active = False
                                break
                            elif room_type == 2:
                                room_entered = 2
                                map_active = False
                                break
                            elif room_type == 3:
                                enemies = self.get_enemies('elite')
                                self.generage_combat_instace(enemies, 'Elite')
                                room_entered = 3
                                map_active = False
                                break
                            elif room_type == 4:
                                self.shop = shop.Shop(self)
                                room_entered = 4
                                map_active = False
                                break
                            elif room_type == 5:
                                self.treasure = chest.Treasure(self)
                                room_entered = 5
                                map_active = False
                                break
                            elif room_type == 6:
                                rest = rest_site.Campfire(self)
                                self.rest_site = rest
                                room_entered = 6
                                map_active = False
                                break
                            elif room_type == 7:
                                enemy = [enemy_data.AncientMech()]
                                self.generage_combat_instace(enemy, 'Boss')
                                room_entered = 7
                                map_active = False
                                break

            pygame.display.flip()
        
        # Handle exit condition
        if exit == 'Main Menu':
            self.main_menu.main_menu()

        # Handle room events
        self.eventMod('Room')
        if room_entered == 1:
            self.start_combat()
        elif room_entered == 2:
            self.unknown_location()
        elif room_entered == 3:
            self.start_combat()
        elif room_entered == 4:
            self.start_shop()
        elif room_entered == 5:
            self.start_treasure()
        elif room_entered == 6:
            self.eventMod('Campfire')
            self.start_campfire()
        elif room_entered == 7:
            self.eventMod('Boss Start')
            self.start_combat()
        
    def upload_save_data(self):
        '''Method to upload save data to file'''
        with open('assets/saves/save_data.txt', 'w') as file:
            json.dump(self.save_data, file)

    def discard_potion(self, potion):
        '''Method to discard a potion'''
        self.player.potions[self.player.potions.index(potion)] = None
        self.clicked_potion = None

    def generate_reward_screen_instance(self, reward_type, set_reward = False, additonal_rewards = {}):
        '''Method to generate a reward screen instance
        
        ### args:
            reward_type: the type of event that this reward screen correspond to, Ex: normal combat, events
            set_reward: predetermained loot, used for events and special occasions
            additional_rewards: additive rewards from certain effects'''
        if self.player.relics:
            '''Check if player has relics and apply additional rewards'''
            for relic in self.player.relics:
                '''Apply additional rewards from relics'''
                additonal_rewards = relic.additionalRewards(reward_type, additonal_rewards)
        self.reward = reward_screen.RewardScreen(self, self.player.character_class, self.rareChanceMult, self.rareChanceOffset, self.potionChance, self.cardRewardOptions, reward_type, set_reward, additonal_rewards)

    def potion_events(self, mouse_pos, events):
        if self.clicked_potion:
            '''Check if a potion is clicked and display use and discard options'''
            box_width = 100
            box_height = 40
            box_x = self.clicked_potion.rect.x + (self.clicked_potion.sprite.get_width() - box_width) // 2
            box_y = self.clicked_potion.rect.y + self.clicked_potion.sprite.get_height() + 10
            use_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            discard_rect = pygame.Rect(box_x, box_y + 45, 100, 40) 
            # Create use and discard rects
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if use_rect.collidepoint(mouse_pos):
                        if self.clicked_potion.time_of_use == 'all':
                            self.use_potion(self.clicked_potion)
                        else:
                            self.clicked_potion.unclick()
                            self.clicked_potion = None
                    elif discard_rect.collidepoint(mouse_pos):
                        self.discard_potion(self.clicked_potion)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    self.clicked_potion.unclick()
                    self.clicked_potion = None
        else:
            for potion in self.player.potions:
                if potion:
                    if potion.rect.collidepoint(mouse_pos): # Check if mouse is hovering over a potion
                        potion.hover() # Highlight the potion
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Check if mouse is clicked on a potion
                                potion.click() # Click the potion
                                self.clicked_potion = potion
                                potion.unhover()
                    else:
                        potion.unhover()

    def bonusEff(self, event):
        if self.player.relics:
            for relic in self.player.relics:
                # Go through all relics
                relic.eventBonus(event, self)
                # Execute condisional effects of relics

    def eventMod(self, event):
        '''Method to modify events based on relics'''
        if self.player.relics:
            for relic in self.player.relics:
                relic.eventModifcation(event, self)

    def card_reward_option_mod(self, mod):
        '''Method to increase or decrease the amount of cards avalible at card rewards'''
        self.cardRewardOptions += mod

    def campfire_restrict(self, action):
        '''Method to Disable an action at campfires'''
        self.campfire[action] = False

    def campfire_add_action(self, action):
        '''Method to add an action to a campfire'''
        self.campfire[action] = True

    def potion_chance_change(self, mod):
        '''Method to change the potion chance'''
        self.potionChance += mod

    def mechanics_change(self, mechanic, details): 
        '''Method to modify core mechanics of the game that relates to combat
        
        ### args:
            mechanic: the mechanic that is being changed
            details: what the mechanic will be changed to'''
        self.mechanics[mechanic] = details
        # Change the mechanic

    def gold_modification(self, amount):
        '''Method to change amount of gold the player has
        
        ### args:
            amount: amount of gold gained or lost'''
        for relic in self.player.relics:
            amount = relic.valueModificationEff('gold', amount)
        self.player.gold += amount
        # Add amount

    def card_pickup_from_id(self, card_id: int):
        '''Method for adding a card directly to the deck
        
        ### args:
            card_id: the card id'''
        card = card_constructor.create_card(card_id, card_data.card_info[card_id])
        if card.type == 4:
            if self.player.relics:
                for relic in self.player.relics:
                    card = relic.valueModificationEff('curse', card)
        if card != None:
            self.card_pickup(card)

    def card_pickup(self, card: card_constructor.Card):
        '''Method for picking up card rewards
        
        ### args:
            card: the card object being added'''
        if card.type in self.eggs:
            if card.id + 100 in card_data.card_info:
                card = card_constructor.create_card(card.id + 100, card_data.card_info[card.id + 100])
        self.player.deck.append(card)

    def egg_relic(self, type: int):
        '''Method to add a type of card to egg stash
        
        ### args: 
            type: card type id for the eggs'''
        self.eggs.append(type)

    def relic_pickup(self, relic):
        '''Method to pickup a relic
        
        ### args:
            relic: the relic object being added'''
        print(f'Pickup {relic}')
        self.player.relics.append(relic)
        relic.pickUp(self)
    
    def potion_pickup(self, potion):
        '''Method to pickup a potion
        
        ### args:
            potion: the potion object being added'''
        if self.player.potions.count(None) > 0:
            # Check if there is an empty potion slot
            for relic in self.player.relics:
                # Apply relic effects to the potion
                potion = relic.valueModificationEff('potion', potion)
            self.player.potions[self.player.potions.index(None)] = potion
            return True
        else:
            return False

    def gain_rand_potion(self):
        '''Method for filling a empty slot with a random potion
        '''
        potion_name, potion_details = random.choice(list(potion_data.potions.items()))
        potion = potion_data.Potion(potion_name, *potion_details)
        self.potion_pickup(potion)
        # Fill the an empty potion slot with a random potion if there is one
    
    def use_potion(self, potion):
        '''Method to use non combat based potions
        
        ### args:
            potion: The potion to be used
        '''
        i = 1
        self.player.potions[self.player.potions.index(potion)] = None
        # Remove the potion from the player's inventory
        self.clicked_potion = None
        # Reset the clicked potion
        for relic in self.player.relics:
            # Check if the relic is a Sacred Bark
            if relic.effect_type == 'Sacred Bark':
                i = 2
                break
        for times in range(0, i):
            # Apply the potion's effects
            for effect, details in potion.effect.items():
                    effect(*details, self)
                # Execute effects
        self.bonusEff('Used Potion')

    def card_select(self, num, restrictions):
        '''Method to select cards from the deck outside of combat
        
        ### args:
            num: Number of cards that needs selecting
            player: The character object that the player controlls
            restrictions = None: What type of cards can't be selected, none by default'''
        self.player.selected_cards = []
        eligible_cards = []
        for card in self.player.deck:
            if card.type not in restrictions:
                eligible_cards.append(card)
        pile = combat.Pile(eligible_cards, "selection")
        if pile.is_empty():
            return None
            
        if len(pile.cards) <= num:
            self.player.selected_cards.extend(pile.cards)
            pile.empty()
            if num == 1:
                return self.player.selected_cards[0].type
            else:
                return len(self.player.selected_cards)
                
        # Create selection surface and pile
        selection_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
        selection_surface.fill((0, 0, 0, 0))  # Completely transparent background
        
        # Create a Pile object to handle drawing the cards in a grid
        selection_pile = pile 
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
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if confirm button clicked
                    if confirm_button.collidepoint(mouse_pos):
                        if len(self.player.selected_cards) == num:
                            selecting = False
                            break
                            
                    # Check if card clicked
                    for card in pile:
                        if card.rect.collidepoint(mouse_pos):
                            if card in self.player.selected_cards:
                                # Unselect card if already selected
                                self.player.selected_cards.remove(card)
                            elif len(self.player.selected_cards) < num:
                                # Select card if under max selections
                                self.player.selected_cards.append(card)
                            break
                
                elif event.type == pygame.QUIT:
                    selecting = False
                    break
            
            # Draw cards
            selection_pile.draw(selection_surface, events)
            
            # Draw highlights around selected cards
            for card in self.player.selected_cards:
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

    def bottle(self):
        '''Method to add bottled tag to selected cards'''
        if self.player.selected_cards:
            for card in self.player.selected_cards:
                card.bottled = True

    def get_enemies(self, combat = 'normal'):
        '''Method to get enemies for combat
        
        ### args:
            combat: the type of combat'''
        enemies_constructors = []
        cap = 0
        # Initialize enemies constructors list and cap
        if self.act == 1:
            cap = 3
        # Set cap to 3 if the player is on the first act
        if combat == 'elite':
            # Get the enemies for elite combat
            enemies_constructors = self.combat_pool_details['elite'][self.elitePool[-1]]
            self.elitePool.pop(-1)
        elif combat == 'boss':
            # Get the enemies for boss combat
            enemies_constructors = self.combat_pool_details['boss'][self.boss[-1]]
        elif self.combats_finished <= cap:
            # Get the enemies for easy combat
            enemies_constructors = self.combat_pool_details['easy'][self.easyPool[-1]]
            self.easyPool.pop(-1)
        else:
            enemies_constructors = self.combat_pool_details['normal'][self.normalPool[-1]]
            self.normalPool.pop(-1)
        enemies = []
        for enemy_class in enemies_constructors:
            # Create enemy instances
            enemies.append(enemy_class())
        return enemies

    def create_combat_deck(self):
        '''Method to create a combat deck'''
        self.combat_deck = [card.create_copy() for card in self.player.deck]

    def generage_combat_instace(self, enemies, combatType):
        '''Method to generate a combat instance
        
        ### args:
            enemies: the enemies for the combat
            combatType: the type of combat'''
        self.create_combat_deck()
        self.combat = combat.Combat(self.player, self.combat_deck, enemies, combatType, self, self.screen)

    def start_combat(self, set_rewards = False):
        '''Method to start combat
        
        ### args:
            set_rewards: whether to set rewards'''
        self.lastInstance = 'C'
        result, screen = self.combat.run_combat()
        if result == 'victory':
            self.combats_finished += 1
            combat_type_conversion = {
                'normal': 0,
                'Normal': 0,
                'Elite': 1,
                'Boss': 2,
            }
            self.generate_reward_screen_instance(combat_type_conversion[self.combat.combat_type], set_rewards, {})
            self.open_reward_screen(screen)
            self.eventMod('Combat End')
            self.mapNav()
        elif result == 'defeat':
            self.defeat()
        elif result == 'escape':
            self.combats_finished += 1
            self.mapNav()

    def victory(self):
        '''Method to display the victory screen'''
        running = True
        self.clear_save_file()
        while running:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            
            # Create semi-transparent background
            overlay = pygame.Surface((1600, 900))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            # Create fonts
            defeat_font = pygame.font.Font(None, 128)
            menu_font = pygame.font.Font(None, 36)
            
            # Create text surfaces
            defeat_text = defeat_font.render("Victory!", True, (255, 255, 255))
            menu_text = menu_font.render("Return to Main Menu", True, (255, 255, 255))
            
            # Get text rectangles
            defeat_rect = defeat_text.get_rect(center=(800, 400))
            menu_rect = menu_text.get_rect(center=(800, 500))
            
            # Draw text
            self.screen.blit(defeat_text, defeat_rect)
            self.screen.blit(menu_text, menu_rect)
            
            # Check for clicks on menu text
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    self.exit_game()
                    break

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if menu_rect.collidepoint(mouse_pos):
                        self.main_menu.main_menu()
            
            pygame.display.flip()

    def defeat(self):
        '''Method to display the defeat screen'''
        running = True
        self.clear_save_file()
        while running:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            
            # Create semi-transparent background
            overlay = pygame.Surface((1600, 900))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            # Create fonts
            defeat_font = pygame.font.Font(None, 128)
            menu_font = pygame.font.Font(None, 36)
            
            # Create text surfaces
            defeat_text = defeat_font.render("Defeat", True, (255, 255, 255))
            menu_text = menu_font.render("Return to Main Menu", True, (255, 255, 255))
            
            # Get text rectangles
            defeat_rect = defeat_text.get_rect(center=(800, 400))
            menu_rect = menu_text.get_rect(center=(800, 500))
            
            # Draw text
            self.screen.blit(defeat_text, defeat_rect)
            self.screen.blit(menu_text, menu_rect)
            
            # Check for clicks on menu text
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    self.exit_game()
                    break

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if menu_rect.collidepoint(mouse_pos):
                        self.main_menu.main_menu()
            
            pygame.display.flip()

    def clear_save_file(self):
        '''Method to clear the save file'''
        with open('assets/saves/save_data.txt', 'w') as file:
            json.dump({}, file)

    def open_reward_screen(self, screen):
        '''Method to open the reward screen
        
        ### args:
            screen: the screen to display the rewards on'''
        self.reward.listRewards(screen)

    def start_treasure(self):
        '''Method to start the treasure event
        
        ### args:
            screen: the screen to display the rewards on'''
        self.lastInstance = 'T'
        self.treasure.start_event()
        self.mapNav()
    
    def start_shop(self):
        '''Method to start the shop event'''
        self.lastInstance = 'S'
        self.eventMod('shop')
        self.shop.generate_wares()
        self.shop.interact()
        self.mapNav()

    def start_event(self):
        '''Method to start the event
        
        ### args:
            screen: the screen to display the rewards on'''
        self.lastInstance = 'E'
        self.event.run_event()
        self.mapNav()

    def start_campfire(self):
        '''Method to start the campfire event'''
        self.lastInstance = 'R'
        self.rest_site.run_campfire()
        self.mapNav()

    def generate_event_list(self):
        '''Method to generate the list of random events the player will encouter'''
        possible_events = list(events.events1.keys())
        encounter_list = []
        combat_chance = 10
        treasure_chance = 2
        shop_chance = 3
        # Initialize encounter list and chances
        while possible_events:
            # Generate a random number between 1 and 100
            rng = random.randint(1, 100)
            if rng <= combat_chance:
                # Add combat to the encounter list
                encounter_list.append('combat')
                combat_chance = 10
                treasure_chance += 2
                shop_chance += 3
            elif rng <= combat_chance + treasure_chance:
                # Add treasure to the encounter list
                encounter_list.append('treasure')
                treasure_chance = 2
                combat_chance += 10
                shop_chance += 3
            elif rng <= combat_chance + treasure_chance + shop_chance:
                # Add shop to the encounter list
                encounter_list.append('shop')
                combat_chance += 10
                treasure_chance += 2
                shop_chance = 3
            else:
                # Add a random event to the encounter list
                combat_chance += 10
                treasure_chance += 2
                shop_chance += 3
                rng = random.randint(1, 100)
                if rng <= 95:
                    event_pick = random.choice(possible_events)
                    encounter_list.append(event_pick)
                    possible_events.remove(event_pick)
                else:
                    event_pick = random.choice(possible_events)
                    encounter_list.append(event_pick)
                    possible_events.remove(event_pick)
                    # encounter_list.append('shrine') # Placeholder
        return encounter_list

    def create_shop_instance(self):
        '''Method to create a shop instance'''
        self.shop = shop.Shop(self)
    
    def create_event_instance(self, event):
        '''Method to create an event instance
        
        ### args:
            event: the event to create'''
        self.event = events.events1[event](self.player, self)

    def create_treasure_instance(self):
        '''Method to create a treasure instance'''
        chest_event = chest.Treasure(self)
        self.treasure = chest_event

    def unknown_location(self):
        '''Method to handle unknown locations'''
        event = self.eventList[-1]
        self.eventList.pop(-1)
        # Check if the event is combat and random combat is disabled
        while event == 'combat' and self.mechanics['Random_Combat'] == False:
            self.eventList.pop(-1)
            event = self.eventList[-1]
        if event == 'combat':
            # Get enemies for combat
            enemies = self.get_enemies()
            # Generate a combat instance
            self.generage_combat_instace(enemies, 'normal')
            # Start combat
            self.start_combat()
        elif event == 'treasure':
            # Create a treasure instance
            self.create_treasure_instance()
            # Start the treasure event
            self.start_treasure()
        elif event == 'shop':
            # Create a shop instance
            self.create_shop_instance()
            # Start the shop event
            self.start_shop()
        else:
            # Create an event instance
            self.create_event_instance(event)
            # Start the event
            self.start_event()

game = MainMenu() # Initialize the game
game.main_menu() # Start the game
