#!/usr/bin/env python

"""Web-сервис для сортировки и записи массива целых чисел.
Данные (целые чила раздленные запятой) от пользователя принимаются через форму,
сортируются, запсываются в базу данных. В ответе отправки формы возвращается
статус и id записи в базе данных.
Для получения записи из базы данных, необходимо через API-интерфейс указать
id записи.
Пример:
Оправка данных
http://localhost:8888/post/
Получение результата первой записи
http://localhost:8888/id/1"""

import os
import uuid
import tornado.ioloop
import logging

from datetime import datetime
from tornado_sqlalchemy import SQLAlchemy, SessionMixin
from sqlalchemy import Column, BigInteger, String, DateTime
from tornado.web import Application, RequestHandler

# Переменные окружения для подключения к базе данных
db_name = os.getenv('POSTGRES_DB', 'test')
db_user = os.getenv('POSTGRES_USER', 'user')
db_password = os.getenv('POSTGRES_PASSWORD', 'pass')
db_port = os.getenv('POSTGRES_PORT', 5432)
db_host = os.getenv('POSTGRES_HOST', 'localhost')


database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

db = SQLAlchemy(url=database_url)


async def sort_array(array: str) -> str or None:
    # Функция сортировки массива.
    result = []
    # Проверяем данные навалидность
    try:
        [result.append(int(i)) for i in array.split(',')]
        return str(sorted(result))
    except ValueError:
        return None


# Объявляем модель
class DataSet(db.Model):
    __tablename__ = 'dataset'
    id = Column(BigInteger, primary_key=True)
    array = Column(String(255))
    result_array = Column(String(255))
    created_on = Column(DateTime(), default=datetime.now())


class GetIDHandler(SessionMixin, RequestHandler):
    # API для получения данных
    async def get(self, id):
        self.id = id
        # Проверям является ли переданное значение числом
        if id.isdigit():
            with self.make_session() as session:
                # Отправлям запрос в базу данных, если такой id есть, возвращаем результат
                try:
                    data = session.query(DataSet).get(id)
                    result = {
                        'id': data.id,
                        'array': data.array,
                        'result_array': data.result_array,
                        'date_of_creation': data.created_on.strftime('%d.%m.%Y %H:%M:%S')
                    }
                    self.write(result)
                except AttributeError as e:
                    logging.exception(f'Возникло исключение: {e}')
                    self.write({"result": "ERROR"})
        else:
            self.write({"result": "ERROR"})


class PostHandler(SessionMixin, RequestHandler):
    # Отправка данных через форму
    async def get(self):
        # Загружаем шаблон с формой
        self.render("templates/post.html") # костыль, не берет шаблон из папки templates

    async def post(self):
        # Обработка принятых данных с формы
        result = await sort_array(self.get_body_argument('array'))
        # Если данные валидны, записываем результат в базу данных
        if result:
            with self.make_session() as session:
                new_data = DataSet(
                    array=self.get_body_argument('array'),
                    result_array=result,
                    created_on=datetime.now()
                )
                session.add(new_data)
                session.commit()
                # Получаем id записи
                get_id = new_data.id

            # Возвращаем ответ и id записи
            self.write({'result': 'OK', 'id': get_id})
        else:
            self.write({'result': 'ERROR'})


def main():
    # Функция точки входа
    app = Application(
        [
            (r'/id/(.*)', GetIDHandler),
            (r'/post', PostHandler),
        ],
        db=SQLAlchemy(database_url),
        settings=dict(
            title=u'Dataset',
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
            cookie_secret=str(uuid.uuid4().int),
            debug=False,
        )
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
