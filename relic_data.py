import effects
import random
import pygame
import os

class Relics: # Relic Object Class
    '''Class for the function and properties of relics
    
    ### args:
        name: name of the relic
        description: the description of the effect
        effect_type: An effect from effects.py that determains what the relic can do
        effect_class: The kind of action the effect_type does, EX: modifies values (valueMod)
        condition: The condition to be met in order to activate the effect
        consumable: whether the relic is a consumable relic
        effect_details: Arguments for the effect_type function
        targets: The entities the relic effects
        counter = None: If the relic is a counter type relic, this will be 0 when initialized
        counter_needed = None: The number the counter needs to reach to activate the relic's effect
        counter_type = None: The type of counter being used by the relic, Ex: resets per turn or global counter'''
    def __init__(self, name, description, rarity, effect_type, effect_class, condition, consumable, effect_details, targets = None, energy_relic = False, counter = None, count_needed = None, counter_type = None):
        self.name = name # Name
        self.description = description
        self.rarity = rarity
        self.effect_type = effect_type # Effect represented by a function can also be a list of effects for upon pickups effects
        self.effect_class = effect_class # Type of effect represented by a string
        self.condition = condition # Condition for the effect
        self.consumable = consumable # If the relic is one time use
        self.used = None
        if consumable == True:
            self.used = False
        self.effect_details = effect_details # The details of the effect, depends on the arguments of the effect_type
        self.targets = targets # Targets of the relic's effect, only applies to combat relics that effect entities, other relics will have None
        self.energy_relic = energy_relic
        self.counter = counter
        self.count_needed = count_needed
        self.counter_type = counter_type
        self.is_hovered = False
        self.sprite = pygame.image.load(os.path.join('assets', 'sprites', 'relics', f'{self.name}.png'))
        # Scale sprite to double size while maintaining aspect ratio
        width = self.sprite.get_width() * 2
        height = self.sprite.get_height() * 2
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 18)
        self.name_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 24)
        self.counter_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Kreon-Bold.ttf'), 22)
        self.rect = self.sprite.get_rect()


    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.description

    def hover(self):
        self.is_hovered = True

    def unhover(self):
        self.is_hovered = False

    def draw(self, screen, x, y):
        self.rect.x = x
        self.rect.y = y
        if self.is_hovered:
            screen.blit(self.sprite, (x, y))
            self.draw_description(screen, x, y)
        else:
            screen.blit(self.sprite, (x, y))
        if self.counter != None:
            # Draw counter number with black outline
            counter_text = str(self.counter)
            text_color = (255, 255, 255)  # White text
            outline_color = (0, 0, 0)     # Black outline
            
            # Position in bottom right of sprite
            text_x = x + self.sprite.get_width() - 20
            text_y = y + self.sprite.get_height() - 20
            
            # Draw black outline by offsetting text in each direction
            for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]:
                outline_surf = self.counter_font.render(counter_text, True, outline_color)
                screen.blit(outline_surf, (text_x + dx, text_y + dy))
            
            # Draw main white text
            text_surf = self.counter_font.render(counter_text, True, text_color)
            screen.blit(text_surf, (text_x, text_y))

    def draw_rect_box(self, screen):
        """Draw a rectangular box around the relic sprite"""
        # Create a rect for the sprite
        rect = pygame.Rect(self.rect.x, self.rect.y, self.sprite.get_width(), self.sprite.get_height())
        
        # Draw white rectangle outline
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

    def draw_description(self, screen, x, y):
        '''Draw a text box below the relic 
        sprite showing its description'''
        # Draw name as first line
        name_surf = self.name_font.render(self.name, True, (255, 255, 255))
        
        # Split description into 30 char lines
        desc = self.description
        lines = []
        while len(desc) > 40:
            split = desc[:40].rfind(' ')
            if split == -1:
                split = 40
            lines.append(desc[:split])
            desc = desc[split:].lstrip()
        lines.append(desc)
        
        # Create text surfaces for each line
        text_surfs = [name_surf]  # Start with name surface
        max_width = name_surf.get_width()
        total_height = name_surf.get_height()
        for line in lines:
            surf = self.font.render(line, True, (255, 255, 255))
            text_surfs.append(surf)
            max_width = max(max_width, surf.get_width())
            total_height += surf.get_height()
            
        # Calculate box dimensions
        padding = 10
        box_width = max_width + padding * 2
        box_height = total_height + padding * 2
        
        # Position box, shift left if too far
        box_x = x
        if box_x + box_width > 800:
            box_x = x - box_width
        box_y = y + self.sprite.get_height() + 5
        
        # Draw semi-transparent background
        box_surface = pygame.Surface(
            (box_width, box_height))
        box_surface.fill((0, 0, 0))
        box_surface.set_alpha(200)
        screen.blit(box_surface, (box_x, box_y))
        
        # Draw text lines
        text_y = box_y + padding
        for surf in text_surfs:
            text_x = box_x + padding
            screen.blit(surf, (text_x, text_y))
            text_y += surf.get_height()


    def valueModificationEff(self, event, context): # Method to apply the effect
        if event == self.condition and self.effect_class == 'valueMod': # Check if the condition is met 
            return self.effect_type(context, *self.effect_details) # Apply the effect
        return context # Nothing Happens
    
    def combatActionEff(self, event, combat):
        '''Handles relic effects that does an action in combat

        args: 
            event: The event occuring represented by a string
            combat: the combat object that holds all data related to a combat instance
        '''
        if self.counter == None:
            if event == self.condition and self.effect_class == 'combatAct': # Check if the condition is met 
                context = {
                    # Default info to pass on for executing effects
                    'user': combat.player, # The player is playing the card
                    'enemies': combat.enemies, # List of enemies
                    'draw': combat.draw_pile, # The draw pile
                    'discard': combat.discard_pile, # The discard pile
                    'hand': combat.hand, # the hand
                    'exhaust': combat.exhaust_pile, # The exhaust pile
                    'target': None # the target of the card, This is mainly the one that gets overrided
                }
                context['target'] = combat.player_targeting(context, self.targets)
                for i in range(0, len(self.effect_type)):
                        self.effect_type[i](*self.effect_details[i], context, combat)
        else:
            if event == self.condition and self.effect_class == 'combatAct':
                context = {
                    # Default info to pass on for executing effects
                    'user': combat.player, # The player is playing the card
                    'enemies': combat.enemies, # List of enemies
                    'draw': combat.draw_pile, # The draw pile
                    'discard': combat.discard_pile, # The discard pile
                    'hand': combat.hand, # the hand
                    'exhaust': combat.exhaust_pile, # The exhaust pile
                    'target': None # the target of the card, This is mainly the one that gets overrided
                }
                context['target'] = combat.player_targeting(context, self.targets)
                self.counter += 1
                if self.counter == self.count_needed:
                    for i in range(0, len(self.effect_type)):
                        self.effect_type[i](*self.effect_details[i], context, combat)
                    self.counter = 0

    def pickUp(self, run):
        '''Method for handling on pickup effects of relics'''
        if self.effect_class == 'pickUp':
            for i in range(0, len(self.effect_type)):
                self.effect_type[i](*self.effect_details[i], run)
    
    def eventBonus(self, event, run):
        if self.effect_class == 'eventBonus' and self.condition == event:
            self.effect_type(*self.effect_details, run)
    
    def additionalRewards(self, event, reward):
        if self.effect_class == 'additionalRewards' and self.condition == event:
            return self.effect_type(*self.effect_details, reward)
    
    def eventModifcation(self, action, run):
        if self.consumable == True:
            if self.used == True:
                return None
        if self.effect_class == 'eventMod' and self.condition == action:
            self.effect_type(*self.effect_details, run)
    
    def rewardModification(self, reward_type, additional_rewards):
        if self.effect_class == 'rewardMod':
            if reward_type in self.condition:
                return self.effect_type(*self.effect_details, additional_rewards)
        return additional_rewards

    def turnEff(self, combat):
        '''Handles relic effects that does an action in combat on specific turns

        args: 
            event: The event occuring represented by a string
            combat: the combat object that holds all data related to a combat instance
        '''
        if combat.turn == self.condition and self.effect_class == 'turnEff':
            context = {
                # Default info to pass on for executing effects
                'user': combat.player, # The player is playing the card
                'enemies': combat.enemies, # List of enemies
                'draw': combat.draw_pile, # The draw pile
                'discard': combat.discard_pile, # The discard pile
                'hand': combat.hand, # the hand
                'exhaust': combat.exhaust_pile, # The exhaust pile
                'target': None # the target of the card, This is mainly the one that gets overrided
            }
            context['target'] = combat.player_targeting(context, self.targets)
            self.effect_type(*self.effect_details, context, combat)

