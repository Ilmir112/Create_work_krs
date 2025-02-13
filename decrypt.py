from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os




def decrypt(name):
    # Загрузка ключа
    with open('key.key', 'rb') as key_file:
        key = key_file.read()
    cipher = Fernet(key)

    # Загружаем .env файл
    load_dotenv()
    encrypted_value = os.getenv(name).encode()

    # Дешифруем значение
    decrypted_value = cipher.decrypt(encrypted_value)
    return decrypted_value.decode()

