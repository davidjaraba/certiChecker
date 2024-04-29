from app.models.models import URL as URLDBModel
from app.models.models import Company as CompanyDBModel
from app.schemas.url import CreateURLDto, UpdateURLDto, ResponseURLDto
from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_url(db_session: AsyncSession, url_name: str):
    cert = (await db_session.scalars(select(URLDBModel).where(URLDBModel.url == url_name))).first()

    if not cert:
        return Response(status_code=404, content="URL not found")
    return cert


async def get_urls_by_company_id(db_session: AsyncSession, company_id: int):
    result = await db_session.scalars(
        select(URLDBModel).where(URLDBModel.company_id == company_id)
    )
    urls = result.fetchall()
    if not urls:
        return []
    return urls



async def get_urls(db_session: AsyncSession):
    return (await db_session.scalars(select(URLDBModel))).fetchall()


async def create_url(db_session: AsyncSession, create_url: CreateURLDto):
    cert = (await db_session.scalars(
        select(URLDBModel).where(URLDBModel.url == create_url.url))).first()

    if cert:
        return Response(status_code=409, content="URL alredy exist.")

    company = (await db_session.scalars(
        select(CompanyDBModel).where(CompanyDBModel.id == create_url.company_id))).first()

    if not company:
        return Response(status_code=400, content="Invalid company.")

    new_url = URLDBModel(**create_url.dict())
    db_session.add(new_url)
    await db_session.commit()
    await db_session.refresh(new_url)
    return new_url


async def update_url(db_session: AsyncSession, url_name: str, update_url: UpdateURLDto):
    cert = (await db_session.scalars(
        select(URLDBModel).where(URLDBModel.url == url_name))).first()

    if update_url.company_id:
        company = (await db_session.scalars(
            select(CompanyDBModel).where(CompanyDBModel.id == update_url.company_id))).first()

        if not company:
            return Response(status_code=400, content="Invalid company.")

    if not cert:
        return Response(status_code=404, content="URL not found")

    for field, value in update_url:
        if value:
            setattr(cert, field, value)

    await db_session.commit()
    await db_session.refresh(cert)

    return cert


async def delete_url(db_session: AsyncSession, cert_name: str):
    cert = (await db_session.scalars(
        select(URLDBModel).where(URLDBModel.url == cert_name))).first()

    if not cert:
        return Response(status_code=404, content="URL not found")

    await db_session.delete(cert)

    await db_session.commit()

    return Response(status_code=204)