def createRelic(name: str, details: tuple):
    return Relics(name, *details)

def createCommon():
    '''Function to create a random common relic'''
    relic_name = random.choice(list(commonRelics.keys()))
    return Relics(relic_name, *commonRelics[relic_name])

def createUncommon():
    '''Function to create a random uncommon relic'''
    relic_name = random.choice(list(UncommonRelics.keys()))
    return Relics(relic_name, *UncommonRelics[relic_name])

def createRare():
    '''Function to create a random rare relic'''
    relic_name = random.choice(list(rareRelics.keys()))
    return Relics(relic_name, *rareRelics[relic_name])

def spawnRelic(common = 50, uncommon = 33):
    '''Function to generate a random relic for elite fights'''
    rng = random.randint(1, 100)
    if rng <= common:
        return createCommon()
    elif rng <= common + uncommon:
        return createUncommon()
    else:
        return createRare()

Relics
bossRelics = {
    'Pandora\'s Box': ('Upon pickup, Transform all Basic cards.', 1, [effects.transform_card], 'pickUp', None, False, [['Basic']], 0),
    'Astrolabe': ('Upon pickup, choose and Transfrom 3 cards, then Upgrade them.', 1, [effects.card_select, effects.transform_card, effects.upgrade_card], 'pickUp', None, False, [[3, {}], ['Selected'], ['Selected']], 0),
    'Rabbit\'s Foot': ('Elites now drop 2 relics instead of 1.', 1, effects.additonal_rewards, 'additionalRewards', 1, False, ['Relic'], 0),
    'Alchemical Workbench': ('Potion effects are doubled.', 1, 'Sacred Bark', 'Special', None, False, 'Potion', 0), 
    'Stasis Chamber': ('You no longer discard your hand at the end of your turn.', 1, [effects.combat_mechanic_change], 'pickUp', None, False, [['Turn_End_Discard', False]], 0),
    'Cursed Talisman': ('Upon pickup, obtain 1 common relic, 1 uncommon relic, 1 rare relic and a Unique Curse.', 1, [effects.add_card_to_deck, effects.generate_rewards], 'pickUp', None, False, [[21], ['Bell']], 0),
    'Eye of Eris': ('Become Confused at the start of combat. Draw 2 additional cards at the start of every turn.', 1, [effects.sneko_eye], 'combatAct', 'Turn Start', False, [[]], 0),
    'House Deed': ('Upon pickup, obtain 2 potions, gain 100 Gold. increase your Max Hp by 10, Upgrade a card and obtain a random card.', 1, [effects.upgrade_card, effects.max_hp_change, effects.generate_rewards], 'pickUp', None, False, [['Card'], [10], ['Tiny House']], 0),
    'Bag of Holding': ('Upon pickup, choose and Remove 2 cards.', 1, [effects.card_select, effects.remove_card], 'pickUp', None, False, [[2, {}], ['Selected']], 0),
    'Threat Detector': ('During Elite and Boss combats, gain 1 Energy at the start of each turn.', 1, [], None, None, False, [], 0, 'Elite'),
    'Temporal Hiccup': ('For the first 3 turns of combat, your turns are treated as the start of combat.', 1 , [effects.temporal_hiccup], 'combatAct', 'Turn Start', False, [[]], 0),
    'Coffee Mug': ('Gain 1 Energy at thes start of each turn. You can no longer Rest at Campfires.', 1, [effects.campfire_chance], 'pickUp', None, False, [['Rest']], 0, True),
    'Molten Hammer': ('Gain 1 Energy at thes start of each turn. You can no longer Upgrade at Campfires.', 1, [effects.campfire_chance], 'pickUp', None, False, [['Smith']], 0, True),
    'Erosive Slime': ('Gain 1 Energy at thes start of each turn. You can no longer gain Gold.', 1, effects.gold_amount_mod, 'valueMod', 'gold', False, [-9999], 0, True),
    'Ball n\' Chain': ('Gain 1 Energy at thes start of each turn. You can only play 6 cards per turn.', 1, [effects.card_play_limit], 'combatAct', 'Card Played', False, [[6]], 0, True, 0, 6, 'Turn'),
    'Philosopher\'s Stone': ('Gain 1 Energy at thes start of each turn. All enemies gain 1 Strength at the start of combat.', 1, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Strength'], [1]]], 3, True),
    'Holographic Eyeglass': ('Gain 1 Energy at thes start of each turn. On card reward screens, you recieve 2 less options to pick from.', 1, [effects.card_reward_option_mod], 'pickUp', None, False, [[-2]], 0, True),
    'Cursed Tome': ('Gain 1 Energy at thes start of each turn. Upon opening a non-boss chest, gain a random Curse.', 1, effects.add_card_to_deck, 'eventMod', 'Open Chest', False, ['curse'], 0, True),
    'Eye of Átē': ('Gain 1 Energy at thes start of each turn. You can no longer see enemy intent. (not recommended for unexperienced players)', 1, [effects.combat_mechanic_change], 'pickUp', None, False, [['Intent', False]], 0, True),
    'Sozu': ('Gain 1 Energy at thes start of each turn. You can no longer pickup Potions. ', 1, effects.potion_to_nothing, 'valueMod', 'potion', False, [], 0, True)
}
commonRelics = {
    'Dumbbell': ('At the start of combat, gain 1 Strength.', 4, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Strength'], [1]]], 0),
    'Smooth Stone': ('At the start of combat, gain 1 Dexterity', 4, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Dexterity'], [1]]], 0),
    'Backpack': ('Draw 2 Additional cards at the start of combat.', 4, effects.draw_cards, 'combatAct', 'Combat Start', False, [2], 0),
    'Art of War': ('If you do not play any Attacks during your turn, gain 1 additional Energy next turn.', 4, [effects.effect_for_card_type_not_played], 'combatAct', 'Turn End', False, [[[effects.apply_buff], [[0, ['Energized'], [1]]]]], 0),
    'Holy Cross': ('If you do not play any Skills during your turn, gain 1 additional Energy next turn.', 4, [effects.effect_for_card_type_not_played], 'combatAct', 'Turn End', False, [[[effects.apply_buff], [[1, ['Energized'], [1]]]]], 0),
    'Sharpening Stone': ('Upon pickup, Upgrade 2 random Attakcs.', 4, [effects.upgrade_card], 'pickUp', None, False, [['Attack', 'Attack']], 0),
    'Armour Polish': ('Upon pickup, Upgrade 2 random Skills.', 4, [effects.upgrade_card], 'pickUp', None, False, [['Skill', 'Skill']], 0),
    'Anvil': ('Upon pickup, Upgrade 2 random cards.', 4, [effects.upgrade_card], 'pickUp', None, False, [['Card', 'Card']], 0),
    'Meal Ticket': ('When you enter a Shop, heal 10 Hp.', 4, effects.heal_player, 'eventMod', 'shop', False, [10], 0),
    'Comfy Pillow': ('When you Rest, heal 15 additional Hp.', 4, effects.heal_player, 'eventMod', 'rest', False, [15], 0),
    'Lantern': ('At the start of combat, gain 1 Energy.', 4, [effects.energy_manip], 'combatAct', 'Combat Start', False, [[1]], 0),
    'Javalin': ('At the start of combat, gain 8 Vigour', 4, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Vigour'], [8]]], 0),
    'Crystal Ball': ('You can no longer encounter enemy combat in Event rooms.', 4, [effects.combat_mechanic_change], 'pickUp', None, False, [['Random_Combat', False]], 0),
    'Lucky 7': ('On turn 7, gain 17 Gold.', 4, effects.combat_gold_gain, 'turnEff', 7, False, [17], 0),
    'Coupon': ('Removing a card at a Shop always costs 50 Gold.', 4, effects.card_removal_cost_set, 'eventMod', 'removal', False, [50], 0),
    'Strawberry': ('Upon pickup, Increase Max Hp by 7.', 4, [effects.max_hp_change], 'pickUp', None, False, [[7]], 0),
    'Fancy Bottles': ('Whenever you use a potion, heal 5 Hp.', 4, effects.heal_player, 'eventBonus', 'Used Potion', False, [5], 0),
    'Nunchuck': ('After playing 10 attacks, gian 1 Energy.', 4, [effects.energy_manip], 'combatAct', 'Attack Played', False, [[1]], 0, False, 0, 10, 'global'),
    'Pen Nib': ('After playing 10 attacks, your next attack is played twice.', 4, [effects.apply_buff], 'combatAct', 'Attack Played', False, [[['Double Tap'], [1]]], 0, False, 0, 10, 'global'),
    'Anchor': ('At the start of combet, gain 10 block.', 4, [effects.block_gain_power], 'combatAct', 'Combat Start', False, [[10]], 0),
    'Potion Belt': ('Gain 2 potion slots.', 4, [effects.potion_slot_addition], 'pickUp', None, False, [[2]], 0),
    '333': ('On the third turn, draw 3 cards.', 4, effects.draw_cards, 'turnEff', 3, False, [3], 0),
    'Adventurer Pamphlet': ('Elites start with 75% of their Hp instead of full Hp.', 4, [effects.combat_mechanic_change], 'pickUp', None, False, [['Insect', True]], 0),
    'Piggy Bank': ('When you enter a room, gain 12 Gold. After spending Gold at a shop, this relic no longer works.', 4, effects.gold_gain, 'eventMod', 'Room', True, [12], 0),
    'Sunflower': ('Every 3 turns, gain 1 Energy.', 4, [effects.energy_manip], 'combatAct', 'Turn Start', False, [[1]], 0, False, 0, 3, 'global'),
    'Bronze Scales': ('At the start of combat, gain 3 thorns.', 4, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Thorns'], [3]]], 0),
    'Haunted Stone': ('At the start of combat, apply 1 Vulnerable to all enemies.', 4, [effects.apply_debuff], 'combatAct', 'Combat Start', False, [[['Vulnerable'], [1]]], 3),
    'Orichalcum': ('When you end your turn with no block, gain 6 block.', 4, [effects.no_block_buffer], 'combatAct', 'Turn End', False, [[6]], 0)
}
Relics
UncommonRelics = {
    'Horse Wagon': ('Gain 125 Gold. Your next Event room will always be a shop.', 3, [effects.gold_gain, effects.eventChange], 'pickUp', None, False, [[125], ['shop']], 0),
    'Bottled Flames': ('Upon pickup, choose an Attack card. Start combat with that card in your hand.', 3, [effects.bottle], 'pickUp', None, False, [[0]], 0),
    'Bottled Lightning': ('Upon pickup, choose an Skill card. Start combat with that card in your hand.', 3, [effects.bottle], 'pickUp', None, False, [[1]], 0),
    'Bottled Storm': ('Upon pickup, choose an Power card. Start combat with that card in your hand.', 3, [effects.bottle], 'pickUp', None, False, [[2]], 0),
    'Molten Egg': ('Whenever an Attack card is added to your deck, it is Upgraded.', 3, [effects.egg], 'pickUp', None, False, [[0]], 0),
    'Toxic Egg': ('Whenever an Skill card is added to your deck, it is Upgraded.', 3, [effects.egg], 'pickUp', None, False, [[1]], 0),
    'Frozen Egg': ('Whenever an Power card is added to your deck, it is Upgraded.', 3, [effects.egg], 'pickUp', None, False, [[2]], 0),
    'Candle': ('Curses can now be played. Playing a Curse exhausts it and causes you to lose 1 HP.', 3, [effects.combat_mechanic_change], 'pickUp', None, False, [['Playable_Curse', True]], 0),
    'Eternal Feather': ('Whenever you enter a Campfire, heal 3 Hp for every 5 cards in your deck.', 3, effects.eternal_feather, 'eventMod', 'Campfire', False, [], 0),
    'Goblin Horn': ('Whenever you kill an enemy, draw 1 card and gain 1 Energy.', 3, [effects.draw_cards, effects.energy_manip], 'combatAct', 'Lethal', False, [[1], [1]], 0),
    # 'Lucky Charm': ('The next 2 chests you open has 2 relics instead of 1.', 3),
    'Meat on a Bone': ('At the end of combat, if you are below 50% Hp, heal 12 Hp.', 3, effects.meat, 'eventMod', 'Combat End', False, [], 0),
    'Pear': ('Upon pickup, increase your Max Hp by 10.', 3, [effects.max_hp_change], 'pickUp', None, False, [[10]], 0),
    'Metal Detector': ('card rewards now have 1 extra option to choose from.', 3, [effects.card_reward_option_mod], 'pickUp', None, False, [[1]], 0),
    'Paper Clip': ('Whenever you play 3 skill cards in a single turn, deal 5 damage to all enemies.', 3, [effects.deal_damage], 'combatAct', 'Skill Played', False, [[5]], 3, False, 0, 3, 'Turn'),
    'Sands of Time': ('At the start of your turn, deal 3 damage to all enemies.', 3, [effects.deal_damage], 'combatAct', 'Turn Start', False, [[3]], 3),
    'Leather Boots': ('Every time you play 3 Attacks in a single turn, gain 1 Dexterity.', 3, [effects.apply_buff], 'combatAct', 'Attack Played', False, [[['Dexterity'], [1]]], 0, False, 0, 3, 'Turn'),
    'Leather Gloves': ('Every time you play 3 Attacks in a single turn, gain 1 Strength.', 3, [effects.apply_buff], 'combatAct', 'Attack Played', False, [[['Strength'], [1]]], 0, False, 0, 3, 'Turn'),
    'Potted Plant': ('You can now gain 5 Max Hp at a Campfire as a free action. ', 3, [effects.additional_campfire], 'pickUp', None, False, [['Potted Plant']], 0),
    'Horn Cleat': ('On your second turn, gain 14 block.', 3, effects.block_gain_power, 'turnEff', 2, False, [14], 0),
    'D10': ('For every 10 cards you play, draw 1 card.', 3, [effects.draw_cards], 'combatAct', 'Card Played', False, [[1]], 0, False, 0, 10, 'global'),
    'Cauldron': ('Enemy combat rewards always contain a potion.', 3, [effects.potion_chance_mod], 'pickUp', None, False, [[9999]], 0),
    'Ahnk': ('After playing a Power card, reduce the cost of a random card in your hand to 0 that turn.', 3, [effects.rand_card_no_cost], 'combatAct', 'Power Played', False, [[]], 0),
    'Bamboo Stilts': ('At the start of boss combat, heal 25 Hp.', 3, effects.heal_player, 'eventMod', 'Boss Start', False, [25], 0),
    'Sundial': ('Every 3 times the draw pile is shuffled, gain 2 Energy.', 3, [effects.energy_manip], 'combatAct', 'Shuffle', False, [[2]], 0, False, 0, 3, 'Global')
}
rareRelics = {
    'Brewing Stand': ('Whenever you rest, obatin a random potion.', 2, effects.generate_rewards, 'eventBonus', 'Rest', False, ['Brewing Stand'], 0),
    'Covert Cloak': ('At the start of combat, gain 1 Intangible.', 2, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Intangible'], [1]]], 0),
    'Magic Mushrooms': ('At the start of combat, gain 1 Duplicate.', 2, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Duplicate'], [1]]], 0),
    'Captain\'s Wheel': ('On the 3rd turn, gain 18 block.', 2, effects.block_gain_power, 'turnEff', 3, False, [18], 0),
    'Rusted Plate': ('At the start of combat, gain 4 plated armour.', 2, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Plated Armour'], [4]]], 0),
    'Ginger': ('You can no longer be Weakened.', 2, effects.debuff_reduction, 'valueMod', 'Weak', False, [999], 0),
    'Garlic': ('You can no longer be Frail.', 2, effects.debuff_reduction, 'valueMod', 'Frail', False, [999], 0),
    'Apple': ('Upon pickup, increase your Max Hp by 14.', 2, [effects.max_hp_change], 'pickUp', None, False, [[14]], 0),
    'Card Sleeves': ('Combats now drop 2 card rewards.', 2, effects.additonal_rewards, 'eventBonus', {0, 1, 2}, False, [['Card'], 1]),
    'Gold Bar': ('Upon pickup, gain 300 Gold.', 2, [effects.gold_gain], 'pickUp', None, False, [[300]], 0),
    'Holographic Watch': ('Whenever you play 3 or less cards in your turn, draw 3 additional cards the next turn.', 2, [effects.pocket_watch], 'combatAct', 'Turn End', False, [[3]]),
    'Cheater\'s Coat': ('Whenever you have no cards during your turn, draw 1 card.', 2, [effects.draw_cards], 'combatAct', 'Empty Hand', False, [[1]], 0),
    'Small Shield': ('You now lose a maximun of 15 block at the start of your turn.', 2, [effects.combat_mechanic_change], 'pickUp', None, False, [['Block_Loss', 15]], 0),
    'Dead Branch': ('Whenever you Exhaust a card in your hand, add a random card to your hand.', 2, [effects.add_card_to_pile], 'combatAct', 'Exhaust', False, [['hand', 'card', 1, 'na']], 0),
    '1 Up': ('At the start of combat, gain 1 Buffer.', 2, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Buffer'], [1]]], 0),
    'Dual Disk': ('At the start of combat, you may discard any amount of cards from your hand and draw that amount.', 2, [effects.gamble], 'combatAct', 'Combat Start', False, [[]], 0),
    'Divider': ('When you die, consume this relic and set your Hp to 50% instead.', 2, effects.revive, 'valueMod', 'dead', True, [50], 0),
    'Paper Shredder': ('You can now remove a card at a Campfire.', 2, [effects.additional_campfire], 'pickUp', None, False, [['Shred']], 0),
    'Drill': ('You can now dig for a relic at a Campfire.', 2, [effects.additional_campfire], 'pickUp', None, False, [['Dig']], 0),
    'Urn': ('Whenever you play a Power, heal 2 Hp.', 2, [effects.combat_heal_player], 'combatAct', 'Power Played', False, [[2]], 0),
    'Steel Rod': ('Whenever you lose Hp, lose 1 less.', 2, effects.hp_loss_reduction, 'valueMod', 'HpLoss', False, [1], 0),
    'The Arch': ('Whenever you take attack damage below or equal to 5, it is reduced to 1.', 2, effects.small_damage_reduction, 'valueMod', 'damageTaken', False, [5], 0),
    'Pot': ('Every 6 turns, gain 1 Intangible.', 2, [effects.apply_buff], 'combatAct', 'Turn Start', False, [[['Intangible'], [1]]], 0, False, 0, 6, 'global')
}
shopRelics = {
    'Treasure Map': ('Your next Event room will always be a Treasure.', 5, [effects.change_next_event], 'pickUp', None, False, [['Treasure']], 0),
    'Damaged Duplicator': ('Upon pickup, duplicate a card in your deck.', 5, [effects.card_select, effects.duplicate_card], 'pickUp', None, False, [[1, {}], ['Selected']], 0),
    'Biomechanical Arm': ('At the start of combat, gain 1 Artifact.', 5, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Artifact'], [1]]], 0),
    'The Third Eye': ('When viewing your draw pile, it is now shown in order.', 5, [effects.combat_mechanic_change], 'pickUp', None, False, [['Ordered_Draw_Pile', True]], 0),
    'Pancakes': ('Upon pickup, increase your Max Hp by 7 and heal all your Hp.', 5, [effects.max_hp_change, effects.heal_player], 'pickUp', None, False, [[7], [9999]], 0),
    'X': ('Whenever you play an X cost card, its effects are increased by 2.', 5, [effects.combat_mechanic_change], 'pickUp', None, False, [[2]], 0),
    'Costco\'s Membership Card': ('50% discount on all shop items.', 5, effects.price_discount, 'valueMod', 'Price', False, [0.5], 0),
    'Sling of Courage': ('Gain 2 Strength during Elite combats.', 5, [effects.apply_buff], 'combatAct', 'Elite Start', False, [[['Strength'], [2]]], 0),
    'Booster Pack': ('Upon pickup, gain 5 card rewards.', 5, [effects.generate_rewards], 'pickUp', None, False, [['Booster Pack']], 0),
    'Cauldron+': ('Upon pickup, Brew 5 potions.', 5, [effects.generate_rewards], 'pickUp', None, False, [['Cauldron']], 0),
    '2 Leaf Clover': ('Cards that Exhaust from being played don\'t 50% of the time.', 5, [effects.combat_mechanic_change], 'pickUp', None, False, [['Exhaust_Chance', 50]], 0),
    'Rainbow': ('At the start of combat, add a random card to your hand, it costs 0 that turn.', 5, [effects.add_card_to_pile], 'combatAct', 'Combat Start', False, [['hand', 'Card', 1, 'na']], 0),
    'Sandvich': ('Status cards can now be played, they are Exhausted when played.', 5, [effects.combat_mechanic_change], 'pickUp', None, False, [['Playable_Status', True]], 0),
    'Iron Plated Cards': ('When ever you shuffle your draw pile, gain 6 block.', 5, [effects.block_gain_power], 'combatAct', 'Shuffle', [[6]], 0)
}
eventRelics = {
    'Golden Statue': ('Gain an 15 gold at the end of combat. ', 6, effects.gold_gain, 'eventMod', 'Combat End', False, [15], 0),
    'Broken Arms': ('At the start of combat, apply 1 Weak to all enemies.', 6, [effects.apply_debuff], 'combatAct', 'Combat Start', False, [[['Weak'], [1]]], 3),
    'Christmas Present': ('Rare cards appear more often.', 6, [effects.rare_base_chance_mult], 'pickUp', None, False, [[3]], 0),
    'Steroids': ('At the start of combat, gain 3 Temporary Strength.', 6, [effects.apply_buff], 'combatAct', 'Combat Start', False, [[['Strength', 'Chained'], [3, 3]]], 0),
    'Necronomicon': ('Upon pickup, add a Necronomicurse to the deck. The first Attack you play every turn that costs 2 or more is played twice.', 6, [effects.add_card_to_deck, effects.combat_mechanic_change], 'pickUp', None, False, [[22], ['Necro', True]]),
    'Knownledge Book': ('At the start of combat, add a random Power to your hand, it costs 0 that turn.', 6, [effects.add_card_to_pile], 'combatAct', 'Combat Start', False, [['hand', 'Power', 1, (0, 'Turn')]], 0),
    'The Codex': ('At the start of the turn, you can choose 1 of 3 cards to add to your hand.', 6, [effects.discover], 'combatAct', 'Turn Start', False, [['Card', 'na']], 0),
    'Heart Disease': ('You can no longer heal.', 6, effects.healing_reduction, 'valueMod', 'Healing', False, [9999], 0),
    'Strange Mushroom': ('At the start of combat, add a random card of any class to your hand, it costs 0 this turn. ', 6, [effects.add_card_to_pile], 'combatAct', 'Combat Start', False, [['hand', 'Card', 1, (0, 'Turn')]])
}
