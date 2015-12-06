# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HighSchoolAdviser', '0005_auto_20151206_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='favhs',
            field=models.CharField(max_length=3000, default='[]'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='favpl',
            field=models.CharField(max_length=3000, default='[]'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='specs',
            field=models.CharField(max_length=3000, default='[]'),
        ),
    ]
