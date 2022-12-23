"""
Super Admin is for managing top level DB operations like 
DB migration using alembic, dropping and creating new DB,
insert initial data to all tables
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseSettings

from app.models.client_contact_model import ClientContactInput
from app.routes.client_contact.client_contact_dao import ClientContactDAO

router = APIRouter()

# def create_db(drop_db_if_exist: bool = False):
#     """Create DB if not exist"""
#     import asyncio
#     from app.db.utils import create_database

#     loop = asyncio.get_event_loop()

#     async def create_tasks_func():
#         tasks = list()
#         tasks.append(
#             asyncio.create_task(create_database(drop_db_if_exist=drop_db_if_exist))
#         )
#         await asyncio.wait(tasks)

#     loop.run_until_complete(create_tasks_func())
#     loop.close()


# def init_db():
#     """Insert inital data into different tables if not inserted"""

#     import asyncio
#     from app.db.init_db import init_db

#     # from fastapi import Depends

#     loop = asyncio.get_event_loop()

#     async def create_tasks_func():
#         tasks = list()
#         tasks.append(asyncio.create_task(init_db()))
#         await asyncio.wait(tasks)

#     loop.run_until_complete(create_tasks_func())
#     loop.close()


class SuperAdminConfig(BaseSettings):
    """
    Super Admin settings.

    These parameters can be configured
    with environment variables.
    """

    # super_admin_username: str = ""
    super_admin_password: str = ""

    class Config:
        env_file = "envs/dev.env"
        env_file_encoding = "utf-8"


super_admin_config = SuperAdminConfig()


def check_super_admin_cred(password: str) -> None:
    if not (super_admin_config.super_admin_password == password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password is invalid",
        )


@router.post("/db/create")
async def create_database(auth=Depends(check_super_admin_cred), drop_db_if_exist: bool = False):

    from app.db.utils import create_database

    await create_database(drop_db_if_exist=drop_db_if_exist)
    return {"result": "success"}


@router.post("/alembic/upgrade-head")
async def alembic_upgrade_head(
    auth=Depends(check_super_admin_cred),
):
    import asyncio

    proc = await asyncio.create_subprocess_exec(
        "alembic",
        "upgrade",
        "head",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {
        "stdout": stdout,
        "stderr": stderr,
    }


@router.post("/db/insert-inital-data")
async def insert_inital_data(
    auth=Depends(check_super_admin_cred),
):
    from app.db.init_db import init_db

    await init_db()
    return {"result": "success"}


@router.post("/test")
async def test(
    # auth=Depends(check_super_admin_creds),
    client_contact_input: ClientContactInput,
    client_contact_dao: ClientContactDAO = Depends(),
):
    return await client_contact_dao.insert(client_contact_input)
