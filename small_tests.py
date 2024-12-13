import copy
class event:
    def __init__(self):
        pass

    def __repr__(self):
        return 'Event'

class combat:
    def __init__(self):
        pass

    def __repr__(self):
        return 'Combat'
    
class shop:
    def __repr__(self):
        return 'Shop'
    
    def __init__(self):
        pass

event1 = event()
event2 = event()
combat1 = combat()
shop1 = shop()
list = [event1, event2, combat1, shop1]
print(isinstance(event1, event))