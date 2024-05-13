import asyncio
import logging
import multiprocessing
import sys
import ssl
from contextlib import asynccontextmanager
from multiprocessing import Queue, Process
# from text_extract import extract

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
    # extracted_entities = extract("ACCIONA ha implantado un sistema orie"
    #                              "ntado hacia la mejora continua y la sostenibilidad en todos sus productos y servicios. ACCIONA ha implantado un sistema de gestión que integra los aspectos económicos, técnicos, legales, ambientales y sociales de la empresa, basados ​​en sus pr"
    #                              "ocesos, y orientado hacia la mejora continua y la prevención de la contaminación.El sistema de gestión establecido ha sido auditado por AENOR, según los requisitos de las normas internacionales ISO 9001: 2015 e ISO 14001: 2015, obteniendo la certificación de la empresa tanto en el sistema de gestión de calidad como en el sistema de gestión amb"
    #                              "obtenidos abarca la promoción de bienes inmuebles (gestión de diseño, gestión de construcción y gestión de), así como la administración de patrimonio inmobiliario.")
    # print(extracted_entities)
    #
    # extracted_entities2 = extract("La valoración y percepción del cliente es muy importante para nosotros. En este sentido se realizan varios análisis en relación con las decisiones tomadas por los clientes:"
    #                               "Análisis de los motivos de no compra: Todos los años se realiza un seguimiento de las razones por las que los clientes interesados en nuestras promociones terminan no comprando su vivienda con ACCIONA. Este análisis se realiza por cada una de las promociones."
    #                               "ncuestas de satisfacción al cliente: Estas encuestas evalúan todas las fases del proceso de compra, desde el punto de venta y la firma del contrato, la valoración del inmueble y oferta, el funcionamiento de la vivienda y la actitud posterior a la entrega de esta. Se realiza de forma anual, sobre todas las promociones entregadas durante el año"
    #                               "Derivadas de estos análisis selabora un plan de acción dedicado a la mejora de los puntos críticos detectados.")
    # print(extracted_entities2)

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
