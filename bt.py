class Node(object):
    def __init__(self, parent, left, right, letter, key):
        self.parent = parent
        self.letter = letter
        self.left = left
        self.right = right
        self.key = key

        
class BT(object):
    def __init__(self):
        self.root = None
        self.leaves = []
