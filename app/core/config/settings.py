# app/config/settings.py

from pathlib import Path
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.service.logging.logger import (
    logger,
    START_MODULE_MESSAGE,
    str_object_is_created
)


MODULE_DESCRIPTION = "This module is used to save all creds and settings for the program"


_THIS_FILE  = Path(__file__).resolve()
ROOT_DIR    = _THIS_FILE.parents[2]            # app/config/settings.py -> app -> root
DEFAULT_ENV = ROOT_DIR / ".env"                # root/.env
ENV_FILE    = str(DEFAULT_ENV) if DEFAULT_ENV.exists() else ".env"

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # region telegram settings

    BOT_TOKEN:           str

    # endregion telegram settings

    # region database settings

    DB_ENGINE:   str # if sqlite, then use sqlite
    DB_FILE:     str
    # settings for PostgresSQL
    DB_HOST:     str
    DB_PORT:     str
    DB_NAME:     str
    DB_USER:     str
    DB_PASSWORD: str

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_ENGINE.startswith("sqlite"):
            db_path = (ROOT_DIR / self.DB_FILE).resolve()
            return f"{self.DB_ENGINE}:///{db_path.as_posix()}"
        # postgres
        return (
            f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # endregion database settings

settings = Settings()


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(settings))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
