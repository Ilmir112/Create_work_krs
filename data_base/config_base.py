import os
import sys

from dotenv import load_dotenv
import psycopg2


# Загрузите переменные окружения из файла .env
load_dotenv()

# Получите настройки подключения из переменных окружения
DB_WELL_DATA = os.getenv('DB_WELL_DATA')
DB_NAME_USER = os.getenv('DB_NAME_USER')
DB_USER = os.getenv('DB_USER')
DB_NAME_GNKT = os.getenv('DB_NAME_GNKT')
DB_CLASSIFICATION = os.getenv('DB_CLASSIFICATION')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


# Функция подключения к базе данных
def connect_to_database(DB_NAME):
    # Определяем путь к файлу .env
    if getattr(sys, 'frozen', False):  # Проверка, запущен ли скрипт как исполняемый файл
        print('1')
        env_path = os.path.join(sys._MEIPASS, '.env')  # Получаем путь к .env
    else:
        env_path = '.env'  # Если не исполняемый файл, используем текущую директорию
    print(env_path)
    # Загрузите переменные окружения из файла .env
    load_dotenv(env_path)

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    print(DB_USER)

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



