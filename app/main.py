import asyncio
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app.api.routers.certificates import router as certificates_router
from app.api.routers.companies import router as companies_router
from app.api.routers.urls import router as urls_router
from app.api.routers.resources import router as resources_router

# from app.config import settings
from database import sessionmanager
from models.models import Base

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.log_level == "DEBUG" else logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# engine = create_async_engine('sqlite+aiosqlite:///base.db')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="ssss", docs_url="/api/docs", debug=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Routers
app.include_router(certificates_router)
app.include_router(companies_router)
app.include_router(urls_router)
app.include_router(resources_router)

# async def init_models():
#     async with sessionmanager._engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
# engine = create_async_engine('sqlite+aiosqlite:///base.db', echo=True)
async def async_main() -> None:
    print("Creando tablas...")
    async with sessionmanager._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




if __name__ == "__main__":
    print("Inicializando API REST")
    asyncio.run(async_main())
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)











# from typing import Any, Annotated
#
# from fastapi import FastAPI, Request, Body
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from sqlalchemy import create_engine, select, insert
# from sqlalchemy.orm import Session
# from models.models import Base
# from models.models import Certificate
# from pydantic import BaseModel
#
# from schemas.certificate import *
#
# app = FastAPI(debug=True)
#
# ruta = "base.db"
#
# engine = create_engine("sqlite:///" + ruta, echo=True)
# session = Session(engine)
#
# prefix = "/api"
#
# Base.metadata.create_all(engine)
#
# #
# # class UnicornException(Exception):
# #     def __init__(self, name: str):
# #         self.name = name
# #
# #
# # @app.exception_handler(UnicornException)
# # async def unicorn_exception_handler(request: Request, exc: UnicornException):
# #     return JSONResponse(
# #         status_code=418,
# #         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
# #     )
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# @app.get(prefix + "/certificates/")
# async def list_certificates():
#     stmt = select(Certificate)
#     res = session.execute(stmt).fetchall()
#
#     if res is not None:
#         res = [row._asdict() for row in res]
#         json_response = jsonable_encoder(res)
#     else:
#         json_response = []
#
#     return JSONResponse(content=json_response)
#
#
# @app.post(prefix + "/certificates/")
# async def create_certificate(create_certificate: CreateCertificateDto) -> Any:
#     stmt = insert(Certificate).values(create_certificate)
#
#     session.execute(stmt)
#     session.commit()
#
#     json_response = jsonable_encoder(create_certificate)
#
#     return json_response
#
#
# @app.get(prefix + "/certificates/{cert_id}")
# async def get_certificate(cert_id):
#     stmt = select(Certificate).where(Certificate.id == cert_id)
#     res = session.execute(stmt).fetchone()
#
#     if res is not None:
#         res = res._asdict()
#         json_response = jsonable_encoder(res)
#     else:
#         return JSONResponse(status_code=404, content={"message": "Certificate not found"})
#
#     return JSONResponse(content=json_response)
