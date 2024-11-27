class Book:
    __COUNT_OBJ = 0
    STATUSES = ['в наличии', 'выдана']

    def __init__(self, title, author, year, status='в наличии'):
        self.id = self._set_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def change_status(self):
        self.status = self.STATUSES[(self.STATUSES.index(self.status) + 1) % 2]
        return self.status

    def __setattr__(self, key, value):
        if key == 'id':
            # не позволяет изменить id
            if key in self.__dict__:
                return
        object.__setattr__(self, key, value)

    def __str__(self):
        return f'Книга: {self.title}. Автор: {self.author}. Дата издания: {self.year}. Сатус: {self.status}.'

    @classmethod
    def _set_id(cls):
        cls.__COUNT_OBJ += 1
        return cls.__COUNT_OBJ


class Library:
    def __init__(self, safe_mode=True):
        self.db = self.download_db()  # dict

    def download_db(self):
        books = {}
        with open('db.txt', 'r') as db:
            for i in db:
                book = self.create_book(i, sep='|')
                books[book.id] = book
        return books

    def show_books(self):
        for book_id in self.db:
            print(f'ID:{book_id}. {str(self.db[book_id])}')

    def add_book_to_lib(self, title, author, year):
        book = self.create_book(title, author, year)
        self.db[book.id] = book
        print('Книга добавлена.')

    def delete_book_from_db(self, book_id):
        if not self.is_valid_id(book_id):
            print('Значение id указано не верно (Значение должно быть числом и быт доступным в библиотеке).')
            return
        del self.db[book_id]
        print('Книга удалена.')

    def is_valid_id(self, book_id):
        return book_id in self.db

    def search_by(self, var, value):
        res = [
            self.db[b_id] for b_id in self.db if self.db[b_id].__dict__[var].lower() == value.lower()
        ]
        return res

    def change_status_book(self, book_id):
        return self.db[book_id].change_status()

    @staticmethod
    def create_book(*args, sep=None):
        if sep:
            args = args[0].strip().split(sep)
        return Book(*args)


if __name__ == "__main__":
    lib = Library(True)
    lib.show_books()
    print()
    lib.add_book_to_lib('Сборник стихов', 'Пушкин', '1900')
    lib.show_books()
    print()
    lib.delete_book_from_db(5)
    lib.show_books()
    print()
    lib.delete_book_from_db(5)
    lib.show_books()
    print()
    print(f'{lib.is_valid_id(1) = }')
    print(f'{lib.is_valid_id(5) = }')
    print(f'{lib.is_valid_id(0) = }')
    print(f'{lib.is_valid_id("2") = }')
    print()
    print(*lib.search_by("author", "толстой"), sep='\n', end='\n#\n')
    print()
    print(*lib.search_by("author", "ЛЕРМАНТОВ"), sep='\n', end='\n#\n')
    print()
    print(*lib.search_by("author", "Чехов"), sep='\n', end='\n#\n')
    print()
    print(*lib.search_by("year", "1980"), sep='\n', end='\n#\n')
    print()
    print(*lib.search_by("year", "1950"), sep='\n', end='\n#\n')
    print()
    print(lib.search_by("year", "1980")[0])
    print(f'Книга {lib.search_by("year", "1980")[0].change_status()}')
    print(f'Книга {lib.search_by("year", "1980")[0].change_status()}')
    print()

    book = Book('Кавказский пленник', 'Лермантов', '1981')
    print(book)
    print(f'{book.status}')
    book.change_status()
    print(f'{book.status}')
    book.change_status()
    print(f'{book.status}')
