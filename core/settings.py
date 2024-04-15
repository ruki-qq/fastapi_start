from pathlib import Path
from typing import Final

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR: Final[Path] = Path(__file__).parent.parent

DB_PATH: Final[Path] = BASE_DIR / "db.sqlite3"


class DBSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DBSettings = DBSettings()


settings = Settings()
