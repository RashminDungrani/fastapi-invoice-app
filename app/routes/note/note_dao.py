from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Executable
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db_session
from app.models.note_model import Note, NoteInput


class NoteDAO:
    """Class for accessing Note table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def select_one(self, note_id: int) -> Note:
        note = await self.session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="note id not found")

        return note

    async def select_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[Note]:
        query = select(Note).offset(offset).limit(limit)
        notes = (await self.session.execute(query)).scalars().all()
        return notes

    async def select_custom(self, statement: Executable) -> Any:
        return await self.session.execute(statement)

    async def insert(self, inserted_note: NoteInput) -> Note:
        try:
            note: Note = Note.from_orm(inserted_note)
            self.session.add(note)
            await self.session.commit()
            return note
        except exc.IntegrityError as error:
            print(error.code, error.params)
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invoice id {inserted_note.invoice_id} does not exist",
            )

    async def update(self, db_note: Note, updated_note: NoteInput) -> Note:

        for key, value in (updated_note.dict(exclude_unset=True)).items():
            setattr(db_note, key, value)
        self.session.add(db_note)
        await self.session.commit()
        await self.session.refresh(db_note)

        return db_note

    async def delete(self, note_item: Note) -> None:
        await self.session.delete(note_item)
        await self.session.commit()
