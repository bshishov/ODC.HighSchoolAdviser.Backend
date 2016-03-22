# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151205_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='fav_hs',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='fav_pl',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='favhs',
            field=models.CharField(max_length=3000, default='[]'),
        ),
        migrations.AddField(
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
