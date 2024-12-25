class player:
    def __init__(self):
        self.hp = 10

    def hp_change(self, amount):
        self.hp += amount
        return self.hp
    
char = player()
print(char.hp_change(-5))