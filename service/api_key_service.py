from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.api_key.crud import api_key_dao
from backend.plugin.api_key.model import ApiKey
from backend.plugin.api_key.schema.api_key import (
    CreateApiKeyParam,
    UpdateApiKeyParam,
)
from backend.plugin.api_key.utils.key_ops import generate_api_key, mask_key


class ApiKeyService:
    """API Key 服务类"""

    @staticmethod
    async def _get(*, db: AsyncSession, user_id: int, is_superuser: bool, pk: int) -> ApiKey:
        """
        获取 API Key

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_superuser: 用户超级管理员权限
        :param pk: API Key ID
        :return:
        """
        if not is_superuser:
            api_key = await api_key_dao.get_by_user_id(db, user_id, pk)
        else:
            api_key = await api_key_dao.get(db, pk)
        if not api_key:
            raise errors.NotFoundError(msg='API Key 不存在')
        return api_key

    async def get(self, *, db: AsyncSession, user_id: int, is_superuser: bool, pk: int) -> ApiKey:
        """
        获取 API Key

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_superuser: 用户超级管理员权限
        :param pk: API Key ID
        :return:
        """
        return await self._get(db=db, user_id=user_id, is_superuser=is_superuser, pk=pk)

    @staticmethod
    async def get_list(
        *,
        db: AsyncSession,
        user_id: int | None = None,
        is_superuser: bool,
        name: str | None = None,
        status: int | None = None,
    ) -> dict:
        """
        获取 API Key 分页列表

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_superuser: 用户超级管理员权限
        :param name: API Key 名称
        :param status: 状态
        :return:
        """
        api_key_select = await api_key_dao.get_select(user_id, is_superuser, name, status)
        page_data = await paging_data(db, api_key_select)

        for item in page_data['items']:
            if item.get('key') is not None:
                item['key'] = mask_key(item.get('key'))

        return page_data

    @staticmethod
    async def create(*, db: AsyncSession, user_id: int, obj: CreateApiKeyParam) -> ApiKey:
        """
        创建 API Key

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param obj: 创建 API Key 参数
        :return:
        """
        api_key = generate_api_key()
        return await api_key_dao.create(db, user_id, api_key, obj)

    async def update(
        self, *, db: AsyncSession, user_id: int, is_superuser: bool, pk: int, obj: UpdateApiKeyParam
    ) -> int:
        """
        更新 API Key

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_superuser: 用户超级管理员权限
        :param pk: API Key ID
        :param obj: 更新 API Key 参数
        :return:
        """
        api_key = await self._get(db=db, user_id=user_id, is_superuser=is_superuser, pk=pk)
        if not is_superuser and user_id != api_key.user_id:
            raise errors.AuthorizationError
        return await api_key_dao.update(db, pk, obj)

    async def update_status(self, *, db: AsyncSession, user_id: int, is_superuser: bool, pk: int) -> int:
        """
        切换 API Key 状态

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_superuser: 用户超级管理员权限
        :param pk: API Key ID
        :return:
        """
        api_key = await self._get(db=db, user_id=user_id, is_superuser=is_superuser, pk=pk)
        if not is_superuser and user_id != api_key.user_id:
            raise errors.AuthorizationError
        next_status = 0 if api_key.status == 1 else 1
        return await api_key_dao.set_status(db, pk, next_status)

    async def delete(self, *, db: AsyncSession, user_id: int, is_superuser: bool, pks: list[int]) -> int:
        """
        批量删除 API Key

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_superuser: 用户超级管理员权限
        :param pks: API Key ID 列表
        :return:
        """
        for pk in pks:
            api_key = await self._get(db=db, user_id=user_id, is_superuser=is_superuser, pk=pk)
            if not is_superuser and user_id != api_key.user_id:
                raise errors.AuthorizationError
        return await api_key_dao.delete(db, pks)


api_key_service: ApiKeyService = ApiKeyService()
