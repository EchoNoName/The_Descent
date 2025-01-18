import random
import effects
import os
import pygame

class Enemy:
    def __init__(self):
        self.x = 0  # Initial x position
        self.y = 0  # Initial y position
        self.buffs = {'Strength': 0, 'Vigour': 0, 'Ritual': 0, 'Plated Armour': 0, 'Metalicize': 0, 'Blur': 0, 'Thorns': 0, 'Regen': 0, 'Artifact': 0, 'Next Turn Block': 0, 'Split': 0, 'Anger': 0, 'Enraged': 0, 'Thievery': 0, 'Stolen': 0, 'Infestation': 0, 'Curl Up': 0}
        self.debuffs = {'-Strength': 0, 'Vulnerable': 0, 'Weak': 0, 'Chained': 0, 'Poison': 0, 'Asleep': 0}
        self.block_overlay_sprite = pygame.image.load(os.path.join("assets", "ui", "hp_bar", "block_overlay.png"))
        hp_bar_path = os.path.join("assets", "ui", "hp_bar", f"hp_bar_8_8.png")
        self.hp_bar_sprite = pygame.image.load(hp_bar_path)
        
        # Set font sizes based on enemy size
        pygame.font.init()
        self.size_scales = {
            'small': {
                'block_font_size': 10,
                'hp_font_size': 16,
                'block_x_offset': -1,  # Smaller offset for small enemies
                'hp_x_offset': 8,
                'y_spacing': 5  # Less vertical space between sprite and health bar
            },
            'medium': {
                'block_font_size': 18,
                'hp_font_size': 20,
                'block_x_offset': -2,
                'hp_x_offset': 12,
                'y_spacing': 8
            },
            'large': {
                'block_font_size': 26,
                'hp_font_size': 24,
                'block_x_offset': 0,
                'hp_x_offset': 25,
                'y_spacing': 10
            }
        }
        self.font_initialized = False
        self.intent_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 18)
        self.attack_intent_sprite = pygame.image.load(os.path.join("assets", "icons", "intents", "attack.png"))
        self.block_intent_sprite = pygame.image.load(os.path.join("assets", "icons", "intents", "block.png"))
        self.debuff_intent_sprite = pygame.image.load(os.path.join("assets", "icons", "intents", "debuff.png"))
        self.mega_debuff_intent_sprite = pygame.image.load(os.path.join("assets", "icons", "intents", "mega_debuff.png"))
        self.buff_intent_sprite = pygame.image.load(os.path.join("assets", "icons", "intents", "buff.png"))
        self.special_intent_sprite = pygame.image.load(os.path.join("assets", "icons", "intents", "special.png"))
        self.escape_intent_sprite = pygame.image.load(os.path.join("assets", "icons", "intents", "escape.png"))
        self.buff_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 12)
        self.debuff_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 12)
        self.attack_buff_sprite = pygame.image.load(os.path.join("assets", "icons", "attack_buff.png"))
        self.defense_buff_sprite = pygame.image.load(os.path.join("assets", "icons", "defense_buff.png"))
        self.misc_buff_sprite = pygame.image.load(os.path.join("assets", "icons", "misc_buff.png"))
        self.vulnerable_sprite = pygame.image.load(os.path.join("assets", "icons", "vulnerable.png"))
        self.weak_sprite = pygame.image.load(os.path.join("assets", "icons", "weak.png"))
        self.frail_sprite = pygame.image.load(os.path.join("assets", "icons", "frail.png"))
        self.debuff_sprite = pygame.image.load(os.path.join("assets", "icons", "debuff.png"))
        self.is_hover = False
        self.name_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 24)
        self.description_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 20)

    def __str__(self):
        '''Override for String representation'''
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
        return f'{self.name}   HP: {self.hp}/{self.max_hp}   Block: {self.block}   Buffs: {buffs}   Debuffs: {debuffs}'

    def __repr__(self):
        return self.__str__()

    def hover(self):
        self.is_hover = True

    def unhover(self):
        self.is_hover = False

    def get_buff_description(self, buff):
        desc = {
            'Strength': f'Increases attack damage by {self.buffs["Strength"]}. ',
            'Vigour': f'Increases next attack damage by {self.buffs["Vigour"]}. ',
            'Ritual': f'At the start of your turn, gain {self.buffs["Ritual"]} Strength. ',
            'Plated Armour': f'At the end of your turn, gain {self.buffs["Plated Armour"]} Block, when you take unblocked attack damage, lose 1 Plated Armour. ',
            'Metalicize': f'At the end of your turn, gain {self.buffs["Metalicize"]} Block. ',
            'Thorns': f'When you take unblocked attack damage, deal {self.buffs["Thorns"]} damage to the attacker. ',
            'Regen': f'At the start of your turn, heal {self.buffs["Regen"]} HP. ',
            'Artifact': f'Negate the next {self.buffs["Artifact"]} debuffs. ',
            'Next Turn Block': f'At the start of your next turn, gain {self.buffs["Next Turn Block"]} Block. ',
            'Split': f'When this enemy goes below half HP, split into 2 smaller variants of themselves. ',
            'Anger': f'When this enemy is attacked, it gain {self.buffs["Anger"]} Strength. ',
            'Enraged': f'When a skill card is played, this enemy gains {self.buffs["Enraged"]} Strength. ',
            'Thievery': f'When this enemy attacks, it steals {self.buffs["Thievery"]} gold from the you. ',
            'Stolen': f'This enemy has stolen {self.buffs["Stolen"]} gold from you. ',
            'Infestation': f'When this enemy is killed, apply {self.buffs["Infestation"]} Vulnerable to you. ',
            'Curl Up': f'When this enemy is attacked, it gains {self.buffs["Curl Up"]} Block. ',
        }
        return desc[buff]

    def get_debuff_description(self, debuff):
        desc = {
            'Vulnerable': f'Take 50% more attack damage. ',
            'Weak': f'Deal 25% less attack damage. ',
            'Frail': f'Gain 25% less block from cards. ',
            '-Strength': f'Deal {self.debuffs["-Strength"]} less attack damage. ',
            'Chained': f'Lose {self.debuffs["Chained"]} Strength at the end of your turn. ',
            'Poison': f'Lose {self.debuffs["Poison"]} HP at the start of your turn. ',
            'Asleep': f'This enemy is asleep. ',
        }
        return desc[debuff]

    def set_font_size(self):
        scales = self.size_scales[self.size]
        self.block_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), scales['block_font_size'])
        self.hp_font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), scales['hp_font_size'])
        
        # Pre-render block text surfaces
        self.block_text_surfaces = {}
        for i in range(1000):  # Pre-render numbers 0-999
            outline = self.block_font.render(str(i), True, (0, 0, 0))
            text = self.block_font.render(str(i), True, (255, 255, 255))
            self.block_text_surfaces[i] = (outline, text)

    def update_hp_bar(self):
        health_percent = self.hp / self.max_hp
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

    def draw(self, surface, x = 0, y = 0):
        if not self.font_initialized:
            self.set_font_size()
            self.font_initialized = True
        # Draw enemy sprite
        surface.blit(self.sprite, (x, y))
        
        scales = self.size_scales[self.size]
        
        # Scale up the health bar
        sprite_width = self.sprite.get_width()
        original_ratio = self.hp_bar_sprite.get_height() / self.hp_bar_sprite.get_width()
        scaled_width = sprite_width
        scaled_height = int(scaled_width * original_ratio)
        hp_bar = pygame.transform.scale(self.hp_bar_sprite, (scaled_width, scaled_height))
        
        # Position health bar below character
        bar_x = x + self.sprite.get_width()//2 - hp_bar.get_width()//2
        bar_y = y + self.sprite.get_height() + scales['y_spacing']
        surface.blit(hp_bar, (bar_x, bar_y))
        
        # Draw block overlay and number if enemy has block
        if self.block > 0:
            # Scale block overlay to match health bar size
            block_overlay = pygame.transform.scale(self.block_overlay_sprite, (scaled_width, scaled_height))
            surface.blit(block_overlay, (bar_x, bar_y))
            
            # Use pre-rendered block text surfaces
            block_outline, block_text = self.block_text_surfaces.get(self.block, 
                (self.block_font.render(str(self.block), True, (0, 0, 0)),
                self.block_font.render(str(self.block), True, (255, 255, 255))))
            
            # Position block text
            text_x = bar_x + (scaled_width // 10) + scales['block_x_offset']
            text_y = bar_y + (scaled_height - block_outline.get_height()) // 2
            
            # Draw black outline
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (1,-1), (-1,1), (1,1)]:
                surface.blit(block_outline, (text_x + dx, text_y + dy))
            
            # Draw white text
            surface.blit(block_text, (text_x, text_y))
        
        # Draw HP text
        hp_text = f"{self.hp}/{self.max_hp}"
        hp_outline = self.hp_font.render(hp_text, True, (0, 0, 0))
        text_x = bar_x + (scaled_width - hp_outline.get_width()) // 2 + scales['hp_x_offset']
        text_y = bar_y + (scaled_height - hp_outline.get_height()) // 2
        
        # Draw black outline for HP text
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (1,-1), (-1,1), (1,1)]:
            surface.blit(hp_outline, (text_x + dx, text_y + dy))
        
        # Draw white HP text
        hp_text = self.hp_font.render(hp_text, True, (255, 255, 255))
        surface.blit(hp_text, (text_x, text_y))

        status_x = x + 10  # Start from character's left edge
        status_y = bar_y + scaled_height + 10  # Position below health bar

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
                
                status_x += sprite.get_width() + 5  # Shift right for next icon

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
                
                # Draw amount number in bottom right
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

        if self.is_hover:
            # Combine active buffs and debuffs into one list
            active_effects = []
            active_effects.extend([(buff, amount, True) for buff, amount in self.buffs.items() if amount > 0])
            active_effects.extend([(debuff, amount, False) for debuff, amount in self.debuffs.items() if amount > 0])
            
            box_width = 300
            line_height = 25
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
                box_x = x - self.sprite.get_width() - (box_width + 10) * column # Reduced left offset and column spacing
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
            # Draw name below health bar
            name_text = self.hp_font.render(self.name, True, (255, 255, 255))
            name_x = x + (self.sprite.get_width() - name_text.get_width()) // 2
            name_y = bar_y - 10  # Position below health bar with small gap
            # Draw black outline
            name_outline = self.hp_font.render(self.name, True, (0, 0, 0))
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (1,-1), (-1,1), (1,1)]:
                surface.blit(name_outline, (name_x + dx, name_y + dy))
            surface.blit(name_text, (name_x, name_y))

    def draw_intent(self, surface, x = 0, y = 0):
        # Draw intent
        if self.intent != None:
            intent = self.intent[-1]
            # Draw intent sprite above enemy
            if 'Attack' in intent:
                intent_sprite = self.attack_intent_sprite
            elif 'Block' in intent:
                intent_sprite = self.block_intent_sprite
            elif 'Mega Debuff' in intent:
                intent_sprite = self.mega_debuff_intent_sprite
            elif 'Special' in intent:
                intent_sprite = self.special_intent_sprite
            elif 'Escape' in intent:
                intent_sprite = self.escape_intent_sprite
            # For complex attacks that also apply debuffs/buffs, overlay the icons
            if 'Attack' in intent or 'Block' in intent:
                sprite_x = x + (self.sprite.get_width() - intent_sprite.get_width()) // 2
                sprite_y = y - intent_sprite.get_height() - 10  # 10px padding
                if 'Debuff' in intent:
                    surface.blit(self.debuff_intent_sprite, (sprite_x, sprite_y))
                elif 'Buff' in intent:
                    surface.blit(self.buff_intent_sprite, (sprite_x, sprite_y))
            else:
                # For pure debuff/buff intents, set the main sprite
                if 'Debuff' in intent:
                    intent_sprite = self.debuff_intent_sprite
                elif 'Buff' in intent:
                    intent_sprite = self.buff_intent_sprite
            
            # Draw intent sprite above enemy
            sprite_x = x + (self.sprite.get_width() - intent_sprite.get_width()) // 2
            sprite_y = y - intent_sprite.get_height() - 10  # 10px padding
            surface.blit(intent_sprite, (sprite_x, sprite_y))
            # Draw damage text below intent sprite if it's an attack
            if 'Attack' in intent:
                damage = self.intent[0][effects.deal_attack_damage][0] + self.buffs['Strength'] - self.debuffs['-Strength']
                if self.debuffs['Weak'] > 0:
                    damage = int(damage * 0.75)
                hits = self.intent[0][effects.deal_attack_damage][1]
                damage_text = f"{damage} x {hits}"
                
                # Render damage text
                damage_outline = self.intent_font.render(damage_text, True, (0, 0, 0))
                damage_surface = self.intent_font.render(damage_text, True, (255, 255, 255))
                
                # Position text below intent sprite
                text_x = sprite_x + (intent_sprite.get_width() - damage_outline.get_width()) // 2
                text_y = sprite_y + intent_sprite.get_height() - 10  # 5px padding
                
                # Draw black outline
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    surface.blit(damage_outline, (text_x + dx, text_y + dy))
                    
                # Draw white text
                surface.blit(damage_surface, (text_x, text_y))

    def draw_collision_box(self, surface):
        # Load and transform target corner sprite
        target_corner = pygame.image.load(os.path.join("assets", "ui", "target_corners.png"))
        
        # Draw corners at each corner of the rectangle
        # Top left - no rotation needed
        surface.blit(target_corner, (self.rect.left, self.rect.top))
        
        # Top right - rotate 90 degrees clockwise
        rotated = pygame.transform.rotate(target_corner, -90)
        surface.blit(rotated, (self.rect.right - rotated.get_width(), self.rect.top))
        
        # Bottom right - rotate 180 degrees
        rotated = pygame.transform.rotate(target_corner, -180) 
        surface.blit(rotated, (self.rect.right - rotated.get_width(), self.rect.bottom - rotated.get_height() + 10))
        
        # Bottom left - rotate 270 degrees clockwise
        rotated = pygame.transform.rotate(target_corner, -270)
        surface.blit(rotated, (self.rect.left, self.rect.bottom - rotated.get_height() + 10))

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
        intent = ''
        if self.intent != None:
            intent = self.intent[-1]
            if 'Attack' in intent:
                damage = self.intent[0][effects.deal_attack_damage][0] + self.buffs['Strength'] - self.debuffs['-Strength']
                if self.debuffs['Weak'] > 1:
                    damage = int(damage * 0.75)
                intent += f': {damage} x {self.intent[0][effects.deal_attack_damage][1]}'
        return self.__repr__() + f'   Intent: {intent}'
    
    def turn_start(self):
        '''Method for actions done at the start of turn'''
        if self.debuffs['Vulnerable'] > 0:
            self.debuffs['Vulnerable'] -= 1
        if self.debuffs['Weak'] > 0:
            self.debuffs['Weak'] -= 1
        # Lower some debuff counters by 1 for all enemies
        if self.debuffs['Poison'] > 0:
            self.hp_loss(self.debuffs['Poison'])
        # Lose 1 Hp for every poison
        self.block = 0
        # Lose all block on turn start
    
    def turn_end(self):
        '''Method for actions done at the end of turn'''
        if self.buffs['Ritual'] > 0:
            self.gain_buff('Strength', self.buffs['Ritual'])
        # Gain 1 strength for every ritual
        self.gain_block(self.buffs['Plated Armour'] + self.buffs['Metalicize'])
        self.hp_heal(self.buffs['Regen'])
        if self.debuffs['Poison'] > 0:
            self.debuffs['Poison'] -= 1
        # Execute buffs and debuffs

    def hp_heal(self, amount):
        '''method for healing
        
        ### args:
            amount: amount to heal by'''
        self.hp = min(self.max_hp, self.hp + amount)
        self.update_hp_bar()

    def damage_taken(self, damage):
        '''
        Handles damage taken by the entity
        '''
        damage = damage
        if self.debuffs['Vulnerable'] > 0:
            damage = int(damage * 1.5)
        self.block -= damage
        # Deal damage to block first
        if self.block >= 0:
            # If there is still block left or exacly enough block was spent
            return 0
            # return 0 for no attack damage dealt
        else:
            damage = -self.block
            # Update damage to only amount unblocked
            if self.buffs['Plated Armour'] > 0:
                self.buffs['Plated Armour'] -= 1
            # Remove 1 plated armour for taking damage 
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            # Update entity status
            return self.hp_loss(damage)
            # Hp loss
        self.update_hp_bar()
    
    def true_damage_taken(self, damage):
        '''
        Handles taking true damage that is uneffected by debuffs
        '''
        damage = damage
        self.block -= damage
        # Deal damage to block first
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
        self.update_hp_bar()

    def hp_loss(self, amount):
        '''Handles enemy losing Hp in anyway
        
        ### args: 
            amount: The amount of hp being lost
        
        ### returns: 
            the amount of hp lost, accounting for negatives'''
        self.hp -= amount
        # Subtract amount from hp
        self.update_hp_bar()
        if amount > 0:
            if self.died == True:
                return amount + self.hp
            else:
                return amount
        else:
            return 0
        # Returns actual amount of hp loss 

    def gain_block(self, block):
        '''Getting more block
        
        ### args:
            block: amount being gained'''
        self.block += block
        # Add to block

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
            self.buffs[buff_type] = max(0, self.buffs[buff_type] - amount)
        # Subtract the amount
        
    
    def gain_debuff(self, debuff_type, amount):
        '''Method for gaining debuffs
        
        ### args:
            buff_type: The type of debuff being gained
            amount: amount being gained
        '''
        if self.buffs['Artifact'] > 0:
            # If artifact is present
            self.buffs['Artifact'] -= 1
            # Subtrack 1 from artifact and negate the debuff
        elif debuff_type in {'Strength', '-Dexterity'}:
            # If its Str or Dex
            self.lose_buff(debuff_type[1:], amount)
            # Use the lose_buff funtion instead
        else:
            self.debuffs[debuff_type] += amount
            # Add the amount to debuff
    
    def lose_debuff(self, debuff_type, amount):
        '''Method for Losing debuffs
        
        ### args:
            debuff_type: The type of debuff being lost
            amount: the amount being lost
        '''
        self.debuffs[debuff_type] -= amount
        # Subtract amount from debuff
        if self.debuffs[debuff_type] < 0:
            # if its below 0
            self.debuffs[debuff_type] = 0
            # Make it 0 instead

    def died(self, combat):
        '''Checks if entity is dead'''
        if self.hp <= 0:
            return True
        else:
            return False

