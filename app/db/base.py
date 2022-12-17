from typing import Any, Tuple

from sqlalchemy import Table
from sqlalchemy.orm import as_declarative, declared_attr

from app.db.meta import meta

# from sqlmodel import SQLModel as _SQLModel


# class SQLModel(_SQLModel):
#     @declared_attr  # type: ignore
#     def __tablename__(cls) -> str:
#         return cls.__name__  # type: ignore


@as_declarative(metadata=meta)
class Base:
    """
    Base for all models.

    It has some type definitions to
    enhance autocompletion.
    """

    __tablename__: str
    __table__: Table
    __table_args__: Tuple[Any, ...]
