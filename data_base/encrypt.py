from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key
import os


DB_WELL_DATA = 'well_data'
DB_NAME_USER = 'krs2'
DB_NAME_GNKT = 'gnkt_database'
DB_CLASSIFICATION = 'databaseclassification'
DB_USER = 'postgres'
DB_PASSWORD = '195375AsD+'
DB_HOST = '176.109.106.199'
DB_PORT = 5432

# Генерация ключа
key = Fernet.generate_key()
cipher = Fernet(key)

def generate_key(name, value_to_encrypt):

    # Замените 'your_value' на значение, которое нужно зашифровать

    encrypted_value = cipher.encrypt(value_to_encrypt)

    # Сохранение зашифрованного значения в .env
    load_dotenv()  # Загружаем текущие переменные окружения
    set_key('.env', name, encrypted_value.decode())  # Сохраняем зашифрованное значение

generate_key("DB_PASSWORD", b'195375AsD+')
generate_key("DB_WELL_DATA",b'well_data')
generate_key("DB_HOST", b'176.109.106.199')
generate_key("DB_USER", b'postgres')
generate_key("DB_CLASSIFICATION", b'databaseclassification')
generate_key("DB_NAME_USER", b'krs2')
generate_key("DB_NAME_GNKT", b'gnkt_database')
generate_key("DB_PORT", b'5432')

# Сохраните ключ в безопасном месте
with open('key.key', 'wb') as key_file:
    key_file.write(key)
    



