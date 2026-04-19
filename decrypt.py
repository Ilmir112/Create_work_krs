import os

from cryptography.fernet import Fernet

import data_list
from config import settings


def decrypt(name):
    # Загрузка ключа
    with open(f"{data_list.path_image}key.key", 'rb') as key_file:
        key = key_file.read()
    cipher = Fernet(key)

    settings.load_env()
    value = os.getenv(name)
    if value is None:
        plain_name = f"{name}_PLAIN"
        plain_value = os.getenv(plain_name)
        if plain_value is not None:
            return plain_value
        raise ValueError(
            f"Переменная окружения '{name}' не задана. Для сборки в CI задайте секрет репозитория GitHub "
            f"(Actions); локально — системные переменные или .env рядом с exe; без шифрования — '{plain_name}'."
        )
    encrypted_value = value.encode()

    # Дешифруем значение
    decrypted_value = cipher.decrypt(encrypted_value)
    return decrypted_value.decode()

