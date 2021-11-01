# https://fastapi.tiangolo.com/ja/tutorial/security/first-steps/
# 詳細は上記参照
from fastapi import FastAPI
from routers.auth import router as auth_router
from fastapi.staticfiles import StaticFiles

title = 'Authentication-server-pytest'
description = 'Learn about secure login authentication with fastapi.'
version = '1.0.0'


app = FastAPI(title=title,description=description,version=version)
app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")