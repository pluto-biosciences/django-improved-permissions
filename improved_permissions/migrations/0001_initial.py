# Generated by Django 2.0.1 on 2018-02-27 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.BooleanField(choices=[(True, 'Allow'), (False, 'Deny')], default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_class', models.CharField(max_length=256)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('permissions', models.ManyToManyField(related_name='roles', through='improved_permissions.RolePermission', to='auth.Permission', verbose_name='Permissões')),
            ],
            options={
                'verbose_name_plural': 'Role Instances',
                'verbose_name': 'Role Instance',
            },
        ),
    ]
