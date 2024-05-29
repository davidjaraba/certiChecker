from datetime import datetime

from sqlalchemy.orm import joinedload

from app.models.models import Resource as ResourceDBModel
from app.models.models import CompanyCertificate as CompanyCertificateDBModel
from app.models.models import URL as URLDBModel
from app.models.models import Certificate as CertificateDBModel
from app.schemas.resource import CreateResourceDto, UpdateResourceDto, ResponseResourceDto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response
import uuid


async def get_resource(db_session: AsyncSession, res_id: str):
    cert = (await db_session.scalars(select(ResourceDBModel)
                                     .options(joinedload(ResourceDBModel.certificate).joinedload(CompanyCertificateDBModel.certificate))
                                     .where(ResourceDBModel.id == res_id))).first()

    if not cert:
        return Response(status_code=404, content="Resource not found")
    return cert


async def get_resources(db_session: AsyncSession):
    return (await db_session.scalars(select(ResourceDBModel))).fetchall()


async def create_resource(db_session: AsyncSession, create_resource_dto: CreateResourceDto):
    url = (await db_session.scalars(
        select(URLDBModel).where(URLDBModel.url == create_resource_dto.url_id)
    )).first()

    cert = (await db_session.scalars(
        select(CertificateDBModel).where(CertificateDBModel.id == create_resource_dto.certificate_id)
    )).first()

    if not url:
        return Response(status_code=404, content="URL not found.")

    if not cert:
        return Response(status_code=404, content="Certificate not found.")

    new_resource_dict = create_resource_dto.dict()
    new_resource_dict.pop('certificate_id', None)

    new_resource = ResourceDBModel(**new_resource_dict)
    new_resource.id = str(uuid.uuid4())
    new_resource.type = str(new_resource.type.name)

    db_session.add(new_resource)
    await db_session.flush()  # Ensures new_resource.id is available

    new_certificatecompany = CompanyCertificateDBModel()
    new_certificatecompany.company_id = url.company_id
    new_certificatecompany.certificate_id = cert.id
    new_certificatecompany.found_date = datetime.now()
    new_certificatecompany.resource_id = new_resource.id

    db_session.add(new_certificatecompany)
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
