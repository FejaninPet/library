import os


def identify_os_sep():
    os_name = os.name
    if os_name == 'posix':
        return '/'
    elif os_name == 'nt':
        return'\\'
    else:
        raise OSError('ОС не определена.')


def enable_save_mode():
    print('''Выберите режим работы:
    1). Безопасный (любые изменения сразу будут сохраняться в Базе Данных / требует больше времени на исполнение).
    2). Обычный (данные будут сохранены при окончанни работы приложения / при возникновении ошибок, данные могут быть частично утеряны).''')
    while True:
        res = input('\nВведит номер пункта: ')
        if res.strip() == '1':
            print('Вы работаете в безопасном режиме.\n')
            return True
        elif res.strip() == '2':
            print('Вы работаете в обычном режиме.\n')
            return False
        print('Допустимые значения 1 или 2. Попробуйте ещё раз.')


def menu(path_to_db, save_mode, lib):
    start = True
    menu_length = 6
    while start:
        print('''\nМЕНЮ:
        1). Отобразить список всех книг.
        2). Добавить книгу.
        3). Удалить книгу.
        4). Найти книгу.
        5). Изменить статус книги (получить / вернуть).
        6). Завершить работу (сохранить данные).''')
        user = input('Введит номер пункта: ')
        try:
            if int(user) in range(1, menu_length + 1):
                if user == '1':
                    print(*lib.show_books(), sep='\n')
                elif user == '2':
                    title = input('Укажите название книги: ').strip()
                    if not title:
                        print('Название книги не может быть пустым.')
                        continue
                    author = input('Укажите автора: ').strip()
                    if not author:
                        print('Имя автора не может быть пустым.')
                        continue
                    year = input('Укажите дату издания: ').strip()
                    if not year:
                        print('Дата издания не может быть пустым.')
                        continue
                    print(lib.add_book_to_lib(title, author, year))
                elif user == '3':
                    book_id = input('Укажите id книги, которую необходимо удалить: ').strip()
                    if not book_id:
                        print('id книги не может быть пустым.')
                        continue
                    print(lib.delete_book_from_db(book_id))
                elif user == '4':
                    search_res = search_menu(lib)
                    if type(search_res) is list and search_res:
                        print('Результат поиска:',
                              *[f'ID: {book.id}. {str(book)}' for book in search_res],
                              sep='\n')
                    elif not search_res:
                        print('По вашему запросу ничего не найдено. :(')
                    else:
                        print(search_res)
                elif user == '5':
                    book_id = input('Укажите id книги, которую необходимо удалить: ').strip()
                    if not book_id:
                        print('id книги не может быть пустым.')
                        continue
                    print(lib.change_status_book(book_id))
                elif user == '6':
                    lib.save_db()
                    print('Данные сохранены. Спасибо вам, что пользуетесь нашим программным обеспечением.')
                    input('Нажмите ENTER, для выхода из программы.')
                    break
                else:
                    print('Меню программы работает не коррктно, обратитесь к разработчику :)')
                    input('Нажмите ENTER, для выхода из программы.')
                    break
            else:
                print(f'Необходимо ввести число от 1 до {menu_length} (включительно).\nПопробуйте еще раз.\n')
        except ValueError:
            print('Необходимо вводить число!\n')


def search_menu(lib):
    while True:
        print('''\nПроизвести поиск по:
        1). Названию.
        2). Автору.
        3). Дате издания.
        4). Отменить поиск.''')
        res = input('\nВведит номер пункта: ').strip()
        if res not in ('1', '2', '3', '4'):
            print('Допустимые значения: 1, 2, 3 или 4. Попробуйте ещё раз.')
        else:
            if res == '1':
                title = input('Введите название (или часть названия) книги: ').strip()
                if not title:
                    print('Название книги не может быть пустым.')
                    continue
                return lib.search_by_match(title, 'title')
            elif res == '2':
                author = input('Введите фамилию (или часть фамилии) автора: ').strip()
                if not author:
                    print('Имя автора не может быть пустым.')
                    continue
                return lib.search_by_match(author, 'author')
            elif res == '3':
                year = input('Введите дату издания книги: ').strip()
                if not year:
                    print('Дата издания не может быть пустым.')
                    continue
                return lib.search_by_year(year)
            elif res == '4':
                return 'Вы отменили поиск.'
            else:
                return 'Меню поиска работает не коррктно, обратитесь к разработчику :)'
