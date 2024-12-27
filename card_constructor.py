import random
import pygame
import os
import math

common_1 = [1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024]
uncommon_1 = [1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056]
rare_1 = [1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074]
attack_card_1 = [1003, 1004, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1022, 1023, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1057, 1058, 1059, 1060, 1061, 1062]
skill_card_1 = [1005, 1006, 1007, 1008, 1017, 1018, 1019, 1020, 1021, 1024, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1063, 1064, 1065, 1066, 1067, 1068]
power_card_1 = [1050, 1051, 1052, 1053, 1054, 1055, 1056, 1069, 1070, 1071, 1072, 1073, 1074]
weak_curse = [0, 1, 2, 3, 4, 5, 6]
medium_curse = [8, 12]
strong_curse = [9, 10, 11]

def random_card(type: str, character = None):
    type = type.lower()
    if type == 'curse':
        return random.choice(weak_curse + medium_curse + strong_curse)
    elif type == 'weak curse':
        return random.choice(weak_curse)
    elif type == 'status':
        return 'placeholer'
    elif type == 'atk':
        if character.character_class == 1:
            return random.choice(attack_card_1)
        else:
            return 'placeholder'
    elif type == 'skill':
        if character.character_class == 1:
            return random.choice(skill_card_1)
        else:
            return 'placeholder'
    elif type == 'power':
        if character.character_class == 1:
            return random.choice(power_card_1)
        else:
            return 'placeholder'
    elif type == 'card':
        if character.character_class == 1:
            return random.choice(power_card_1 + skill_card_1 + attack_card_1)
        else:
            return 'placeholder'

