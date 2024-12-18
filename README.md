# Тестовое задание.
### Описание
Необходимо разработать консольное приложение для управления библиотекой книг. Приложение должно позволять добавлять, удалять, искать и отображать книги. Каждая книга должна содержать следующие поля:
- id (уникальный идентификатор, генерируется автоматически)
- title (название книги)
- author (автор книги)
- year (год издания)
- status (статус книги: “в наличии”, “выдана”)

### Дополнительные требования
- Реализовать хранение данных в текстовом или json формате.
- Обеспечить корректную обработку ошибок (например, попытка удалить несуществующую книгу).
- Написать функции для каждой операции (добавление, удаление, поиск, отображение, изменение статуса).
- Не использовать сторонние библиотеки.

### Будет плюсом:
- Аннотации: Аннотирование функций и переменных в коде.
- Документация: Наличие документации к функциям и основным блокам кода.
- Описание функционала: Подробное описание функционала приложения в README файле.
- Тестирование.
- Объектно-ориентированный подход программирования.


<hr>

### Реализация

> Запуск программы осуществляется через файл main.py. 

> Далее определяется ОС пользователя, для формирования корректного пути к 
файлу, выполняющему функции БД (db.txt).

> Затем пользователю предлагается выбрать режим работы: безопасный 
(производит сохранения в БД, после внесения любого изменения в библиотеку), 
обычный (сохранение изменений производится только перед завершением работы 
приложения).

> После выполнения подготовительных шагов создается экземпляр класса 
Library, в котором и реализован основной функционал программы (добавление, 
удаление, поиск, отображение и изменение статуса).

> И наконец с помощью функции menu, вызывается основной интерфейс для 
взаимодействия с пользователем.

<hr>

## Классы

### Library

Атрибуты:<br>
>path_to_db:
>> Динамический атрибут. Содердит путь к базе данных.

>db:
>> Динамический атрибут. Содержит словарь, хранящий в качестве ключа 
> id экземпляра класса Book, а в качестве значения сам экземпляр.

>save_mode:
>> Динамический атрибут. Содержит булевое значение, где True - 
> безопасный режим, а False - обычный.

Методы:<br>
>download_db:
>> Загружает данные из файла db.txt, преобразует их в словарь и 
возвращает результат.

>save_db:
>> Сохраняет данные в файл db.txt.

>show_books:
>> Возвращает список строк, содержащих информацию о книгах.

>add_book_to_lib:
>> Создает новый экземпляр класса Book и добавляет его в словарь db.
В случае успеха, возвращает информацию о выполненном действии, в противном 
случае информацию об ошибке.

>delete_book_from_db:
>> Удаляет экземпляр объекта Book из словаря db.В случае успеха, 
возвращает информацию о выполненном действии, в противном случае 
информацию об ошибке.

>check_valid_data:
>> Используя методы is_valid_author_name и is_valid_year, проверяет 
корректность данных от пользователя. Кроме того проверяет, что бы в 
названии книги не присутствовал символ |, так как он используется в 
качестве разделителя в БД. В случае ошибки, возвращает строку с 
информацией о ней (иначе None).

>check_valid_id:
>> В случае не корректного указания id, возвращает строку с информацией
о ней (иначе None).

>search_by_match:
>> При поиске книг (по автору или по названию), принимает в качестве 
аргумента строку и проверяет ее вхождение в соответсвующем поле.
Функция возвращает список, содержащий экземпляры класса Book, имеющих
соответсвие по указанной категории (или пустой список, если совпадений 
не было).

>search_by_year:
>> Возвращает списов экземпляров класса Book, соответствующих указанной
дате издания (или пустой список, если совпадений не было).

>change_status_book:
>> Меняет статус экземпляра класса Book на противоположный("в наличии" 
или "выдана").

>is_valid_year:
>>Статический метод класса. Возвращает True, если указанное значение
даты издания является допустимым (иначе False).

>is_valid_author_name:
>>Статический метод класса. Возвращает True, если указанное значение
имени автора является допустимым (иначе False).

>create_book:
>>Статический метод класса. Создает и возвращает экземпляр класса 
Book, с указанными аргументами.

<hr>

### Book

Атрибуты:<br>
>__COUNT_OBJ:
>> Статичный атрибут класса, предназначенный для хранения максимального
ID его экземпляров.

>STATUSES:
>> Статичный атрибут класса, хранящего кортеж с возможными состояниями
("в наличии" или "выдана").

>id:
>> Динамический атрибут. Хранит уникальный id (число) экземпляра класса.

>title:
>> Динамический атрибут. Содержит строку с названием книги.

>author:
>> Динамический атрибут. Содержит строку с именем автора.

>year:
>> Динамический атрибут. Содержит строку с датой издания.

>status:
>> Динамический атрибут. Содержит строку со статусом книги.

Методы:<br>
>change_status:
>> Меняет состояние статуса книги на противоположный ("в наличии" или 
"выдана").

>__ __setattr__ __:
>> Переопределён "магический метод", чтобы не допустить изменение
атрибута id.

>__ __str__ __:
>> Переопределён "магический метод", чтобы возвращать строковую информацию
об экземпляре класса.

>_set_id:
>> Предназначен для присваивания уникальног id, при создании экземпляра
класса.
