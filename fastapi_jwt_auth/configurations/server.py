from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from fastapi_jwt_auth.pkg.db.database import engine

from fastapi import FastAPI

from fastapi_jwt_auth.configurations.routes import __routes__
from fastapi_jwt_auth.internal.events.example_event import register_startup_event


class Server:

    __app = FastAPI()

    def __init__(self, app: FastAPI):

        self.__app = app
        self.__register_routes(app)
        self.__register_events(app)

    def get_app(self) -> FastAPI:

        return self.__app

    @staticmethod
    def __register_events(app):

        register_startup_event(app)

    @staticmethod
    def __register_routes(app):

        __routes__.register_routes(app)
