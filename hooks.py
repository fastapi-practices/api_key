from contextlib import asynccontextmanager

from backend.plugin.api_key.middleware import JwtApiKeyAuthMiddleware
from backend.plugin.patching import replace_middleware
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware


def setup(app: FastAPI):
    # 替换中间件为插件自定义的中间件
    replace_middleware(
        app,
        AuthenticationMiddleware,
        AuthenticationMiddleware,
        backend=JwtApiKeyAuthMiddleware(),
        on_error=JwtApiKeyAuthMiddleware.auth_exception_handler,
    )
