from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.auth import AuthHandler
from app.models.client_contact_model import ClientContact, ClientContactInput
from app.routes.client_contact.client_contact_dao import ClientContactDAO

auth_handler = AuthHandler()

router = APIRouter()


# * POST
@router.post("/create", response_model=ClientContact)
async def create_client_contact(
    inserted_client_contact: ClientContactInput,
    client_contact_dao: ClientContactDAO = Depends(),
):
    client_contact = await client_contact_dao.insert(inserted_client_contact=inserted_client_contact)
    return client_contact


# * GET
@router.get("/all", response_model=list[ClientContact])
async def get_all_client_contacts(
    limit: Optional[int] = Query(default=100, ge=0),
    client_contact_dao: ClientContactDAO = Depends(),
):
    client_contacts = await client_contact_dao.select_all()
    return client_contacts


# * PUT
@router.put("/update", response_model=ClientContact)
async def update_client_contact(
    client_contact_id: int,
    updated_client_contact: ClientContactInput,
    client_contact_dao: ClientContactDAO = Depends(),
):
    client_contact = await client_contact_dao.select_one(client_contact_id=client_contact_id)
    client_contact.modified_at = datetime.now()
    client_contact = await client_contact_dao.update(
        db_client_contact=client_contact, updated_client_contact=updated_client_contact
    )
    return client_contact


# * DELETE
@router.delete("/delete", status_code=204)
async def delete_client_contact(
    client_contact_id: int,
    client_contact_dao: ClientContactDAO = Depends(),
):
    client_contact = await client_contact_dao.select_one(client_contact_id=client_contact_id)
    await client_contact_dao.delete(client_contact_item=client_contact)
