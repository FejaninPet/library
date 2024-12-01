from obj.objects import Library
from interface.interface import identify_os_sep, enable_save_mode, menu


if __name__ == "__main__":
    sep = identify_os_sep()
    path_to_db = f'db{sep}db.txt'
    save_mode = enable_save_mode()
    lib = Library(path_to_db, save_mode)
    menu(path_to_db, save_mode, lib)

