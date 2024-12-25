import random

class Treasure:
    def __init__(self, run):
        self.run = run
        self.rewards = None
        self.empty = False
        self.type = None
        self.opened = False
    
    def start_event(self):
        rng = random.randint(1, 100)
        if self.type == None:
            if rng <= 50:
                self.type = 3
            elif rng <= 83:
                self.type = 4
            else:
                self.type = 5
        self.interact()

    def interact(self):
        action = input('Open or Skip')
        if action == 'Open':
            if self.opened == False:
                self.run.generate_reward_screen_instance(self.type, False, {})
                self.run.reward.listRewards()
                if self.run.reward.isEmpty():
                    self.empty = True
                self.interact()
            else:
                if self.empty == False:
                    self.run.reward.listRewards()
                    if self.run.reward.isEmpty():
                        self.empty = True
                    self.interact()
                else:
                    print('Chest empty')
                    self.interact()
        else:
            self.run.mapNav()