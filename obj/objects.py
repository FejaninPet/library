from datetime import datetime
from interface.interface import identify_os_sep


class Book:
    '''
    Класс для представления книги.
    ...
    Атрибуты
    --------
    title: str
        Название книги.
    author: str
        Автор книги.
    year: str
        Дата издания книги.
    status: str
        Сатус книги ( наличии/выдана).

    Методы
    ------
    change_status():
        Меняет текущий статус книги.
    _set_id():
        Предоставляет id для нового объекта класса (классовый метод).
    '''
    __COUNT_OBJ = 0
    STATUSES = ('в наличии', 'выдана')

    def __init__(self, title, author, year, status='в наличии'):
        '''
        Создает все необходимые атрибуты для экзепляра класса Book.
        :param title: str
        :param author: str
        :param year: str
        :param status: str
        '''
        self.id = self._set_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def change_status(self):
        '''
        Меняет текущее значение статуса книги на противоположное (в наличии/выдана)
        :return: str
        '''
        self.status = self.STATUSES[(self.STATUSES.index(self.status) + 1) % 2]
        return f'Статус кинги "{self.title}" изменен. Теперь она {self.status}.'

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
        '''
        Увеличивает значение __COUNT_OBJ на 1 и возвращает результат
        :return: int
        '''
        cls.__COUNT_OBJ += 1
        return cls.__COUNT_OBJ


class Library:
    '''
    Класс для представления библиотеки.
    ...
    Атрибуты
    --------
    path_to_db: str
        Путь к БД.
    db: dict
        Хранилище. Словарь содержащий всю информацию о книгах.
    save_mode: bool
        Режим работы.

    Методы
    ------
    download_db(path_to_db):
        Загружает в хранилище информацию из БД.
    save_db():
        Сохраняет информацию, содержащуюся в хранилищу, в БД.
    show_books():
        Возвращает список с информацией о книгах в хранилище.
    add_book_to_lib(title, author, year):
        Сохраняет книгу с заданными значениями в хранилище.
    delete_book_from_db(book_id):
        Удаляет книгу из хранилища, по указанному id.
    check_valid_data(title, author, year):
        Проверяет валидность переданных пользователем данных.
    check_valid_id(book_id):
        Проверяет валидность переданного id книги.
    is_valid_year(year):
        Проверяет валидность года издания книги (статический метод).
    is_valid_author_name(surname):
        Проверяет валидность имени автора (статический метод).
    search_by_match(value, key):
        Нахождение книг по совпадению в имени автора или названии книги.
    search_by_year(year):
        Нахождение книг(и) по году издания.
    change_status_book(book_id):
        Меняет статус книги, находящейся в хранилище.
    create_book(*args, sep=None):
        Создает новый экземпляр класса Book, согласно переданным аргументам.
    '''
    def __init__(self, path_to_db, save_mode=True):
        '''
        Создает все необходимые атрибуты для экзепляра класса Library.
        :param path_to_db: str
        :param save_mode: bool
        '''
        self.path_to_db = path_to_db
        self.db = self.download_db(path_to_db)  # dict
        self.save_mode = save_mode

    def download_db(self, path_to_db):
        '''
        Принимает в качестве параметра путь к БД, считывает из нее данные, преобразует их в
        экземпляры класса Book. Полученные объекты сохраняет в словаре, где ключом служит id
        объекта.
        :param path_to_db: str
        :return: dict
        '''
        books = {}
        with open(path_to_db, 'r') as f:
            for i in f:
                book = self.create_book(i, sep='|')
                books[book.id] = book
        return books

    def save_db(self):
        '''
        Сохраняет данные в файле, выполняющем роль БД.
        :return: None
        '''
        with open(self.path_to_db, 'w') as f:
            for i in self.db:
                f.write(f'{self.db[i].title}|{self.db[i].author}|{self.db[i].year}|{self.db[i].status}\n')

    def show_books(self):
        '''
        Возвращает список строк, хранящих информацию об имеющихся в библиотеке книгах.
        :return: list
        '''
        res = []
        for book_id in self.db:
            res.append(f'ID:{book_id}. {str(self.db[book_id])}')
        return res

    def add_book_to_lib(self, title, author, year):
        '''
        Принимает в качестве аргументов строки с названием книги, фамилией автора и датой издания.
        В случае прохождения проверки на валидность данных, добавляет новую книгу в хранилище и
        возвращает информацию об успешном выполнении задания. Иначе возвращает информацию об ошибке.
        :param title: str
        :param author: str
        :param year: str
        :return: str
        '''
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
        '''
        Принимает в качестве аргумента id книги, проверяет валидность принятого аргумента. В случае
        корректных данных, возвращает информацию об удалении книги из хранилища. Иначе возвращает
        информацию об ошибке.
        :param book_id: int
        :return: str
        '''
        not_valid_id = self.check_valid_id(book_id)
        if not_valid_id:
            return not_valid_id
        book_name = self.db[int(book_id)].title
        del self.db[int(book_id)]
        if self.save_mode:
            self.save_db()
        return f'Книга "{book_name}" удалена.'

    def check_valid_data(self, title, author, year):
        '''
        Проверяет валидность данных с использованием функций: is_valid_author_name и is_valid_year,
        а также проверяет, не содержит ли заголовок символ |, т.к. данный символ используется в качестве
        разделителя в БД. Если данные не являются валидными, возвращает строку с описанием ошибки. Иначе
        возвращает None.
        :param title: str
        :param author: str
        :param year: str
        :return: str or None
        '''
        if '|' in title:
            return 'Название книги не должно содержать символ "|".'
        if not self.is_valid_author_name(author):
            return 'Имя автора может состоять только из букв и символов: дефис, пробел и точка.'
        if not self.is_valid_year(year):
            return f'Значение год должно быть числом в промежутке от 0 до {datetime.now().year} включительно.'

    def check_valid_id(self, book_id):
        '''
        Принимает id книги в качестве аргумента и проводит 2-е проверки.
        1). Является ли id положительным, целым чисом.
        2). Присутствует ли данное число в качестве ключа в хранилище книг.
        Если выявлена ошибка, то возвращается информация об ошибке. Иначе - None.
        :param book_id: int
        :return: str or None
        '''
        if not book_id.isdigit():
            return 'id должно быть положительным числом, больше 0.'
        if not int(book_id) in self.db:
            return 'Книги с таким id не существует.'

    @staticmethod
    def is_valid_year(year):
        '''
        Принимает в качестве значения строку и проверяет ли она положительным целым числом и
        не превышает ли ее значение текущего года. Возвращает булевое значение.
        :param year: str
        :return: bool
        '''
        return year.isdigit() and (int(year) <= datetime.now().year)

    @staticmethod
    def is_valid_author_name(surname):
        '''
        Проверяет содержит ли строка только допустимые значения (буквы, символы дефис и точка).
        Возвращает булевое значение
        :param surname: str
        :return: bool
        '''
        return ''.join(''.join(''.join(surname.split()).split('-')).split('.')).isalpha()

    def search_by_match(self, value, key):
        '''
        Формирует и возвращает список экземпляров класса Book, имеющих вхождение подстроки (value) в строку,
        хранящуюся в атрибуте, соответствующем key.
        :param value: str
        :param key: str
        :return: list
        '''
        value = value.strip()
        # поиск по автору или названию
        return [self.db[book_id] for book_id in self.db if value.lower() in self.db[book_id].__dict__[key].lower()]

    def search_by_year(self, year):
        '''
        Формирует и возвращает список экземпляров класса Book, содержащих в атрибуте key значение year.
        :param year: str
        :return: list
        '''
        year = year.strip()
        # поиск по году
        return [self.db[book_id] for book_id in self.db if year == self.db[book_id].year]

    def change_status_book(self, book_id):
        '''
        Проверяет на валидность полученный id книги. Если книга с таким id существует, меняет ее статус,
        с помощью метода change_status класса Book. Иначе, возвращает информацию об ошибке.
        :param book_id: str
        :return: str
        '''
        not_valid_id = self.check_valid_id(book_id)
        if not_valid_id:
            return not_valid_id
        res = self.db[int(book_id)].change_status()
        if self.save_mode:
            self.save_db()
        return res

    @staticmethod
    def create_book(*args, sep=None):
        '''
        Преобразует args в аргументы необходимые для создания экземпляра класса Book. Далее создает
        и возвращает созданный экземпляр.
        :param args: list or str
        :param sep: str or None
        :return: None
        '''
        if sep:
            args = args[0].strip().split(sep)
        return Book(*args)


