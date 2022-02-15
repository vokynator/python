from typing import Dict, List, Optional, Set


class Person:
    def __init__(self, pid: int, name: str, birth_year: int,
                 parent: Optional['Person'], children: List['Person']):
        self.pid = pid
        self.name = name
        self.birth_year = birth_year
        self.parent = parent
        self.children = children

    def is_valid(self) -> bool:
        siblings = set()
        if self.name == "":
            return False
        for child in self.children:
            if child.name in siblings:
                return False
            siblings.add(child.name)
        for child in self.children:
            if child.birth_year <= self.birth_year or not child.is_valid():
                return False
        return True

    def childless(self) -> Set[int]:
        if self.children == []:
            return {self.pid}
        total = set()
        for child in self.children:
            total.update(child.childless())
        return total

    def parents_younger_than(self, age_limit: int) -> Set[int]:
        return parents_age(set(), self, age_limit, True)

    def parents_older_than(self, age_limit: int) -> Set[int]:
        return parents_age(set(), self, age_limit, False)

    def ancestors(self) -> List['Person']:
        if self.parent is None:
            return []
        ancestors = self.parent.ancestors()
        ancestors.append(self.parent)
        return ancestors

    def remove_extinct_branches(self, alive: Set[int]) -> None:
        for child in reversed(self.children):
            if child.dead(alive):
                self.children.remove(child)
                continue
            child.remove_extinct_branches(alive)

    def dead(self, alive: Set[int]) -> bool:
        if self.children == []:
            return self.pid not in alive
        if self.pid not in alive:
            return all([child.dead(alive) for child in self.children])
        return False

    def order_of_succession(self, alive: Set[int]) -> Dict[int, int]:
        if not self.children:
            return {}
        order_list = []
        for child in sorted(self.children, key=lambda child: child.birth_year):
            if child.pid in alive:
                order_list.append(child.pid)
            order_list += child.order_of_succession(alive)
        result = {}
        for i, person in enumerate(order_list):
            result[person] = i + 1
        return result

    def draw(self, names_only: bool) -> None:
        self.draw_tree(names_only, "")

    def draw_tree(self, names_only: bool, level: str) -> None:
        if names_only:
            print(self.name)
        else:
            print(self.name + " (" + str((self.birth_year)) +
                  ") " + str([self.pid]))
        for child in self.children:
            if child == self.children[-1]:
                print(level + "└─ ", end="")
                child.draw_tree(names_only, level + "   ")
            else:
                print(level + "├─ ", end="")
                child.draw_tree(names_only, level + "│  ")


def parents_age(parents: Set[int], person: Person,
                age_limit: int, young: bool) -> Set[int]:
    for i in person.children:
        if young and i.birth_year - person.birth_year < age_limit:
            parents.add(person.pid)
        if not young and i.birth_year - person.birth_year > age_limit:
            parents.add(person.pid)
        parents_age(parents, i, age_limit, young)
    return parents


def build_person(parent: Optional[Person], pid: int,
                 names: Dict[int, str],
                 children: Dict[int, List[int]],
                 birth_years: Dict[int, int]) -> Person:

    father = Person(pid, names[pid], birth_years[pid], parent, [])
    if pid in children:
        for child in children[pid]:
            new_person = (build_person(father, child, names,
                                       children, birth_years))
            father.children.append(new_person)
    return father


def build_family_tree(names: Dict[int, str],
                      children: Dict[int, List[int]],
                      birth_years: Dict[int, int]) -> Optional[Person]:
    if not rules(names, birth_years, children):
        return None
    children_set = set()
    names_set = set(names)
    for parent in children:
        for child in children[parent]:
            children_set.add(child)
    head = list(names_set - children_set)

    if len(head) == 1:
        return build_person(None, head[0], names, children, birth_years)
    return None


def rules(names: Dict[int, str], birth_years: Dict[int, int],
          children: Dict[int, List[int]]) -> bool:
    names_set = set(names)
    brth_set = set(birth_years)
    kids = []
    parents = []
    for key in children:
        parents.append(key)
        for kid in children[key]:
            if kid in kids:
                return False
            kids.append(kid)
    children_set = set(kids + parents)
    if names_set > brth_set or brth_set > names_set or \
       children_set > names_set:
        return False
    return True


def valid_family_tree(person: Person) -> bool:
    if person.parent is None:
        return person.is_valid()
    return valid_family_tree(person.parent)


def test_one_person() -> None:
    adam = build_family_tree({1: "Adam"}, {}, {1: 1})
    assert isinstance(adam, Person)
    assert adam.pid == 1
    assert adam.birth_year == 1
    assert adam.name == "Adam"
    assert adam.children == []
    assert adam.parent is None

    assert adam.is_valid()
    assert adam.parents_younger_than(18) == set()
    assert adam.parents_older_than(81) == set()
    assert adam.childless() == {1}
    assert adam.ancestors() == []
    assert adam.order_of_succession({1}) == {}


