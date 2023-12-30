class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class HashTableLL:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size

    def hash(self, value):
        hash_value = 0
        for char in value:
            hash_value = (hash_value + ord(char)) % self.size
        return hash_value

    def add(self, value):
        index = self.hash(value)
        new_node = Node(value)
        if self.table[index] is None:
            self.table[index] = new_node
        else:
            # previous_node = None
            # current_node = self.table[index]
            # while current_node is not None and current_node.value < value:
            #     previous_node = current_node
            #     current_node = current_node.next
            #
            # if previous_node is not None:
            #     previous_node.next = new_node
            # new_node.next = current_node
            new_node.next = self.table[index]
            self.table[index] = new_node


        return index

    def delete(self, value):
        index = self.hash(value)
        current = self.table[index]
        prev = None
        while current:
            if current.value == value:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                return
            prev = current
            current = current.next

    def find(self, value):
        index = self.hash(value)
        current = self.table[index]
        while current:
            if current.value == value:
                return index
            current = current.next
        return None

    def prinTable(self):
        index = 0
        for node in self.table:
            if node is not None:
                print(index, end = " : ")
                while node is not None:
                    print(node.value,end = "->")
                    node = node.next
                print()
            index+=1