class test:
    def __init__(self):
        pass

obj = test()
a = []
a.append(obj)
b = []
b.append(a[0])
b.remove(obj)
print(a)