from rest_framework import serializers

from models import OdcInfoHighschool, OdcPlan, OdcInfoSpec, OdcInfoSpecGroup, OdcResults

class HighSchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OdcInfoHighschool
        fields = ('id', 'website', 'name')

class PlanSerializer(serializers.ModelSerializer):
    highschool = serializers.SlugRelatedField(read_only=True, slug_field='id')
    # spec = serializers.SlugRelatedField(read_only=True, slug_field='id')
    form = serializers.SlugRelatedField(read_only=True, slug_field='id')
    plan_type = serializers.SlugRelatedField(read_only=True, slug_field='id')
    commercial_type = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = OdcPlan

class SpecSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OdcInfoSpec
        fields = ('id', 'group_id', 'name')

class SpecGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OdcInfoSpecGroup
        fields = ('id', 'name')

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