# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('HighSchoolAdviser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='highschools',
            field=models.CharField(max_length=3000, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='biology',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='chemistry',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='foreign_language',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='geography',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='history',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='informatics',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='literature',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='math',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='physics',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='russian',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='social_science',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='specs',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_info'),
        ),
    ]
