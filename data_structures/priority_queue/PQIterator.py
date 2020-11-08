class PQIterator(object):
    """description of class"""

    def __init__(self, pqueue):
        self.pq = pqueue;
        self.index = 0;

    def __next__(self):
        if self.index < len(self.pq.pq):
            result = self.pq.pq[self.index][2];
            self.index += 1;
            return result;
        self.index = 0;
        raise StopIteration;


