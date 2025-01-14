import effects
import random
import pygame
import os
import math
#effect:
# dmg: (#, Times, target(Override)
# block: (#, Times)
# buff: (id, stacks, id, stacks, id, stacks...)
# debuff: (id, stacks, id, stacks, id, stacks...)
# draw: #
# discard: #
# place: (start, #, end, position if needed, cost)
# exhaust: (#, location, choice/random/condition/position)
# add: (location, card, #, cost(if applicable))
# search: (location, card/type, #)
# condition (Based on previous effect): (cond, cond eff, norm eff)
# retain: (location, #)
# play: (location, position, discard/exhaust, #)
# Hp: #
# Drawn: (eff)
# turn end: (eff)
# cost: (target, #, cond if applicable)
# modify: (target, eff, modification, combat/Perm)
# power: (name, duration(# OR Perm), amount)
# E: # 
# Exhausted: {eff}
# Discarded: {eff}
# upgrade: (target(s), #, combat/perm)
# gamble: # (Do a mulligan # of times)
# potion: (Slots, Type), adds potions to empty slots
# MaxHp: #
# Chaotic: Location

# 'NAME': ('DESCRIPTION', 'TIME OF USE', ('EFFECT': 'MAGNITUDE'...), 'TARGET')
class Potion:
    def __init__(self, name, desciption, time_of_use, effect, target, rarity):
        self.name = name
        self.description = desciption
        self.time_of_use = time_of_use
        self.effect = effect
        self.target = target
        self.rarity = rarity
        sprite = pygame.image.load(os.path.join('assets', 'sprites', 'potions', 'basic_potion.png'))
        self.sprite = pygame.transform.scale(sprite, (sprite.get_width() // 5, sprite.get_height() // 5))
        self.is_hovered = False
        self.rect = self.sprite.get_rect()
        self.hover_scale = 1.1
        self.clicked = False
        self.targeting = False
        self.arrow_body_sprite = pygame.image.load(os.path.join("assets", "arrows", "arrow_body.png"))
        self.arrow_head_sprite = pygame.image.load(os.path.join("assets", "arrows", "arrow_head.png"))
        self.arrow_body_sprite = pygame.transform.scale(self.arrow_body_sprite, 
            (self.arrow_body_sprite.get_width()//4, self.arrow_body_sprite.get_height()//4))
        self.arrow_head_sprite = pygame.transform.scale(self.arrow_head_sprite,
            (self.arrow_head_sprite.get_width()//4, self.arrow_head_sprite.get_height()//4))
    
    def __str__(self):
        return f'{self.name}: {self.description}'
    
    def __repr__(self):
        return self.__str__()

    def draw(self, screen, x, y):
        y -= 4
        if self.is_hovered:
            scaled_sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * self.hover_scale), int(self.sprite.get_height() * self.hover_scale)))
            screen.blit(scaled_sprite, (x, y))
        else:
            screen.blit(self.sprite, (x, y))
        self.rect.x = x
        self.rect.y = y
        if self.clicked:
            # Draw boxes
            box_width = 100
            box_height = 40
            box_x = x + (self.sprite.get_width() - box_width) // 2  # Center below potion
            box_y = y + self.sprite.get_height() + 10  # Below potion with padding
            
            # Use box
            pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y, box_width, box_height), 2)
            
            # Cancel box
            pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y + box_height + 5, box_width, box_height))
            pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y + box_height + 5, box_width, box_height), 2)
            
            # Text
            font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 16)
            use_text = font.render("Use", True, (255, 255, 255))
            cancel_text = font.render("Discard", True, (255, 255, 255))
            
            # Center text in boxes
            use_x = box_x + (box_width - use_text.get_width()) // 2
            use_y = box_y + (box_height - use_text.get_height()) // 2
            cancel_x = box_x + (box_width - cancel_text.get_width()) // 2
            cancel_y = box_y + box_height + 5 + (box_height - cancel_text.get_height()) // 2
            
            screen.blit(use_text, (use_x, use_y))
            screen.blit(cancel_text, (cancel_x, cancel_y))
            
            # Check for cancel click
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                cancel_rect = pygame.Rect(box_x, box_y + box_height + 5, box_width, box_height)
                if cancel_rect.collidepoint(mouse_pos):
                    self.clicked = False
            
        elif self.is_hovered:
            # Set up font
            font = pygame.font.Font(os.path.join("assets", "fonts", "Kreon-Bold.ttf"), 16)
            
            # Split description into lines of max 20 chars
            desc_words = self.description.split()
            desc_lines = []
            current_line = []
            current_length = 0
            
            for word in desc_words:
                if current_length + len(word) + 1 <= 60:
                    current_line.append(word)
                    current_length += len(word) + 1
                else:
                    desc_lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word) + 1
            if current_line:
                desc_lines.append(' '.join(current_line))

            # Render text surfaces
            name_text = font.render(self.name, True, (255, 255, 255))
            desc_text_surfaces = [font.render(line, True, (255, 255, 255)) for line in desc_lines]
            
            # Calculate box dimensions
            box_width = max(name_text.get_width(), max(surface.get_width() for surface in desc_text_surfaces)) + 20
            box_height = 40 + (len(desc_lines) * 30)  # 40 for name + padding, 30 per description line
            
            # Draw box
            box_x = x
            box_y = y + self.sprite.get_height() + 10
            pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y, box_width, box_height), 2)
            
            # Draw text
            screen.blit(name_text, (box_x + 10, box_y + 10))
            for i, surface in enumerate(desc_text_surfaces):
                screen.blit(surface, (box_x + 10, box_y + 40 + (i * 30)))
    
    def hover(self):
        self.is_hovered = True
    
    def unhover(self):
        if not self.clicked:
            self.is_hovered = False
    
    def click(self):
        self.clicked = True
    
    def unclick(self):
        self.clicked = False
        self.targeting = False
    
    def start_targeting(self):
        """Start the targeting state instead of dragging"""
        self.targeting = True

    def stop_targeting(self):
        """Stop the targeting state"""
        self.targeting = False
        
    def draw_targeting_arrow(self, surface, mouse_pos):
        """Draw an arrow from the card to the mouse position using separate head and body sprites"""
        if self.targeting:
            # Calculate start position (center of card)
            self.current_pos = self.rect.center
            start_pos = (
                self.current_pos[0],  # Divide by 4 because sprite is scaled by 1/2
                self.current_pos[1] + self.sprite.get_height()//2
            )
            
            
            # Calculate angle between start and mouse pos
            angle = math.degrees(math.atan2(mouse_pos[1] - start_pos[1], mouse_pos[0] - start_pos[0]))
            
            # Get the arrow head dimensions
            head_width = self.arrow_head_sprite.get_width()
            
            # Calculate the position where the arrow head should end (at mouse cursor)
            # Then work backwards to find where the body should end
            head_offset = head_width // 2  # Distance from head center to tip
            
            # Calculate the actual end point for the body (where head begins)
            body_end_x = mouse_pos[0] - math.cos(math.radians(angle)) * head_offset
            body_end_y = mouse_pos[1] - math.sin(math.radians(angle)) * head_offset
            
            # Calculate distance between start and body end
            distance = math.sqrt((body_end_x - start_pos[0])**2 + (body_end_y - start_pos[1])**2)
            
            # Calculate number of body segments needed
            segment_width = self.arrow_body_sprite.get_width()
            spacing = segment_width * 1.2  # Add 20% spacing between segments
            num_segments = int(distance / spacing)
            
            # Rotate sprites
            rotated_body = pygame.transform.rotate(self.arrow_body_sprite, -angle)
            rotated_head = pygame.transform.rotate(self.arrow_head_sprite, -angle)
            
            # Draw body segments
            for i in range(num_segments):
                # Calculate position for this segment
                segment_pos = (
                    start_pos[0] + math.cos(math.radians(angle)) * (i * spacing),
                    start_pos[1] + math.sin(math.radians(angle)) * (i * spacing)
                )
                segment_rect = rotated_body.get_rect()
                segment_rect.center = segment_pos
                surface.blit(rotated_body, segment_rect)
            
            # Draw final shortened body segment to reach arrow head
            final_segment_pos = (
                start_pos[0] + math.cos(math.radians(angle)) * (num_segments * spacing),
                start_pos[1] + math.sin(math.radians(angle)) * (num_segments * spacing)
            )
            remaining_distance = distance - (num_segments * spacing)
            if remaining_distance > 0:
                # Scale the final segment to fit the remaining distance
                scale_factor = remaining_distance / segment_width
                final_segment = pygame.transform.scale(
                    self.arrow_body_sprite,
                    (int(self.arrow_body_sprite.get_width() * scale_factor), 
                    self.arrow_body_sprite.get_height())
                )
                final_rotated = pygame.transform.rotate(final_segment, -angle)
                final_rect = final_rotated.get_rect()
                final_rect.center = final_segment_pos
                surface.blit(final_rotated, final_rect)
            
            # Draw arrow head at mouse position
            head_rect = rotated_head.get_rect()
            # Position the head so its tip is at the mouse cursor
            head_rect.center = (
                mouse_pos[0] - math.cos(math.radians(angle)) * head_offset,
                mouse_pos[1] - math.sin(math.radians(angle)) * head_offset
            )
            surface.blit(rotated_head, head_rect)

    def update_rect(self):
        self.rect = self.sprite.get_rect()

