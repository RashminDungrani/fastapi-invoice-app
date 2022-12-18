from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.core.auth import AuthHandler
from app.models.client_contact_model import (
    ClientContact,
    ClientContactInput,
    ClientContactWithInvoices,
)
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
    limit: Optional[int] = Query(default=None, ge=0),
    client_contact_dao: ClientContactDAO = Depends(),
):
    client_contacts = await client_contact_dao.select_all(limit=limit)
    return client_contacts


@router.get("/all-with-invoices", response_model=list[ClientContactWithInvoices])
async def get_all_client_contacts_with_invoices(
    limit: Optional[int] = Query(default=None, ge=0),
    client_contact_dao: ClientContactDAO = Depends(),
):
    statement = (
        select(ClientContact)
        .options(
            selectinload(ClientContact.invoices),
        )
        .limit(limit)
    )

    result = await client_contact_dao.select_custom(statement)
    result = result.scalars().all()
    return result


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
