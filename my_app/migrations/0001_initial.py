# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthAppShopUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('myshopify_domain', models.CharField(max_length=255, unique=True, editable=False)),
                ('token', models.CharField(max_length=32, default='00000000000000000000000000000000', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
