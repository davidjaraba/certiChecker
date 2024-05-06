import asyncio
import logging
import multiprocessing
import sys
import ssl
from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app.api.routers.certificates import router as certificates_router
from app.api.routers.companies import router as companies_router
from app.api.routers.urls import router as urls_router
from app.api.routers.resources import router as resources_router

from home import Home

from webscrapper import get_queue, start_consumer

from fastapi.middleware.cors import CORSMiddleware

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

webscrap_queue = get_queue()
consumer = start_consumer(webscrap_queue)

# CORS Allow all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    webscrap_queue.put('SDASSD')
    return {"message": "Hello World"}


# Routers
app.include_router(certificates_router)
app.include_router(companies_router)
app.include_router(urls_router)
app.include_router(resources_router)


async def async_main() -> None:
    print("Creando tablas...")
    async with sessionmanager._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('./cert/cert.pem', keyfile='./cert/key.pem')
    print("Inicializando API REST")
    asyncio.run(async_main())
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
