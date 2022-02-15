from typing import Optional, List


class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None


# Napište čistou funkci ‹filter_linked›, která vytvoří nový
# zřetězený seznam, který vznikne z toho vstupního (‹num_list›)
# vynecháním všech uzlů s hodnotou menší než ‹lower_bound›.

def filter_linked(lower_bound: int,
                  num_list: LinkedList) -> LinkedList:
    node = num_list.head
    nums = []
    if num_list.head is None:
        return num_list
    while node is not None:
        if node.value >= lower_bound:
            nums.append(node.value)
        node = node.next
    return build_linked(nums)


def main() -> None:
    assert check_filter(0, [], [])
    assert check_filter(0, [1, 1], [1, 1])
    assert check_filter(0, [-1, 1, -1], [1])
    assert check_filter(1, [0, 0, 0], [])
    assert check_filter(1, [-1, 1, -2, 2, -3, 0], [1, 2])

    assert check_filter(1, [-2, -3, 0, 3], [3])
    assert check_filter(2000, [1024, -257], [])
    assert check_filter(-2, [-2, -3, 0, 3], [-2, 0, 3])


def build_linked(nums: List[int]) -> LinkedList:
    result = LinkedList()

    if len(nums) == 0:
        return result

    result.head = Node(nums[0])
    tail = result.head

    for i in range(1, len(nums)):
        tail.next = Node(nums[i])
        tail = tail.next

    return result


def check_list_content(to_check: LinkedList,
                       expected_content: List[int]) -> bool:
    curr_idx = 0
    curr_node = to_check.head

    while curr_node is not None:
        if len(expected_content) == curr_idx:
            return False

        if curr_node.value != expected_content[curr_idx]:
            return False

        curr_node = curr_node.next
        curr_idx += 1

    return len(expected_content) == curr_idx


def check_filter(lower_bound: int,
                 list_nums: List[int],
                 expected_content: List[int]) -> bool:
    test_list = build_linked(list_nums)
    filter_res = filter_linked(lower_bound, test_list)

    if (test_list.head is not None and
            test_list.head is filter_res.head):
        return False

    return check_list_content(filter_res, expected_content)


if __name__ == "__main__":
    main()
