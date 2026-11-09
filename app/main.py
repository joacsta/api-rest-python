from fastapi import FastAPI

from app.database import Base, engine
from app.routers import usuarios

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(usuarios.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Api funcionando"}
