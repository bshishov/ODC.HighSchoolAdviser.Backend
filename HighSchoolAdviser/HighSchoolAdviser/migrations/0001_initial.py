# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OdcEnrollee',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('full_name', models.CharField(max_length=511)),
                ('date_created', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'odc_enrollee',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoCommercialType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_commercial_type',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoContestType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_contest_type',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoExamsAvg',
            fields=[
                ('year', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('russian', models.FloatField()),
                ('math', models.FloatField()),
                ('physics', models.FloatField()),
                ('chemistry', models.FloatField()),
                ('informatics', models.FloatField()),
                ('biology', models.FloatField()),
                ('history', models.FloatField()),
                ('geography', models.FloatField()),
                ('foreign_language', models.FloatField()),
                ('social_science', models.FloatField()),
                ('literature', models.FloatField()),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_exams_avg',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoExamsMin',
            fields=[
                ('year', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('russian', models.SmallIntegerField()),
                ('math', models.SmallIntegerField()),
                ('physics', models.SmallIntegerField()),
                ('chemistry', models.SmallIntegerField()),
                ('informatics', models.SmallIntegerField()),
                ('biology', models.SmallIntegerField()),
                ('history', models.SmallIntegerField()),
                ('geography', models.SmallIntegerField()),
                ('foreign_language', models.SmallIntegerField()),
                ('social_science', models.SmallIntegerField()),
                ('literature', models.SmallIntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_exams_min',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoForm',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_form',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoHighschool',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
                ('website', models.CharField(max_length=511, blank=True, null=True)),
                ('city', models.CharField(max_length=511, blank=True, null=True)),
                ('address', models.CharField(max_length=511, blank=True, null=True)),
                ('raiting', models.FloatField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_highschool',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoResultType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_result_type',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoSpec',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_spec',
            },
        ),
        migrations.CreateModel(
            name='OdcInfoSpecGroup',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_info_spec_group',
            },
        ),
        migrations.CreateModel(
            name='OdcPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('year', models.SmallIntegerField()),
                ('planned', models.IntegerField()),
                ('russian', models.IntegerField()),
                ('math', models.IntegerField()),
                ('physics', models.IntegerField()),
                ('chemistry', models.IntegerField()),
                ('informatics', models.IntegerField()),
                ('biology', models.IntegerField()),
                ('history', models.IntegerField()),
                ('geography', models.IntegerField()),
                ('foreign_language', models.IntegerField()),
                ('social_science', models.IntegerField()),
                ('literature', models.IntegerField()),
                ('additional_exam', models.IntegerField()),
                ('debug_url', models.CharField(max_length=511, blank=True, null=True)),
                ('debug_comment', models.CharField(max_length=511, blank=True, null=True)),
                ('min_sum_1', models.FloatField(blank=True, null=True)),
                ('max_sum_1', models.FloatField(blank=True, null=True)),
                ('min_sum_2', models.FloatField(blank=True, null=True)),
                ('max_sum_2', models.FloatField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_plan',
            },
        ),
        migrations.CreateModel(
            name='OdcPlanType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=511)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_plan_type',
            },
        ),
        migrations.CreateModel(
            name='OdcRegion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('center', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_region',
            },
        ),
        migrations.CreateModel(
            name='OdcResults',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('year', models.SmallIntegerField()),
                ('date_created', models.DateTimeField()),
                ('enrollee_full_name', models.CharField(max_length=255, blank=True, null=True)),
                ('enrollee_id', models.IntegerField(blank=True, null=True)),
                ('spec_id', models.IntegerField()),
                ('hostel_required', models.IntegerField(blank=True, null=True)),
                ('total', models.SmallIntegerField(blank=True, null=True)),
                ('russian', models.SmallIntegerField(blank=True, null=True)),
                ('math', models.SmallIntegerField(blank=True, null=True)),
                ('physics', models.SmallIntegerField(blank=True, null=True)),
                ('chemistry', models.SmallIntegerField(blank=True, null=True)),
                ('informatics', models.SmallIntegerField(blank=True, null=True)),
                ('biology', models.SmallIntegerField(blank=True, null=True)),
                ('history', models.SmallIntegerField(blank=True, null=True)),
                ('geography', models.SmallIntegerField(blank=True, null=True)),
                ('foreign_language', models.SmallIntegerField(blank=True, null=True)),
                ('social_science', models.SmallIntegerField(blank=True, null=True)),
                ('literature', models.SmallIntegerField(blank=True, null=True)),
                ('additional_exam', models.SmallIntegerField(blank=True, null=True)),
                ('personal_score', models.SmallIntegerField(blank=True, null=True)),
                ('debug_url', models.CharField(max_length=511, blank=True, null=True)),
                ('debug_comment', models.CharField(max_length=511, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'odc_results',
            },
        ),
        migrations.CreateModel(
            name='OdcResultsBins',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('highschool_id', models.IntegerField()),
                ('spec_id', models.IntegerField()),
                ('below_150', models.IntegerField()),
                ('below_160', models.IntegerField()),
                ('below_170', models.IntegerField()),
                ('below_180', models.IntegerField()),
                ('below_190', models.IntegerField()),
                ('below_200', models.IntegerField()),
                ('below_210', models.IntegerField()),
                ('below_220', models.IntegerField()),
                ('below_230', models.IntegerField()),
                ('below_240', models.IntegerField()),
                ('below_250', models.IntegerField()),
                ('below_260', models.IntegerField()),
                ('below_270', models.IntegerField()),
                ('below_280', models.IntegerField()),
                ('below_290', models.IntegerField()),
                ('below_300', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'odc_results_bins',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('russian', models.IntegerField()),
                ('math', models.IntegerField()),
                ('physics', models.IntegerField()),
                ('chemistry', models.IntegerField()),
                ('informatics', models.IntegerField()),
                ('biology', models.IntegerField()),
                ('history', models.IntegerField()),
                ('geography', models.IntegerField()),
                ('foreign_language', models.IntegerField()),
                ('social_science', models.IntegerField()),
                ('literature', models.IntegerField()),
                ('specs', models.CharField(max_length=2000)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
