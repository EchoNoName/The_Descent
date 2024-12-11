import effects

class Relics: # Relic Object Class
    '''Class for the function and properties of relics
    
    ### args:
    name: name of the relic
    effect_type: An effect from effects.py that determains what the relic can do
    effect_class: The kind of action the effect_type does, EX: modifies values (valueMod)
    condition: The condition to be met in order to activate the effect
    consumable: whether the relic is a consumable relic
    effect_details: Arguments for the effect_type function
    targets: The entities the relic effects
    counter = None: If the relic is a counter type relic, this will be 0 when initialized
    counter_needed = None: The number the counter needs to reach to activate the relic's effect
    counter_type = None: The type of counter being used by the relic, Ex: resets per turn or global counter'''
    def __init__(self, name, effect_type, effect_class, condition, consumable, effect_details, targets, counter = None, count_needed = None, counter_type = None):
        self.name = name # Name
        self.effect_type = effect_type # Effect represented by a function can also be a list of effects for upon pickups effects
        self.effect_class = effect_class # Type of effect represented by a string
        self.condition = condition # Condition for the effect
        self.consumable = consumable # If the relic is one time use
        self.used = None
        if consumable == True:
            self.used = False
        self.effect_details = effect_details # The details of the effect, depends on the arguments of the effect_type
        self.targets = targets # Targets of the relic's effect, only applies to combat relics that effect entities, other relics will have None
        self.counter = counter
        self.count_needed = count_needed
        self.counter_type = counter_type
    
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
        context['target'] = combat.player_targeting(self.targets)
        if self.counter != None:
            if event == self.condition and self.effect_class == 'combatAct': # Check if the condition is met 
                self.effect_type(*self.effect_details, context, combat)
        else:
            if event == self.condition:
                self.counter += 1
                if self.counter == self.count_needed:
                    self.effect_type(*self.effect_details, context, combat)
                    self.counter = 0

    def pickUp(self, player):
        '''Method for handling on pickup effects of relics'''
        if self.effect_class == 'pickUp':
            for i in range(0, len(self.effect_type)):
                self.effect_type[i](*self.effect_details[i], player)
    
    def eventBonus(self, event, player):
        if self.effect_class == 'eventBonus' and self.condition == event:
            self.effect_type(*self.effect_details, player)
    
    

