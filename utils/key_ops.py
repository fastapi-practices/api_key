import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.enums import StatusType
from backend.common.exception import errors
from backend.core.conf import settings
from backend.plugin.api_key.crud import api_key_dao
from backend.plugin.api_key.model import ApiKey
from backend.utils.timezone import timezone


def generate_api_key() -> str:
    """生成 API Key"""
    return f'{settings.API_KEY_GENERATE_PREFIX}{secrets.token_urlsafe(32)}'


def mask_key(key: str) -> str:
    """
    隐藏 API Key 中间部分

    :param key: 完整的 API Key
    :return:
    """
    return key[:8] + '********' + key[-4:]


async def api_key_verify(db: AsyncSession, key: str) -> ApiKey:
    """
    验证 API Key

    :param db: 数据库会话
    :param key: API Key
    :return:
    """
    api_key = await api_key_dao.get_by_key(db, key)
    if not api_key:
        raise errors.AuthorizationError(msg='API Key 无效')

    if api_key.status == StatusType.disable:
        raise errors.AuthorizationError(msg='API Key 已被禁用')

    if api_key.expire_time is not None and api_key.expire_time < timezone.now():
        raise errors.AuthorizationError(msg='API Key 已过期')

    return api_key
