from data.block import Block


class Work(Block):
    def __init__(self, start, category="", summary="", stop=0):
        """
        start: time
        category: string (optional)
        summary: string (optional)
        stop: time (optional)
        """
        Block.__init__(self, start, category, summary, stop)
