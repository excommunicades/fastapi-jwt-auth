from fastapi_jwt_auth.configurations.routes.routes import Routes
from fastapi_jwt_auth.internal.routes import health
from fastapi_jwt_auth.internal.routes.auth import auth

__routes__ = Routes(routers=(
                        health.router,
                        auth.router,
                        ))
