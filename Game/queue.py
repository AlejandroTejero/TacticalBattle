class Node:
    def __init__(self, item, siguiente=None):
        self.item = item
        self.siguiente = siguiente

    def get_siguiente(self):
        return self.siguiente

    def set_siguiente(self, siguiente):
        self.siguiente = siguiente

    def __str__(self):
        return str(self.item)

class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0

    def __str__(self):
        s = "["
        paux = self.first
        while paux:
            s += str(paux.item)
            paux = paux.get_siguiente()
            if paux:
                s += ", "
        s += "]"
        return s

    def __len__(self):
        return self.size

    def enqueue(self, item):
        n = Node(item)
        if self.esta_vacio():
            self.first = n
        else:
            self.last.set_siguiente(n)
        self.last = n
        self.size += 1

    def dequeue(self):
        if self.esta_vacio():
            raise Exception("La cola esta vacia")
        item = self.first.item
        self.first = self.first.get_siguiente()
        if not self.first:
            self.last = None
        self.size -= 1
        return item

    def esta_vacio(self):
        return self.size == 0

    def peek(self):
        if self.esta_vacio():
            raise Exception("La cola esta vacia")
        return self.first.item

    def clear(self):
        self.first = None
        self.last = None
        self.size = 0
