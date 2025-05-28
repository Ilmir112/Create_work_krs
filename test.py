import subprocess

# Настройки подключения
HOST = '176.109.106.199'
USER = 'postgres'  # или ваш пользователь
PASSWORD = '195375AsD+'  # если требуется
DB_NAME = 'zima_data'
PORT_SOURCE = 5432
PORT_TARGET = 5433

# Пути к утилитам (если не в PATH, укажите полный путь)
PG_DUMP = r"C:\Program Files\PostgreSQL\15\bin\pg_dump.exe"
CREATE_DB = r"C:\Program Files\PostgreSQL\15\bin\createdb.exe"
PG_RESTORE = r"C:\Program Files\PostgreSQL\15\bin\pg_restore.exe"

# Файл дампа
DUMP_FILE = f'D:/Documents/Create_work_krs/users/{DB_NAME}_backup.dump'

def run_command(command, env=None):
    """Выполняет команду и выводит результат."""
    print(f"Выполняется: {' '.join(command)}")
    result = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Ошибка: {result.stderr}")
        raise Exception(f"Команда {' '.join(command)} завершилась с ошибкой.")
    return result.stdout

def dump_database():
    """Делает дамп базы данных."""
    command = [
        PG_DUMP,
        '-U', USER,
        '-h', HOST,
        '-p', str(PORT_SOURCE),
        '-Fc',
        '-f', DUMP_FILE,
        DB_NAME
    ]
    run_command(command)
    print(f"Дамп базы {DB_NAME} сохранен в {DUMP_FILE}")

def create_database():
    """Создает новую базу данных на целевом порту."""
    command = [
        CREATE_DB,
        '-U', USER,
        '-h', HOST,
        '-p', str(PORT_TARGET),
        DB_NAME
    ]
    run_command(command)
    print(f"База {DB_NAME} создана на порту {PORT_TARGET}")

def restore_database():
    """Восстанавливает базу из дампа."""
    command = [
        PG_RESTORE,
        '-U', USER,
        '-h', HOST,
        '-p', str(PORT_TARGET),
        '-d', DB_NAME,
        DUMP_FILE
    ]
    run_command(command)
    print(f"База {DB_NAME} восстановлена из {DUMP_FILE}")

def main():
    # Установка переменной окружения для пароля (если нужно)
    env = {'PGPASSWORD': PASSWORD}

    dump_database()
    create_database()
    restore_database()

if __name__ == "__main__":
    main()