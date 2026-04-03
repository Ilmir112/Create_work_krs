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
            f"Переменная окружения '{name}' не задана. Укажите её в системных переменных Windows "
            f"или в .env рядом с exe (либо '{plain_name}' для значения без шифрования)."
        )
    encrypted_value = value.encode()

    # Дешифруем значение
    decrypted_value = cipher.decrypt(encrypted_value)
    return decrypted_value.decode()

