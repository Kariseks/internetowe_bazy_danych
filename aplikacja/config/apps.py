from django.contrib.admin.apps import AdminConfig


class SklepAdminConfig(AdminConfig):
    default_site = 'config.admin.SklepAdminSite'
