delete from sys_menu where name in ('AddApiKey', 'EditApiKey', 'DeleteApiKey');

delete from sys_menu where name = 'PluginApiKey';

drop table if exists sys_api_key;

select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;
