<h3>**Web-service**</h3>
***
**Web-сервис для сортировки и записи массива целых чисел в базу данных.**
***
<h5>Установка приложения</h5>

Перейдите в домашний каталог пользователя сервера ubuntu и запустите:<br>

$ git clone https://github.com/dimkinsl/webservice

$ cd webservice



В корне проекта создайте файл .env с вашими значениями переменных:

POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=database_name
POSTGRES_HOST=db
POSTGRES_PORT=5432

Важное замечание!
POSTGRES_HOST в файле .env и имя в сервисе файла docker-compose.yml должны быть одинаковы.

Запустите docker-compose up --build -d

После запуска контейнеров в терминале выполните команду:

docker-compose exec app bash

Выполните инициализацию Alembic компандой:

alembic init alembic

Перейдите в каталог alembic и отредактируйте файл env.py

Добавьте следующие строки:

from tornado_sqlalchemy import SQLAlchemy

database_url = 'postgresql://user_name:password@database_host:port/database_name'

db = SQLAlchemy(database_url)

target_metadata = db.metadata

database_url - согласно вашим переменным окружения.

В файле alembic.ini в корне проекта, также укажите данные для подключения к базе данных в переменной sqlalchemy.url

Введите в терминале команду для генерации миграции: 

alembic revision --message="You_message" --autogenerate

<h5>Запуск приложения</h5>

В браузере введите http://127.0.0.1:8888/post


Инструкция по API:

Отправка данных методом POST:

Вы можете отправить массив чисел разделенный запятыми в форме:
http://127.0.0.1:8888/post

Результат ответа: если данные валидны и обработаны, в ответ вернется статус и номер id в базе данных

Получение данных из БД методом GET:

В адресной строке браузера введите, к примеру:
http:/127.0.0.1:8888/id/{id}

{id} - номер записи в базе.

Результат ответа: если введенный id валидный и такой id есть в БД, в ответ вернется json, содержащий поля: id, переданный массив, результирующий массив и дату создания записи.
