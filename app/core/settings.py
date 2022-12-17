import enum

from pydantic import BaseSettings
from yarl import URL

# TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    app_name: str = ""
    app_desc: str = ""

    # host: str = "192.168.1.237"
    host: str = "0.0.0.0"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_type: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "UNDEFINED"
    db_pass: str = "UNDEFINED"
    db_base: str = "UNDEFINED"
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        generated_url = URL.build(
            scheme="postgresql+asyncpg" if self.db_type == "postgres" else "mysql+aiomysql",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            # path should be commented only while creating db from main file
            path=f"/{self.db_base}",
        )

        print("Generated DB URL ::", generated_url)
        return generated_url

    class Config:
        env_file = "envs/dev.env"
        env_file_encoding = "utf-8"


settings = Settings()
