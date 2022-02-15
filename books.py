from typing import List, Dict


# V této úloze naprogramujeme jednoduchou knihovnu (kolekci knížek).
# Nejprve implementujte třídu ‹Book› s atributy ‹name› a ‹author›.

class Book:
    def __init__(self, name: str, author: str):
        self.name = name
        self.author = author


# Dále naprogramujte třídu ‹Bookshelf›, která reprezentuje knihovnu,
# do které lze přidávat knížky a případně je pak odebírat.

class Bookshelf:

    def __init__(self, books: List[Book]):
        self.bookss = books

    def add_book(self, book: Book) -> None:
        self.bookss.append(book)

    # Metoda ‹books› vrátí seznam knih v pořadí, v jakém byly do
    # knihovny přidány.

    def books(self) -> List[Book]:
        return self.bookss

    # Metoda ‹group_by_author› vrátí slovník, který přiřadí každému
    # autorovi seznam knih, které napsal.

    def group_by_author(self) -> Dict[str, List[Book]]:
        result = {}
        for i in self.bookss:
            if i.author in result:
                result[i.author].append(i)
            else:
                result[i.author] = [i]
        return result


def main() -> None:
    lotr1 = Book('Fellowship', 'Tolkien')
    assert lotr1.name == 'Fellowship'
    assert lotr1.author == 'Tolkien'

    lotr2 = Book('Two Towers', 'Tolkien')
    as1 = Book('End of Eternity', 'Asimov')

    shelf = Bookshelf([lotr1, as1])
    assert shelf.books() == [lotr1, as1]
    assert shelf.group_by_author() == {'Tolkien': [lotr1], 'Asimov': [as1]}

    shelf.add_book(lotr2)
    assert shelf.books() == [lotr1, as1, lotr2]
    assert shelf.group_by_author() \
        == {'Tolkien': [lotr1, lotr2], 'Asimov': [as1]}

    clarke1 = Book('Rama', 'Clarke')
    clarke2 = Book('The City and the Stars', 'Clarke')
    shelf.add_book(clarke1)
    shelf.add_book(clarke2)
    assert shelf.books() == [lotr1, as1, lotr2, clarke1, clarke2]
    assert shelf.group_by_author() \
        == {'Tolkien': [lotr1, lotr2],
            'Asimov': [as1],
            'Clarke': [clarke1, clarke2]}

    empty_shelf = Bookshelf([])
    assert empty_shelf.books() == []
    assert empty_shelf.group_by_author() == {}


if __name__ == "__main__":
    main()

