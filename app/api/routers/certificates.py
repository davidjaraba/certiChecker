from app.api.dependencies.core import DBSessionDep
from app.crud.certificate import get_certificate, get_certificates, create_certificate
from app.schemas.certificate import CreateCertificateDto
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/certificates",
    tags=["certificates"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{cert_id}", response_model=CreateCertificateDto)
async def get_cert_by_id(
        cert_id: int,
        db_session: DBSessionDep
):
    user = await get_certificate(db_session, cert_id)
    return user


@router.get("/", response_model=list[CreateCertificateDto])
async def get_all_cert(
        db_session: DBSessionDep
):
    return await get_certificates(db_session)


@router.post("/", response_model=CreateCertificateDto, status_code=201)
async def create_cert(create_certificate_dto: CreateCertificateDto,
                      db_session: DBSessionDep
):
    return await create_certificate(db_session, create_certificate_dto)