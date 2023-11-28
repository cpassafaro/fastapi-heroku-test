import socket
import sys
from src.kayak import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://storied-piroshki-4c2db4.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hostname = socket.gethostname()

version = f"{sys.version_info.major}.{sys.version_info.minor}"


@app.get("/")
async def read_root():
    return {
        "name": "my-app",
        "host": hostname,
        "version": f"Hello world! From FastAPI running on Uvicorn. Using Python {version}"
    }
@app.get("/all-kayaks")
def getAll():
  return getAllKayaks()

@app.get("/company/{name}")
def getByCompany(name: str):
  if name == 'next-adventure':
    return getBoatsNA()
  if name == 'colorado-kayak':
    return getBoatsFromColoradoKayak()
  if name == 'rutabaga-shop':
    return getBoatsFromRutabaga()