relicsList = {
    'Pandora\'s Box': ('Upon pickup, Transform all Basic cards.', 1),
    'Astrolabe': ('Upon pickup, choose and Transfrom 3 cards, then Upgrade them.', 1),
    'Rabbit\'s Foot': ('Elites now drop 2 relics instead of 1.', 1),
    'Alchemical Workbench': ('Potion effects are doubled.', 1), 
    'Stasis Chamber': ('You no longer discard your hand at the end of your turn.', 1),
    'Cursed Talisman': ('Upon pickuup, obtain 1 common relic, 1 uncommon relic, 1 rare relic and a Unique Curse.', 1),
    'Eye of Eris': ('Become Confused at the start of combat. Draw 2 additional cards at the start of every turn.', 1),
    'House Deed': ('Upon pickup, obtain 2 potions, gain 100 Gold. increase your Max Hp by 10, Upgrade a card and obtain a random card.', 1),
    'Bag of Holding': ('Upon pickup, choose and Remove 2 cards.', 1),
    'Threat Detector': ('During Elite and Boss combats, gain 1 Energy at the start of each turn.', 1),
    'Temporal Hiccup': ('For the first 3 turns of combat, your turns are treated as the start of combat.', 1 ),
    'Coffee Mug': ('Gain 1 Energy at thes start of each turn. You can no longer Rest at Campfires.', 1),
    'Molten Hammer': ('Gain 1 Energy at thes start of each turn. You can no longer Upgrade at Campfires.', 1),
    'Erosive Slime': ('Gain 1 Energy at thes start of each turn. You can no longer gain Gold.', 1),
    'Ball n\' Chain': ('Gain 1 Energy at thes start of each turn. You can only play 6 cards per turn.', 1),
    'Philosopher\'s Stone': ('Gain 1 Energy at thes start of each turn. All enemies gain 1 Strength at the start of combat.', 1),
    'Holographic Eyeglass': ('Gain 1 Energy at thes start of each turn. On card reward screens, you recieve 2 less options to pick from.', 1),
    'Cursed Tome': ('Gain 1 Energy at thes start of each turn. Upon opening a non-boss chest, gain a random Curse.', 1),
    'Eye of Átē': ('Gain 1 Energy at thes start of each turn. You can no longer see enemy intent. (not recommended for unexperienced players)', 1),
    'Dumbbell': ('At the start of combat, gain 1 Strength.', 4),
    'Smooth Stone': ('At the start of combat, gain 1 Dexterity', 4),
    'Backpack': ('Draw 2 Additional cards at the start of combat.', 4),
    'Art of War': ('If you do not play any Attacks during your turn, gain 1 additional Energy next turn.', 4),
    'Holy Cross': ('If you do not play any Skills during your turn, gain 1 additional Energy next turn.', 4),
    'Omamori': ('Negate the next 2 Curses you obtain.', 4),
    'Sharpening Stone': ('Upon pickup, Upgrade 2 random Attakcs.', 4),
    'Armour Polish': ('Upon pickup, Upgrade 2 random Skills.', 4),
    'Anvil': ('Upon pickup, Upgrade 2 random cards.', 4),
    'Meal Ticket': ('When you enter a Shop, heal 10 Hp.', 4),
    'Comfy Pillow': ('When you Rest, heal 15 additional Hp.', 4),
    'Lantern': ('At the start of combat, gain 1 Energy.', 4),
    'Javalin': ('At the start of combat, gain 8 Vigour', 4),
    'Crystal Ball': ('You can no longer encounter enemy combat in Event rooms.', 4),
    'Lucky 7': ('On turn 7, gain 17 Gold.', 4),
    'Coupon Sheet': ('Removing a card at a Shop always costs 50 Gold.', 4),
    'Strawberry': ('Upon pickup, Increase Max Hp by 7.', 4),
    'Fancy Bottles': ('Whenever you use a potion, heal 5 Hp.', 4),
    'Nunchuck': ('After playing 10 attacks, gian 1 Energy.', 4),
    'Pen Nib': ('After playing 10 attacks, your next attack does double damage.', 4),
    'Anchor': ('At the start of combet, gain 10 block.', 4),
    'Potion Belt': ('Gain 2 potion slots.', 4),
    'Ritual Dagger': ('The first time you lose Hp each combat, draw 3 cards.', 4),
    'Adventurer Pamphlet': ('Elites start with 75% of their Hp instead of full Hp.', 4),
    'Piggy Bank': ('When you enter a room, gain 12 Gold. After spending Gold at a shop. this relic no longer works.', 4),
    'Sunflower': ('Every 3 turns, gain 1 Energy.', 4),
    'Bronze Scales': ('At the start of combat, gain 3 thorns.', 4),
    'Haunted Stone': ('At the start of combat, apply 1 Vulnerable to all enemies.', 4),
    'Orichalcum': ('When you end your turn with no block, gain 6 block.', 4),
    'Horse Wagon': ('Gain 125 Gold. Your next Event room will always be a shop.', 3),
    'Bottled Flames': ('Upon pickup, choose an Attack card. Start combat with that card in your hand.', 3),
    'Bottled Lightning': ('Upon pickup, choose an Skill card. Start combat with that card in your hand.', 3),
    'Bottled Storm': ('Upon pickup, choose an Power card. Start combat with that card in your hand.', 3),
    'Molten Egg': ('Whenever an Attack card is added to your deck, it is Upgraded.', 3),
    'Toxic Egg': ('Whenever an Skill card is added to your deck, it is Upgraded.', 3),
    'Frozen Egg': ('Whenever an Power card is added to your deck, it is Upgraded.', 3),
    'Candle': ('Curses can now be played. Playing a Curse exhausts it and causes you to lose 1 HP.', 3),
    'Eternal Feather': ('Whenever you enter a Campfire, heal 3 Hp for every 5 cards in your deck.', 3),
    'Goblin Horn': ('Whenever you kill an enemy, draw 1 card and gain 1 Energy.', 3),
    'Lucky Charm': ('The next 2 chests you open has 2 relics instead of 1.', 3),
    'Meat on a Bone': ('At the end of combat, if you are below 50% Hp, heal 12 Hp.', 3),
    'Pear': ('Upon pickup, increase your Max Hp by 10.', 3),
    'Metal Detector': ('card rewards now have 1 extra option to choose from.', 3),
    'Paper Clip': ('Whenever you play 3 skill cards in a single turn, deal 5 damage to all enemies.', 3),
    'Sands of Time': ('At the start of your turn, deal 3 damage to all enemies.', 3),
    'Leather Boots': ('Every time you play 3 Attacks in a single turn, gain 1 Dexterity.', 3),
    'Leather Gloves': ('Every time you play 3 Attacks in a single turn, gain 1 Strength.', 3),
    'Potted Plant': ('When adding a card to your deck, you may gain 2 Max Hp instead.', 3),
    'Horn Cleat': ('On your second turn, gain 14 block.', 3),
    'D10': ('For every 10 cards you play, draw 1 card.', 3),
    'Cauldron': ('Enemy combat rewards always contain a potion.', 3),
    'Ahnk': ('After playing a Power card, reduce the cost of a random card in your hand to 0 that turn.', 3),
    'Bamboo Stilts': ('At the start of boss combat, heal 25 Hp.', 3),
    'Sundial': ('Every 3 times the draw pile is shuffled, gain 2 Energy.', 3),
    'Midas\'s Hand': ('Upon killing an enemy, gain Gold equal to overkill damage done.', 2),
    'Brewing Stand': ('Whenever you rest, obatin a random potion.', 2),
    'Covert Cloak': ('At the start of combat, gain 1 Intangable.', 2),
    'Magic Mushrooms': ('At the start of combat, gain 1 Duplicate.', 2),
    'Captain\'s Wheel': ('On the 3rd turn, gain 18 block.', 2),
    'Rusted Plate': ('At the start of combat, gain 4 plated armour.', 2),
    'Ginger': ('You can no longer be Weakened.', 2),
    'Garlic': ('You can no longer be Frail.', 2),
    'Apple': ('Upon pickup, increase your Max Hp by 14.', 2),
    'Card Sleeves': ('Normal enemies now drop 2 card rewards.', 2),
    'Gold Bar': ('Upon pickup, gain 300 Gold.', 2),
    'Voodoo Doll': ('At the start of combat, gain 1 Strength for every Curse in your deck.', 2),
    'Holographic Watch': ('Whenever you play 3 or less cards in your turn, draw 3 additional cards the next turn.', 2),
    'Cheater\'s Coat': ('Whenever you have no cards during your turn, draw 1 card.', 2),
    'Small Shield': ('You now lose a maximun of 15 block at the start of your turn.', 2),
    'Dead Branch': ('Whenever you Exhaust a card in your hand, add a random card to your hand.', 2),
    '1 Up': ('At the start of combat, gain 1 Buffer.', 2),
    'Dual Disk': ('At the start of combat, you may discard any amount of cards from your hand and draw that amount.', 2),
    'Divider': ('When you die, consume this relic and set your Hp to 50% instead.', 2),
    'Paper Shredder': ('You can now remove a card at a Campfire.', 2),
    'Drill': ('You can now dig for a relic at a Campfire.', 2),
    'Urn': ('Whenever you play a Power, heal 2 Hp.', 2),
    'Ballistic Armour': ('Whenever you lose Hp, lose 1 less.', 2),
    'The Arch': ('Whenever you take attack damage below or equal to 5, it is reduced to 1.', 2),
    'Pot': ('Every 6 turns, gain 1 Intangible.', 2),
    'Treasure Map': ('Your next Event room will always be a Chest.', 5),
    'Damaged Duplicator': ('Upon pickup, duplicate a card in your deck.', 5),
    'Biomechanical Arm': ('At the start of combat, gain 1 Artifact.', 5),
    'The Third Eye': ('When viewing your draw pile, it is now shown in order.', 5),
    'Pancakes': ('Upon pickup, increase your Max Hp by 7 and heal all your Hp.', 5),
    'X': ('Whenever you play an X cost card, its effects are increased by 2.', 5),
    'Costco\'s Membership Card': ('50% discount on all shop items.', 5),
    'Sling of Courage': ('Gain 2 Strength during Elite combats.', 5),
    'Booster Pack': ('Upon pickup, gain 5 card rewards.', 5),
    'Cauldron+': ('Upon pickup, Brew 5 potions.', 5),
    '2 Leaf Clover': ('Cards that Exhaust from being played don\'t 50% of the time.', 5),
    'Rainbow': ('At the start of combat, add a non-class card to your hand, it costs 0 that turn.', 5),
    'Sandvich': ('Status cards can now be played, they are Exhausted when played.', 5),
    'Iron Plated Cards': ('When ever you shuffle your draw pile, gain 6 block.', 5),
    'Broken Arms': ('At the start of combat, apply 1 Weak to all enemies.', 6),
    'Christmas Present': ('Rare cards appear more often.', 6),
    'Steroids': ('At the start of combat, gain 3 Temporary Strength.', 6),
    'Necronomicon': ('Upon pickup, add a Necronomicurse to the deck. The first Attack you play every turn that costs 2 or more is played twice.', 6),
    'Knownledge Book': ('At the start of combat, add a random Power to your hand, it costs 0 that turn.', 6),
    'The Codex': ('At the end of the turn, you can choose 1 of 3 cards to add to your discard pile.', 6),
    'Heart Disease': ('You can no longer heal.', 6)
}