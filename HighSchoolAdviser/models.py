# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class OdcEnrollee(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    full_name = models.CharField(max_length=511)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'odc_enrollee'


class OdcInfoCommercialType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_commercial_type'


class OdcInfoContestType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_contest_type'


class OdcInfoExamsAvg(models.Model):
    year = models.IntegerField(primary_key=True)
    russian = models.FloatField()
    math = models.FloatField()
    physics = models.FloatField()
    chemistry = models.FloatField()
    informatics = models.FloatField()
    biology = models.FloatField()
    history = models.FloatField()
    geography = models.FloatField()
    foreign_language = models.FloatField()
    social_science = models.FloatField()
    literature = models.FloatField()

    class Meta:
        managed = False
        db_table = 'odc_info_exams_avg'


class OdcInfoExamsMin(models.Model):
    year = models.IntegerField(primary_key=True)
    russian = models.IntegerField()
    math = models.IntegerField()
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    informatics = models.IntegerField()
    biology = models.IntegerField()
    history = models.IntegerField()
    geography = models.IntegerField()
    foreign_language = models.IntegerField()
    social_science = models.IntegerField()
    literature = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'odc_info_exams_min'


class OdcInfoForm(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_form'


class OdcInfoHighschool(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=511)
    website = models.CharField(max_length=511, blank=True)
    city = models.CharField(max_length=511, blank=True)
    address = models.CharField(max_length=511, blank=True)
    raiting = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'odc_info_highschool'


class OdcInfoResultType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_result_type'


class OdcInfoSpec(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group_id = models.IntegerField()
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_spec'


class OdcInfoSpecGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_spec_group'


class OdcPlan(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    year = models.IntegerField()
    highschool = models.ForeignKey(OdcInfoHighschool)
    spec_id = models.IntegerField()
    form = models.ForeignKey(OdcInfoForm)
    plan_type = models.ForeignKey('OdcPlanType')
    commercial_type = models.ForeignKey(OdcInfoCommercialType)
    planned = models.IntegerField()
    russian = models.IntegerField()
    math = models.IntegerField()
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    informatics = models.IntegerField()
    biology = models.IntegerField()
    history = models.IntegerField()
    geography = models.IntegerField()
    foreign_language = models.IntegerField()
    social_science = models.IntegerField()
    literature = models.IntegerField()
    additional_exam = models.IntegerField()
    debug_url = models.CharField(max_length=511, blank=True)
    debug_comment = models.CharField(max_length=511, blank=True)
    min_sum_1 = models.FloatField(blank=True, null=True)
    max_sum_1 = models.FloatField(blank=True, null=True)
    min_sum_2 = models.FloatField(blank=True, null=True)
    max_sum_2 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'odc_plan'


class OdcPlanType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_plan_type'


class OdcPlanView(models.Model):
    year = models.IntegerField()
    highschool_id = models.BigIntegerField()
    spec_code = models.IntegerField()
    form_id = models.IntegerField()
    plan_type_id = models.IntegerField()
    commercial_type_id = models.IntegerField(blank=True, null=True)
    min_sum = models.IntegerField(blank=True, null=True)
    max_sum = models.IntegerField(blank=True, null=True)
    result_type_id = models.IntegerField(blank=True, null=True)
    russian = models.IntegerField(blank=True, null=True)
    math = models.IntegerField(blank=True, null=True)
    physics = models.IntegerField(blank=True, null=True)
    chemistry = models.IntegerField(blank=True, null=True)
    informatics = models.IntegerField(blank=True, null=True)
    biology = models.IntegerField(blank=True, null=True)
    history = models.IntegerField(blank=True, null=True)
    geography = models.IntegerField(blank=True, null=True)
    foreign_language = models.IntegerField(blank=True, null=True)
    social_science = models.IntegerField(blank=True, null=True)
    literature = models.IntegerField(blank=True, null=True)
    additional_exam = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'odc_plan_view'


class OdcRegion(models.Model):
