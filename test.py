import psycopg2



# Создание подключения
conn = psycopg2.connect(**well_data.postgres_params_classif)

with conn:
    with conn.cursor() as cursor:
        print("Подключение установлено")

# Создание курсора
cur = conn.cursor()

# Выполнение запроса (например, выбор всех записей из таблицы "users")
cur.execute("SELECT * FROM users;")

# Получение результатов
rows = cur.fetchall()

# Обработка результатов (например, печать каждой строки)
for row in rows:
    print(row)

# Закрытие курсора и подключения
cur.close()
conn.close()