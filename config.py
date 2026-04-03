import os
import sys

from dotenv import load_dotenv


class settings:
    _env_loaded = False
    _env_path = None

    def __init__(self):
        pass

    @classmethod
    def _dotenv_candidate_paths(cls):
        """Порядок: пользовательский .env рядом с exe, затем _internal, затем бандл PyInstaller."""
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
            paths = [
                os.path.join(base_dir, ".env"),
                os.path.join(base_dir, "_internal", ".env"),
            ]
            meipass = getattr(sys, "_MEIPASS", None)
            if meipass:
                paths.append(os.path.join(meipass, ".env"))
            return paths
        return [os.path.join(os.getcwd(), ".env")]

    @classmethod
    def get_env_path(cls):
        """Путь к существующему .env или куда его положить (exe/cwd)."""
        if cls._env_path is not None:
            return cls._env_path
        for path in cls._dotenv_candidate_paths():
            if os.path.isfile(path):
                cls._env_path = path
                return path
        if getattr(sys, "frozen", False):
            cls._env_path = os.path.join(os.path.dirname(sys.executable), ".env")
        else:
            cls._env_path = os.path.join(os.getcwd(), ".env")
        return cls._env_path

    @classmethod
    def load_env(cls, force=False):
        """Подмешать переменные из .env, если файлы есть. Уже заданные в ОС не трогаем."""
        if cls._env_loaded and not force:
            return
        for path in cls._dotenv_candidate_paths():
            if os.path.isfile(path):
                load_dotenv(dotenv_path=path, override=False)
        cls._env_loaded = True