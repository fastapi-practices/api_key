# API Key

用户自定义 API Key 管理，支持生成、管理和使用 API Key 进行接口认证

- API Key 使用 `Authorization: Bearer <api_key>` 传递
- 认证成功后继承所属用户权限
- 可通过专用 API 用户和角色限制访问范围

## 插件类型

- 扩展级插件
- 扩展目标：`admin`

## 配置说明

插件目录下 `plugin.toml` 的 `[settings]` 中包含以下内容：

```toml
[settings]
API_KEY_GENERATE_PREFIX = 'fba-'
```

## 使用方式

1. 安装并启用插件后，重启后端服务
2. 在后台为指定用户创建 API Key
3. 请求接口时使用 `Authorization: Bearer <api_key>`
4. 自 fba v1.13.3 起，插件安装后会自动应用；旧版本需在 `backend/core/registrar.py` 中将 `JwtAuthMiddleware` 替换为
   `JwtApiKeyAuthMiddleware`
5. 如需限制 API Key 权限，请创建专用角色和 API 用户，再使用该用户创建 API Key

## 卸载说明

- 卸载插件后，建议删除已签发的 API Key 数据
- 如外部系统仍在使用 API Key 调用接口，请同步清理对应配置

## 联系方式

- 作者：`wu-clan`
- 反馈方式：提交 Issue 或 PR
