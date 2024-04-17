from app.api.dependencies.core import DBSessionDep
from app.crud.company import get_company, get_companies, delete_company, update_company
from app.schemas.company import CreateCompanyDto, UpdateCompanyDto, ResponseCompanyDto
from fastapi import APIRouter, Response

router = APIRouter(
    prefix="/api/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{comp_id}", response_model=ResponseCompanyDto)
async def get_company_by_id(
        comp_id: int,
        db_session: DBSessionDep
):
    company = await get_company_by_id(db_session, comp_id)
    return company


@router.get("/", response_model=list[ResponseCompanyDto])
async def get_all_companies(
        db_session: DBSessionDep
):
    return await get_companies(db_session)


@router.post("/", response_model=ResponseCompanyDto, status_code=201)
async def create_company(create_certificate_dto: CreateCompanyDto,
                         db_session: DBSessionDep
                         ):
    return await create_company(db_session, create_certificate_dto)


@router.put("/{cert_id}", response_model=ResponseCompanyDto)
async def update_company(cert_id: int,
                         update_company_dto: UpdateCompanyDto,
                         db_session: DBSessionDep
                         ):
    return await update_company(db_session, cert_id, update_company_dto)


@router.delete("/{cert_id}", status_code=204)
async def delete_company(cert_id: int,
                         db_session: DBSessionDep
                         ):
    await delete_company(db_session, cert_id)
    return Response(status_code=204)
