from app.api.dependencies.core import DBSessionDep
from app.crud.resource import get_resource, get_resources, create_resource, delete_resource, update_resource
from app.schemas.resource import CreateResourceDto, UpdateResourceDto
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/resources",
    tags=["resources"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{res_id}")
async def get_res_by_id(
        res_id: str,
        db_session: DBSessionDep
):
    return await get_resource(db_session, res_id)


@router.get("/")
async def get_all_res(
        db_session: DBSessionDep
):
    return await get_resources(db_session)


@router.post("/", status_code=201)
async def create_res(create_resource_dto: CreateResourceDto,
                     db_session: DBSessionDep
                     ):
    return await create_resource(db_session, create_resource_dto)


@router.put("/{res_id}")
async def update_res(res_id: str,
                     update_resource_dto: UpdateResourceDto,
                     db_session: DBSessionDep
                     ):
    return await update_resource(db_session, res_id, update_resource_dto)


@router.delete("/res_id}")
async def delete_res(res_id: str,
                     db_session: DBSessionDep
                     ):
    return await delete_resource(db_session, res_id)
