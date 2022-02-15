from typing import Optional


class Tree:
    def __init__(self, key: int,
                 left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.key = key
        self.left = left
        self.right = right


# Binární halda je binární strom, který má dvě speciální vlastnosti
# uvedené níže. V tomto příkladu budeme kontrolovat pouze tu druhou,
# totiž vlastnost haldy:
#
#  1. každé patro je plné (s možnou výjimkou posledního),
#  2. hodnota každého uzlu je větší nebo rovna hodnotě libovolného
#     jeho potomka.
#
# Predikát ‹is_heap› rozhodne, splňuje-li vstupní strom tuto druhou
# vlastnost.

def is_heap(tree: Optional[Tree]) -> bool:
    if not tree:
        return True
    
    return False if not heap_property_check(tree) \
           else is_heap(tree.left) and is_heap(tree.right)


def heap_property_check(node: Tree) -> bool:
    if node.left is not None and node.left.key > node.key:
        return False
    if node.right is not None and node.right.key > node.key:
        return False
    return True
def main() -> None:
    assert is_heap(None)
    assert is_heap(Tree(1))
    assert is_heap(Tree(1, Tree(0), Tree(0)))
    assert is_heap(Tree(1, Tree(1), Tree(1)))
    assert is_heap(Tree(1, Tree(0)))
    assert not is_heap(Tree(1, Tree(2), Tree(0)))
    assert not is_heap(Tree(1, Tree(1), Tree(2)))
    assert not is_heap(Tree(1, Tree(8)))

    assert is_heap(Tree(10, Tree(9,
                                 Tree(7, Tree(3), Tree(2)),
                                 Tree(6, Tree(1), Tree(0))),
                        Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(10, Tree(9,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(10, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(10, Tree(9,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(6, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(9))))
    assert not is_heap(Tree(10, Tree(9,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(6, Tree(11), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(10, Tree(11,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(6, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(-10, Tree(9,
                                      Tree(7, Tree(3), Tree(2)),
                                      Tree(6, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))


if __name__ == "__main__":
    main()
