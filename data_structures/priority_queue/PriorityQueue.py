import heapq
import itertools
from data_structures.priority_queue import PQIterator

class PriorityQueue:

    REMOVED = '<removed-task>'      # placeholder for a removed task

    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    def __nonzero__(self):
        return bool(self.pq)

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in  self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = PriorityQueue.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not PriorityQueue.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def __iter__(self):
        return PQIterator.PQIterator(self);

    def __len__(self):
        return len(self.entry_finder);
        
