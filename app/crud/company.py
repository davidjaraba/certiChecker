from app.models.models import Company as CompanyDBModel
from app.models.models import URL as URLDBModel
from app.schemas.company import CreateCompanyDto, UpdateCompanyDto
from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_company(db_session: AsyncSession, cert_id: int):
    cert = (await db_session.scalars(select(CompanyDBModel).where(CompanyDBModel.id == cert_id))).first()

    if not cert:
        return Response(status_code=404, content="Company not found")
    return cert


async def get_companies(db_session: AsyncSession):
    return (await db_session.scalars(select(CompanyDBModel))).fetchall()


async def create_company(db_session: AsyncSession, create_company: CreateCompanyDto):
    cert = (await db_session.scalars(
        select(CompanyDBModel).where(CompanyDBModel.name == create_company.name))).first()

    if cert:
        return Response(status_code=409, content="Company alredy exist")

    new_certificate = CompanyDBModel(**create_company.dict())
    db_session.add(new_certificate)
    await db_session.commit()
    await db_session.refresh(new_certificate)
    return new_certificate


async def update_company(db_session: AsyncSession, cert_id: int, update_company: UpdateCompanyDto):
    cert = (await db_session.scalars(
        select(CompanyDBModel).where(CompanyDBModel.id == cert_id))).first()

    if not cert:
        return Response(status_code=404, content="Company not found")

    for field, value in update_company:
        if value:
            setattr(cert, field, value)

    await db_session.commit()
    await db_session.refresh(cert)

    return cert


async def delete_company(db_session: AsyncSession, cert_id: int):
    cert = (await db_session.scalars(
        select(CompanyDBModel).where(CompanyDBModel.id == cert_id))).first()

    if not cert:
        return Response(status_code=404, content="Company not found")

    await db_session.delete(cert)

    await db_session.commit()

    return Response(status_code=204)
