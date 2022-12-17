import uvicorn

from app.core.settings import settings
from app.models import load_all_models


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app.routes.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        # TODO: if only show open api docs if env is in these from three
        # SHOW_DOCS_ENVIRONMENT = (
        # "local",
        # "staging",
        # "dev",
        # )  # explicit list of allowed envs
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":

    # ! Run any one function at a time
    # * self.db_base path should be commented in settings.py file only while creating db
    # create_db(drop_db_if_exist=True)  # create db

    # * Insert intial data to tables if not exist
    # init_db()

    load_all_models()

    main()
