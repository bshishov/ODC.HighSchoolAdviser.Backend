from rest_framework import serializers

from .models import OdcInfoHighschool, OdcPlan, OdcInfoSpec, OdcInfoSpecGroup, OdcResults


# odc.results

class OdcResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdcResults

class ShortOdcResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdcResults
        fields = ('total',)


# odc.highschools

class HighSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdcInfoHighschool

class HighSchoolWithResultsSerializer(HighSchoolSerializer):
    results = serializers.SlugRelatedField(many=True, read_only=True, slug_field='total')

class HighSchoolWithResultsBySpecSerializer(serializers.HyperlinkedModelSerializer):
    results = serializers.SlugRelatedField(many=True, read_only=True, slug_field='total')

    class Meta:
        model = OdcInfoHighschool


# odc.specs and odc.groups

class SpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdcInfoSpec

class SpecGroupSerializer(serializers.ModelSerializer):
    specs = SpecSerializer(many=True, read_only=True)

    class Meta:
        model = OdcInfoSpecGroup

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdcInfoSpecGroup


# others

class PlanSerializer(serializers.ModelSerializer):
    highschool = serializers.SlugRelatedField(read_only=True, slug_field='id')
    # spec = serializers.SlugRelatedField(read_only=True, slug_field='id')
    form = serializers.SlugRelatedField(read_only=True, slug_field='id')
    plan_type = serializers.SlugRelatedField(read_only=True, slug_field='id')
    commercial_type = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = OdcPlan

class SearchResultSerializer(serializers.ModelSerializer):
    highschool = HighSchoolSerializer(read_only=True)
    form = serializers.SlugRelatedField(read_only=True, slug_field='id')
    commercial_type = serializers.SlugRelatedField(read_only=True, slug_field='id')
    contest_type = serializers.SlugRelatedField(read_only=True, slug_field='id')
    result_type = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = OdcResults
        fields = ('highschool','year','spec_id','contest_type','result_type','commercial_type','form',
            'total',
            'debug_url','debug_comment')
