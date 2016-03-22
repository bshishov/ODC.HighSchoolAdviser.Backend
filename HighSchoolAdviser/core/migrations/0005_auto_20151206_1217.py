# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151206_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='favhs',
            field=core.models.ListField(),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='favpl',
            field=core.models.ListField(),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='specs',
            field=core.models.ListField(),
        ),
    ]
