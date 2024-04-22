from app.models.models import Resource as ResourceDBModel
from app.models.models import URL as URLDBModel
from app.schemas.resource import CreateResourceDto, UpdateResourceDto, ResponseResourceDto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response
import uuid


async def get_resource(db_session: AsyncSession, res_id: str):
    cert = (await db_session.scalars(select(ResourceDBModel).where(ResourceDBModel.id == res_id))).first()

    if not cert:
        return Response(status_code=404, content="Resource not found")
    return cert


async def get_resources(db_session: AsyncSession):
    return (await db_session.scalars(select(ResourceDBModel))).fetchall()


async def create_resource(db_session: AsyncSession, create_resource_dto: CreateResourceDto):
    url = (await db_session.scalars(
        select(URLDBModel).where(URLDBModel.url == create_resource_dto.url_id))).first()

    if not url:
        return Response(status_code=404, content="URL not found.")

    # create_resource_dto.id = uuid.uuid4()
    new_resource = ResourceDBModel(**create_resource_dto.dict())
    new_resource.id = str(uuid.uuid4())
    new_resource.type = str(new_resource.type.name)
    db_session.add(new_resource)
    await db_session.commit()
    await db_session.refresh(new_resource)
    return new_resource


async def update_resource(db_session: AsyncSession, res_id: str, update_resource: UpdateResourceDto):
    resource = (await db_session.scalars(
        select(ResourceDBModel).where(ResourceDBModel.id == res_id))).first()

    if not resource:
        return Response(status_code=404, content="Resource not found")

    if update_resource.url_id:
        url = (await db_session.scalars(
            select(URLDBModel).where(URLDBModel.url == update_resource.url_id))).first()
        if not url:
            return Response(status_code=400, content="Invalid url")

    for field, value in update_resource:
        if value:
            setattr(resource, field, value)

    if update_resource.type:
        resource.type = str(resource.type.name)

    await db_session.commit()
    await db_session.refresh(resource)

    return resource


async def delete_resource(db_session: AsyncSession, res_id: str):
    resource = (await db_session.scalars(
        select(ResourceDBModel).where(ResourceDBModel.id == res_id))).first()

    if not resource:
        return Response(status_code=404, content="Resource not found")

    await db_session.delete(resource)

    await db_session.commit()

    return Response(status_code=204)
