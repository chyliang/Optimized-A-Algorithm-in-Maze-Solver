class Node:  # define a Node class
    def __init__(self,parent=None,position=None):
        self.parent = parent
        self.position = position
        self.g_value = 0
        self.h_value = 0
        self.f_value = 0
    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return (self.f_value < other.f_value) or (self.f_value == other.f_value and self.g_value > other.g_value)

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f_value > other.f_value