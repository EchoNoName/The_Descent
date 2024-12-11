import copy

class test:
    def __init__(self):
        self.name = "obj 1"

obj1 = test()
obj2 = copy.deepcopy(obj1)
obj2.name = 2
print(obj1.name)
print(obj2.name)