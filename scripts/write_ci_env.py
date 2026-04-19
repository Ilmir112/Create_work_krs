#!/usr/bin/env python3
"""
Формирует .env из переменных окружения CI.

В GitHub Actions значения задаются через Settings → Secrets and variables → Actions
и пробрасываются в workflow в блоке ``env:`` (см. ``.github/workflows/build.yml``).
Скрипт содержит единый список имён ключей для сборки PyInstaller.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REQUIRED_KEYS = (
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_WELL_DATA",
    "DB_NAME_USER",
    "DB_NAME_GNKT",
    "DB_PORT",
)


def _configure_stdio_utf8() -> None:
    """Windows/GitHub Actions по умолчанию используют cp1252 — русский текст и символы вне ASCII ломают print."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # Python 3.7+
        except (AttributeError, OSError, ValueError, TypeError):
            pass


def _env_line(key: str) -> str:
    raw = os.environ.get(key)
    if raw is None:
        raw = ""
    escaped = (
        raw.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return f'{key}="{escaped}"'


def main() -> int:
    _configure_stdio_utf8()
    missing = [k for k in REQUIRED_KEYS if not (os.environ.get(k) or "").strip()]
    if missing:
        print(
            "Нет переменных окружения для сборки. Задайте секреты репозитория:",
            "(GitHub -> Settings -> Secrets and variables -> Actions)",
            file=sys.stderr,
            sep="\n",
        )
        for key in missing:
            print(f"  - {key}", file=sys.stderr)
        return 1

    root = Path(__file__).resolve().parent.parent
    out_path = root / ".env"
    content = "\n".join(_env_line(k) for k in REQUIRED_KEYS) + "\n"
    out_path.write_text(content, encoding="utf-8")
    print(f"Записан файл: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