class JawWorm(Enemy):
    def __init__(self) -> None:
        self.name = 'Jaw Worm'
        self.sprite = 'jaw_worm.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite)
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() // 2), int(self.sprite.get_height() // 2)))
        
        # Create collision rect matching sprite size
        self.rect = self.sprite.get_rect()  # Creates rect same size as sprite
        
        self.size = 'medium'
        self.max_hp = random.randint(40, 44)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Chomp': ({effects.deal_attack_damage: (11, 1)}, 1, 'Attack'),
            'Thrash': ({effects.deal_attack_damage: (7, 1), effects.enemy_block_gain: (5, )}, 1, 'Block Attack'),
            'Bellow': ({effects.apply_buff: (['Strength'], [3]), effects.enemy_block_gain: (6, )}, 0, 'Block Buff')
        }
        self.intent = None
        super().__init__()
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if combat.turn == 1:
            self.intent = self.actions['Chomp']
            self.actions_done.append('Chomp')
            # Always bellow on turn 1
            return self.intent
        # Generate a random number from 1 - 100 for percentage based actions
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Loop until condition is met and the loop is broken
            if rng <= 25:
                # 67% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 1:
                        if 'Chomp' == self.actions_done[-1]:
                            continue
                        else:
                            action = 'Chomp'
                            self.actions_done.append(action)
                    else:
                        action = 'Chomp'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            elif rng <= 70: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Bellow' == self.actions_done[-1]:
                            continue
                        else:
                            action = 'Bellow'
                            self.actions_done.append(action)
                    else:
                        action = 'Bellow'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else:
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Thrash' == self.actions_done[-1] and 'Thrash' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Thrash'
                            self.actions_done.append(action)
                    else:
                        action = 'Thrash'
                        self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

