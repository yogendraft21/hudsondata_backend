from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.index import user_router
from config.db import meta, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

meta.create_all(engine)
app.include_router(user_router, prefix="/user")
