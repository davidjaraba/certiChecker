
from app.api.dependencies.core import DBSessionDep
from app.crud.company import get_company, get_companies, delete_company, update_company, create_company
from app.crud.url import get_urls_by_company_id
from app.schemas.company import CreateCompanyDto, UpdateCompanyDto, ResponseCompanyDto
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{comp_id}")
async def get_company_by_id(
        comp_id: int,
        db_session: DBSessionDep
):
    company = await get_company(db_session, comp_id)
    return company


@router.get("/")
async def get_all_companies(
        db_session: DBSessionDep
):
    return await get_companies(db_session)


@router.post("/", status_code=201)
async def create_compa(create_certificate_dto: CreateCompanyDto,
                       db_session: DBSessionDep
                       ):
    return await create_company(db_session, create_certificate_dto)


@router.post("/{company_id}/rescan", status_code=201)
async def rescan_company_urls(company_id: int,
                              db_session: DBSessionDep,
                              ):
    urls = await get_urls_by_company_id(db_session, company_id)

    for url in urls:
        add_url_to_queue(url.url)

    return urls


@router.put("/{cert_id}")
async def update_company_by_id(cert_id: int,
                               update_company_dto: UpdateCompanyDto,
                               db_session: DBSessionDep
                               ):
    return await update_company(db_session, cert_id, update_company_dto)


@router.delete("/{cert_id}")
async def delete_company_by_id(cert_id: int,
                               db_session: DBSessionDep
                               ):
    return await delete_company(db_session, cert_id)
