class Array:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.size = 0
        self.data = [None] * self.capacity

    def _resize(self):
        self.capacity *= 2
        new_data = [None] * self.capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data

    def get(self, i):
        if 0 <= i < self.size:
            return self.data[i]
        return None

    def append(self, v):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = v
        self.size += 1

    def insert(self, i, v):
        if i < 0 or i > self.size:
            return
        if self.size == self.capacity:
            self._resize()
        for j in range(self.size, i, -1):
            self.data[j] = self.data[j-1]
            
        self.data[i] = v
        self.size += 1

    def delete(self, i):
        if 0 <= i < self.size:
            removed = self.data[i]
            for j in range(i, self.size - 1):
                self.data[j] = self.data[j+1]
            self.data[self.size - 1] = None
            self.size -= 1
            return removed
        return None


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def get(self, i):
        if i < 0 or i >= self.size:
            return None
        current = self.head
        for _ in range(i):
            current = current.next
        return current.data

    def append(self, v):
        new_node = Node(v)
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert(self, i, v):
        if i < 0 or i > self.size:
            return
            
        new_node = Node(v)
        if i == 0:
            new_node.next = self.head
            self.head = new_node
            if self.size == 0:
                self.tail = new_node
        else:
            current = self.head
            for _ in range(i - 1):
                current = current.next
            
            new_node.next = current.next
            current.next = new_node

            if new_node.next is None:
                self.tail = new_node
                
        self.size += 1

    def delete(self, i):
        if i < 0 or i >= self.size:
            return None
            
        if i == 0:
            removed = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return removed
            
        current = self.head
        for _ in range(i - 1):
            current = current.next
            
        removed = current.next.data
        current.next = current.next.next
        
        if current.next is None:
            self.tail = current
            
        self.size -= 1
        return removed