class SmallGreenSlime(Enemy):
    def __init__(self, max_hp = random.randint(8, 12)):
        super().__init__()
        self.name = 'Small Green Slime'
        self.sprite = 'green_slime.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.175), int(self.sprite.get_height() * 0.175)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (3, 1)}, 1, 'Attack'),
            'Lick': ({effects.apply_debuff: (['Weak'], [1])}, 1, 'Small Debuff')
        }
        self.intent = None
        self.actions_done = []
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if combat.turn == 1:
            # If its turn 1
            if random.randint(0, 1) == 0:
                self.intent = self.actions['Tackle']
                self.actions_done.append('Tackle')
            else:
                self.intent = self.actions['Lick']
                self.actions_done.append('Lick')
            # 50/50 Which move to use
        else:
            if self.actions_done[-1] == 'Tackle':
                self.intent = self.actions['Lick']
                self.actions_done.append('Lick')
            else:
                self.intent = self.actions['Tackle']
                self.actions_done.append('Tackle')
            # Alternates moves
        return self.intent

class MediumGreenSlime(Enemy):
    def __init__(self, max_hp = random.randint(28, 32)):
        super().__init__()
        self.name = 'Medium Green Slime'
        self.sprite = 'green_slime.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(
            self.sprite, 
            (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3))
        )
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (10, 1)}, 1, 'Attack'),
            'Lick': ({effects.apply_debuff: (['Weak'], [1])}, 1, 'Small Debuff'),
            'Corrosive Spit': ({effects.deal_attack_damage: (7, 1), effects.add_card_to_pile: ('draw', 50, 1, 'na')}, 1, 'Attack Debuff')
        }
        self.intent = None
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 40:
                # 40% Chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Tackle' == self.actions_done[-1] and 'Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Tackle'
                        self.actions_done.append(action)
                else:
                    action = 'Tackle'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            elif rng <= 70:
                # 30% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                else:
                    action = 'Lick'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Corrosive Spit' == self.actions_done[-1] and 'Corrosive Spit' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Corrosive Spit'
                            self.actions_done.append(action)
                    else:
                        action = 'Corrosive Spit'
                        self.actions_done.append(action)
                else:
                    action = 'Corrosive Spit'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

