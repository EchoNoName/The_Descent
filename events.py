import relic_data
import enemy_data
import card_constructor
import potion_data
import effects
import random

class ScorchedForest:
    def __init__(self, player, run):
        self.name = 'Scorched Forest'
        self.player = player
        self.run = run
        self.event_active = True
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('As you wander through the thick forest, the air suddenly grows hot, and the scent of burning wood fills your nostrils. You come upon a clearing, blackened by fire, where flames still dance hungrily on the remnants of trees.')
        # Normal text
        print('In the center of the grove, a strange figure looms—an ember-wreathed dryad, her fiery eyes watching you intently. She extends a charred hand toward you, her voice crackling like the flames:')
        # Normal Text
        print('\"These flames cleanse and destroy... but they also forge and strengthen. Will you step into the fire to claim its gifts, or will you turn away?\"')
        # slanted text
        self.choose_your_path()

    def choose_your_path(self):
        print('[Gold for the burning!] Lose 8 HP, gain 75 gold. ')
        print('[Brewed in flame!] Lose 8 HP, gain a random potion. ')
        print('[Strength through suffering!] Lose 8 HP, gain a random card. ')
        print('[This is not my path.] Nothing happens. ')
        choice = int(input())
        if choice == 1:
            self.player.hp_loss(8)
            self.run.gold_modification(75)
            print('The flames lick at your skin as you reach into the inferno. When you withdraw, your hands clutch a small pouch of seared coins.')
        elif choice == 2:
            self.player.hp_loss(8)
            self.run.generate_reward_screen_instance(False, {'Potions': [potion_data.randomPotion()]})
            print('You plunge your hand into the inferno and withdraw a small, smoking vial. The liquid inside swirls with a fiery glow.')
        elif choice == 3:
            self.player.hp_loss(8)
            card_reward, self.run.rareChanceOffset = card_constructor.generate_card_reward('normal', self.run.rareChanceOffset, self.run.cardRewardOptions, self.player.character_class, self.run.rareChanceMult)
            self.run.generate_reward_screen_instance(False, {'Cards': [card_reward]})
            self.run.reward.listRewards()
            print('The fire engulfs you momentarily, and when it subsides, you find yourself holding a scorched card pulsing with latent power.')
        elif choice == 4:
            print('The dryad watches silently as you turn away, her fiery gaze burning into your back until you\'re out of sight.')
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
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('In the heart of the forest, you stumble upon a strange sight. Gnarled vines twist and writhe unnaturally, encasing what appears to be a faintly glowing object. The treasure’s shape is obscured, but its allure is undeniable. As you approach, the vines shift, tightening protectively around the prize.')
        # Normal text
        print('A soft whisper echoes in your mind: ')
        # Normal Text
        print('\""Do you desire what lies within? It will not yield easily... but perhaps your persistence will prove worthy.\" ')
        # slanted text
        print('The vines seem alive, pulsing faintly as if waiting for your decision. ')
        self.choose_your_path()

    def choose_your_path(self):
        print('[Reach Inside] Lose 3 HP. 25% chance to find a Relic. ')
        print('[Leave.] Nothing happens. ')
        choice = int(input())
        if choice == 1:
            self.player.hp_loss(3)
            print('You plunge your hand into the writhing mass. The vines lash at you, cutting into your skin as you grope blindly for the treasure...')
            rng = random.randint(1, 100)
            if rng <= 25:
                self.run.relic_pickup(relic_data.spawnRelic())
                print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
            else:
                print('The vines slap your hand away, leaving only pain for your effort. The treasure remains tantalizingly out of reach.')
                print('[Reach Inside] Lose 4 HP. 35% chance to find a Relic. ')
                print('[Leave.] Nothing happens. ')
                choice = int(input())
                if choice == 1:
                    self.player.hp_loss(4)
                    print('The vines seem to grow angrier, their lashes biting deeper into your skin. You try again, determined to claim the treasure. ')
                    rng = random.randint(1, 100)
                    if rng <= 35:
                        self.run.relic_pickup(relic_data.spawnRelic())
                        print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
                    else:
                        print('The vines slap your hand away, leaving only pain for your effort. The treasure remains tantalizingly out of reach.')
                        print('[Reach Inside] Lose 5 HP. 45% chance to find a Relic. ')
                        print('[Leave.] Nothing happens. ')
                        choice = int(input())
                        if choice == 1:
                            self.player.hp_loss(5)
                            rng = random.randint(1, 100)
                            if rng <= 45:
                                self.run.relic_pickup(relic_data.spawnRelic())
                                print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
                            else:
                                print('The vines slap your hand away, leaving only pain for your effort. The treasure remains tantalizingly out of reach.')
                                print('[Reach Inside] Lose 6 HP. 55% chance to find a Relic. ')
                                print('[Leave.] Nothing happens. ')
                                choice = int(input())
                                if choice == 1:
                                    self.player.hp_loss(6)
                                    rng = random.randint(1, 100)
                                    if rng <= 55:
                                        self.run.relic_pickup(relic_data.spawnRelic())
                                        print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
                                    else:
                                        print('The vines slap your hand away, leaving only pain for your effort. The treasure remains tantalizingly out of reach.')
                                        print('[Reach Inside] Lose 7 HP. 65% chance to find a Relic. ')
                                        print('[Leave.] Nothing happens. ')
                                        choice = int(input())
                                        if choice == 1:
                                            self.player.hp_loss(7)
                                            rng = random.randint(1, 100)
                                            if rng <= 65:
                                                self.run.relic_pickup(relic_data.spawnRelic())
                                                print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
                                            else:
                                                print('The vines slap your hand away, leaving only pain for your effort. The treasure remains tantalizingly out of reach.')
                                                print('[Reach Inside] Lose 8 HP. 75% chance to find a Relic. ')
                                                print('[Leave.] Nothing happens. ')
                                                choice = int(input())
                                                if choice == 1:
                                                    self.player.hp_loss(8)
                                                    rng = random.randint(1, 100)
                                                    if rng <= 75:
                                                        self.run.relic_pickup(relic_data.spawnRelic())
                                                        print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
                                                    else:
                                                        print('The vines slap your hand away, leaving only pain for your effort. The treasure remains tantalizingly out of reach. ')
                                                        print('[Reach Inside] Lose 9 HP. 85% chance to find a Relic. ')
                                                        print('[Leave.] Nothing happens. ')
                                                        choice = int(input())
                                                        if choice == 1:
                                                            self.player.hp_loss(9)
                                                            rng = random.randint(1, 100)
                                                            if rng <= 85:
                                                                self.run.relic_pickup(relic_data.spawnRelic())
                                                                print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
                                                            else:
                                                                print('The vines slap your hand away, leaving only pain for your effort. The treasure remains tantalizingly out of reach. ')
                                                                print('[Reach Inside] Lose 10 HP. 100% chance to find a Relic. ')
                                                                print('[Leave.] Nothing happens. ')
                                                                choice = int(input())
                                                                if choice == 1:
                                                                    self.player.hp_loss(10)
                                                                    self.run.relic_pickup(relic_data.spawnRelic())
                                                                    print('Your fingers close around a cold, solid object, and with a sharp tug, you wrench it free. The vines hiss angrily as the treasure is revealed: a Relic of unmistakable power.')
                                                                elif choice == 2:
                                                                    print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
                                                        elif choice == 2:
                                                            print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
                                                elif choice == 2:
                                                    print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
                                        elif choice == 2:
                                            print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
                                elif choice == 2:
                                    print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
                        elif choice == 2:
                            print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
                elif choice == 2:
                    print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
        elif choice == 2:
            print('You turn away, leaving the mysterious treasure behind. The whispers fade, and the vines settle back into stillness.')
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
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('A strange blue humanoid with a golden helm(?) approaches you with a huge smile. ')
        # Normal text
        print('\"Hello friend! I am Cleric! Are you interested in my services?!\" the creature shouts, loudly.')
        # Normal Text
        self.choose_your_path()

    def choose_your_path(self):
        print('[Heal] Lose 35 Gold. Heal 25% of your Max HP. ')
        print('[Purify] Lose 50 Gold. Remove a card from your deck. ')
        print('[Leave] Nothing happens. ')
        while True:
            choice = int(input())
            if choice == 1 and self.player.gold >= 35:
                self.run.gold_modification(-35)
                effects.heal_player(int(self.player.maxHp * 0.25), self.run)
                print('A warm golden light envelops your body and dissipates. ')
                print('The creature grins.')
                print('Cleric: \"Cleric best healer. Have a good day!\"')
            elif choice == 2 and self.player.gold >= 50:
                self.run.gold_modification(-50)
                effects.card_select(1, {}, self.run)
                self.player.deck.remove(self.player.selected_cards)
                print('A cold blue flame envelops your body and dissipates. ')
                print('The creature grins.')
                print('Cleric: \"Cleric talented. Have a good day!\"')
            elif choice == 3:
                print('You don\'t trust this \"Cleric\", so you leave.')
                break
            else:
                print('Invalid Choice')
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
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('As you wander deeper into the forest, the trees part to reveal a clearing bathed in soft, ethereal light. In the center stands a towering statue of a serene goddess, her expression calm and unjudging. Her hands are clasped in prayer, and an ancient plaque at her feet reads: ')
        # Normal text
        print('\"Offer your burdens to the goddess, and she shall grant you freedom.\"')
        # Slanted
        print('You feel an inexplicable pull toward the statue, though the air grows heavy with the weight of what you might lose. ')
        self.choose_your_path()

    def choose_your_path(self):
        print('[Pray] Lose 7 HP. Remove a card from your deck. ')
        print('[Leave] Nothing happens. ')
        choice = int(input())
        if choice == 1:
            self.player.hp_loss(7)
            effects.card_select(1, {}, self.run)
            self.player.deck.remove(self.player.selected_cards)
            print('You kneel before the statue and press your hand to its cold, weathered surface. A warmth spreads through your body as a shimmering light envelops you. You feel a burden lift—a card you no longer need is gone.')
        elif choice == 2:
            print('You bow respectfully to the statue and step away. The clearing remains tranquil, the goddess watching silently as you depart.')
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
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('You emerge into a secluded grove where an ancient monument stands, weathered but still imposing. Vines creep along its crumbling stone base, yet one feature remains untouched: a gleaming golden statue at its peak. The figure shimmers unnaturally, as if resisting the ravages of time. ')
        # Normal text
        print('The air grows tense, and you can’t shake the feeling that the monument is watching you.')
        self.choose_your_path()

    def choose_your_path(self):
        print('[Take] Obtain Golden Statue. Trigger a trap. ')
        print('[Leave] Nothing happens. ')
        choice = int(input())
        if choice == 1:
            self.run.relic_pickup(relic_data.createRelic('Golden Statue', relic_data.eventRelics['Golden Statue']))
            print('As you grab the statue and stow it away, a deep rumble shakes the monument. Hidden mechanisms spring to life, and deadly traps activate around you! ')
            print(f'[Dodge] Lose {int(self.player.maxHp * 0.08)} Max HP. ')
            print('[Tank] Become Cursed - Injury. ')
            print(f'[Run] Take {int(self.player.maxHp * 0.25)} damage. ')
            choice = int(input())
            if choice == 1:
                amount = int(self.player.maxHp * 0.08) * -1
                effects.max_hp_change(amount, self.run)
                print('RUUUUUUUUUUN!')
                print('You barely leap into a side passageway, dodging the arrows fly all over the place. Unfortunately it feels like you sprained something however.')
            elif choice == 2:
                self.run.card_pickup_from_id(4)
                print('You brace for impact, and as the dust settles, you make your way out of the monument, injured. ')
            elif choice == 3:
                self.player.hp_loss(int(self.player.maxHp * 0.25))
                print('You look for the nearest cover and hide behind it, managing to get away with minor injury. ')
        elif choice == 2:
            print('You resist the lure of the golden statue, stepping back cautiously. As you leave, the monument\'s warning lingers in your mind, its gleaming treasure untouched.')
        self.end_event()
    
    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class DeadAdventurers:
    def __init__(self, player, run):
        self.name = 'Dead Adventurers'
        self.player = player
        self.run = run
        self.event_active = True
        self.elite = None
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('As you walk on the path towards your destination, you come a across a group of dead adventures on the side. ')
        # Normal text
        rng = random.randint(1, 3)
        if rng == 1:
            print('Their pants has been stolen! Also, the armour and face appear to be scoured by flames. ')
            self.elite = 'Sentries'
        elif rng == 2:
            print('Their pants has been stolen! Also, they look to have been eviscerated and chopped by giant blades. ')
            self.elite = 'Goblin Giant'
        elif rng == 3:
            print('Their pants has been stolen! Also, purple liquid leaks from giant bite marks on their bodies. ')
            self.elite = 'Giant Louse'
        self.choose_your_path()

    def choose_your_path(self):
        loot = ['Gold', 'N']
        possbible_fights = {
            'Sentries': [enemy_data.SentryA(), enemy_data.SentryB(), enemy_data.SentryA()],
            'Goblin Giant': [enemy_data.GoblinGiant()],
            'Giant Louse': [enemy_data.GiantLouseAwake()]
        }
        print('[Search] Find Loot. 25% that an Elite will return to fight you. ')
        print('[Escape] End the search and resume your journey. ')
        choice = int(input())
        if choice == 1:
            rng = random.randint(1, 100)
            if rng <= 75:
                item = random.choice(loot)
                loot.remove(item)
                if item == 'N':
                    print('Hmm, couldn\'t find anything...')
                elif item == 'Gold':
                    self.run.gold_modification(30)
                    print('You found some gold!')
                print('[Search] Find Loot. 50% that an Elite will return to fight you. ')
                print('[Escape] End the search and resume your journey. ')
                choice = int(input())
                if choice == 1:
                    rng = random.randint(1, 100)
                    if rng <= 50:
                        item = random.choice(loot)
                        loot.remove(item)
                        loot.append('Relic')
                        if item == 'N':
                            print('Hmm, couldn\'t find anything...')
                        elif item == 'Gold':
                            self.run.gold_modification(30)
                            print('You found some gold!')
                        print('[Search] Find Loot. 75% that an Elite will return to fight you. ')
                        print('[Escape] End the search and resume your journey. ')
                        choice = int(input())
                        if choice == 1:
                            rng = random.randint(1, 100)
                            if rng <= 25:
                                item = random.choice(loot)
                                loot.remove(item)
                                if item == 'N':
                                    print('Hmm, couldn\'t find anything...')
                                elif item == 'Gold':
                                    self.run.gold_modification(30)
                                    print('You found some gold!')
                                elif item == 'Relic':
                                    relic = relic_data.spawnRelic()
                                    self.run.relic_pickup(relic)
                                    print('You found a relic!!')
                                print('Looks like you searched all his belongings without a hitch!')
                            else:
                                print('While searching the adventurer you are caught off guard!')
                                self.run.generage_combat_instace(possbible_fights[self.elite], 'Elite')
                                start = input('[Continue]')
                                self.run.start_combat()
                        elif choice == 2:
                            print('You leave without a sound. ')
                    else:
                        print('While searching the adventurer you are caught off guard!')
                        self.run.generage_combat_instace(possbible_fights[self.elite], 'Elite')
                        start = input('[Continue]')
                        self.run.start_combat()
                elif choice == 2:
                    print('You leave without a sound. ')
            else:
                print('While searching the adventurer you are caught off guard!')
                self.run.generage_combat_instace(possbible_fights[self.elite], 'Elite')
                start = input('[Continue]')
                self.run.start_combat()
        elif choice == 2:
            print('You leave without a sound. ')
        self.end_event()
    
    def end_event(self):
        self.event_active = False
        self.run.mapNav()


