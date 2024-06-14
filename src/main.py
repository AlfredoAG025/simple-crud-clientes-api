from contextlib import asynccontextmanager

import datetime
import random
import string

from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from . import config

client = AsyncIOMotorClient(config.DB_URI)
database = client[str(config.DB_NAME)]
collection = database.clientes


def generate_random_id():
    # Get current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS

    # Generate a random string of length 6
    random_str = ''.join(random.choices(
        string.ascii_letters + string.digits, k=6))

    # Combine date and random string
    random_id = f"{date_str}_{random_str}"

    return random_id


class Cliente(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    empresa: str
    puesto: str
    estado: int
    id: Optional[str] = None


app = FastAPI(
    title="Clientes",
)

origins = [
    config.FRONTEND_URL,
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/clientes', tags=['clientes'], response_model=list[Cliente])
async def get_clientes():
    cursor = collection.find()
    clientes = []
    for document in await cursor.to_list(length=100):
        clientes.append(document)
    return clientes


@app.get('/clientes/{id}', tags=['clientes'], response_model=Cliente)
async def get_one_cliente(id: str):
    cliente = await collection.find_one({"id": id})
    return cliente


@app.post('/clientes', tags=['clientes'])
async def insert_cliente(data: Cliente):
    data.id = generate_random_id()
    result = await collection.insert_one(data.model_dump())
    return {
        "message": "cliente agregado!",
    }


@app.put('/clientes/{id}', tags=['clientes'])
async def replace_cliente(id: str, data: Cliente):
    result = await collection.replace_one({"id": id}, data.model_dump())
    return {
        "message": "cliente remplazado/actualizado!",
    }


@app.patch('/clientes/{id}', tags=['clientes'])
async def update_cliente(id: str, partial_data: dict):
    result = await collection.update_one({"id": id}, {"$set": partial_data})
    return {
        "message": "cliente parcialmente/actualizado!",
    }


@app.delete('/clientes/{id}', tags=['clientes'])
async def delete_cliente(id: str):
    result = await collection.delete_one({"id": id})
    return {
        "message": "cliente eliminado!",
    }
