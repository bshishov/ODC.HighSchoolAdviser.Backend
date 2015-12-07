# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HighSchoolAdviser', '0002_auto_20151205_2048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='highschools',
            new_name='fav_hs',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='fav_pl',
            field=models.CharField(max_length=3000, default=''),
            preserve_default=False,
        ),
    ]
