from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class ApiKeySchemaBase(SchemaBase):
    """API Key 基础模型"""

    name: str = Field(description='API Key 名称')
    status: StatusType = Field(description='状态')
    remark: str | None = Field(None, description='备注')


class CreateApiKeyParam(ApiKeySchemaBase):
    """创建 API Key 参数"""

    expire_days: int | None = Field(None, ge=1, le=365, description='过期天数（空表示永不过期，最大 365 天）')


class UpdateApiKeyParam(ApiKeySchemaBase):
    """更新 API Key 参数"""

    expire_days: int | None = Field(None, ge=1, le=365, description='过期天数（空表示永不过期，最大 365 天）')


class DeleteApiKeyParam(SchemaBase):
    """删除 API Key 参数"""

    pks: list[int] = Field(description='API Key ID 列表')


class GetApiKeyDetail(ApiKeySchemaBase):
    """API Key 列表详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='API Key ID')
    user_id: int = Field(description='用户 ID')
    key: str = Field(description='API Key')
    expire_time: datetime | None = Field(description='过期时间')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(description='更新时间')
