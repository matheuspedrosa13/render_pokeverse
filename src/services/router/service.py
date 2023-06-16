from fastapi import APIRouter


class Router:
    __router = None

    @classmethod
    def get_router(cls):
        if cls.__router is None:
            cls.__router = APIRouter()
        return cls.__router
