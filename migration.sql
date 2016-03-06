UPDATE django_content_type SET app_label='passwords.core' WHERE app_label='team_passwords';
ALTER TABLE team_passwords_group RENAME TO core_group;
ALTER TABLE team_passwords_groupuserpermission RENAME TO core_groupuserpermission;
ALTER TABLE team_passwords_site RENAME TO core_site;
-- UPDATE django_content_type SET name='<newModelName>' where name='<oldModelName>' AND app_label='team_passwords'
UPDATE django_migrations SET app='core' WHERE app='team_passwords';

-- Change migrations files