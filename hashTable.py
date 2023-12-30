class HashTable:
    def __init__(self, size = 10):
        self.size = size # Initial size of the table
        self.table = [None] * self.size
        self.count = 0  # Number of elements in the table

    def hash(self, value):
        # Custom hash function suitable for your regex range
        hash_value = 0
        for char in value:
            hash_value = (hash_value + ord(char)) % self.size
        return hash_value

    def resize(self):
        # Double the size of the table when it's too full
        self.size *= 2
        new_table = [None] * self.size
        for value in self.table:
            if value is not None:
                index = self.hash(value)
                while new_table[index] is not None:
                    index = (index + 1) % self.size
                new_table[index] = value
        self.table = new_table

    def add(self, value):
        if self.count >= self.size // 2:
            self.resize()
        index = self.hash(value)
        while self.table[index] is not None:
            index = (index + 1) % self.size
        self.table[index] = value
        self.count += 1
        return index

    def delete(self, value):
        index = self.hash(value)
        while self.table[index] is not None:
            if self.table[index] == value:
                self.table[index] = None
                self.count -= 1
                return
            index = (index + 1) % self.size

    def find(self, value):
        index = self.hash(value)
        while self.table[index] is not None:
            if self.table[index] == value:
                return index
            index = (index + 1) % self.size
        return None

    def prinTable(self):
        for i in range(0, self.size):
            if self.table[i] is not None:
                print(i, self.table[i])
