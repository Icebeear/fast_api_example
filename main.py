from fastapi import FastAPI
from src.settings.config import settings

from src.task.router import router as task_router

# from src.user.router import router as user_router
# from src.auth.demo import router as auth_router

app = FastAPI(
    title="ToDo app API",
    description="Just simple todo app on FastAPI",
    version="0.0.1",
)

api_prefix = settings.api_v1_prefix

app.include_router(router=task_router, prefix=api_prefix)
# app.include_router(router=user_router, prefix=api_prefix)
# app.include_router(router=auth_router, prefix=api_prefix)
