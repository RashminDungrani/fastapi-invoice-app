from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.core.auth import AuthHandler
from app.models.note_model import Note, NoteInput
from app.routes.note.note_dao import NoteDAO

auth_handler = AuthHandler()

router = APIRouter()


# * POST
@router.post("/create", response_model=Note)
async def create_note(
    inserted_note: NoteInput,
    note_dao: NoteDAO = Depends(),
):
    note = await note_dao.insert(inserted_note=inserted_note)
    return note


# * GET
@router.get("/all", response_model=list[Note])
async def get_all_notes(
    limit: Optional[int] = Query(default=None, ge=0),
    note_dao: NoteDAO = Depends(),
):
    notes = await note_dao.select_all(limit=limit)
    return notes


# * PUT
@router.put("/update", response_model=Note)
async def update_note(
    note_id: int,
    updated_note: NoteInput,
    note_dao: NoteDAO = Depends(),
):
    note = await note_dao.select_one(note_id=note_id)
    note.modified_at = datetime.now()
    note = await note_dao.update(db_note=note, updated_note=updated_note)
    return note


# * DELETE
@router.delete("/delete", status_code=204)
async def delete_note(
    note_id: int,
    note_dao: NoteDAO = Depends(),
):
    note = await note_dao.select_one(note_id=note_id)
    await note_dao.delete(note_item=note)