class Card():
    def __init__(self, id : int, name : str, rarity, type, cost, card_text, innate, exhaust, retain, ethereal, effect, target, x = 1650, y = 950, bottled = False, removable = True, x_cost_effect = {}):
        self.id = id # Card ID, which is an integer
        self.name = name # Name of the card, a string
        self.rarity = rarity # rarity represented by an integer
        self.type = type # type of card (attack, skill, power, curse, status), represented by an integer
        self.cost = cost # cost of the card, can be just a number, x or a special cost written like ('C', original cost, +/-, condition)
        self.card_text = card_text # Base card text, a string
        self.innate = innate # Boolean representing whether a card is innate
        self.exhaust = exhaust # Boolean representing whether a card is exhaust
        self.retain = retain # Boolean representing whether a card is retain
        self.ethereal = ethereal # Boolean representing whether a card is ethereal
        self.effect = effect # what the card actually does, represented by a dictonary that contains its actions
        self.target = target # The targets of the card, represented by an integer
        sprite = name.lower()
        sprite = sprite.replace(' ', '_')
        sprite = f'{sprite}.png'
        sprite = os.path.join("assets", "sprites", "cards", sprite)
        self.sprite = pygame.image.load(sprite) # The sprite of a card
        self.removable = removable # Whether the card can be removed from the deck
        self.combat_cost = (None, None) #(Cost, Duration of cost (Played, Turn, Combat))
        self.chaotic = False # whether a card is chaotic, represented by boolean
        self.x_cost_effect = x_cost_effect
        # rarity:(0 = starter, 1 = common, 2 = uncommon, 3 = rare, 4 = other), type: (0 = atk, 1 = skill, 2 = power, 3 = status, 4 = curse)
        self.bottled = bottled
        self.in_hand = False
        self.x = x
        self.y = y
        self.hand_location = [self.x, self.y]
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
        self.targeting = False
        self.dragging = False
        # Position and movement attributes
        self.current_pos = pygame.Vector2(x, y)
        self.target_pos = pygame.Vector2(x, y)
        self.snap_speed = 30  # Speed of snapping animation
        self.offset = pygame.Vector2(0, 0)  # Offset between mouse and card position during drag
        
        # Add hover state attributes
        self.is_hovered = False
        self.original_size = self.sprite.get_size()
        self.hover_scale = 1.5  # Scale factor when hovering
        self.hover_y_offset = -150  # How many pixels to move up when hovering
        self.hover_sprite = pygame.transform.scale(
            self.sprite,
            (int(self.original_size[0] * self.hover_scale), 
             int(self.original_size[1] * self.hover_scale))
        )

    def __str__(self):
        card_descrip = []
        if self.cost == 'U':
            card_descrip.append('Unplayable')
        if self.innate == True:
            card_descrip.append('Innate')
        if self.retain == True:
            card_descrip.append('Retain')
        if self.card_text != None and self.effect != None:
            card_descrip.append(self.card_text)
        if self.removable == False:
            card_descrip.append('Cannot be removed from your deck')
        if self.ethereal == True:
            card_descrip.append('Ethereal')
        if self.exhaust == True:
            card_descrip.append('Exhaust')
        card_descrip = str('. '.join(card_descrip))
        if card_descrip[-1] != ' ' and card_descrip[-2] != '.':
            card_descrip += '. '
        rarity = {
            0: 'Starter',
            1: 'Common',
            2: 'Uncommon',
            3: 'Rare',
        }
        if self.rarity in rarity:
            rarity = rarity[self.rarity]
        elif self.removable == True:
            rarity = 'Normal'
        else:
            rarity = 'Special'
        type = {
            0: 'Attack',
            1: 'Skill',
            2: 'Power',
            3: 'Status',
            4: 'Curse'
        }
        type = type[self.type]
        return f'{self.name}: {rarity} {type}. {card_descrip}Cost: {self.get_cost()}'

    def __repr__(self):
        return self.__str__()

    def set_target_position(self, x, y):
        self.target_x = x
        self.target_y = y

    def update(self):
        if self.dragging:
            # When dragging, follow mouse position
            mouse_pos = pygame.mouse.get_pos()
            self.current_pos = pygame.Vector2(
                mouse_pos[0] + self.drag_offset[0],
                mouse_pos[1] + self.drag_offset[1]
            )
        else:
            # Normal movement toward target position
            direction = self.target_pos - self.current_pos
            distance = direction.length()
            if distance > 1:
                direction = direction.normalize()
                self.current_pos += direction * min(self.snap_speed, distance)
            else:
                self.current_pos = self.target_pos

        # Update collision rect position
        if self.is_hovered or self.targeting or self.dragging:  # Changed condition here
            # Use larger collision box for hover sprite
            scaled_hover = pygame.transform.smoothscale(self.hover_sprite,
                (self.hover_sprite.get_width()//2, self.hover_sprite.get_height()//2))
            self.rect = pygame.Rect(
                self.current_pos[0] - (scaled_hover.get_width() - self.sprite.get_width()//2) / 2,
                self.current_pos[1],
                scaled_hover.get_width(),
                scaled_hover.get_height()
            )
        else:
            # Use normal sprite collision box
            scaled_sprite = pygame.transform.smoothscale(self.sprite,
                (self.sprite.get_width()//2, self.sprite.get_height()//2))
            self.rect = pygame.Rect(
                self.current_pos[0],
                self.current_pos[1], 
                scaled_sprite.get_width(),
                scaled_sprite.get_height()
            )

    def check_hover(self, mouse_pos):
        # Check if mouse is over card
        was_hovered = self.is_hovered
        
        # Simply check if mouse collides with card rect
        self.is_hovered = self.rect.collidepoint(mouse_pos)
            
        # If hover state changed and not targeting, update target position
        if was_hovered != self.is_hovered and not self.targeting:
            if self.is_hovered:
                # Move up and straighten when hovering
                self.target_pos.y += self.hover_y_offset
            else:
                # Return to original position when not hovering
                self.target_pos.y -= self.hover_y_offset

    def draw(self, surface):
        # Draw either normal or enlarged sprite based on hover/targeting/dragging state
        if self.is_hovered or self.targeting or self.dragging:  # Changed condition here
            # Scale down hover sprite to half size while preserving quality
            scaled_hover = pygame.transform.smoothscale(self.hover_sprite, 
                (self.hover_sprite.get_width()//2, self.hover_sprite.get_height()//2))
            surface.blit(scaled_hover,
                        (self.current_pos[0] - (scaled_hover.get_width() - self.sprite.get_width()//2) / 2,
                        self.current_pos[1]))
        else:
            # Scale down normal sprite to half size while preserving quality
            scaled_sprite = pygame.transform.smoothscale(self.sprite,
                (self.sprite.get_width()//2, self.sprite.get_height()//2))
            surface.blit(scaled_sprite, self.current_pos)

    def start_targeting(self, mouse_pos):
        """Start the targeting state instead of dragging"""
        self.targeting = True
        self.is_hovered = True  # Keep the card in hover state while targeting

    def stop_targeting(self):
        """Stop the targeting state"""
        self.targeting = False
        
    def draw_targeting_arrow(self, surface, mouse_pos):
        """Draw an arrow from the card to the mouse position"""
        if self.targeting:
            # Calculate start position (center of card)
            start_pos = (
                self.current_pos[0] + self.sprite.get_width()//4,  # Divide by 4 because sprite is scaled by 1/2
                self.current_pos[1] + self.sprite.get_height()//4
            )
            
            # Draw the line
            pygame.draw.line(surface, (255, 255, 255), start_pos, mouse_pos, 2)
            
            # Draw arrow head
            arrow_length = 20
            angle = math.atan2(mouse_pos[1] - start_pos[1], mouse_pos[0] - start_pos[0])
            
            # Calculate arrow head points
            arrow_angle = math.pi/6  # 30 degrees
            x1 = mouse_pos[0] - arrow_length * math.cos(angle + arrow_angle)
            y1 = mouse_pos[1] - arrow_length * math.sin(angle + arrow_angle)
            x2 = mouse_pos[0] - arrow_length * math.cos(angle - arrow_angle)
            y2 = mouse_pos[1] - arrow_length * math.sin(angle - arrow_angle)
            
            # Draw arrow head
            pygame.draw.polygon(surface, (255, 255, 255), [
                mouse_pos,
                (x1, y1),
                (x2, y2)
            ])

    def start_dragging(self, mouse_pos):
        """Start dragging the card"""
        self.dragging = True
        self.drag_offset = (
            self.current_pos[0] - mouse_pos[0],
            self.current_pos[1] - mouse_pos[1]
        )

    def stop_dragging(self):
        """Stop dragging the card"""
        self.dragging = False

    def modify_effect(self, effect_change, modifications):
        new_eff = {}
        for effect, details in self.effect.items():
            if effect == effect_change:
                new_magnitude = [*details]
                new_magnitude[0] += modifications
                new_eff[effect] = tuple(new_magnitude)
            else:
                new_eff[effect] = details
        self.effect = new_eff

    def get_cost(self, combat = None):
        if combat == None:
            if self.cost == 'c':
                return 6
            else: 
                return self.cost
        elif isinstance(self.cost, str):
            if self.cost == 'U':
                return 'U'
            elif self.cost == 'X':
                return combat.energy
            elif self.cost == 'c':
                return max(0, 6 - combat.curse_count())
        elif isinstance(self.combat_cost[0], int):
            return self.combat_cost[0]
        else:
            return self.cost

    def played(self):
        if isinstance(self.combat_cost[1], str):
            if self.combat_cost == 'Played':
                self.combat_cost = (None, None)

    def chaos(self):
        if self.cost not in {'U', 'X'}:
            self.combat_cost = (random.randint(0, 3), 'Combat')
    
    def cost_change(self, cost, duration):
        self.combat_cost = (cost, duration)

    def property_change(self, property, new_value):
        properties = {
            'innate': self.innate,
            'exhaust': self.exhaust,
            'retain': self.retain,
            'ethereal': self.ethereal,
            'chaotic': self.chaotic
        }
        properties[property] = new_value

    def play_x_cost(self, cost):
        for effect, details in self.effect.items():
            self.x_cost_effect[effect] = [i if i != 'X' else cost for i in details]

def create_card(card_id, card_data: tuple):
    return Card(card_id, *card_data)

def generate_card_reward(type, rareChanceOffset, numberOfOptions, character_class, rareChanceMult = 1):
    '''Function for generating card rewards
    
    ### args:
        type: type of card reward being generated
        rareChanceOffset: the rare chance offset modifier that modifies the chance of getting a rare card
        numberOfOptions: the number of card rewards to pick from
        character_class: what class the player is currently'''

    card_pool = {
        'Common': [],
        'Uncommon': [],
        'Rare': []
    }
    if character_class == 1:
        card_pool['Common'] = common_1
        card_pool['Uncommon'] = uncommon_1
        card_pool['Rare'] = rare_1

    baseRareChance = 0 # Initializing variable for base rare chance
    uncommChance = 0 # Initializing variable for uncommon chance

    if type == "normal": #base rare chance decided by combat type
        baseRareChance = 3
        uncommChance = 37
    elif type == "elite":
        baseRareChance = 10
        uncommChance = 40
    else:
        baseRareChance = 105 #guarenteed rare for boss fights
    
    baseRareChance *= rareChanceMult
    card_options = []

    for i in range(numberOfOptions): #Runs x amount of random card choices
        x = random.randrange(0, 100) #random num from 0-99 inclusive
        rareChance = baseRareChance + rareChanceOffset #calculate actual rare chance
        if x < rareChance or type == "boss": #if the random num rolled is below rare chance that means they got a rare card, or if its a boss fight
            cardPoolSel = [item for item in card_pool['Rare'] if item not in card_options] #create a pool of cards from the correct rarity and remove dupes from cards already part of the selection
            card_options.append(random.choice(cardPoolSel)) #random card chosen from the pool
            if type != "boss":
                rareChanceOffset = -5 #if its not a boss card reward, reset the rare chance offset
        elif x < uncommChance: #same as above expect for uncommons
            cardPoolSel = [item for item in card_pool['Uncommon'] if item not in card_options]
            card_options.append(random.choice(cardPoolSel))
        else:  #for commons
            cardPoolSel = [item for item in card_pool['Common'] if item not in card_options]
            card_options.append(random.choice(cardPoolSel))
            rareChanceOffset += 1 #increase the rare chance offset when ever a common card is rolled
    
    return card_options, rareChanceOffset