class CoolFunList:
    def __init__(self):
        self.items = []

    def append(self, item):
        self.items += [item]

    def __len__(self):
        return len(self.items)

    def removeLast(self):
        return self.items.pop()

    # if we want to iterate over this sequence, we define the special method
    # called __iter__(self). Without this we'll get "builtins.TypeError:
    # 'CoolFunList' object is not iterable" if we try to write
    # for cmd in seq:
    # where seq is one of these sequences. The yield below will yield an
    # element of the sequence and will suspend the execution of the for 
    # loop in the method below until the next element is needed. The ability 
    # to yield each element of the sequence as needed is called "lazy" evaluation
    # and is very powerful. It means that we only need to provide access to as
    # many of elements of the sequence as are necessary and no more.
    def __iter__(self):
        for c in self.items:
            yield c 