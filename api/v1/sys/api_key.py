from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.common.response.response_code import CustomResponse
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.api_key.schema.api_key import (
    CreateApiKeyParam,
    DeleteApiKeyParam,
    GetApiKeyDetail,
    UpdateApiKeyParam,
)
from backend.plugin.api_key.service import api_key_service

router = APIRouter()


@router.get('/{pk}', summary='获取 API Key 详情', dependencies=[DependsJwtAuth])
async def get_api_key(
    db: CurrentSession, request: Request, pk: Annotated[int, Path(description='通知公告 ID')]
) -> ResponseSchemaModel[GetApiKeyDetail]:
    data = await api_key_service.get(db=db, user_id=request.user.id, is_superuser=request.user.is_superuser, pk=pk)
    return response_base.success(data=data)


@router.get('', summary='分页获取所有 API Key', dependencies=[DependsJwtAuth])
async def get_api_keys_paginated(
    db: CurrentSession,
    request: Request,
    name: Annotated[str | None, Query(description='API Key 名称')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[list[GetApiKeyDetail]]:
    data = await api_key_service.get_list(
        db=db, user_id=request.user.id, is_superuser=request.user.is_superuser, name=name, status=status
    )
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建 API Key',
    dependencies=[
        Depends(RequestPermission('sys:apikey:add')),
        DependsRBAC,
    ],
)
async def create_api_key(
    db: CurrentSessionTransaction,
    request: Request,
    obj: CreateApiKeyParam,
) -> ResponseSchemaModel[GetApiKeyDetail]:
    data = await api_key_service.create(db=db, user_id=request.user.id, obj=obj)
    return response_base.success(
        res=CustomResponse(
            code=200,
            msg='创建成功，请妥善保管此 API Key，仅显示一次',
        ),
        data=data,
    )


@router.put(
    '/{pk}',
    summary='更新 API Key',
    dependencies=[
        Depends(RequestPermission('sys:apikey:edit')),
        DependsRBAC,
    ],
)
async def update_api_key(
    db: CurrentSessionTransaction,
    request: Request,
    pk: Annotated[int, Path(description='API Key ID')],
    obj: UpdateApiKeyParam,
) -> ResponseModel:
    await api_key_service.update(db=db, user_id=request.user.id, is_superuser=request.user.is_superuser, pk=pk, obj=obj)
    return response_base.success()


@router.delete(
    '',
    summary='批量删除 API Key',
    dependencies=[
        Depends(RequestPermission('sys:apikey:del')),
        DependsRBAC,
    ],
)
async def delete_api_keys(
    db: CurrentSessionTransaction,
    request: Request,
    obj: DeleteApiKeyParam,
) -> ResponseModel:
    await api_key_service.delete(db=db, user_id=request.user.id, pks=obj.pks)
    return response_base.success()