class LargeGreenSlime(Enemy):
    def __init__(self, max_hp = random.randint(65, 69)):
        super().__init__()
        self.name = 'Large Green Slime'
        self.sprite = 'green_slime.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(
            self.sprite, 
            (int(self.sprite.get_width() * 0.6), int(self.sprite.get_height() * 0.6))
        )
        self.rect = self.sprite.get_rect()
        self.size = 'large'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (16, 1)}, 1, 'Attack'),
            'Lick': ({effects.apply_debuff: (['Weak'], [2])}, 1, 'Small Debuff'),
            'Corrosive Spit': ({effects.deal_attack_damage: (11, 1), effects.add_card_to_pile: ('draw', 50, 2, 'na')}, 1, 'Attack Debuff'),
            'Split': ({effects.split: ('Green', )}, 0, 'Special')
        }
        self.intent = None
        self.buffs['Split'] = 1
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 40:
                # 40% Chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Tackle' == self.actions_done[-1] and 'Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Tackle'
                        self.actions_done.append(action)
                else:
                    action = 'Tackle'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            elif rng <= 70:
                # 30% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                else:
                    action = 'Lick'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Corrosive Spit' == self.actions_done[-1] and 'Corrosive Spit' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Corrosive Spit'
                            self.actions_done.append(action)
                    else:
                        action = 'Corrosive Spit'
                        self.actions_done.append(action)
                else:
                    action = 'Corrosive Spit'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def died(self, combat):
        '''Override Method for the died Method, used to determain if the slime will split'''
        if self.hp <= 0:
            # If the slime has no hp left
            return True
            # They have died
        elif self.hp <= self.max_hp // 2 and self.intent[2] != 'Special':
            # If the slime is below half HP and not splitting
            self.intent = self.actions['Split']
            # Slime intends splits
            return False
            # Not dead yet
        else:
            return False
            # Not dead yet

class SmallBlueSlime(Enemy):
    def __init__(self, max_hp = random.randint(10, 14)) -> None:
        super().__init__()
        self.name = 'Small Blue Slime'
        self.sprite = 'blue_slime.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.175), int(self.sprite.get_height() * 0.175)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Tackle': ({effects.deal_attack_damage: (5, 1)}, 1, 'Attack'),
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Tackle']
        return self.intent

class MediumBlueSlime(Enemy):
    def __init__(self, max_hp = random.randint(28, 32)):
        super().__init__()
        self.name = 'Medium Blue Slime'
        self.sprite = 'blue_slime.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Lick': ({effects.apply_debuff: (['Frail'], [1])}, 1, 'Small Debuff'),
            'Flame Tackle': ({effects.deal_attack_damage: (8, 1), effects.add_card_to_pile: ('draw', 50, 1, 'na')}, 1, 'Attack Debuff')
        }
        self.intent = None
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 70:
                # 70% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                else:
                    action = 'Lick'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Flame Tackle' == self.actions_done[-1] and 'Flame Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Flame Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Flame Tackle'
                        self.actions_done.append(action)
                else:
                    action = 'Flame Tackle'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

