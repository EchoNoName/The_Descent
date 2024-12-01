class obj():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def incre(self, num):
        self.value += num
        return num

a = obj('enemy a', 0, 1)
l = []
l.append(a)
p = []
p = l.copy()
p[0].incre(5)
print(l[0].value)