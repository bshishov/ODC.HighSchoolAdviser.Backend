# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import HighSchoolAdviser.models


class Migration(migrations.Migration):

    dependencies = [
        ('HighSchoolAdviser', '0004_auto_20151206_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='favhs',
            field=HighSchoolAdviser.models.ListField(),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='favpl',
            field=HighSchoolAdviser.models.ListField(),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='specs',
            field=HighSchoolAdviser.models.ListField(),
        ),
    ]
