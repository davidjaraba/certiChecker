from app.models.models import Certificate as CertificateDBModel
from app.schemas.certificate import CreateCertificateDto, UpdateCertificateDto
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_certificate(db_session: AsyncSession, cert_id: int):

    print("por algun motivo llega aqui")
    cert = (await db_session.scalars(select(CertificateDBModel).where(CertificateDBModel.id == cert_id))).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


async def get_certificates(db_session: AsyncSession):
    return (await db_session.scalars(select(CertificateDBModel))).fetchall()


async def create_certificate(db_session: AsyncSession, create_certificate: CreateCertificateDto):
    cert = (await db_session.scalars(
        select(CertificateDBModel).where(CertificateDBModel.name == create_certificate.name))).first()

    if cert:
        raise HTTPException(status_code=409, detail="Certificate alredy exist")

    new_certificate = CertificateDBModel(**create_certificate.dict())
    db_session.add(new_certificate)
    await db_session.commit()
    await db_session.refresh(new_certificate)
    return new_certificate


async def update_certificate(db_session: AsyncSession, cert_id: int, update_certificate: UpdateCertificateDto):
    cert = (await db_session.scalars(
        select(CertificateDBModel).where(CertificateDBModel.id == cert_id))).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    for field, value in update_certificate:
        setattr(cert, field, value)

    await db_session.commit()
    await db_session.refresh(cert)

    return cert


async def delete_certificate(db_session: AsyncSession, cert_id: int):
    cert = (await db_session.scalars(
        select(CertificateDBModel).where(CertificateDBModel.id == cert_id))).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    await db_session.delete(cert)

    await db_session.commit()

    return True
