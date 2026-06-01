import secrets

from backend.core.conf import settings


def generate_api_key() -> str:
    """生成 API Key"""
    return f'{settings.API_KEY_GENERATE_PREFIX}{secrets.token_urlsafe(32)}'
