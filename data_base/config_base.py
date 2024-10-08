import os
import sys

from dotenv import load_dotenv
import psycopg2





# Функция подключения к базе данных
def connect_to_database(DB_NAME):
    # Определяем путь к файлу .env
    # if getattr(sys, 'frozen', False):  # Проверка, запущен ли скрипт как исполняемый файл
    #
    #     env_path = os.path.join(sys._MEIPASS, '.env')
    # else:
    #     env_path = '.env'

    load_dotenv()  # Получаем путь к .env
    print("DB_USER:", os.getenv('DB_USER'))
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')

    try:

        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        return connection
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

# print(connect_to_database(DB_NAME))



