from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Usuario(BaseModel):
    id: int
    nome: str
    email: EmailStr


class UsuarioCriacao(BaseModel):
    nome: str
    email: EmailStr


banco_usuarios = []
proximo_id = 1
