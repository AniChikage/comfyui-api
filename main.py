from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import (
    text2image
)


app = FastAPI(openapi_url="/openapi", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text2image.router)
