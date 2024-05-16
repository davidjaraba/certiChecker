from starlette import status

from app.api.dependencies.core import DBSessionDep
from app.crud.company import get_company, get_companies, delete_company, update_company, create_company
from app.consumer import add_url_to_queue
from app.crud.url import get_urls_by_company_id
from app.schemas.company import CreateCompanyDto, UpdateCompanyDto, ResponseCompanyDto
from fastapi import APIRouter


# router = APIRouter(
#     prefix="/api/companies",
#     tags=["companies"],
#     responses={404: {"description": "Not found"}}
# )


class CompaniesAPI:
    def __init__(self, queue):
        self.queue = queue
        self.router = APIRouter(
            prefix="/api/companies",
            tags=["companies"],
            responses={404: {"description": "Not found"}}
        )
        self.router.add_api_route("/{comp_id}", self.get_company_by_id, methods=["GET"])
        self.router.add_api_route("/", self.get_all_companies, methods=["GET"])
        self.router.add_api_route("/", self.create_company, methods=["POST"], status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/{company_id}/rescan", self.rescan_company_urls, methods=["POST"],
                                  status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/{comp_id}", self.update_company_by_id, methods=["PUT"])
        self.router.add_api_route("/{comp_id}", self.delete_company_by_id, methods=["DELETE"])

    async def get_company_by_id(self, comp_id: int, db: DBSessionDep):
        """
        Retrieve a single company by its ID.
        """
        return await get_company(db, comp_id)

    async def get_all_companies(self, db: DBSessionDep):
        """
        Retrieve all companies.
        """
        companies = await get_companies(db)
        return companies

    async def create_company(self, company_data: CreateCompanyDto, db: DBSessionDep):
        """
        Create a new company.
        """
        return await create_company(db, company_data)

    async def rescan_company_urls(self, company_id: int, db: DBSessionDep):
        """
        Rescan all URLs associated with a given company.
        """
        urls = await get_urls_by_company_id(db, company_id)
        for url in urls:
            add_url_to_queue(self.queue, url.url, url.url)
        return urls

    async def update_company_by_id(self, comp_id: int, update_data: UpdateCompanyDto, db: DBSessionDep):
        """
        Update a company by its ID.
        """
        return await update_company(db, comp_id, update_data)

    async def delete_company_by_id(self, comp_id: int, db: DBSessionDep):
        """
        Delete a company by its ID.
        """
        return await delete_company(db, comp_id)

# class Comapnies:
#
#     def __init__(self):
#         self.router = APIRouter()
#         self.router.add_api_route("/hello", self.hello, methods=["GET"])
#
#     def hello(self):
#         return {"Hello": 'sss'}

#
# @router.get("/{comp_id}")
# async def get_company_by_id(
#         comp_id: int,
#         db_session: DBSessionDep
# ):
#     company = await get_company(db_session, comp_id)
#     return company
#
#
# @router.get("/")
# async def get_all_companies(
#         db_session: DBSessionDep
# ):
#     return await get_companies(db_session)
#
#
# @router.post("/", status_code=201)
# async def create_compa(create_certificate_dto: CreateCompanyDto,
#                        db_session: DBSessionDep
#                        ):
#     return await create_company(db_session, create_certificate_dto)
#
#
# @router.post("/{company_id}/rescan", status_code=201)
# async def rescan_company_urls(company_id: int,
#                               db_session: DBSessionDep,
#                               queue: QueueDep
#                               ):
#     urls = await get_urls_by_company_id(db_session, company_id)
#
#     print(queue)
#
#     for url in urls:
#         queue.put(url)
#
#     return urls
#
#
# @router.put("/{cert_id}")
# async def update_company_by_id(cert_id: int,
#                                update_company_dto: UpdateCompanyDto,
#                                db_session: DBSessionDep
#                                ):
#     return await update_company(db_session, cert_id, update_company_dto)
#
#
# @router.delete("/{cert_id}")
# async def delete_company_by_id(cert_id: int,
#                                db_session: DBSessionDep
#                                ):
#     return await delete_company(db_session, cert_id)