def example_family_tree() -> Person:
    qempa = build_family_tree(
        {
            17: "Qempa'",
            127: "Thok Mak",
            290: "Worf",
            390: "Worf",
            490: "Mogh",
            590: "Kurn",
            611: "Ag'ax",
            561: "K'alaga",
            702: "Samtoq",
            898: "K'Dhan",
            429: "Grehka",
            1000: "Alexander Rozhenko",
            253: "D'Vak",
            106: "Elumen",
            101: "Ga'ga",
        },
        {
            17: [127, 290],
            390: [898, 1000],
            1000: [253],
            127: [611, 561, 702],
            590: [429, 106, 101],
            490: [390, 590],
            290: [490],
            702: [],
        },
        {
            1000: 2366,
            101: 2366,
            106: 2357,
            127: 2281,
            17: 2256,
            253: 2390,
            290: 2290,
            390: 2340,
            429: 2359,
            490: 2310,
            561: 2302,
            590: 2345,
            611: 2317,
            702: 2317,
            898: 2388,
        }
    )

    assert qempa is not None
    return qempa


def test_example() -> None:
    qempa = example_family_tree()
    assert qempa.name == "Qempa'"
    assert qempa.pid == 17
    assert qempa.birth_year == 2256
    assert qempa.parent is None
    assert len(qempa.children) == 2

    thok_mak, worf1 = qempa.children
    assert worf1.name == "Worf"
    assert worf1.pid == 290
    assert worf1.birth_year == 2290
    assert worf1.parent == qempa
    assert len(worf1.children) == 1

    mogh = worf1.children[0]
    assert mogh.name == "Mogh"
    assert mogh.pid == 490
    assert mogh.birth_year == 2310
    assert mogh.parent == worf1
    assert len(mogh.children) == 2

    worf2 = mogh.children[0]
    assert worf2.name == "Worf"
    assert worf2.pid == 390
    assert worf2.birth_year == 2340
    assert worf2.parent == mogh
    assert len(worf2.children) == 2

    alex = worf2.children[1]
    assert alex.name == "Alexander Rozhenko"
    assert alex.pid == 1000
    assert alex.birth_year == 2366
    assert alex.parent == worf2
    assert len(alex.children) == 1

    assert qempa.is_valid()
    assert alex.is_valid()
    assert valid_family_tree(qempa)
    assert valid_family_tree(alex)

    thok_mak.name = ""
    assert not qempa.is_valid()
    assert alex.is_valid()
    assert not valid_family_tree(qempa)
    assert not valid_family_tree(alex)
    thok_mak.name = "Thok Mak"

    thok_mak.birth_year = 2302
    assert not qempa.is_valid()
    assert alex.is_valid()
    assert not valid_family_tree(qempa)
    assert not valid_family_tree(alex)
    thok_mak.birth_year = 2281

    assert qempa.parents_younger_than(12) == set()
    assert qempa.parents_younger_than(15) == {590}
    assert qempa.parents_younger_than(21) == {290, 590}

    assert qempa.parents_older_than(48) == set()
    assert qempa.parents_older_than(40) == {390}

    assert thok_mak.parents_younger_than(21) == set()
    assert thok_mak.parents_older_than(40) == set()

    assert qempa.childless() == {101, 106, 253, 429, 561, 611, 702, 898}
    assert thok_mak.childless() == {611, 561, 702}

    assert alex.ancestors() == [qempa, worf1, mogh, worf2]
    assert thok_mak.ancestors() == [qempa]
    assert qempa.ancestors() == []

    alive = {17, 101, 106, 127, 253, 290, 390, 429,
             490, 561, 590, 611, 702, 898, 1000}
    succession = {
        101: 14,
        106: 12,
        127: 1,
        253: 9,
        290: 5,
        390: 7,
        429: 13,
        490: 6,
        561: 2,
        590: 11,
        611: 3,
        702: 4,
        898: 10,
        1000: 8,
    }

    assert qempa.order_of_succession(alive) == succession

    alive.remove(17)
    assert qempa.order_of_succession(alive) == succession

    alive -= {127, 290, 490, 590}
    assert qempa.order_of_succession(alive) == {
        561: 1,
        611: 2,
        702: 3,
        390: 4,
        1000: 5,
        253: 6,
        898: 7,
        106: 8,
        429: 9,
        101: 10,
    }

    assert mogh.order_of_succession(alive) == {
        390: 1,
        1000: 2,
        253: 3,
        898: 4,
        106: 5,
        429: 6,
        101: 7,
    }


def draw_example() -> None:
    qempa = example_family_tree()
    print("První příklad:")
    qempa.draw(False)

    print("\nDruhý příklad:")
    qempa.children[1].children[0].draw(True)

    alive1 = {101, 106, 253, 429, 561, 611, 702, 898}
    alive2 = {101, 106, 253, 390, 898, 1000}
    for alive in alive1, alive2:
        qempa = example_family_tree()
        qempa.remove_extinct_branches(alive)
        qempa.draw(True)
    qempa = example_family_tree()
    qempa.children[1].children[0].remove_extinct_branches(alive2)
    qempa.draw(True)


if __name__ == '__main__':
    test_one_person()
    test_example()
    draw_example()  # uncomment to run
