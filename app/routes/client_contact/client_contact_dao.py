from typing import Any, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Executable
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db_session
from app.models.client_contact_model import ClientContact, ClientContactInput


class ClientContactDAO:
    """Class for accessing client_contact table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def select_one(self, client_contact_id: int) -> ClientContact:
        client_contact = await self.session.get(ClientContact, client_contact_id)
        if not client_contact:
            raise HTTPException(status_code=404, detail="client_contact id not found")

        return client_contact

    async def select_all(self, limit: Optional[int] = None) -> list[ClientContact]:
        client_contacts = (await self.session.execute(select(ClientContact).limit(limit))).scalars().fetchall()
        return client_contacts

    async def select_custom(self, statement: Executable) -> Any:
        return await self.session.execute(statement)

    async def insert(self, inserted_client_contact: ClientContactInput) -> ClientContact:
        client_contact: ClientContact = ClientContact.from_orm(inserted_client_contact)
        self.session.add(client_contact)
        await self.session.commit()
        return client_contact

    async def update(
        self, db_client_contact: ClientContact, updated_client_contact: ClientContactInput
    ) -> ClientContact:
        for key, value in (updated_client_contact.dict(exclude_unset=True)).items():
            setattr(db_client_contact, key, value)
        self.session.add(db_client_contact)
        await self.session.commit()
        await self.session.refresh(db_client_contact)

        return db_client_contact

    async def delete(self, client_contact_item: ClientContact) -> None:
        await self.session.delete(client_contact_item)
        await self.session.commit()
