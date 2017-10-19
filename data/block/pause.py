from block import Block


class Pause(Block):
    def __init__(self, start, end=0):
        """
        start: time
        end: time (optional)
        """
        Block.__init__(self, start, end)
