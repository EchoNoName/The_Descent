class test():
    def __init__(self, test):
        self.test = test
    
    def methA(self, test):
        test.pop(-1)
        
    def methB(self):
        testList = [1, 2, 3, 4]
        self.methA(testList)
        print(testList)

do = test(1)
do.methB()
