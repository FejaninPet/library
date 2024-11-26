from obj.objects import Library


def enable_safe_mode():
    # TODO
    return True


def menu(safe_mode):
    start = True
    menu_length = 6
    while start:
        print('''МЕНЮ:
        1). Отобразить список всех книг.
        2). Добавить книгу.
        3). Удалить книгу.
        4). Найти книгу.
        5). Изменить статус книги (получить / вернуть).
        6). Завершить работу (сохранить данные).''')
        user = input('Введит номер пункта: ')
        try:
            if int(user) in range(1, menu_length + 1):
                # TODO Выполнить запрос пользователя
                pass
            else:
                print(f'Необходимо ввести число от 1 до {menu_length} (включительно).\nПопробуйте еще раз.\n')
        except ValueError:
            print('Необходимо вводить число!\n')


if __name__ == "__main__":
    safe_mode = enable_safe_mode()
    menu(safe_mode)
