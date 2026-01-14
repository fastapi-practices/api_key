"""
扩展的 JWT 认证中间件，支持 API Key 认证

使用方式：
    Authorization: Bearer <jwt_token>  # JWT 认证
    Authorization: Bearer fba_xxxxx    # API Key 认证（以 fba_ 开头）
"""

from fastapi import Request
from starlette.authentication import AuthCredentials

from backend.app.admin.schema.user import GetUserInfoWithRelationDetail
from backend.common.exception.errors import TokenError
from backend.common.log import log
from backend.common.security.jwt import get_jwt_user
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.middleware.jwt_auth_middleware import AuthenticationError, JwtAuthMiddleware
from backend.plugin.api_key.utils.key_ops import api_key_verify


class JwtApiKeyAuthMiddleware(JwtAuthMiddleware):
    """JWT 认证中间件（扩展支持 API Key）"""

    async def authenticate(self, request: Request) -> tuple[AuthCredentials, GetUserInfoWithRelationDetail] | None:
        """
        认证请求（支持 JWT Token 和 API Key）

        :param request: FastAPI 请求对象
        :return:
        """
        token = self.extract_token(request)
        if token is None:
            return None

        if token.startswith(settings.API_KEY_GENERATE_PREFIX):
            return await self._api_key_authentication(token)

        return await super().authenticate(request)

    @staticmethod
    async def _api_key_authentication(api_key: str) -> tuple[AuthCredentials, GetUserInfoWithRelationDetail]:
        """
        API Key 认证

        :param api_key: API Key
        :return:
        """
        try:
            async with async_db_session() as db:
                api_key_obj = await api_key_verify(db=db, key=api_key)
                user_id = api_key_obj.user_id
                user = await get_jwt_user(user_id)
        except TokenError as exc:
            raise AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except Exception as e:
            log.exception(f'API Key 授权异常：{e}')
            raise AuthenticationError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        return AuthCredentials(['authenticated']), user
