from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models.models import Base
from models.models import Certificate

import json

app = FastAPI()

ruta = "base.db"

engine = create_engine("sqlite:///" + ruta, echo=True)
session = Session(engine)

prefix = "/api"

Base.metadata.create_all(engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get(prefix + "/certificates/")
async def list_certificates():
    stmt = select(Certificate)
    res = session.execute(stmt).fetchall()


    json_response = jsonable_encoder(res)

    return JSONResponse(content=json_response)


@app.get(prefix + "/certificates/{cert_id}")
async def get_certificate(cert_id):
    stmt = select(Certificate).where(Certificate.id == cert_id)
    res = session.execute(stmt).fetchone()

    json_response = jsonable_encoder(res[0])

    return JSONResponse(content=json_response)