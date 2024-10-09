import os
import sys

from dotenv import load_dotenv
import psycopg2


# Функция подключения к базе данных
def connect_to_database(DB_NAME):
    # Определяем путь к файлу .env
    extDataDir = os.getcwd()
    if getattr(sys, 'frozen', False):
        extDataDir = sys._MEIPASS
    load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')

    if DB_USER:
        print(f"The value of MY_SECRET is: {extDataDir, DB_USER}")
    else:
        print("MY_SECRET is not set.")

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