class ColouredMushrooms:
    def __init__(self, player, run):
        self.name = 'Coloured Mushrooms'
        self.player = player
        self.run = run
        self.event_active = True
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('You enter a area full of hypnotizing colored mushrooms. ')
        print('Due to your lack of specialization in mycology you are unable to identify the specimens. ')
        print('You want to escape, but feel oddly compelled to eat a mushroom.')
        # Text related to mushroom are coloured
        self.choose_your_path()

    def choose_your_path(self):
        print('[Stomp] Anger the Mushrooms. ')
        print('[Eat] Heal 25% HP. Become Cursed: Parasite. ')
        choice = int(input())
        if choice == 1:
            print('Ambushed!!')
            # Red Text
            print('Corpes infested by the mushrooms appear out of nowhere! ')
            start = input('[Continue]')
            self.run.generage_combat_instace([enemy_data.InfestedCorpes(), enemy_data.InfestedCorpes(), enemy_data.InfestedCorpes()], 'normal')
            gold = random.randint(10, 20)
            cards, self.run.rareChanceOffset = card_constructor.generate_card_reward('normal', self.run.rareChanceOffset, self.run.cardRewardOptions, self.player.character_class)
            potions = []
            rng = random.randint(1, 100)
            if rng <= self.run.potionChance:
                potion = potion_data.randomPotion()
                potions.append(potion)
                self.run.potionChance -= 10
            else:
                self.run.potionChance += 20
            self.run.start_combat({'Gold': gold, 'Cards': [cards], 'Potions': potions, 'Relics': [relic_data.createRelic('Strange Mushroom', relic_data.eventRelics['Strange Mushroom'])]})
        elif choice == 2:
            self.player.hp_recovery(int(self.player.maxHp * 0.25))
            print('You give in to the unnatural desire to eat. As you consume mushroom after mushroom, you feel yourself entering into a daze and pass out. As you awake, you feel very odd. ')
            print('You Heal 25% of your HP, but you also get infected. ')
            # infected is coloured red
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
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('As you tread deeper into the forest, a dense fog begins to roll in, swirling around your feet and creeping into your lungs. The world around you warps and twists—the trees seem to breathe, the ground pulses like a heartbeat, and whispers echo from unseen figures in the mist. ')
        # Normal text
        print('A voice, soft and disorienting, speaks directly into your mind: ')
        # Normal Text
        print('\"Lost traveler, the fog can reshape what is... if you dare to let it touch you. Will you embrace the change, or will you turn away?\"')
        # slanted text
        print('You blink, and suddenly your weapons and armour glimmers in your mind\'s eye, the items shifting and morphing as if alive.')
        self.choose_your_path()

    def choose_your_path(self):
        print('[Embrace Change] Transform a card. ')
        print('[Shed the Old] Remove a card. ')
        print('[Forge Through] Upgrade a card. ')
        choice = int(input())
        if choice == 1:
            effects.card_select(1, {}, self.run)
            self.player.transform_card()
            print('The fog envelops you, its edges blurring and shifting as it twists into something new. The whispers in the mist grow louder before abruptly ceasing, leaving behind an unfamiliar power in your hands. ')
        elif choice == 2:
            effects.card_select(1, {}, self.run)
            self.player.remove_card()
            print('The fog swirls around you, then turning it into nothingness. A faint sense of relief washes over you, as though a burden you didn\'t realize you carried has vanished. ')
        elif choice == 3:
            effects.card_select(1, {}, self.run)
            self.player.upgrade_card()
            print('The fog clings to one of your items, its energy intensifying as it glows brighter and stronger. When the fog lifts, the item gleams with newfound power. ')
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
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('As you reach an enclosure in the forest, You find a shimmering mass of light at the center of a circle of trees. ')
        # Normal text
        print('Its warm glow and enchanting patterns invite you in. ')
        # Normal Text
        self.choose_your_path()

    def choose_your_path(self):
        print(f'[Enter] Upgrade 2 random cards. Take {int(self.player.maxHp * 0.2)} damage. ')
        print('[Leave] Nothing happens. ')
        choice = int(input())
        if choice == 1:
            print('As you walk through the light, you notice that the light is absorbed into you. ')
            print('It\'s scorching hot! However, the pain quickly recedes.')
            # scorching hot is read
            print('You feel invigorated, as though you received a well deserved slap. ')
            # Invigorated is blue
            self.player.hp_loss(int(self.player.maxHp * 0.2))
            self.player.upgrade_card(['Card', 'Card'])
        elif choice == 2:
            print('You walk around it, wondering what could have been. ')
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
    
    def __str__(self):
        return self.name
    
    def start_event(self):
        print('You fall into a puddle. ')
        # Normal text
        print('IT\'S MADE OF SLIME GOOP!! ')
        # Slime goop is green
        print('Frantically, you claw yourself out over several minutes as you feel the goop starting to burn. ')
        print('You can feel goop in your ears, goop in your nose, goop everywhere. ')
        print('Climbing out, you notice that some of your gold is missing. Looking back to the puddle you see your missing coins combined with gold from unfortunate adventurers mixed together in the puddle. ')
        self.choose_your_path()

    def choose_your_path(self):
        gold_loss = max(random.randint(20, 50), self.player.gold)
        print(f'[Gather Gold] Gain 75 Gold. Lose 11 HP.')
        print(f'[Leave it] Lose {gold_loss} gold. ')
        choice = int(input())
        if choice == 1:
            print('Feeling the sting of the goop as the prolonged exposure starts to melt away at your skin, you manage to fish out the gold. ')
            self.player.hp_loss(11)
            self.run.gold_modification(75)
        elif choice == 2:
            print('You decide that mess is not worth it. ')
        self.end_event()
    
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