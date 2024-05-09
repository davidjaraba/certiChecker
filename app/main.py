import asyncio
import logging
import multiprocessing
import sys
import ssl
from contextlib import asynccontextmanager
from multiprocessing import Queue, Process

import uvicorn

from fastapi import FastAPI, APIRouter
from sqlalchemy.ext.asyncio import create_async_engine

from app.api.routers.certificates import router as certificates_router
from app.api.routers.companies import CompaniesAPI
from app.api.routers.urls import router as urls_router
from app.api.routers.resources import router as resources_router

from scrap_queue import get_webscrap_queue

from home import Home

from consumer import consumer_handler, add_url_to_queue

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





# @app.get("/")
# async def root():
#     webscrap_queue.put('SDASSD')
#     return {"message": "Hello World"}

from multiprocessing import Queue



class Test:

    def __init__(self, name: str, queue: Queue):
        self.name = name
        self.queue = queue
        self.router = APIRouter()
        self.router.add_api_route("/hello", self.hello, methods=["GET"])

    def hello(self):
        add_url_to_queue(self.queue, self.name)
        return {"Hello": self.name}




async def async_main() -> None:
    print("Creando tablas...")
    async with sessionmanager._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    # queue = get_webscrap_queue()
    app = FastAPI(lifespan=lifespan, title="ssss", docs_url="/api/docs", debug=True)

    # CORS Allow all
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # _webscrap_queue = Queue()
    manager = multiprocessing.Manager()
    _webscrap_queue = manager.Queue()

    consumer_process = Process(target=consumer_handler, args=(_webscrap_queue,))
    consumer_process.start()

    test = Test("test", _webscrap_queue)

    companies = CompaniesAPI(_webscrap_queue)

    app.include_router(test.router)
    app.include_router(certificates_router)
    app.include_router(companies.router)
    app.include_router(urls_router)
    app.include_router(resources_router)

    # add_url_to_queue(_webscrap_queue, 'EOOEOEOE')
    # add_url_to_queue(_webscrap_queue, '22222')

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('./cert/cert.pem', keyfile='./cert/key.pem')
    print("Inicializando API REST")
    asyncio.run(async_main())
    uvicorn.run(app, host="0.0.0.0", reload=False, port=8000)
