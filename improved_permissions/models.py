""" permissions models """
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from improved_permissions.roles import Role
from improved_permissions.utils import get_roleclass


class RolePermission(models.Model):
    """
    Role

    This model rocks.

    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roles',
        verbose_name='Usuário'
    )

    role_class = models.CharField(max_length=256)

    _role_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    _role_object_id = models.PositiveIntegerField(blank=True, null=True)
    obj = GenericForeignKey(ct_field='_role_object_type', fk_field='_role_object_id')

    class Meta:
        verbose_name = 'Role Instance'
        verbose_name_plural = 'Role Instances'
        unique_together = ('user', 'role_class', '_role_object_type', '_role_object_id')

    def __str__(self):
        role = get_roleclass(self.role_class)
        output = '{user} as {role}'.format(user=self.user, role=role.get_verbose_name())
        if self.obj:
            output += ' in {obj}'.format(obj=self.obj)
        return output

    def clean(self):
        for role_class in Role.get_roles():
            if self.role_class == role_class.get_class_name():
                return
        raise ValidationError(
            {'role_class': 'This string representation does not exist as a Role class.'}
        )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ,unused-argument
        self.clean()
        super().save()
