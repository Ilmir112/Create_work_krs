import sys

from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import data_list

def decrypt(name):

    # Загрузка ключа
    with open(f"{data_list.path_image}key.key", 'rb') as key_file:
        key = key_file.read()
    cipher = Fernet(key)

    # В продакшене (frozen) .env лежит рядом с exe (например D:\ZIMA), не в MEIPASS
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        env_path = os.path.join(base_dir, '.env')
        if not os.path.isfile(env_path):
            env_path = os.path.join(base_dir, '_internal', '.env')
        load_dotenv(dotenv_path=env_path)
    else:
        ext_data_dir = os.getcwd()
        load_dotenv(dotenv_path=os.path.join(ext_data_dir, '.env'))

    value = os.getenv(name)
    if value is None:
        plain_name = f"{name}_PLAIN"
        plain_value = os.getenv(plain_name)
        if plain_value is not None:
            return plain_value
        raise ValueError(
            f"Переменная окружения '{name}' не найдена в .env. "
            f"Добавьте '{name}' или '{plain_name}' в .env в папке приложения (рядом с exe)."
        )
    encrypted_value = value.encode()

    # Дешифруем значение
    decrypted_value = cipher.decrypt(encrypted_value)
    return decrypted_value.decode()

