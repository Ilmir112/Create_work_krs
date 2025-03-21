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

    ext_data_dir = os.getcwd()
    if getattr(sys, 'frozen', False):
        ext_data_dir = sys._MEIPASS

    # Загружаем .env файл
    load_dotenv(dotenv_path=os.path.join(ext_data_dir, '.env'))
    encrypted_value = os.getenv(name).encode()

    # Дешифруем значение
    decrypted_value = cipher.decrypt(encrypted_value)
    return decrypted_value.decode()

