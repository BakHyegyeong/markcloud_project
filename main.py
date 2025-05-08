
from fastapi import FastAPI

from domain.search import search_router

app = FastAPI()

app.include_router(search_router.router)