class LargeBlueSlime(Enemy):
    def __init__(self, max_hp = random.randint(64, 70)):
        super().__init__()
        self.name = 'Large Blue Slime'
        self.sprite = 'blue_slime.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.6), int(self.sprite.get_height() * 0.6)))
        self.rect = self.sprite.get_rect()
        self.size = 'large'
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Lick': ({effects.apply_debuff: (['Frail'], [2])}, 1, 'Small Debuff'),
            'Flame Tackle': ({effects.deal_attack_damage: (16, 1), effects.add_card_to_pile: ('draw', 50, 2, 'na')}, 1, 'Attack Debuff'),
            'Split': ({effects.split: ('Blue', )}, 0, 'Special')
        }
        self.intent = None
        self.buffs['Split'] = 1
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 70:
                # 70% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Lick' == self.actions_done[-1] and 'Lick' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Lick'
                            self.actions_done.append(action)
                    else:
                        action = 'Lick'
                        self.actions_done.append(action)
                else:
                    action = 'Lick'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Flame Tackle' == self.actions_done[-1] and 'Flame Tackle' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Flame Tackle'
                            self.actions_done.append(action)
                    else:
                        action = 'Flame Tackle'
                        self.actions_done.append(action)
                else:
                    action = 'Flame Tackle'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def died(self, combat):
        '''Override Method for the died Method, used to determain if the slime will split'''
        if self.hp <= 0:
            # If the slime has no hp left
            return True
            # They have died
        elif self.hp <= self.max_hp // 2 and self.intent[2] != 'Special':
            # If the slime is below half HP and not splitting
            self.intent = self.actions['Split']
            # Slime intends splits
            return False
            # Not dead yet
        else:
            return False
            # Not dead yet

class SneakyGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Sneaky Goblin'
        self.sprite = 'sneaky_goblin.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = random.randint(10, 14)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Puncture': ({effects.deal_attack_damage: (9, 1)}, 1, 'Attack'),
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Puncture']
        # Only has one move
        return self.intent

class FatGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Fat Goblin'
        self.sprite = 'fat_goblin.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = random.randint(13, 17)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Smash': ({effects.deal_attack_damage: (4, 1), effects.apply_debuff: (['Weak'], [1])}, 1, 'Debuff Attack'),
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Smash']
        # Only has one move
        return self.intent

class WizardGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Wizard Goblin'
        self.sprite = 'wizard_goblin.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = random.randint(23, 25)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Charging': (None, 0, 'Special'),
            'Ultimate Blast': ({effects.deal_attack_damage: (25, 1)}, 1, 'Attack'),
        }
        self.charge = 0
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if self.charge < 2:
            self.intent = self.actions['Charging']
            self.charge += 1
        else:
            self.intent = self.actions['Ultimate Blast']
            self.charge = 0
        # 2 turns of charging then ultimate blast
        return self.intent

class MadGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Mad Goblin'
        self.sprite = 'mad_goblin.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = random.randint(20, 24)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Scratch': ({effects.deal_attack_damage: (4, 1)}, 1, 'Attack'),
        }
        self.intent = None
        self.buffs['Anger'] = 1
        # Initilize Properties of an enemy
    
    def damage_taken(self, damage):
        '''
        Handles damage taken by the entity
        '''
        damage = damage
        self.block -= damage
        # Deal damage to block first
        if self.block >= 0:
            # If there is still block left or exacly enough block was spent
            return 0
            # return 0 for no attack damage dealt
        else:
            damage = -self.block
            # Update damage to only amount unblocked
            if self.buffs['Plated Armour'] > 0:
                self.buffs['Plated Armour'] -= 1
            # Remove 1 plated armour for taking damage 
            if self.buffs['Anger'] > 0:
                self.gain_buff('Strength', self.buffs['Anger'])
            # Gain Strength for taking damage
            self.block = 0
            # If block isn't enough, Hp is used
            self.died
            # Update entity status
            return self.hp_loss(damage)
            # Hp loss
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        self.intent = self.actions['Scratch']
        # Only has one move
        return self.intent

