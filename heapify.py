class Heap(object):
    def __init__(self, h_type):
        # h_type must be 'max' or 'min'
        self.queue = []
        self.heapsize = 0
        if h_type != 'max' and h_type != 'min':
            raise Exception('Wrong argument passed to heap.')
        self.h_type = h_type

    def __len__(self):
        return len(self.queue)

    def perc_up(self, i):
        p = (i+1)//2-1
        if self.h_type == 'max':
            while i > 0 and self.queue[p] > self.queue[i]:
                self.queue[i], self.queue[p] = self.queue[p], self.queue[i]
                i = p
                p = (i+1)//2-1
        else:
            while i > 0 and self.queue[p] < self.queue[i]:
                self.queue[i], self.queue[p] = self.queue[p], self.queue[i]
                i = p
                p = (i+1)//2-1
                    
    def insert(self, key):
        self.queue.append(key)
        self.heapsize += 1
        self.perc_up(self.heapsize-1)

    def pop(self):
        len_h = self.heapsize-1
        self.queue[len_h], self.queue[0] = self.queue[0], self.queue[len_h]
        popped_key = self.queue.pop()
        self.heapsize -= 1
        if self.h_type == 'max':
            if self.heapsize > 1 and self.queue[0] < self.queue[1]:
                self.queue[0], self.queue[1] = self.queue[1], self.queue[0]
            self.min_heapify(1)
        else:
            if self.heapsize > 1 and self.queue[0] > self.queue[1]:
                self.queue[0], self.queue[1] = self.queue[1], self.queue[0]
            self.max_heapify(1)
        return popped_key

    def min_heapify(self, index):
        n = self.heapsize+1
        right = 2*index + 1
        left = 2*index
        smallest = index
        if left < n and self.queue[left-1] < self.queue[index-1]:
            smallest = left
        else:
            smallest = index
        if right < n and self.queue[right-1] < self.queue[smallest-1]:
            smallest = right
        if smallest != index:
            self.queue[index-1], self.queue[smallest-1] = \
             self.queue[smallest-1], self.queue[index-1]
            return self.min_heapify(smallest)

    def max_heapify(self, index):
        n = self.heapsize+1
        right = 2*index + 1
        left = 2*index
        largest = index
        if left < n and self.queue[left-1] > self.queue[index-1]:
            largest = left
        else:
            largest = index
        if right < n and self.queue[right-1] > self.queue[largest-1]:
            largest = right
        if largest != index:
            self.queue[index-1], self.queue[largest-1] = \
             self.queue[largest-1], self.queue[index-1]
            return self.max_heapify(largest)

    def build_max_heap(self):
        n = self.heapsize
        for i in range(n//2+1, 0, -1):
            self.max_heapify(i)
            
    def build_min_heap(self):
        n = self.heapsize
        for i in range(n//2+1, 0, -1):
            self.min_heapify(i)
        
