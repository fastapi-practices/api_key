INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
SELECT
  'api_key.menu',
  'PluginApiKey',
  '/plugins/api-key',
  11,
  'mdi:key-outline',
  1,
  '/plugins/api_key/views/index',
  NULL,
  1,
  1,
  1,
  '',
  'API Key 管理',
  (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'System' LIMIT 1) AS tmp_parent),
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM sys_menu WHERE name = 'PluginApiKey'
);

UPDATE sys_menu
SET
  title = 'api_key.menu',
  path = '/plugins/api-key',
  sort = 11,
  icon = 'mdi:key-outline',
  type = 1,
  component = '/plugins/api_key/views/index',
  perms = NULL,
  status = 1,
  display = 1,
  cache = 1,
  link = '',
  remark = 'API Key 管理',
  parent_id = (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'System' LIMIT 1) AS tmp_parent),
  updated_time = CURRENT_TIMESTAMP
WHERE name = 'PluginApiKey';

INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
SELECT
  '新增',
  'AddApiKey',
  NULL,
  0,
  NULL,
  2,
  NULL,
  'sys:apikey:add',
  1,
  0,
  1,
  '',
  NULL,
  (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'PluginApiKey' LIMIT 1) AS tmp_parent),
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM sys_menu WHERE name = 'AddApiKey'
);

UPDATE sys_menu
SET
  title = '新增',
  path = NULL,
  sort = 0,
  icon = NULL,
  type = 2,
  component = NULL,
  perms = 'sys:apikey:add',
  status = 1,
  display = 0,
  cache = 1,
  link = '',
  remark = NULL,
  parent_id = (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'PluginApiKey' LIMIT 1) AS tmp_parent),
  updated_time = CURRENT_TIMESTAMP
WHERE name = 'AddApiKey';

INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
SELECT
  '修改',
  'EditApiKey',
  NULL,
  0,
  NULL,
  2,
  NULL,
  'sys:apikey:edit',
  1,
  0,
  1,
  '',
  NULL,
  (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'PluginApiKey' LIMIT 1) AS tmp_parent),
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM sys_menu WHERE name = 'EditApiKey'
);

UPDATE sys_menu
SET
  title = '修改',
  path = NULL,
  sort = 0,
  icon = NULL,
  type = 2,
  component = NULL,
  perms = 'sys:apikey:edit',
  status = 1,
  display = 0,
  cache = 1,
  link = '',
  remark = NULL,
  parent_id = (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'PluginApiKey' LIMIT 1) AS tmp_parent),
  updated_time = CURRENT_TIMESTAMP
WHERE name = 'EditApiKey';

INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
SELECT
  '删除',
  'DeleteApiKey',
  NULL,
  0,
  NULL,
  2,
  NULL,
  'sys:apikey:del',
  1,
  0,
  1,
  '',
  NULL,
  (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'PluginApiKey' LIMIT 1) AS tmp_parent),
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM sys_menu WHERE name = 'DeleteApiKey'
);

UPDATE sys_menu
SET
  title = '删除',
  path = NULL,
  sort = 0,
  icon = NULL,
  type = 2,
  component = NULL,
  perms = 'sys:apikey:del',
  status = 1,
  display = 0,
  cache = 1,
  link = '',
  remark = NULL,
  parent_id = (SELECT id FROM (SELECT id FROM sys_menu WHERE name = 'PluginApiKey' LIMIT 1) AS tmp_parent),
  updated_time = CURRENT_TIMESTAMP
WHERE name = 'DeleteApiKey';
