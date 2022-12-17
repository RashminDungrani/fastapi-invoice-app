"""
This file can perform deleting and creating new database at same time
Currently Postgres and MySQL Database supported
"""
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import settings


async def create_database(drop_db_if_exist: bool = False) -> None:
    """Create a databse."""

    is_postgres_db: bool = settings.db_type == "postgres"

    db_url = (
        make_url(str(settings.db_url.with_path("/postgres"))) if is_postgres_db else make_url(str(settings.db_url))
    )

    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{settings.db_base}'"  # PostgreSQL
                if is_postgres_db
                else f"SHOW DATABASES WHERE `database` = '{settings.db_base}'",  # MySQL
            ),
        )

        is_database_exists = (
            database_existance.scalar() == 1 if is_postgres_db else database_existance.scalar() == settings.db_base
        )
        if is_database_exists:
            print("-- database already exist")

    if is_database_exists and drop_db_if_exist:
        await drop_database()
        print("-- drop database")

    if is_database_exists and not drop_db_if_exist:
        print("-- not creating db because db already exist and drop_db_if_exist value is False")
    else:
        async with engine.connect() as conn:  # noqa: WPS440
            await conn.execute(
                text(
                    f'CREATE DATABASE "{settings.db_base}" ENCODING "utf8" TEMPLATE template1'  # Postgres
                    if settings.db_type == "postgres"
                    else f"CREATE DATABASE {settings.db_base} CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"  # MySQL
                ),
            )
            print("-- database created")

    await engine.dispose()


async def drop_database() -> None:
    """Drop current database."""

    is_postgres_db: bool = settings.db_type == "postgres"

    db_url = (
        make_url(str(settings.db_url.with_path("/postgres")))
        if is_postgres_db
        else make_url(str(settings.db_url))  # MySQL
    )

    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        if is_postgres_db:
            disc_users = (
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
                "FROM pg_stat_activity "
                f"WHERE pg_stat_activity.datname = '{settings.db_base}' "
                "AND pid <> pg_backend_pid();"
            )
            await conn.execute(text(disc_users))
        await conn.execute(
            text(f'DROP DATABASE "{settings.db_base}"' if is_postgres_db else f"DROP DATABASE {settings.db_base}")
        )

    await engine.dispose()
