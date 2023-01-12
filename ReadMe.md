````
Мережа ресторанів доставки "жрачка топ" має безліч точок, на яких готуються замовлення для клієнтів. Кожен клієнт хоче разом із замовленням отримати чек, що містить детальну інформацію про замовлення. Співробітники кухні також хочуть чек, щоб у процесі приготування та упаковки замовлення не забути покласти все що потрібно. Наше завдання допомогти і тим, і іншим, написавши сервіс для генерації чеків.
Схема роботи сервісу:

Сервіс отримує інформацію про нове замовлення, створює в БД чеки для всіх принтерів точки, зазначеної в замовленні, і ставить асинхронні завдання на генерацію PDF-файлів для цих чеків. Якщо точка не має жодного принтера - повертає помилку. Якщо чеки для цього замовлення вже були створені – повертає помилку(передається номер замовлення).
Асинхронний воркер за допомогою wkhtmltopdf генерують PDF-файл із HTML-шаблону. Ім'я файлу повинно мати такий вигляд <ID замовлення>_<тип чека>.pdf (123456_client.pdf). Файли повинні зберігатися у папці media/pdf у корені проекту.
Програма опитує сервіс на наявність нових чеків. Опитування відбувається наступним шляхом: спочатку запитується список чеків, які вже згенеровані для конкретного принтера, після скачується PDF-файл для кожного чека і відправляється на друк. (це типу принтер, який міняє статус в друці чеку)
Технічні вимоги:
Сервіс повинен бути написаний на python та Django
База даних - PostgreSQL
Всі інфраструктурні речі, необхідні для сервісу (PostgreSQL, Redis, wkhtmltopdf) запускати в docker за допомогою docker-compose, сам проект не потрібно обертати в docker.
Крім API, має бути адмінка для обох моделей, з можливістю фільтрувати чеки за принтером, типом і статусом

Моделі:
Принтер (Printer). Кожен принтер друкує лише свій тип чеків. Поле api_key набуває унікальних значень, по ньому однозначно визначається принтер. Для цієї моделі повинні бути fixtures (принтери для обох типів чеків для кількох точок).
Поле
Тип
Значення
Опис
name
CharField


назва принтеру
api_key
CharField


ключ доступу до API
check_type
CharField
kitchen|client
тип чеку який друкує принтер
point_id
IntegerField


точка до якої привязаний принтер

Чек (Check). Інформація про замовлення кожного чека зберігається в JSON, немає необхідності робити окремі моделі.
Поле
Тип
Значение
Описание
printer_id
ForeignKey


принтер
type
CharField
kitchen|client
тип чеку
order
JSONField


інформація про замовлення
status
CharField
new|rendered|printed
статус чеку
pdf_file
FileField


посилання на створений PDF-файл



````

For possibility to run services need install **docker, docker-compose**
* Activate virtual environment run -- poetry shell (required **Poetry** https://python-poetry.org/docs/basic-usage/)
* Install dependencies run -- poetry install
* docker-compose up (install and run services)
* python manage.py makemigrations
* python manage.py migrate
* python manage.py create_mock_data --points 5 ->"[insted 5 you can provide any number of points which want to use in for test ]"
* python manage.py rqworker (run rq worker)

### API endpoints:

1) Create check with orders -
**/api/create_checks/**

    data for test create:
````
    {
    "order":{"items": [
    {
      "name": "Test",
      "quantity": 1,
      "unit_price": 100
    }], 
   "client": {
      "name": "Test User", 
      "phone": "0000000000"
       }, 
   "address": "Test Address",
   "point_id": 4,
   "order_id": 5
    }}
````

2) List with new checks - 
**/api/new_checks/{printer_api}/**
3) Get pdf check for print
**/api/check/{id}/**