class ShieldGoblin(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Shield Goblin'
        self.sprite = 'shield_goblin.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = random.randint(12, 15)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Protect': ({effects.enemy_block_gain: (7, )}, 2, 'Block'),
            'Shield Bash': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack')
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if len(combat.enemies) > 1:
            self.intent = self.actions['Protect']
        else:
            self.intent = self.actions['Shield Bash']
        # Protect if there are other enemies, attack if there isn't
        return self.intent

class Looter(Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Looter'
        self.sprite = 'looter.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.4), int(self.sprite.get_height() * 0.4)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = random.randint(44, 48)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Mug': ({effects.deal_attack_damage: (10, 1), effects.rob: ()}, 1, 'Attack'),
            'Lunge': ({effects.deal_attack_damage: (12, 1), effects.rob: ()}, 1, 'Attack'),
            'Smoke Bomb': ({effects.enemy_block_gain: (6, )}, 0, 'Block'),
            'Escape': ({effects.bandit_escape: ()}, 0, 'Escape')
        }
        self.buffs['Thievery'] = 15
        self.buffs['Stolen'] = 0
        self.smoked = False
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if combat.turn < 3:
            self.intent = self.actions['Mug']
        elif combat.turn == 3:
            rng = random.randint(0, 1)
            if rng == 0:
                self.intent = self.actions['Lunge']
            else:
                self.intent = self.actions['Smoke Bomb']
                self.smoked = True
        else:
            if self.smoked == True:
                self.intent = self.actions['Escape']
            else:
                self.intent = self.actions['Smoke Bomb']
                self.smoked = True
        return self.intent
            

class InfestedCorpes(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Infested Corpes'
        self.sprite = 'infested_corpes.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.4), int(self.sprite.get_height() * 0.4)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = random.randint(22, 28)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Grow': ({effects.apply_buff: (['Strength'], [3])}, 0, 'Buff')
        }
        self.intent = None
        self.buffs['Infestation'] = 2
        # Initilize Properties of an enemy

    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 60:
                # 60% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Bite' == self.actions_done[-1] and 'Bite' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Bite'
                            self.actions_done.append(action)
                    else:
                        action = 'Bite'
                        self.actions_done.append(action)
                else:
                    action = 'Bite'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Grow' == self.actions_done[-1]:
                            continue
                        else:
                            action = 'Grow'
                            self.actions_done.append(action)
                    else:
                        action = 'Grow'
                        self.actions_done.append(action)
                else:
                    action = 'Grow'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

    def died(self, combat):
        '''Override Method for the died Method, used to determain if the slime will split'''
        if self.hp <= 0:
            # If the enemy has no hp left
            combat.player.gain_debuff('Vulnerable', 2)
            return True
            # They have died
        else:
            return False
            # They alive

class Cultist(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Cultist'
        self.sprite = 'cultist.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = random.randint(48, 54)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Dark Strike': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Incantation': ({effects.apply_buff: (['Ritual'], [3])}, 0, 'Buff')
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if combat.turn == 1:
            # if its the first turn
            self.intent = self.actions['Incantation']
            # Use incantation
            return self.intent
        else:
            self.intent = self.actions['Dark Strike']
            # Use dark strike
            return self.intent

class RedArachnid(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Red Arachnid'
        self.sprite = 'red_spider.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.7), int(self.sprite.get_height() * 0.7)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = random.randint(46, 52)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Stab': ({effects.deal_attack_damage: (12, 1)}, 1, 'Attack'),
            'Scrape': ({effects.deal_attack_damage: (7, 1), effects.apply_debuff: (['Weak'], [1])}, 1, 'Debuff Attack')
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 40:
                # 40% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Stab' == self.actions_done[-1] and 'Stab' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Stab'
                            self.actions_done.append(action)
                    else:
                        action = 'Stab'
                        self.actions_done.append(action)
                else:
                    action = 'Stab'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Scrape' == self.actions_done[-1]:
                            continue
                        else:
                            action = 'Scrape'
                            self.actions_done.append(action)
                    else:
                        action = 'Scrape'
                        self.actions_done.append(action)
                else:
                    action = 'Scrape'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
class BlueArachnid(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Blue Arachnid'
        self.sprite = 'blue_spider.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.7), int(self.sprite.get_height() * 0.7)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = random.randint(46, 50)
        self.hp = self.max_hp
        self.block = 0
        self.special_done = False
        self.actions = {
            'Stab': ({effects.deal_attack_damage: (13, 1)}, 1, 'Attack'),
            'Scrape': ({effects.deal_attack_damage: (8, 1), effects.apply_debuff: (['Weak'], [1])}, 1, 'Debuff Attack'),
            'Entangle': ({effects.apply_debuff: (['Entangle'], [1])}, 1, 'Mega Debuff')
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if self.special_done == False:
            # If entangle hasn't been used yet
            if combat.turn == 1:
                # if its the first turn
                self.intent = self.actions['Stab']
                # Use stab
                return self.intent
            elif combat.turn % 3 == 1:
                # follows a pattern
                if random.randint(1, 4) != 1:
                    # 25% percent chance
                    self.intent = self.actions['Entangle']
                    # Use Entangle
                    self.special_done = True
                    # Special move used
                    return self.intent
                else:
                    self.intent = self.actions['Stab']
                    # Use stab
                    return self.intent
            else:
                if random.randint(1, 4) != 1:
                    # 25% percent chance
                    self.intent = self.actions['Entangle']
                    # Use Entangle
                    self.special_done = True
                    # Special move used
                    return self.intent
                else: 
                    self.intent = self.actions['Scrape']
                    # Use Scrape
                    return self.intent
        else:
            action = ''
            # Initialize action variable
            while not action:
                rng = random.randint(1, 100)
                # Generate a random number from 1 - 100 for percentage based actions
                # Loop until condition is met and the loop is broken
                if rng <= 45:
                    # 45% chance move
                    action = 'Stab'
                else: 
                    action = 'Scrape'
            self.intent = self.actions[action]
            # Update intent to correct move
            return self.intent

class GreenLouse(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Green Louse'
        self.sprite = 'green_louse.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = random.randint(10, 15)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Grow': ({effects.apply_buff: (['Strength'], [3])}, 0, 'Buff')
        }
        self.intent = None
        self.buffs['Curl Up'] = random.randint(3, 7)
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 75:
                # 75% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Bite' == self.actions_done[-1] and 'Bite' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Bite'
                            self.actions_done.append(action)
                    else:
                        action = 'Bite'
                        self.actions_done.append(action)
                else:
                    action = 'Bite'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 2:
                        if 'Grow' == self.actions_done[-1] and 'Grow' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Grow'
                            self.actions_done.append(action)
                    else:
                        action = 'Grow'
                        self.actions_done.append(action)
                else:
                    action = 'Grow'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def damage_taken(self, damage):
        '''
        Handles damage taken by the entity
        '''
        damage = damage
        if self.debuffs['Vulnerable'] > 0:
            damage = int(damage * 1.5)
        self.block -= damage
        # Deal damage to block first
        if self.block >= 0:
            # If there is still block left or exacly enough block was spent
            return 0
            # return 0 for no attack damage dealt
        else:
            damage = -self.block
            # Update damage to only amount unblocked
            if self.buffs['Plated Armour'] > 0:
                self.buffs['Plated Armour'] -= 1
            # Remove 1 plated armour for taking damage 
            self.block = 0
            # If block isn't enough, Hp is used
            if self.buffs['Curl Up'] > 0:
                self.block = self.buffs['Curl Up']
                self.buffs['Curl Up'] = 0
            # Consume curl up after taking damage to gain block
            self.died
            # Update entity status
            return self.hp_loss(damage)
            # Hp loss

class RedLouse(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Red Louse'
        self.sprite = 'red_louse.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.3), int(self.sprite.get_height() * 0.3)))
        self.rect = self.sprite.get_rect()
        self.size = 'small'
        self.max_hp = random.randint(11, 17)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (6, 1)}, 1, 'Attack'),
            'Spit Web': ({effects.apply_debuff: (['Weak'], [2])}, 1, 'Debuff')
        }
        self.intent = None
        self.buffs['Curl Up'] = random.randint(3, 7)
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 75:
                # 75% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Bite' == self.actions_done[-1] and 'Bite' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Bite'
                            self.actions_done.append(action)
                    else:
                        action = 'Bite'
                        self.actions_done.append(action)
                else:
                    action = 'Bite'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Spit Web' == self.actions_done[-1] and 'Spit Web' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Spit Web'
                            self.actions_done.append(action)
                    else:
                        action = 'Spit Web'
                        self.actions_done.append(action)
                else:
                    action = 'Spit Web'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent
    
    def damage_taken(self, damage):
        '''
        Handles damage taken by the entity
        '''
        damage = damage
        if self.debuffs['Vulnerable'] > 0:
            damage = int(damage * 1.5)
        self.block -= damage
        # Deal damage to block first
        if self.block >= 0:
            # If there is still block left or exacly enough block was spent
            return 0
            # return 0 for no attack damage dealt
        else:
            damage = -self.block
            # Update damage to only amount unblocked
            if self.buffs['Plated Armour'] > 0:
                self.buffs['Plated Armour'] -= 1
            # Remove 1 plated armour for taking damage 
            self.block = 0
            # If block isn't enough, Hp is used
            if self.buffs['Curl Up'] > 0:
                self.block = self.buffs['Curl Up']
                self.buffs['Curl Up'] = 0
            # Consume curl up after taking damage to gain block
            self.died
            # Update entity status
            return self.hp_loss(damage)
            # Hp loss

class SentryA(Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Sentry'
        self.sprite = 'sentry.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.5), int(self.sprite.get_height() * 0.5)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = random.randint(38, 42)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Beam': ({effects.deal_attack_damage: (8, 1)}, 1, 'Attack'),
            'Bolt': ({effects.add_card_to_pile: ('discard', 53, 2, 'na')}, 1, 'Small Debuff')
        }
        self.intent = None
        self.actions_done = []
        self.buffs['Artifact'] = 1
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if combat.turn == 1:
            # If its turn 1
            self.intent = self.actions['Beam']
            self.actions_done.append('Beam')
            # Use beam
        else:
            if self.actions_done[-1] == 'Beam':
                self.intent = self.actions['Bolt']
                self.actions_done.append('Bolt')
            else:
                self.intent = self.actions['Beam']
                self.actions_done.append('Beam')
            # Alternates moves
        return self.intent

class SentryB(Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Sentry'
        self.sprite = 'sentry.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.5), int(self.sprite.get_height() * 0.5)))
        self.rect = self.sprite.get_rect()
        self.size = 'medium'
        self.max_hp = random.randint(38, 42)
        self.hp = self.max_hp
        self.block = 0
        self.actions = {
            'Beam': ({effects.deal_attack_damage: (8, 1)}, 1, 'Attack'),
            'Bolt': ({effects.add_card_to_pile: ('discard', 53, 2, 'na')}, 1, 'Small Debuff')
        }
        self.intent = None
        self.actions_done = []
        self.buffs['Artifact'] = 1
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
        
        ### args: 
            combat: the combat session currently in'''
        if combat.turn == 1:
            # If its turn 1
            self.intent = self.actions['Bolt']
            self.actions_done.append('Bolt')
            # Use beam
        else:
            if self.actions_done[-1] == 'Beam':
                self.intent = self.actions['Bolt']
                self.actions_done.append('Bolt')
            else:
                self.intent = self.actions['Beam']
                self.actions_done.append('Beam')
            # Alternates moves
        return self.intent

class GiantLouse(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Giant Louse'
        self.sprite = 'red_louse.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.rect = self.sprite.get_rect()
        self.size = 'large'
        self.max_hp = random.randint(109, 111)
        self.hp = self.max_hp
        self.block = 8
        self.special_done = False
        self.counter = 0
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (18, 1)}, 1, 'Attack'),
            'Asleep': (None, 1, 'Special'),
            'Web': ({effects.apply_debuff: (['-Dexterity', '-Strength'], [1, 1])}, 1, 'Mega Debuff'),
            'Stunned': (None, 1, 'Special')
        }
        self.intent = None
        self.buffs['Metalicize'] = 8
        self.debuffs['Asleep'] = 1
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if self.special_done == False and combat.turn < 4:
            # If hasn't woke up yet
            self.intent = self.actions['Asleep']
            return self.intent
        else:
            if self.counter == 0 or self.counter == 1:
                # Pattern move
                self.intent = self.actions['Bite']
                self.counter += 1
                # Increase counter
            else:
                self.intent = self.actions['Web']
                self.counter = 0
                # Reset counter after webbing
            return self.intent
    
    def hp_loss(self, amount):
        '''Handles enemy losing Hp in anyway
        
        ### args: 
            amount: The amount of hp being lost
        
        ### returns: 
            the amount of hp lost, accounting for negatives'''
        self.hp -= amount
        # Subtract amount from hp
        if amount > 0:
            # Toke damage, wakes up
            self.buffs['Metalicize'] -= 8
            self.debuffs['Asleep'] = 0
            # Change buffs and debuffs
            self.intent = self.actions['Stunned']
            self.special_done = True
            # Awakens
            self.update_hp_bar()
            if self.died == True:
                return amount + self.hp
            else:
                return amount
        else:
            return 0
        # Returns actual amount of hp loss 

class GiantLouseAwake(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Giant Louse'
        self.sprite = 'red_louse.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.rect = self.sprite.get_rect()
        self.size = 'large'
        self.max_hp = random.randint(109, 111)
        self.hp = self.max_hp
        self.block = 0
        self.special_done = False
        self.counter = 0
        self.actions = {
            'Bite': ({effects.deal_attack_damage: (18, 1)}, 1, 'Attack'),
            'Web': ({effects.apply_debuff: (['-Dexterity', '-Strength'], [1, 1])}, 1, 'Mega Debuff'),
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if self.counter == 0 or self.counter == 1:
            # Pattern move
            self.intent = self.actions['Bite']
            self.counter += 1
            # Increase counter
        else:
            self.intent = self.actions['Web']
            self.counter = 0
            # Reset counter after webbing
        return self.intent

class GoblinGiant(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Goblin Giant'
        self.sprite = 'goblin_giant.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.8), int(self.sprite.get_height() * 0.8)))
        self.rect = self.sprite.get_rect()
        self.size = 'large'
        self.max_hp = random.randint(82, 86)
        self.hp = self.max_hp
        self.block = 0
        self.actions_done = []
        self.actions = {
            'Skull Bash': ({effects.deal_attack_damage: (6, 1), effects.apply_debuff: (['Vulnerable'], [2])}, 1, 'Debuff Attack'),
            'Rush': ({effects.deal_attack_damage: (14, 1)}, 1, 'Attack'),
            'Bellow': ({effects.apply_buff: (['Enraged'], [2])}, 0, 'Buff')
        }
        self.intent = None
        self.buffs['Enraged'] = 0
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if combat.turn == 1:
            self.intent = self.actions['Bellow']
            # Always bellow on turn 1
            return self.intent
        action = ''
        # Initialize action variable
        while not action:
            rng = random.randint(1, 100)
            # Generate a random number from 1 - 100 for percentage based actions
            # Loop until condition is met and the loop is broken
            if rng <= 67:
                # 67% chance move
                if self.actions_done:
                    # If there were previous actions
                    if len(self.actions_done) >= 2:
                        if 'Rush' == self.actions_done[-1] and 'Rush' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Rush'
                            self.actions_done.append(action)
                    else:
                        action = 'Rush'
                        self.actions_done.append(action)
                else:
                    action = 'Rush'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
            else: 
                if self.actions_done:
                    if len(self.actions_done) >= 1:
                        if 'Skull Bash' == self.actions_done[-1] and 'Skull Bash' == self.actions_done[-2]:
                            continue
                        else:
                            action = 'Skull Bash'
                            self.actions_done.append(action)
                    else:
                        action = 'Skull Bash'
                        self.actions_done.append(action)
                else:
                    action = 'Skull Bash'
                    self.actions_done.append(action)
                # Checks if the move was used twice in the previous 2 turns already and if not makes it the action done
        self.intent = self.actions[action]
        # Update intent to correct move
        return self.intent

class AncientMech(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Ancient Mech'
        self.sprite = 'ancient_mech.png'
        self.sprite = os.path.join("assets", "sprites", "enemies", self.sprite)
        self.sprite = pygame.image.load(self.sprite) # The sprite of a card
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() // 1.5, self.sprite.get_height() // 1.5))
        self.rect = self.sprite.get_rect()
        self.size = 'large'
        self.max_hp = 250
        self.hp = self.max_hp
        self.block = 0
        self.counter = 0
        self.actions = {
            'Mode Shift: Initiate': (None, 0, 'Special'),
            'Laser Barrage': ({effects.deal_attack_damage: (5, 6)}, 1, 'Multi Attack'),
            'Sword Sweep': ({effects.deal_attack_damage: (6, 2)}, 1, 'Multi Attack'),
            'Mode Shift: Defense': ({effects.enemy_block_gain: (20, )}, 0, 'Special'),
            'Defensive Shock': ({effects.enemy_block_gain: (15, ), effects.add_card_to_pile: ('discard', 53, 2, 'na')}, 0, 'Debuff Block'),
            'Sonic Pulse': ({effects.apply_debuff: (['Weak', 'Frail'], [3, 3])}, 1, 'Mega Debuff'),
            'Mode Shift: Offense': ({effects.apply_buff: (['Strength'], [3])}, 0, 'Special')
        }
        self.intent = None
        # Initilize Properties of an enemy
    
    def intent_get(self, combat):
        '''Gets what the enemy intends to do
    
        ### args: 
        combat: the combat session currently in
        '''
        if combat.turn == 1:
            self.intent = self.actions['Mode Shift: Initiate']
            # Always initiates on turn 1
            return self.intent
        else:
            # Follows a set pattern
            if self.counter == 0:
                self.intent = self.actions['Laser Barrage']
                self.counter += 1
            elif self.counter == 1:
                self.intent = self.actions['Sword Sweep']
                self.counter += 1
            elif self.counter == 2:
                self.intent = self.actions['Mode Shift: Defense']
                self.counter += 1
            elif self.counter == 3:
                self.intent = self.actions['Defensive Shock']
                self.counter += 1
            elif self.counter == 4:
                self.intent = self.actions['Sonic Pulse']
                self.counter += 1
            else:
                self.intent = self.actions['Mode Shift: Offense']
                self.counter = 0
            return self.intent
        # Repeats this loop over and over


def generate_act1_pools():
    '''Function to generage enemy encouters for act 1, mainly used for some encounters that have some random variation
    
    ### returns:
        act1_fights: A dictonary containing all easy, normal, elite and boss encounters'''
    act1_easy_combats = {
        'Single Cultist': [Cultist], # Easy encounter
        'Single Jawworm': [JawWorm], # Easy encounter
    }
    rng = random.randint(0, 1)
    if rng == 0:
        act1_easy_combats['2 Slimes'] = [MediumBlueSlime, SmallGreenSlime] # Easy encounter
    else:
        act1_easy_combats['2 Slimes'] = [MediumGreenSlime, SmallBlueSlime] # Easy encounter
    louse_encounter = []
    for i in range(0, 2):
        rng = random.randint(0, 1)
        if rng == 0:
            louse_encounter.append(RedLouse) # Easy encounter
        else:
            louse_encounter.append(GreenLouse) # Easy encounter
    act1_easy_combats['2 Louses'] = louse_encounter

    act1_normal_combat = {
        '5 Slimes': [SmallBlueSlime, SmallBlueSlime, SmallBlueSlime, SmallGreenSlime, SmallGreenSlime], # Normal encounter
        'Blue Spider': [BlueArachnid], # Normal encounter
        'Red Spider': [RedArachnid], # Normal encounter
        '2 Corpes': [InfestedCorpes, InfestedCorpes], # Normal encounter
        'Single Looter': [Looter] # Normal encounter
    }

    goblin_pool = [MadGoblin, MadGoblin, SneakyGoblin, SneakyGoblin, FatGoblin, FatGoblin, ShieldGoblin, WizardGoblin] # Pool of goblins to choose from
    fight = []
    for i in range(0, 4):
        enemy = random.choice(goblin_pool) # Choose a random goblin from the pool
        fight.append(enemy) # Add the goblin to the fight
        goblin_pool.remove(enemy) # Remove the goblin from the pool
    act1_normal_combat['4 Goblins'] = fight # Add the fight to the normal encounter pool
    slime = [random.choice([LargeBlueSlime, LargeGreenSlime])] # Choose a random slime from the pool
    act1_normal_combat['Single LSlime'] = slime # Add the slime to the normal encounter pool
    louses = []
    for i in range(0, 3):
        rng = random.randint(0, 1)
        if rng == 0:
            louses.append(RedLouse)
        else:
            louses.append(GreenLouse)
    act1_normal_combat['3 Louses'] = louses
    act1_normal_combat['Forest and Human'] = [random.choice([RedLouse, GreenLouse, MediumBlueSlime, MediumGreenSlime]), random.choice([Looter, Cultist, RedArachnid, BlueArachnid])]
    act1_normal_combat['Double Forest'] = [random.choice([InfestedCorpes, JawWorm]), random.choices([RedLouse, GreenLouse, MediumBlueSlime, MediumGreenSlime])] # Normal encounter

    act1_elites = {
        'Goblin Giant' : [GoblinGiant], # Elite encounter
        'Giant Louse': [GiantLouse], # Elite encounter
        'Sentries': [SentryA, SentryB, SentryA] # Elite encounter
    }

    act1_bosses = {
        'Ancient Mech': [AncientMech] # Boss encounter
    }

    act1_fights = {
        'easy': act1_easy_combats, # Easy encounter pool
        'normal': act1_normal_combat, # Normal encounter pool
        'elite': act1_elites, # Elite encounter pool
        'boss': act1_bosses # Boss encounter pool
    }
    
    return act1_fights

def act_1_easy_pool():
    '''Function to generate the encounter order'''
    pool = ['Single Cultist', 'Single Jawworm', '2 Slimes', '2 Louses'] # Easy encounter pool
    random.shuffle(pool)
    return pool
    
def act_1_normal_pool():
    pool = ['5 Slimes', 'Blue Spider', 'Red Spider', '2 Corpes', 'Single Looter', '4 Goblins', 'Single LSlime', '3 Louses', 'Forest and Human', 'Double Forest'] # Normal encounter pool
    random.shuffle(pool)
    return pool

def act_1_elite_pool():
    pool = ['Goblin Giant', 'Giant Louse', 'Sentries'] # Elite encounter pool
    random.shuffle(pool)
    pool2 = ['Goblin Giant', 'Giant Louse', 'Sentries'] # Elite encounter pool
    random.shuffle(pool2)
    pool.extend(pool2)
    return pool

def act_1_boss_pool():
    pool = ['Ancient Mech'] # Boss encounter pool
    random.shuffle(pool)
    return pool


