import os
import sys

from dotenv import load_dotenv


class settings:
    _env_loaded = False
    _env_path = None

    def __init__(self):
        pass

    @classmethod
    def get_env_path(cls):
        """Путь к файлу .env (папка приложения или cwd)."""
        if cls._env_path is not None:
            return cls._env_path
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
            path = os.path.join(base_dir, ".env")
            if not os.path.isfile(path):
                path = os.path.join(base_dir, "_internal", ".env")

            print(base_dir, path)
        else:
            path = os.path.join(os.getcwd(), ".env")
        cls._env_path = path
        return path

    @classmethod
    def load_env(cls, force=False):
        """Загрузить переменные из .env. Вызывать при старте или перед чтением env."""
        if cls._env_loaded and not force:
            return
        load_dotenv(dotenv_path=cls.get_env_path())
        cls._env_loaded = True