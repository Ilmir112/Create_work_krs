import sqlite3
import psycopg2

# Параметры подключения к SQLite
sqlite_db_path = 'data_base/data_base_well/databaseWell.db'

# Параметры подключения к PostgreSQL
postgres_db_config = {
    'host': 'localhost',
    'database': 'databaseWell.db',
    'user': 'postgres',
    'password': '1953'
}

# Подключение к базам данных
sqlite_conn = sqlite3.connect(sqlite_db_path)
postgres_conn = psycopg2.connect(*postgres_db_config)
sqlite_cursor = sqlite_conn.cursor()
postgres_cursor = postgres_conn.cursor()

# Получение списка таблиц из SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = sqlite_cursor.fetchall()

# Перенос данных для каждой таблицы
for table_name, in tables:
    # Получение схемы таблицы
    sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
    table_info = sqlite_cursor.fetchall()

    # Создание таблицы в PostgreSQL
    create_table_sql = f"CREATE TABLE {table_name} ("
    for column_info in table_info:
        column_name, data_type, _, _, _, _ = column_info
        create_table_sql += f"{column_name} {data_type},"
    create_table_sql = create_table_sql[:-1] + ")"
    postgres_cursor.execute(create_table_sql)

    # Получение данных из SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    data = sqlite_cursor.fetchall()

    # Вставка данных в PostgreSQL
    insert_sql = f"INSERT INTO {table_name} VALUES ({','.join(['%s' for _ in range(len(table_info))])})"
    postgres_cursor.executemany(insert_sql, data)

# Сохранение изменений и закрытие соединений
postgres_conn.commit()
sqlite_conn.close()
postgres_conn.close()
