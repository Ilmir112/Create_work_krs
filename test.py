import psycopg2



# Создание подключения
import well_data
from data_base.config_base import connect_to_database, DB_CLASSIFICATION

conn = connect_to_database(well_data.DB_CLASSIFICATION)

with conn:
    with conn.cursor() as cursor:
        print("Подключение установлено")

# Создание курсора
cur = conn.cursor()

# Выполнение запроса (например, выбор всех записей из таблицы "users")
cur.execute("SELECT * FROM users;")

# Получение результатов
rows = cur.fetchall()

# # Обработка результатов (например, печать каждой строки)
# for row in rows:
#     print(row)

# Закрытие курсора и подключения
cur.close()
conn.close()