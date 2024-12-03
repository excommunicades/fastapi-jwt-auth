from fastapi import FastAPI

from fastapi_jwt_auth.configurations.server import Server

def create_app(_=None) -> FastAPI:

    app = FastAPI()

    return Server(app).get_app()


if __name__ == '__main__':

    import uvicorn

    app = create_app()

    uvicorn.run("main:create_app", host="0.0.0.0", port=8000, reload=True)