from app.api.dependencies.core import DBSessionDep
from app.crud.certificate import get_certificate, get_certificates, create_certificate, delete_certificate, update_certificate
from app.schemas.certificate import CreateCertificateDto, ResponseCertificateDto, UpdateCertificateDto
from fastapi import APIRouter, Response, HTTPException

router = APIRouter(
    prefix="/api/certificates",
    tags=["certificates"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{cert_id}")
async def get_cert_by_id(
        cert_id: int,
        db_session: DBSessionDep
):
    return await get_certificate(db_session, cert_id)


@router.get("/")
async def get_all_cert(
        db_session: DBSessionDep
):
    return await get_certificates(db_session)


@router.post("/", status_code=201)
async def create_cert(create_certificate_dto: CreateCertificateDto,
                      db_session: DBSessionDep
                      ):
    return await create_certificate(db_session, create_certificate_dto)


@router.put("/{cert_id}")
async def update_cert(cert_id: int,
                      update_certificate_dto: UpdateCertificateDto,
                      db_session: DBSessionDep
                      ):
    return await update_certificate(db_session, cert_id, update_certificate_dto)


@router.delete("/{cert_id}")
async def delete_cert(cert_id: int,
                      db_session: DBSessionDep
                      ):
    return await delete_certificate(db_session, cert_id)





