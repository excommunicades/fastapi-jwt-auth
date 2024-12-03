from fastapi_jwt_auth.configurations.routes.routes import Routes
from fastapi_jwt_auth.internal.routes import example

__routes__ = Routes(routers=(example.router, ))