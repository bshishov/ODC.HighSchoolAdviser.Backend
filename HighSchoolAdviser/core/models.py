# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# deprecated, needed for migartions
class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='user_info')
    russian = models.IntegerField(default=0)
    math = models.IntegerField(default=0)
    physics = models.IntegerField(default=0)
    chemistry = models.IntegerField(default=0)
    informatics = models.IntegerField(default=0)
    biology = models.IntegerField(default=0)
    history = models.IntegerField(default=0)
    geography = models.IntegerField(default=0)
    foreign_language = models.IntegerField(default=0)
    social_science = models.IntegerField(default=0)
    literature = models.IntegerField(default=0)
    specs = models.CharField(default='[]', max_length=3000)
    favhs = models.CharField(default='[]', max_length=3000)
    favpl = models.CharField(default='[]', max_length=3000)

    def setspecs(self, x):
        import json
        self.specs = json.dumps(x)
    def getspecs(self):
        import json
        return json.loads(self.specs)
    def setfavhs(self, x):
        import json
        self.favhs = json.dumps(x)
    def getfavhs(self):
        import json
        return json.loads(self.favhs)
    def setfavpl(self, x):
        import json
        self.favpl = json.dumps(x)
    def getfavpl(self):
        import json
        return json.loads(self.favpl)


class OdcEnrollee(models.Model):
    full_name = models.CharField(max_length=511)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'odc_enrollee'


class OdcInfoCommercialType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_commercial_type'


class OdcInfoContestType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_contest_type'


class OdcInfoExamsAvg(models.Model):
    year = models.SmallIntegerField(primary_key=True)
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
    year = models.SmallIntegerField(primary_key=True)
    russian = models.SmallIntegerField()
    math = models.SmallIntegerField()
    physics = models.SmallIntegerField()
    chemistry = models.SmallIntegerField()
    informatics = models.SmallIntegerField()
    biology = models.SmallIntegerField()
    history = models.SmallIntegerField()
    geography = models.SmallIntegerField()
    foreign_language = models.SmallIntegerField()
    social_science = models.SmallIntegerField()
    literature = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'odc_info_exams_min'


class OdcInfoForm(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_form'


class OdcInfoHighschool(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=511)
    website = models.CharField(max_length=511, blank=True, null=True)
    city = models.CharField(max_length=511, blank=True, null=True)
    address = models.CharField(max_length=511, blank=True, null=True)
    raiting = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'odc_info_highschool'


class OdcInfoResultType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_result_type'


class OdcInfoSpec(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey('OdcInfoSpecGroup', related_name='specs')
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_spec'


class OdcInfoSpecGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_info_spec_group'


class OdcPlan(models.Model):
    year = models.SmallIntegerField()
    highschool = models.ForeignKey(OdcInfoHighschool)
    spec = models.ForeignKey(OdcInfoSpec)
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
    debug_url = models.CharField(max_length=511, blank=True, null=True)
    debug_comment = models.CharField(max_length=511, blank=True, null=True)
    min_sum_1 = models.FloatField(blank=True, null=True)
    max_sum_1 = models.FloatField(blank=True, null=True)
    min_sum_2 = models.FloatField(blank=True, null=True)
    max_sum_2 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'odc_plan'


class OdcPlanType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=511)

    class Meta:
        managed = False
        db_table = 'odc_plan_type'


class OdcRegion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    center = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'odc_region'


class OdcResults(models.Model):
    id = models.BigIntegerField(primary_key=True)
    year = models.SmallIntegerField()
    date_created = models.DateTimeField()
    enrollee_full_name = models.CharField(max_length=255, blank=True, null=True)
    enrollee_id = models.IntegerField(blank=True, null=True)
    highschool = models.ForeignKey(OdcInfoHighschool, related_name='results')
    spec_id = models.IntegerField()
    form = models.ForeignKey(OdcInfoForm)
    commercial_type = models.ForeignKey(OdcInfoCommercialType, blank=True, null=True)
    contest_type = models.ForeignKey(OdcInfoContestType, blank=True, null=True)
    result_type = models.ForeignKey(OdcInfoResultType, blank=True, null=True)
    hostel_required = models.IntegerField(blank=True, null=True)
    total = models.SmallIntegerField(blank=True, null=True)
    russian = models.SmallIntegerField(blank=True, null=True)
    math = models.SmallIntegerField(blank=True, null=True)
    physics = models.SmallIntegerField(blank=True, null=True)
    chemistry = models.SmallIntegerField(blank=True, null=True)
    informatics = models.SmallIntegerField(blank=True, null=True)
    biology = models.SmallIntegerField(blank=True, null=True)
    history = models.SmallIntegerField(blank=True, null=True)
    geography = models.SmallIntegerField(blank=True, null=True)
    foreign_language = models.SmallIntegerField(blank=True, null=True)
    social_science = models.SmallIntegerField(blank=True, null=True)
    literature = models.SmallIntegerField(blank=True, null=True)
    additional_exam = models.SmallIntegerField(blank=True, null=True)
    personal_score = models.SmallIntegerField(blank=True, null=True)
    debug_url = models.CharField(max_length=511, blank=True, null=True)
    debug_comment = models.CharField(max_length=511, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'odc_results'


class OdcResultsBins(models.Model):
    highschool_id = models.IntegerField()
    spec_id = models.IntegerField()
    result_type = models.ForeignKey(OdcInfoResultType)
    below_150 = models.IntegerField()
    below_160 = models.IntegerField()
    below_170 = models.IntegerField()
    below_180 = models.IntegerField()
    below_190 = models.IntegerField()
    below_200 = models.IntegerField()
    below_210 = models.IntegerField()
    below_220 = models.IntegerField()
    below_230 = models.IntegerField()
    below_240 = models.IntegerField()
    below_250 = models.IntegerField()
    below_260 = models.IntegerField()
    below_270 = models.IntegerField()
    below_280 = models.IntegerField()
    below_290 = models.IntegerField()
    below_300 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'odc_results_bins'