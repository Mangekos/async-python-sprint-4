import os

from pydantic import (
    BaseSettings,
    # PostgresDsn
)
from logging import config as logging_config
from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

db_echo_mode = True


class AppSettings(BaseSettings):
    app_title: str = "Some API"
    # database_dsn: PostgresDsn = (
    #     "postgresql+asyncpg://practicum:yandex@localhost:5432/yandex"
    # )
    # не получилось подключить постгрес, не могу запустить докер на ПК
    project_name: str = "Some API project"
    project_host: str = "0.0.0.0"
    project_port: int = 8000


app_settings = AppSettings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
