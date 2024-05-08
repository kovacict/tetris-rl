from block import Block


class LBlock(Block):
    def __init__(self):
        super().__init__(id=0)
        self.cells = {
            0: [(1, 0), (0, 2),  (1, 1), (1, 2)], #ok
            90: [(0, 1), (1, 1), (2, 1), (2, 2)], #ok
            180: [(1, 0), (1, 1), (1, 2), (2, 0)], #ok
            270: [(0, 0), (0, 1), (1, 1), (2, 1)], #ok
        }
        #self.move(0, 3)


class JBlock(Block):
    def __init__(self):
        super().__init__(id=1)
        self.cells = {
            0: [(0, 0), (1, 0), (1, 1), (1, 2)], #ok
            90: [(0, 1), (0, 2), (1, 1), (2, 1)], #ok
            180: [(1, 0), (1, 1), (1, 2), (2, 2)], #ok
            270: [(2, 0), (0, 1), (1, 1),  (2, 1)], #ok
        }
        #self.move(0, 3)


class IBlock(Block): #ok
    def __init__(self):
        super().__init__(id=2)
        self.cells = {
            0: [(1, 0), (1, 1), (1, 2), (1, 3)], 
            90: [(0, 2), (1, 2), (2, 2), (3, 2)],
            180: [(2, 0), (2, 1), (2, 2), (2, 3)],
            270: [(0, 1), (1, 1), (2, 1), (3, 1)],
        }
        #self.move(-1, 3)


class OBlock(Block): #ok
    def __init__(self):
        super().__init__(id=3)
        self.cells = {
            0: [(0, 0), (0, 1), (1, 0), (1, 1)],
            90: [(0, 0), (0, 1), (1, 0), (1, 1)],
            180: [(0, 0), (0, 1), (1, 0), (1, 1)],
            270: [(0, 0), (0, 1), (1, 0), (1, 1)],
        }
        #self.move(0, 4)


class SBlock(Block):
    def __init__(self):
        super().__init__(id=4)
        self.cells = {
            0: [(1, 0), (0, 1), (0, 2),  (1, 1)], #ok
            90: [(0, 1), (1, 1), (1, 2), (2, 2)], #ok
            180: [(2, 0), (1, 1), (1, 2),  (2, 1)], #ok
            270: [(0, 0), (1, 0), (1, 1), (2, 1)], #ok
        }
        #self.move(0, 3)


class ZBlock(Block):
    def __init__(self):
        super().__init__(id=5)
        self.cells = {
            0: [(0, 0), (0, 1), (1, 1), (1, 2)], #ok
            90: [(1, 1), (0, 2),  (1, 2), (2, 1)], #ok
            180: [(1, 0), (1, 1), (2, 1), (2, 2)], #ok
            270: [ (1, 0), (0, 1), (1, 1), (2, 0)], #ok
        }
        #self.move(0, 3)


class TBlock(Block):
    def __init__(self):
        super().__init__(id=6)
        self.cells = {
            0: [(1, 0), (0, 1),  (1, 1), (1, 2)], #ok
            90: [(0, 1), (1, 1), (1, 2), (2, 1)], #ok
            180: [(1, 0), (1, 1), (1, 2), (2, 1)], #ok
            270: [(1, 0), (0, 1),  (1, 1), (2, 1)], #ok
        }
        #self.move(0, 3)