if __name__ == "__main__":
    sep = identify_os_sep()
    db_name = f'..{sep}db{sep}db.txt'
    lib = Library(db_name, True)

    print(lib.__doc__)

    # print(f'{lib.show_books() = }\n')
    #
    # print(*lib.search_by_match('ТОЛСТОЙ', 'author'), sep='\n', end='\n\n')
    # print(*lib.search_by_match('пушк', 'author'), sep='\n', end='\n\n')
    #
    # print(*lib.search_by_match('Мир', 'title'), sep='\n', end='\n\n')
    # print(*lib.search_by_match('#', 'title'), sep='\n', end='\n\n')
    #
    # print(lib.db[1].year)
    #
    # print(lib.search_by_year('2025'), sep='\n', end='\n\n')
    # print(*lib.search_by_year('1900'), sep='\n', end='\n\n')

    # print(lib.change_status_book(1))

    # print(f"{lib.is_valid_author_name('zsfsgzrzF') = }")
    # print(f"{lib.is_valid_author_name('zsfsfzs SEefzsf sf') = }")
    # print(f"{lib.is_valid_author_name('2025') = }")
    # print(f"{lib.is_valid_author_name('zs-1000sfs') = }")
    # print(f"{lib.is_valid_author_name('szcsz-zsfs') = }")
    # print(f"{lib.is_valid_author_name('szcsz|zsfs') = }")
    # print(f"{lib.is_valid_author_name('szc@sz-zsf&s') = }")
    # print(f"{lib.is_valid_author_name('Толстой Л.Н.') = }")

