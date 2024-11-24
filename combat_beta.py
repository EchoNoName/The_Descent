import effects
import random

class Combat():
    def __init__(self, player, deck, relics, potions, enemies, combat_type, mechanics):
        self.player = player
        self.enemies = enemies
        self.deck = deck
        self.relics = relics
        self.potions = potions
        self.combat_type = combat_type
        self.mechanics = mechanics # {Intent: True/False, Ordered_Draw_Pile: True/False, Turn_End_Discard: True/False, Playable_Curse: True/False, Playable_Status: True/False, Exhaust_Change: %, }
        self.turn = 0
        self.start_of_combat = True
        self.draw_pile = deck
        self.cards_played = 0
        self.hand = []
        self.discard_pile = []
        self.exhaust_pile = []

    def get_targets(self, target_code):
        if target_code == 0:
            return self.player
        elif target_code == 1:
            return 'Placeholder' # Player selects target
        elif target_code == 2:
            return self.enemies[random.randint(0, len(self.enemies) - 1)]
        elif target_code == 3:
            return self.enemies
        else:
            raise ValueError(f"Unknown target code: {target_code}")

    def player_turn_start(self):
        self.turn += 1
        if self.start_of_combat == True:
            for relic in self.relics:
                relic.combatActionEff('Combat Start')