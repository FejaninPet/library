from datetime import datetime


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
        return f'Статус кинги изменен. Теперь она {self.status}.'

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
        self.save_mode = safe_mode

    def download_db(self):
        books = {}
        with open('db.txt', 'r') as db:
            for i in db:
                book = self.create_book(i, sep='|')
                books[book.id] = book
        return books

    def save_db(self):
        with open('db.txt', 'w') as f:
            for i in self.db:
                f.write(f'{self.db[i].title}|{self.db[i].author}|{self.db[i].year}|{self.db[i].status}\n')

    def show_books(self):
        res = []
        for book_id in self.db:
            res.append(f'ID:{book_id}. {str(self.db[book_id])}')
        return res

    def add_book_to_lib(self, title, author, year):
        title, author, year = title.strip(), author.strip(), year.strip()
        not_valid_data = self.check_valid_data(title, author, year)
        if not_valid_data:
            return not_valid_data
        book = self.create_book(title, author, year)
        self.db[book.id] = book
        if self.save_mode:
            self.save_db()
        return 'Книга добавлена.'

    def delete_book_from_db(self, book_id):
        if not book_id.isdigit():
            return 'id должно быть числом.'
        if not self.is_valid_id(book_id):
            return 'Книги с таким id не существует.'
        book_name = self.db[int(book_id)].title
        del self.db[int(book_id)]
        if self.save_mode:
            self.save_db()
        return f'Книга "{book_name}" удалена.'

    def check_valid_data(self, title, author, year):
        if '|' in title:
            return 'Название книги не должно содержать символ "|".'
        if not self.is_valid_author_name(author):
            return 'Имя автора может состоять только из букв и символов дефис, пробел и точка.'
        if not self.is_valid_year(year):
            return f'Значение год должно быть числом в промежутке от 0 до {datetime.now().year} включительно.'

    def is_valid_id(self, book_id):
        return int(book_id) in self.db

    @staticmethod
    def is_valid_year(year):
        return year.isdigit() and (int(year) <= datetime.now().year)

    @staticmethod
    def is_valid_author_name(surname):
        return ''.join(''.join(''.join(surname.split()).split('-')).split('.')).isalpha()

    def search_by_match(self, value, key):
        value = value.strip()
        # поиск по автору или названию
        return [self.db[book_id] for book_id in self.db if value.lower() in self.db[book_id].__dict__[key].lower()]

    def search_by_year(self, year):
        year = year.strip()
        # поиск по году
        return [self.db[book_id] for book_id in self.db if year == self.db[book_id].year]

    def change_status_book(self, book_id):
        res = self.db[book_id].change_status()
        if self.save_mode:
            self.save_db()
        return res

    @staticmethod
    def create_book(*args, sep=None):
        if sep:
            args = args[0].strip().split(sep)
        return Book(*args)


if __name__ == "__main__":
    lib = Library(True)
    print(f'{lib.show_books() = }\n')

    print(*lib.search_by_match('ТОЛСТОЙ', 'author'), sep='\n', end='\n\n')
    print(*lib.search_by_match('пушк', 'author'), sep='\n', end='\n\n')

    print(*lib.search_by_match('Мир', 'title'), sep='\n', end='\n\n')
    print(*lib.search_by_match('#', 'title'), sep='\n', end='\n\n')

    print(lib.db[1].year)

    print(lib.search_by_year('2025'), sep='\n', end='\n\n')
    print(*lib.search_by_year('1900'), sep='\n', end='\n\n')

    # print(lib.change_status_book(1))

    # print(f"{lib.is_valid_author_name('zsfsgzrzF') = }")
    # print(f"{lib.is_valid_author_name('zsfsfzs SEefzsf sf') = }")
    # print(f"{lib.is_valid_author_name('2025') = }")
    # print(f"{lib.is_valid_author_name('zs-1000sfs') = }")
    # print(f"{lib.is_valid_author_name('szcsz-zsfs') = }")
    # print(f"{lib.is_valid_author_name('szcsz|zsfs') = }")
    # print(f"{lib.is_valid_author_name('szc@sz-zsf&s') = }")
    # print(f"{lib.is_valid_author_name('Толстой Л.Н.') = }")

