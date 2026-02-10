class Node:
    def __init__(self, item, anterior=None, siguiente=None):
        self.anterior = anterior
        self.item = item
        self.siguiente = siguiente

    def get_anterior(self):
        return self.anterior

    def set_anterior(self, anterior):
        self.anterior = anterior

    def get_siguiente(self):
        return self.siguiente

    def set_siguiente(self, siguiente):
        self.siguiente = siguiente

    def __str__(self):
        return str(self.item)


class DoublyLinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.total = 0

    def __len__(self):
        return self.total

    def esta_vacia(self):
        return self.total == 0

    def add_ordered(self, item):
        if self.esta_vacia():
            self.first = Node(item)
            self.last = self.first
        else:
            actual = self.first
            while actual and actual.item > item:
                actual = actual.get_siguiente()

            if not actual:
                new_node = Node(item, anterior=self.last)
                self.last.set_siguiente(new_node)
                self.last = new_node
            elif actual == self.first:
                new_node = Node(item, siguiente=self.first)
                self.first.set_anterior(new_node)
                self.first = new_node
            else:
                new_node = Node(item, anterior=actual.get_anterior(), siguiente=actual)
                actual.get_anterior().set_siguiente(new_node)
                actual.set_anterior(new_node)

        self.total += 1

    def get_item(self, index):
        if 0 <= index < self.total:
            actual = self.first
            for i in range(index):
                actual = actual.get_siguiente()
            return actual.item
        else:
            raise Exception(f"Índice inválido {index}")

    def __str__(self):
        result = "["
        actual = self.first
        while actual:
            result += str(actual)
            actual = actual.get_siguiente()
            if actual:
                result += ", "
        result += "]"
        return result
