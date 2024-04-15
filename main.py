from fastapi import FastAPI
from sqlalchemy import create_engine
from models.models import Base

app = FastAPI()


ruta = "base.db"

engine = create_engine("sqlite:///"+ruta, echo=True)


Base.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
