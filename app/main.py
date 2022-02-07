import dotenv

dotenv.load_dotenv()

import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from database.db import engine
from database import models
from routers import recipes

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

origins = os.getenv("CORS_ORIGIN_SERVER")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = "/api/v1"

app.include_router(recipes.router, prefix=prefix)
