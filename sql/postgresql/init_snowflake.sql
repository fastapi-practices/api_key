insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (2147651050620981248, 'api_key.menu', 'PluginApiKey', '/plugins/api-key', 11, 'mdi:key-outline', 1, '/plugins/api_key/views/index', null, 1, 1, 1, '', 'API Key 管理', (select id from sys_menu where name = 'System' limit 1), now(), null);

insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
(2147651050625175552, '新增', 'AddApiKey', null, 0, null, 2, null, 'sys:apikey:add', 1, 0, 1, '', null, 2147651050620981248, now(), null),
(2147651050629369856, '修改', 'EditApiKey', null, 0, null, 2, null, 'sys:apikey:edit', 1, 0, 1, '', null, 2147651050620981248, now(), null),
(2147651050633564160, '删除', 'DeleteApiKey', null, 0, null, 2, null, 'sys:apikey:del', 1, 0, 1, '', null, 2147651050620981248, now(), null);
