class Book:
    __COUNT_OBJ = 0

    def __init__(self, title, author, year, status='в наличии'):
        self.id = self._set_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __setattr__(self, key, value):
        if key == 'id':
            # не позволяет изменить id
            if key in self.__dict__:
                return
        object.__setattr__(self, key, value)

    def __str__(self):
        return f'Книга: {self.title}. Автор {self.author}. Дата издания: {self.year}. Сатус: {self.status}.'

    @classmethod
    def _set_id(cls):
        cls.__COUNT_OBJ += 1
        return cls.__COUNT_OBJ


class Library:
    def __init__(self, safe_mode=True):
        self.data_base = self.download_db()

    def download_db(self):
        books = {}
        with open('db.txt', 'r') as db:
            for i in db:
                book = self.add_book_from_db(i)
                books[book.id] = book
        return books

    def show_books(self):
        for book_id in self.data_base:
            print(f'ID:{book_id}. {str(self.data_base[book_id])}')

    def add_book_to_lib(self):
        pass

    def delete_book_from_db(self):
        pass

    def search_book(self):
        pass

    def change_status(self):
        pass

    @staticmethod
    def add_book_from_db(string):
        values = string.strip().split('|')
        return Book(*values)


if __name__ == "__main__":
    lib = Library(True)
    lib.show_books()
