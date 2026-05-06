""" permissions configs """
from django.apps import AppConfig

from improved_permissions.utils import autodiscover, register_cleanup


class ImprovedPermissionsConfig(AppConfig):
    name = 'improved_permissions'
    verbose_name = 'Django Improved Permissions'
    # Pin to AutoField so host projects whose DEFAULT_AUTO_FIELD is
    # BigAutoField (the Django 3.2+ default) do not produce a spurious
    # AlterField migration against our existing 0001/0002 migrations.
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        register_cleanup()
        autodiscover()
