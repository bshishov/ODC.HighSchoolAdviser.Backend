from django.http import HttpResponse
from django.db.models import Count

from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response

from .serializers import HighSchoolSerializer, HighSchoolWithResultsSerializer, PlanSerializer, SpecSerializer, GroupSerializer, SpecGroupSerializer, SearchResultSerializer, OdcResultsSerializer, ShortOdcResultsSerializer
from .models import OdcInfoHighschool, OdcPlan, OdcInfoSpec, OdcInfoSpecGroup, OdcResults

def index(request):
    return HttpResponse("Welcome to API")


# highschools

class HighSchoolsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoHighschool.objects.all()
    serializer_class = HighSchoolSerializer

class HighSchoolsWithResultsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoHighschool.objects.all()
    serializer_class = HighSchoolWithResultsSerializer

class HighSchoolsWithResultsBySpecView(generics.ListAPIView):
    serializer_class = ShortOdcResultsSerializer
    pagination_class = None

    def get_queryset(self):
        highschool_id = self.kwargs['highschool_id']
        spec_id = self.kwargs['spec_id']
        queryset = OdcResults.objects.select_related().filter(highschool_id=highschool_id, spec_id=spec_id)
        return queryset

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'results': [item['total'] for item in serializer.data]})


# specs and groups

class SpecViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoSpec.objects.all()
    serializer_class = SpecSerializer

class SpecGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoSpecGroup.objects.all()
    serializer_class = SpecGroupSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoSpecGroup.objects.all()
    serializer_class = GroupSerializer


# results

class OdcResultsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcResults.objects.all()
    serializer_class = OdcResultsSerializer

class OdcResultsBySpecViewSet(generics.ListAPIView):
    queryset = OdcResults.objects.all()
    serializer_class = OdcResultsSerializer

    def get_queryset(self):
        spec_id = self.kwargs['spec_id']
        queryset = OdcResults.objects.all(spec_id=spec_id)
        return queryset


# others

class PlanSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcPlan.objects.all()
    serializer_class = PlanSerializer

class PlansByGroupList(generics.ListAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_set = OdcInfoSpec.objects.filter(group_id=group_id).values_list('id', flat=True)
        return OdcPlan.objects.filter(spec_id__in=group_set)

class PlansBySpecList(generics.ListAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        spec_id = self.kwargs['spec_id']
        return OdcPlan.objects.filter(spec_id=spec_id)


# searches

class SearchList(generics.ListAPIView):
    queryset = OdcResults.objects.all()
    serializer_class = SearchResultSerializer

    def get_queryset(self):
        summ = self.request.query_params['sum']
        spec_id = self.kwargs['spec_id']
        query = OdcResults.objects.all()
        query = query.filter(form_id=1, commercial_type_id=1, spec_id=spec_id)
        query = query.filter(result_type_id__in=(1,2))
        return query

class SearchList1(generics.ListAPIView):
    queryset = OdcPlan.objects.all()
    serializer_class = SearchResultSerializer

    def get_queryset(self):
        spec_id = self.kwargs['spec_id']
        query = OdcPlan.objects.all()
        query = query.filter(form_id=1, commercial_type_id=1, spec_id=spec_id)
        query = query.filter(result_type_id=1)
        return query
