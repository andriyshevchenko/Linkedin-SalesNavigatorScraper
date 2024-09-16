class LinkList:
    def __init__(self, link_func, size, log):
        self.log = log
        self.link = link_func
        self.size = size
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.size:
            result = self.link()
            self.i += 1
            return result
        raise StopIteration
