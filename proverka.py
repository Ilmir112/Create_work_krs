import sqlite3
import psycopg2

# Параметры подключения к SQLite
import well_data

sqlite_db_path = 'data_base/data_base_gnkt/gnkt_base.dp'



def copy_tables(sqlite_conn, postgres_conn):
    # Получение списка таблиц из SQLite
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    print(tables)
    # Обработка каждой таблицы
    for table_name in tables[1:]:

        table_name = table_name[0]


        # Получение схемы таблицы SQLite
        sqlite_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        table_schema = sqlite_cursor.fetchone()[0].replace('AUTOINCREMENT', '')
        print(f'jjf {table_schema}')

        # Создание таблицы в PostgreSQL (если она не существует)
        postgres_cursor = postgres_conn.cursor()
        postgres_cursor.execute(f'{table_schema}')

        # Получение данных из таблицы SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table_name};")
        rows = sqlite_cursor.fetchall()

        # Вставка данных в таблицу PostgreSQL
        placeholders = ', '.join(['%s'] * len(rows[0]))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        postgres_cursor.executemany(insert_query, rows)

        postgres_conn.commit()

# Подключение к базам данных
sqlite_conn = sqlite3.connect(sqlite_db_path)
postgres_conn = psycopg2.connect(**well_data.postgres_conn_gnkt)

# # Копирование таблиц
copy_tables(sqlite_conn, postgres_conn)
print('копирование завершено')
cursor = postgres_conn.cursor()
# # Выполнение запроса (например, выбор всех записей из таблицы "users")
# cursor.execute("SELECT * FROM ЧГМ_классификатор")
#
# # Получение результатов
# rows = cursor.fetchall()
#
# # Обработка результатов (например, печать каждой строки)
# for row in rows:
#     print(row)


# import sqlite3
# import psycopg2
#
#
# # Параметры подключения к SQLite
# sqlite_db_path = 'data_base/data_base_well/databaseWell.db'
#
# # Подключение к базам данных
# sqlite_conn = sqlite3.connect(sqlite_db_path)
# postgres_conn = psycopg2.connect(**well_data.postgres_params_classif)
# sqlite_cursor = sqlite_conn.cursor()
# postgres_cursor = postgres_conn.cursor()
#
# # Получение списка таблиц из SQLite
# sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# tables = sqlite_cursor.fetchall()
#
# for data in tables:
#     postgres_cursor.execute("INSERT INTO table VALUES =(%s)", data)
#
# # Сохранение изменений и закрытие соединений
# postgres_conn.commit()
# sqlite_conn.close()
# postgres_conn.close()
