from typing import List, Tuple, Optional


class Clue:
    def __init__(self, total: int, position: Tuple[int, int],
                 is_row: bool, length: int):
        self.total = total
        self.position = position
        self.is_row = is_row
        self.length = length


class Kakuro:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.array = [[-1 for _ in range(width)] for _ in range(height)]
        self.clues: List[Clue] = []

    def set(self, x: int, y: int, value: int) -> None:
        self.array[y][x] = value

    def show_board(self) -> None:
        for line in self.array:
            to_print = ""
            for expr in line:
                if expr == -1:
                    to_print += "\\ "
                elif expr == 0:
                    to_print += ". "
                else:
                    to_print += (str(expr) + " ")
            print(to_print[:-1])

    def save(self, filename: str) -> None:
        game_data = []
        for row in self.array:
            game_data.append(["\\" if expr == -1 else "."
                         if expr == 0 else str(expr) for expr in row])
        for clue in self.clues:
            x, y = clue.position
            if clue.is_row is True:
                game_data[y][x] += str(clue.total)
            else:
                game_data[y][x] = str(clue.total) + game_data[y][x]

        with open(filename, "w") as my_file:
            for line in game_data:
                for word in line:
                    my_file.write(str(word) + " ")
                my_file.write("\n")

    def is_valid(self) -> bool:
        for clue in self.clues:
            x, y = clue.position
            clue_nums = []
            clue_sum = 0
            for i in range(1, clue.length + 1):
                if clue.is_row is True:
                    num = self.array[y][x + i]
                else:
                    num = self.array[y + i][x]
                if num == 0:
                    continue
                clue_sum += num
                if clue_sum > clue.total or num in clue_nums:
                    return False
                clue_nums.append(num)
        return True

    def pick_clue(self) -> Optional[Clue]:
        result = None
        clue_min = 0
        for clue in self.clues:
            x, y = clue.position
            clue_empty = 0
            for i in range(1, clue.length + 1):
                if clue.is_row is True:
                    num = self.array[y][x + i]
                else:
                    num = self.array[y + i][x]
                if num == 0:
                    clue_empty += 1
            if not clue_empty:
                continue
            elif result is None:
                result = clue
                clue_min = clue_empty
            elif clue_empty < clue_min:
                result = clue
                clue_min = clue_empty
            elif clue_empty == clue_min and clue.position != result.position:
                if clue.position < result.position:
                    result = clue
            elif clue_empty == clue_min \
                    and clue.position == result.position and \
                    result.is_row:
                result = clue
        return result

    def solve(self) -> bool:
        pass  # TODO


def load_kakuro(filename: str) -> Kakuro:

    result = []
    kaku_list = []
    kaku_coords = []
    with open(filename, "r") as my_file:
        board = my_file.readlines()
        y = 0
    for line in board:
        line_split = str(line).split()
    
        kaku_list.append(line_split)
        new_line = []
        x = 0
        for expr in line_split:
            if "\\" in expr:
                new_line.append(-1)
                kaku_coords.append((x, y))
            elif expr == ".":
                new_line.append(0)
            else:
                new_line.append(int(expr))
            x += 1
        y += 1
        result.append(new_line)
    kakuro = Kakuro(len(result[0]), len(result))
    kakuro.array = result
    kakuro.clues = build_clues(kaku_coords, kaku_list)
    return kakuro


def build_clues(kaku_coords: List[Tuple[int, int]],
                kaku_list: List[List[str]]) -> List[Clue]:
    list_clues = []
    for x, y in kaku_coords:
        coord_x = x
        coord_y = y
        if kaku_list[y][x] == "\\":
            continue
        num_x, num_y = kaku_list[y][x].split("\\")
        if num_x != "":
            length = 0
            while coord_y + 1 != len(kaku_list) \
                    and "\\" not in kaku_list[coord_y + 1][x]:
                length += 1
                coord_y += 1
            list_clues.append(Clue(int(num_x), (x, y), False, length))

        if num_y != "":
            length = 0
            while coord_x + 1 != len(kaku_list[0]) \
                    and "\\" not in kaku_list[y][coord_x + 1]:
                length += 1
                coord_x += 1
            list_clues.append(Clue(int(num_y), (x, y), True, length))
    return list_clues


def cells_from_empty(total: int, length: int) -> List[List[int]]:
    result: List[List[int]] = []
    nums = [x + 1 for x in range(9)]
    pos_nums = poss_nums(nums, total, length, [], [])
    for nums in pos_nums:
        result += permutations(nums)
    return sorted(result)


def cells_from_partial(total: int, partial: List[int]) -> List[List[int]]:
    nums = list(range(1,10))
    length = len(partial)
    pos_lists = []
    result: List[List[int]] = []
    cells_sum = total
    for num in partial:
        if num != 0:
            if num not in nums:
                return []
            nums.remove(num)
            length -= 1
            total -= num
    if partial.count(0) == 0 and sum(partial) == cells_sum:
        return [partial]
    pos_nums = poss_nums(nums, total, length, [], [])
    for nums in pos_nums:
        pos_lists += permutations(nums)
    for possibility in pos_lists:
        index = 0
        result_kind = []
        for num in partial:
            if num == 0:
                result_kind.append(possibility[index])
                index += 1
            else:
                result_kind.append(num)
        result.append(result_kind)
    return sorted(result)