potions = {
    "Attack Potion": ("Add 1 of 3 random Attack cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Attack', 0)}, 0, 0),
    "Skill Potion": ("Add 1 of 3 random Skill cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Skill', 0)}, 0, 0),
    "Power Potion": ("Add 1 of 3 random Power cards to your hand, it costs 0 this turn.", 'combat', {effects.discover: ('Power', 0)}, 0, 0),
    "Blessing of the Forge": ("Upgrade all cards in your hand for the rest of combat.", 'combat', {effects.upgrade: ('hand', )}, 0, 0),
    "Block Potion": ("Gain 12 block.", 'combat', {effects.block_gain_power: (12, )}, 0, 0),
    "Strength Potion": ("Gain 2 Strength.", 'combat', {effects.apply_buff: (['Strength'], [2])}, 0, 0),
    "Dexterity Potion": ("Gain 2 Dexterity.", 'combat', {effects.apply_buff: (['Dexterity'], [2])}, 0, 0),
    "Flex Potion": ("Gain 5 Temporary Strength.", 'combat', {effects.apply_buff: (['Strength'], [5]), effects.apply_debuff: (['Chained'], [5])}, 0, 0),
    "Speed Potion": ("Gain 5 Temporary Dexterity.", 'combat', {effects.apply_buff: (['Dexterity'], [5]), effects.apply_debuff: (['Atrophy'], [5])}, 0, 0),
    "Fire Potion": ("Deal 20 Damage.", 'combat', {effects.deal_damage: (20, )}, 1, 0),
    "Explosive Potion": ("Deal 10 Damage to all enemies.", 'combat', {effects.deal_damage: (10, )}, 3, 0),
    "Fear Potion": ("Apply 3 Vulnerable to an enemy.", 'combat', {effects.apply_debuff: (['Vulnerable'], [3])}, 1, 0),
    "Weak Potion": ("Apply 3 Weak to an enemy.", 'combat', {effects.apply_debuff: (['Weak'], [3])}, 1, 0),
    "Energy Potion": ("Gain 2 Energy.", 'combat', {effects.energy_manip: (2, )}, 0, 1),
    "Swift Potion": ("Draw 3 cards.", 'combat', {effects.draw_cards: (3, )}, 0, 1),
    "Ancient Potion": ("Gain 1 Artifact.", 'combat', {effects.apply_buff: (['Artifact'], [1])}, 0, 1),
    "Thorns Potion": ("Gain 3 Thorns.", 'combat', {effects.apply_buff: (['Thorns'], [3])}, 0, 1),
    "Liquid Metal": ("Gain 4 Plated Armour.", 'combat', {effects.apply_buff: (['Plated Armour'], [4])}, 0, 1),
    "Regen Potion": ("Gain 5 Regeneration.", 'combat', {effects.apply_buff: (['Regen'], [5])}, 0, 1),
    "Memory Potion": ("Choose 1 card from the discard pile and add it to the hand, it costs 0 this turn.", 'combat', {effects.place_card_in_loction: ('discard', 1, 'hand', (0, 'Played'))}, 0, 1),
    "Duplicate Potion": ("Your next card is played twice.", 'combat', {effects.apply_buff: (['Duplicate'], [1])}, 0, 1),
    "Gambler's Potion": ("Discard any number of cards, then draw that many.", 'combat', {effects.gamble: ()}, 0, 1),
    "Chaos Potion": ("Play the top 3 cards of your Draw pile (This doesn't spend Energy).", 'combat', {effects.havoc: (3, False)}, 2, 1),
    "Ritual Potion": ("Gain 1 Ritual.", 'combat', {effects.apply_buff: (['Ritual'], [1])}, 0, 2),
    "Entropic Brew": ("Fill all your empty potion slots with random potions.", 'all', {effects.entropic: ()}, 0, 2),
    "Fairy in a Bottle": ("When you would die, heal to 30% of your Max HP instead and discard this potion.", 'died', {effects.revive: (30, )}, 0, 2),
    "Fruit Juice": ("Gain 5 Max HP.", 'all', {effects.max_hp_change: (5, )}, 0, 2),
    "Smoke Bomb": ("Escape from a non-boss combat. Receive no rewards.", 'combat', {effects.smoke_bomb: ()}, 0, 2),
    "Chaotic Potion": ("Draw 5 cards. Randomize the costs of all cards in your hand for the rest of the combat.", 'combat', {effects.draw_cards: (5, ), effects.chaos: ()}, 0, 2),
    "Blood Potion": ("Heal for 20% of your Max Hp", 'all', {effects.blood: ('20', )}, 0, 0),
    "Holy Water": ("Exhaust any number of cards in your hand.", 'combat', {effects.purity: ()}, 0, 1)
}

def createPotion(name, data):
    return Potion(name, *data)

def randomPotion():
    name = ''
    data = ()
    rng = random.randint(1, 100)
    if rng <= 65:
        rng = 0
    elif rng <= 90:
        rng = 1
    else:
        rng = 2
    while True:
        name, data = random.choice(list(potions.items()))
        if data[4] != rng:
            continue
        else:
            break
    return createPotion(name, data)

