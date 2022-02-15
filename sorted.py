# V této úloze budete implementovat jednoduchý zřetězený seznam
# s dodatečnou vlastností, že jeho prvky jsou vždy vzestupně
# seřazené.

from typing import List, Optional


# Třída ‹Node› reprezentuje jeden uzel seznamu, a má dva atributy:
# hodnotu typu ‹int› a odkaz na další uzel ‹next›.

class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None


# Následující třída reprezentuje seřazený, zřetězený seznam.
# Implementujte naznačené metody ‹insert› a ‹get_greater_than›.

class SortedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    # Metoda ‹insert› vloží do seznamu nový prvek. Nezapomeňte, že
    # seznam musí být vždy seřazený.

    def insert(self, value: int) -> None:
        node = self.head
        if node is None:
            self.head = Node(value)
            return
        if node.value > value:
            self.head = Node(value)
            self.head.next = node
            return 
        
        while node.next is not None and node.value < value:
            node = node.next
        next_node = node.next
        node.next = Node(value)
        node.next.next = next_node


def main() -> None:
    test_insert()



def test_insert() -> None:
    s_list = SortedList()
    s_list.insert(4)
    assert s_list.head is not None
    assert s_list.head.value == 4
    s_list.insert(5)
    assert s_list.head.value == 4
    assert s_list.head.next is not None
    assert s_list.head.next.value == 5
    s_list.insert(3)
    assert s_list.head.value == 3
    assert s_list.head.next.value == 4
    assert s_list.head.next.next is not None
    assert s_list.head.next.next.value == 5

    s_list = SortedList()
    assert s_list.head is None
    s_list.insert(1)
    s_list.insert(0)
    s_list.insert(-1)
    s_list.insert(5)
    assert s_list.head is not None
    assert s_list.head.value == -1
    assert s_list.head.next is not None
    assert s_list.head.next.value == 0
    assert s_list.head.next.next is not None
    assert s_list.head.next.next.value == 1
    assert s_list.head.next.next.next is not None
    assert s_list.head.next.next.next.value == 5


if __name__ == "__main__":
    main()
