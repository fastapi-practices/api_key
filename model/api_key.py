from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, TimeZone, UniversalText, id_key


class ApiKey(Base):
    """用户 API Key 表"""

    __tablename__ = 'sys_api_key'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='用户 ID')
    name: Mapped[str] = mapped_column(sa.String(64), comment='API Key 名称')
    key: Mapped[str] = mapped_column(sa.String(64), unique=True, index=True, comment='API Key')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1正常）')
    expire_time: Mapped[datetime | None] = mapped_column(TimeZone, default=None, comment='过期时间（空表示永不过期）')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')
