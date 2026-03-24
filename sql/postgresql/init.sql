do $$
declare
    api_key_menu_id bigint;
begin
    insert into sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    values ('api_key.menu', 'PluginApiKey', '/plugins/api-key', 11, 'mdi:key-outline', 1, '/plugins/api_key/views/index', null, 1, 1, 1, '', 'API Key 管理', (select id from sys_menu where name = 'System' limit 1), now(), null)
    returning id into api_key_menu_id;

    insert into sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    values
    ('新增', 'AddApiKey', null, 0, null, 2, null, 'sys:apikey:add', 1, 0, 1, '', null, api_key_menu_id, now(), null),
    ('修改', 'EditApiKey', null, 0, null, 2, null, 'sys:apikey:edit', 1, 0, 1, '', null, api_key_menu_id, now(), null),
    ('删除', 'DeleteApiKey', null, 0, null, 2, null, 'sys:apikey:del', 1, 0, 1, '', null, api_key_menu_id, now(), null);
end $$;

select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;