def poss_nums(nums: List[int], total: int, length: int,
              part: List[int],
              result: List[List[int]]) -> List[List[int]]:
    if sum(part) > total or len(part) > length:
        return []
    if sum(part) == total and len(part) == length:
        result.append(part)
        return result
    for i, j in enumerate(nums):
        rest = nums[i + 1:]
        poss_nums(rest, total, length, part + [j], result)
    return result


def permutations(list_num: List[int]) -> List[List[int]]:
    if len(list_num) == 1:
        return [list_num]
    oder = []
    for i in range(len(list_num)):
        num = list_num[i]
        rest = list_num[:i] + list_num[i+1:]
        for j in permutations(rest):
            oder.append([num] + j)
    return oder


# --- Tests ---

# Note: If there is a file with the following name in the current working
# directory, running these tests will overwrite that file!

TEST_FILENAME = "test"

EXAMPLE = ("\\   11\\  8\\     \\   \\   7\\ 16\\\n"
           "\\16   .   .   11\\   \\4   .   .\n"
           "\\7    .   .     .  7\\13  .   .\n"
           "\\   15\\ 21\\12   .   .    .   .\n"
           "\\12   .   .     .   .   4\\  6\\\n"
           "\\13   .   .     \\6  .    .   .\n"
           "\\17   .   .     \\   \\6   .   .\n")


def write_example(filename: str) -> None:
    with open(filename, "w") as file:
        file.write(EXAMPLE)


def example() -> Kakuro:
    write_example(TEST_FILENAME)
    return load_kakuro(TEST_FILENAME)


def test_1() -> None:
    assert cells_from_partial(2, [1, 1]) == []
    assert cells_from_partial(1, [1]) == [[1]]
    kakuro = example()
    assert kakuro.width == 7
    assert kakuro.height == 7
    assert kakuro.array == [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, -1, -1, 0, 0],
        [-1, 0, 0, 0, -1, 0, 0],
        [-1, -1, -1, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, -1, -1],
        [-1, 0, 0, -1, 0, 0, 0],
        [-1, 0, 0, -1, -1, 0, 0],
    ]

    clue_set = {(clue.total, clue.position, clue.is_row, clue.length)
                for clue in kakuro.clues}
    assert clue_set == {
        (11, (1, 0), False, 2),
        (8, (2, 0), False, 2),
        (7, (5, 0), False, 3),
        (16, (6, 0), False, 3),
        (16, (0, 1), True, 2),
        (11, (3, 1), False, 3),
        (4, (4, 1), True, 2),
        (7, (0, 2), True, 3),
        (7, (4, 2), False, 3),
        (13, (4, 2), True, 2),
        (15, (1, 3), False, 3),
        (21, (2, 3), False, 3),
        (12, (2, 3), True, 4),
        (12, (0, 4), True, 4),
        (4, (5, 4), False, 2),
        (6, (6, 4), False, 2),
        (13, (0, 5), True, 2),
        (6, (3, 5), True, 3),
        (17, (0, 6), True, 2),
        (6, (4, 6), True, 2),
    }


def test_2() -> None:
    kakuro = example()

    print("show_board result:")
    kakuro.show_board()
    print("---")

    print("save result:")
    kakuro.save(TEST_FILENAME)
    with open(TEST_FILENAME) as file:
        print(file.read(), end="")
    print("---")


def test_3() -> None:
    kakuro = example()
    assert kakuro.is_valid()

    kakuro.set(2, 1, 9)
    assert not kakuro.is_valid()

    kakuro.set(2, 1, 0)
    assert kakuro.is_valid()

    kakuro.set(1, 2, 1)
    kakuro.set(2, 2, 1)
    assert not kakuro.is_valid()

    kakuro.set(1, 2, 0)
    kakuro.set(2, 2, 0)
    assert kakuro.is_valid()

    kakuro.set(5, 5, 4)
    assert kakuro.is_valid()


def test_4() -> None:
    assert cells_from_empty(13, 2) \
        == [[4, 9], [5, 8], [6, 7], [7, 6], [8, 5], [9, 4]]

    assert cells_from_partial(12, [0, 0, 6, 0]) \
        == [[1, 2, 6, 3], [1, 3, 6, 2], [2, 1, 6, 3],
            [2, 3, 6, 1], [3, 1, 6, 2], [3, 2, 6, 1]]


def test_5() -> None:
    kakuro = example()
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 16
    assert clue.position == (0, 1)
    assert clue.is_row
    assert clue.length == 2

    kakuro.set(6, 5, 1)
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 6
    assert clue.position == (6, 4)
    assert not clue.is_row
    assert clue.length == 2

    kakuro.set(6, 6, 5)
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 6
    assert clue.position == (4, 6)
    assert clue.is_row
    assert clue.length == 2


def test_6() -> None:
    kakuro = example()
    kakuro.solve()
    assert kakuro.array == [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, 9, 7, -1, -1, 1, 3],
        [-1, 2, 1, 4, -1, 4, 9],
        [-1, -1, -1, 5, 1, 2, 4],
        [-1, 1, 5, 2, 4, -1, -1],
        [-1, 6, 7, -1, 2, 3, 1],
        [-1, 8, 9, -1, -1, 1, 5],
    ]


if __name__ == '__main__':
    # uncomment to visually check the results:
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    # test_6()
