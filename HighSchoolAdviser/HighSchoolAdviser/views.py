from django.http import HttpResponse
from django.db.models import Count, Sum

from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response

from .serializers import HighSchoolSerializer, HighSchoolWithResultsSerializer, PlanSerializer, SpecSerializer, OdcResultsBinsSerializer, GroupSerializer, SpecGroupSerializer, SearchResultSerializer, OdcResultsSerializer, ShortOdcResultsSerializer
from .models import OdcInfoHighschool, OdcPlan, OdcInfoSpec, OdcInfoSpecGroup, OdcResults, OdcResultsBins

def index(request):
    return HttpResponse("Welcome to API")


# highschools

class HighSchoolsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoHighschool.objects.all()
    serializer_class = HighSchoolSerializer

class HighSchoolsWithResultsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoHighschool.objects.all().prefetch_related('results')
    serializer_class = HighSchoolWithResultsSerializer

class HighSchoolsWithResultsBySpecView(generics.ListAPIView):
    serializer_class = ShortOdcResultsSerializer
    pagination_class = None

    def get_queryset(self):
        highschool_id = self.kwargs['highschool_id']
        spec_id = self.kwargs['spec_id']
        queryset = OdcResults.objects.filter(highschool_id=highschool_id, spec_id=spec_id).select_related()
        return queryset

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        results = {}
        for item in serializer.data:
            if not item['result_type'] in results.keys():
                results[item['result_type']] = []
            results[item['result_type']].append(item['total'])
        return Response({'results': results})


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


class Search1(generics.ListAPIView):
    queryset = OdcResultsBins.objects.all()
    serializer_class = OdcResultsBinsSerializer

    def list(self, request, *args, **kwargs):
        # self.object_list = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(self.object_list, many=True)
        specs = self.request.query_params.get('specs').split(',')
        hs = self.queryset.values('highschool_id').annotate(count=Count('highschool_id')).values_list('highschool_id', flat=True)
        highschools = OdcInfoHighschool.objects.filter(id__in=hs).values('name', 'raiting', 'id')
        query = self.queryset.filter(spec_id__in=specs).values('highschool_id', 'result_type').annotate(
            below_150=Sum('below_150'),
            below_160=Sum('below_160'),
            below_170=Sum('below_170'),
            below_180=Sum('below_180'),
            below_190=Sum('below_190'),
            below_200=Sum('below_200'),
            below_210=Sum('below_210'),
            below_220=Sum('below_220'),
            below_230=Sum('below_230'),
            below_240=Sum('below_240'),
            below_250=Sum('below_250'),
            below_260=Sum('below_260'),
            below_270=Sum('below_270'),
            below_280=Sum('below_280'),
            below_290=Sum('below_290'),
            below_300=Sum('below_300')).values()
        results = []
        for item in highschools:
            results.append(item)
        for item in query:
            for result in results:
                if result['id'] == item['highschool_id']:
                    result[item['result_type_id']] = item
        return Response({'results': results})


class Search2(generics.ListAPIView):
    queryset = OdcResultsBins.objects.all()
    serializer_class = OdcResultsBinsSerializer

    def list(self, request, *args, **kwargs):
        # self.object_list = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(self.object_list, many=True)
        specs = self.request.query_params.get('specs').split(',')
        highschool_id = self.kwargs['highschool']
        highschools = OdcInfoHighschool.objects.filter(id=highschool_id).values()
        query = self.queryset.filter(spec_id__in=specs, highschool_id=highschool_id).values('spec_id', 'result_type').annotate(
            below_150=Sum('below_150'),
            below_160=Sum('below_160'),
            below_170=Sum('below_170'),
            below_180=Sum('below_180'),
            below_190=Sum('below_190'),
            below_200=Sum('below_200'),
            below_210=Sum('below_210'),
            below_220=Sum('below_220'),
            below_230=Sum('below_230'),
            below_240=Sum('below_240'),
            below_250=Sum('below_250'),
            below_260=Sum('below_260'),
            below_270=Sum('below_270'),
            below_280=Sum('below_280'),
            below_290=Sum('below_290'),
            below_300=Sum('below_300'))
        results = []
        for item in highschools:
            item['specs'] = {}
            for q in query:
                item['specs'][q['spec_id']] = {}
            results.append(item)
        for item in highschools:
            for q in query:
                item['specs'][q['spec_id']][q['result_type']] = q
        #     if result['id'] == item['highschool_id']:
        #         result[item['result_type_id']] = item
        return Response({'results': results})