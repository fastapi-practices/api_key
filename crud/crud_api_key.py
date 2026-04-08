from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.api_key.model import ApiKey
from backend.plugin.api_key.schema.api_key import CreateApiKeyParam, UpdateApiKeyParam


class CRUDApiKey(CRUDPlus[ApiKey]):
    """API Key 数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> ApiKey | None:
        """
        获取 API Key

        :param db: 数据库会话
        :param pk: API Key ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_user_id(self, db: AsyncSession, user_id: int, pk: int) -> ApiKey | None:
        """
        通过用户 ID 获取 API Key

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param pk: API Key ID
        :return:
        """
        return await self.select_model(db, pk, user_id=user_id)

    async def get_by_key(self, db: AsyncSession, key: str) -> ApiKey | None:
        """
        通过 key 获取 API Key

        :param db: 数据库会话
        :param key: API Key
        :return:
        """
        return await self.select_model_by_column(db, key=key)

    async def get_select(self, user_id: int | None, is_superuser: bool, name: str | None, status: int | None) -> Select:  # noqa: FBT001
        """
        获取 API Key 列表查询表达式

        :param user_id: 用户 ID
        :param is_superuser: 用户超级管理员权限
        :param name: API Key 名称
        :param status: 状态
        :return:
        """
        filters = {}

        if not is_superuser:
            filters['user_id'] = user_id
        if name is not None:
            filters['name__like'] = f'%{name}%'
        if status is not None:
            filters['status'] = status

        return await self.select_order('id', 'desc', **filters)

    async def create(self, db: AsyncSession, user_id: int, key: str, obj: CreateApiKeyParam) -> ApiKey:
        """
        创建 API Key

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param key: API Key
        :param obj: 创建 API Key 参数
        :return:
        """
        dict_obj = obj.model_dump()
        dict_obj['user_id'] = user_id
        dict_obj['key'] = key

        new_api_key = self.model(**dict_obj)
        db.add(new_api_key)
        await db.flush()

        return new_api_key

    async def update(self, db: AsyncSession, pk: int, obj: UpdateApiKeyParam) -> int:
        """
        更新 API Key

        :param db: 数据库会话
        :param pk: API Key ID
        :param obj: 更新 API Key 参数
        :return:
        """
        return await self.update_model(db, pk, obj.model_dump(exclude_unset=True))

    async def set_status(self, db: AsyncSession, pk: int, status: int) -> int:
        """
        设置 API Key 状态

        :param db: 数据库会话
        :param pk: API Key ID
        :param status: 状态
        :return:
        """
        return await self.update_model(db, pk, {'status': status})

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除 API Key

        :param db: 数据库会话
        :param pks: API Key ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


api_key_dao: CRUDApiKey = CRUDApiKey(ApiKey)
