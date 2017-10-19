from block import Block


class Work(Block):
    def __init__(self, start, end=0):
        """
        start: time
        end: time (optional)
        """
        Block.__init__(self, start, end)
