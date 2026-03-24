delete from sys_menu where name in ('AddApiKey', 'EditApiKey', 'DeleteApiKey');

delete from sys_menu where name = 'PluginApiKey';

drop table if exists sys_api_key;
