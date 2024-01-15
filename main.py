from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings.config import settings

from src.task.router import router as task_router
from src.auth.router import router as auth_router


app = FastAPI(
    title="ToDo app API",
    description="Just simple todo app on FastAPI",
    version="0.0.1",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


api_prefix = settings.api_v1_prefix

app.include_router(router=task_router, prefix=api_prefix)
app.include_router(router=auth_router, prefix=api_prefix)
