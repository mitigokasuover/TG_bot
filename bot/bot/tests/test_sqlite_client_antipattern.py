import sqlite3

from clients.sqlite3_client import SQLiteClient
from tests.conftest import TEST_DB_URL

# запрос для создания таблицы
CREATE_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
user_id serial NOT NULL,
username varchar NOT NULL,
chat_id integer NOT NULL
);
"""

# запрос для спиливания таблиц
DROP_USER_TABLE_QUERY = """
DROP TABLE users;
"""

DB_CONNECTION = sqlite3.connect(TEST_DB_URL)


def create_user(user_id: int, username: str, chat_id: int):
    """функция для наполнения базы тестовыми данными"""
    DB_CONNECTION.execute("""INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);""",
                          (user_id, username, chat_id))
    DB_CONNECTION.commit()


def read_users():
    """функция чтения из тестовой базы данных"""
    cursor = DB_CONNECTION.cursor()
    cursor.execute("""SELECT * FROM users;""")
    return cursor.fetchall()

def create_tables():
    cursor = DB_CONNECTION.cursor()
    cursor.execute(CREATE_USER_TABLE_QUERY)


def drop_tables():
    cursor = DB_CONNECTION.cursor()
    cursor.execute(DROP_USER_TABLE_QUERY)


def test_write_to_db_by_command_refactored():
    # команда, которая будет использоваться для тестирования клиента
    command = """
    INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
    """

    # тестовые данные
    user_id = 1
    username = "luchanos"
    chat_id = 123123

    # создаём клиент, который мы будем тестировать
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()

    # запускаем команду на запись в базу
    client.execute_command(command, (user_id, username, chat_id))

    # используем функцию для чтения
    users = read_users()

    # проверяем, что в базу действительно всё прописалось
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id


def test_read_from_db_by_client_refactored():
    # тестовые данные
    user_id = 1
    username = "luchanos"
    chat_id = 123123

    # создадим в базе строку с помощью функции, которую потом будем читать с помощью тестируемого клиента
    create_user(user_id, username, chat_id)

    # команда для передачи в клиент, который мы будем тестировать
    command = """
    SELECT * FROM users;
    """

    # создаем клиент, который будем тестировать
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()
    users = client.execute_select_command(command)

    # проверяем, что достали из базы желаемые значения
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id
