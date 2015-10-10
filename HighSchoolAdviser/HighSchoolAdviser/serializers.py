from rest_framework import serializers

from models import OdcInfoHighschool, OdcPlan

class HighSchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OdcInfoHighschool

class OdcPlanSerializer(serializers.HyperlinkedModelSerializer):
    highschool = serializers.SlugRelatedField(read_only=True, slug_field='id')
    # spec = serializers.SlugRelatedField(read_only=True, slug_field='id')
    form = serializers.SlugRelatedField(read_only=True, slug_field='id')
    plan_type = serializers.SlugRelatedField(read_only=True, slug_field='id')
    commercial_type = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = OdcPlan