from block import Block


class Pause(Block):
    def __init__(self, start, stop=0):
        """
        start: time
        stop: time (optional)
        """
        Block.__init__(self, start, stop)
