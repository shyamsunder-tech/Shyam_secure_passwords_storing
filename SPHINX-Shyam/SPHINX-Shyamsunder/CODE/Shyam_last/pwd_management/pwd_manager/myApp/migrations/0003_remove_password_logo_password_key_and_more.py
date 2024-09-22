# Generated by Django 5.0.2 on 2024-02-29 10:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_alter_password_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='password',
            name='logo',
        ),
        migrations.AddField(
            model_name='password',
            name='key',
            field=models.CharField(default=123456, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='password',
            name='email',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='password',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='password',
            name='password',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='password',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passwords', to=settings.AUTH_USER_MODEL),
        ),
    ]
