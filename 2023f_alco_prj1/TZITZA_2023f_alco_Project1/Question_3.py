class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.table = [None] * size
        self.count = 0

    def hash_function(self, key):
        return key % self.size

    def insert(self, key):
        if self.count >= self.size * 0.7:
            self.size *= 2
            new_table = [None] * self.size
            for i in range(len(self.table)):
                if self.table[i] is not None:
                    new_table[self.hash_function(self.table[i])] = self.table[i]
            self.table = new_table

        self.table[self.hash_function(key)] = key
        self.count += 1

    def find(self, key):
        index = self.hash_function(key)
        while self.table[index] is not None:
            if self.table[index] == key:
                return True
            index = (index + 1) % self.size
        return False

    def delete(self, key):
        index = self.hash_function(key)
        while self.table[index] is not None:
            if self.table[index] == key:
                self.table[index] = None
                self.count -= 1
                return True
            index = (index + 1) % self.size
        return False