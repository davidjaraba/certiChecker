from typing import Optional

from app.api.dependencies.core import DBSessionDep
from app.crud.url import get_url, get_urls, create_url, update_url, delete_url, get_urls_by_company_id
from app.schemas.url import CreateURLDto, UpdateURLDto
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/api/urls",
    tags=["urls"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{url_name}")
async def get_url_by_name(
        url_name: str,
        db_session: DBSessionDep
):
    company = await get_url(db_session, url_name)
    return company


@router.get("/")
async def get_all_urls(
        db_session: DBSessionDep,
        company_id: Optional[int] = Query(None, description="The ID of the company to filter URLs by")
):
    if company_id:
        return await get_urls_by_company_id(db_session, company_id)
    else:
        return await get_urls(db_session)




@router.post("/", status_code=201)
async def create_new_url(create_url_dto: CreateURLDto,
                         db_session: DBSessionDep
                         ):
    return await create_url(db_session, create_url_dto)


@router.put("/{url_name}")
async def update_url_by_id(url_name: str,
                           update_url_dto: UpdateURLDto,
                           db_session: DBSessionDep
                           ):
    return await update_url(db_session, url_name, update_url_dto)


@router.delete("/{url_name}")
async def delete_url_by_id(url_name: str,
                           db_session: DBSessionDep
                           ):
    return await delete_url(db_session, url_name)
