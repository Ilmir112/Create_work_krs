"""Redis-кэш черновика плана работ (TTL 48 ч).

Переменные окружения (можно задать в .env рядом с приложением или Create_work_krs/.env):
  REDIS_URL — redis://[:password@]host:port[/db] (имеет приоритет над отдельными полями)
  REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
  Если REDIS_HOST и REDIS_URL не заданы, подставляется RABBITMQ_HOST из .env (тот же сервер, что и очередь).
  Отключить: REDIS_USE_RABBITMQ_HOST=0
  REDIS_SOCKET_CONNECT_TIMEOUT — секунды на установку TCP (по умолчанию 10)
  REDIS_SOCKET_TIMEOUT — секунды на ответ сервера для команд (по умолчанию 10)
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict, Optional

try:
    import redis  # type: ignore
except ImportError:
    redis = None

import data_list

REDIS_KEY_PREFIX = "krs_plan_draft:"
REDIS_TTL_SECONDS = 172800  # 48 часов

_client: Optional[Any] = None
_env_loaded = False
_last_connect_error_log = 0.0


def _load_env_once() -> None:
    global _env_loaded
    if _env_loaded:
        return
    _env_loaded = True
    try:
        from dotenv import load_dotenv

        here = os.path.dirname(os.path.abspath(__file__))
        for path in (
            os.path.join(here, ".env"),
            os.path.join(os.getcwd(), ".env"),
        ):
            if os.path.isfile(path):
                load_dotenv(dotenv_path=path, override=False, encoding="utf-8-sig")
        try:
            from config import settings

            settings.load_env()
        except Exception:
            pass
    except Exception:
        pass


def _connect_timeout_sec() -> float:
    try:
        return float(os.environ.get("REDIS_SOCKET_CONNECT_TIMEOUT", "10"))
    except ValueError:
        return 10.0


def _socket_timeout_sec() -> float:
    try:
        return float(os.environ.get("REDIS_SOCKET_TIMEOUT", "10"))
    except ValueError:
        return 10.0


def _default_redis_host() -> str:
    """REDIS_HOST; если пусто — RABBITMQ_HOST из того же .env; иначе localhost."""
    h = (os.environ.get("REDIS_HOST") or "").strip()
    if h:
        return h
    if (os.environ.get("REDIS_USE_RABBITMQ_HOST", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "",
    )):
        mq = (os.environ.get("RABBITMQ_HOST") or "").strip()
        if mq:
            return mq
    return "localhost"


def _log_connect_error_once(message: str) -> None:
    """Не засоряем консоль при каждом автосохранении таблицы."""
    global _last_connect_error_log
    now = time.monotonic()
    if now - _last_connect_error_log < 120.0:
        return
    _last_connect_error_log = now
    print(
        "redis_plan_cache: подключение недоступно: "
        f"{message}\n"
        "  Укажите REDIS_URL или REDIS_HOST в .env (см. redis_plan_cache.py), "
        "или поднимите Redis локально."
    )


def _cache_identity_suffix() -> str:
    try:
        u = getattr(data_list, "user", None)
        if u is not None:
            return json.dumps(u, ensure_ascii=False, default=str)
    except Exception:
        pass
    return os.environ.get("REDIS_PLAN_CACHE_USER", "")


def build_cache_key(
    excel_path: str,
    well_number: str,
    well_area: str,
    work_plan: str,
) -> str:
    norm_path = ""
    if excel_path:
        try:
            norm_path = os.path.normcase(os.path.abspath(excel_path))
        except Exception:
            norm_path = str(excel_path)
    base = "|".join(
        [
            norm_path,
            str(well_number),
            str(well_area),
            str(work_plan),
            _cache_identity_suffix(),
        ]
    )
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()[:32]
    return f"{REDIS_KEY_PREFIX}{h}"


def _get_client():
    global _client
    _load_env_once()
    if redis is None:
        return None
    if _client is not None:
        try:
            _client.ping()
            return _client
        except Exception:
            _client = None

    url = (os.environ.get("REDIS_URL") or "").strip()
    ct = _connect_timeout_sec()
    st = _socket_timeout_sec()

    try:
        if url:
            _client = redis.from_url(
                url,
                decode_responses=True,
                socket_connect_timeout=ct,
                socket_timeout=st,
            )
        else:
            host = _default_redis_host()
            port = int(os.environ.get("REDIS_PORT", "6379"))
            db = int(os.environ.get("REDIS_DB", "0"))
            password = os.environ.get("REDIS_PASSWORD") or None
            _client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=ct,
                socket_timeout=st,
            )
        _client.ping()
    except Exception as e:
        _log_connect_error_once(str(e))
        _client = None
    return _client


def save_snapshot(key: str, payload: Dict[str, Any]) -> bool:
    r = _get_client()
    if r is None:
        return False
    try:
        body = json.dumps(payload, ensure_ascii=False, default=str)
        r.setex(key, REDIS_TTL_SECONDS, body)
        return True
    except Exception as e:
        print(f"redis_plan_cache: сохранение не удалось: {e}")
        return False


def load_snapshot(key: str) -> Optional[Dict[str, Any]]:
    r = _get_client()
    if r is None:
        return None
    try:
        raw = r.get(key)
        if not raw:
            return None
        return json.loads(raw)
    except Exception as e:
        print(f"redis_plan_cache: чтение не удалось: {e}")
        return None


def delete_snapshot(key: str) -> bool:
    r = _get_client()
    if r is None:
        return False
    try:
        r.delete(key)
        return True
    except Exception as e:
        print(f"redis_plan_cache: удаление не удалось: {e}")
        return False
