from django.http import HttpResponse
from django.db.models import Count, Sum

from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response

from .serializers import HighSchoolSerializer, HighSchoolWithResultsSerializer, PlanSerializer, SpecSerializer, OdcResultsBinsSerializer, GroupSerializer, SpecGroupSerializer, SearchResultSerializer, OdcResultsSerializer, ShortOdcResultsSerializer
from .models import OdcInfoHighschool, OdcPlan, OdcInfoSpec, OdcInfoSpecGroup, OdcResults, OdcResultsBins
from .helpers import get_int_param, render


def index(request):
    ctx = {}
    return render(request, 'index.html')


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
    pagination_class = None

class SpecGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoSpecGroup.objects.all().prefetch_related('specs')
    serializer_class = SpecGroupSerializer
    pagination_class = None

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoSpecGroup.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


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
        query = self.queryset
        specs = None
        if self.request.query_params.get('specs') is not None:
            specs = self.request.query_params.get('specs').split(',')
            query = self.queryset.filter(spec_id__in=specs).values().annotate(count=Count('spec_id'))
        hs = query.values('highschool_id').annotate(count=Count('highschool_id')).values_list('highschool_id', flat=True)
        highschools = OdcInfoHighschool.objects.filter(id__in=hs).values('name', 'raiting', 'id', 'website')
        query = query.values('highschool_id', 'result_type_id').annotate(
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
        all_results = []
        for item in highschools:
            all_results.append(item)
        for item in query:
            for result in all_results:
                if result['id'] == item['highschool_id']:
                    result[item['result_type_id']] = item

        russian = get_int_param(self.request, 'russian')
        math = get_int_param(self.request, 'math')
        physics = get_int_param(self.request, 'physics')
        chemistry = get_int_param(self.request, 'chemistry')
        informatics = get_int_param(self.request, 'informatics')
        biology = get_int_param(self.request, 'biology')
        history = get_int_param(self.request, 'history')
        geography = get_int_param(self.request, 'geography')
        foreign_language = get_int_param(self.request, 'foreign_language')
        social_science = get_int_param(self.request, 'social_science')
        literature = get_int_param(self.request, 'literature')

        if specs is None:
            plans = OdcPlan.objects.filter(commercial_type='1', form='1')
        else:
            plans = OdcPlan.objects.filter(spec_id__in=specs, commercial_type='1', form='1')
        user_points = {}
        highschools = []
        for plan in plans:
            points = russian*plan.russian + math*plan.math + physics*plan.physics + \
                chemistry*plan.chemistry + informatics*plan.informatics + \
                biology*plan.biology + history*plan.history + geography*plan.geography + \
                foreign_language*plan.foreign_language + social_science*plan.social_science + \
                literature*plan.literature
            if plan.highschool_id not in user_points.keys():
                user_points[plan.highschool_id] = {}
            user_points[plan.highschool_id]['user_points'] = points
            user_points[plan.highschool_id]['all1'] = 0
            user_points[plan.highschool_id]['all2'] = 0
            user_points[plan.highschool_id]['good1'] = 0
            user_points[plan.highschool_id]['good2'] = 0
            highschools = user_points.keys()

        if specs is None:
            results = OdcResults.objects.filter(highschool_id__in=highschools,result_type_id__in=(1,2), commercial_type='1', form='1')
        else:
            results = OdcResults.objects.filter(spec_id__in=specs, highschool_id__in=highschools,result_type_id__in=(1,2), commercial_type='1', form='1')
        all_students = results.values('highschool_id', 'result_type').annotate(count=Count('result_type'))

        for a in all_students:
            user_points[a['highschool_id']]['all' + str(a['result_type'])] = a['count']
        for a in all_students:
            for i in range(1,3):
                all_students = results.filter(highschool_id=a['highschool_id'], total__lte=user_points[a['highschool_id']]['user_points'], result_type_id=i).values_list('total')
                user_points[a['highschool_id']]['good'+str(i)] = len(all_students)
                if user_points[a['highschool_id']]['all'+str(i)] > 0:
                    user_points[a['highschool_id']]['percent'+str(i)] = 100 * user_points[a['highschool_id']]['good'+str(i)] / user_points[a['highschool_id']]['all'+str(i)]
                else:
                    user_points[a['highschool_id']]['percent'+str(i)] = 0

        for a in all_results:
            a['points'] = {}
            if a['id'] in user_points.keys():
                a['points'] = user_points[a['id']]

        return Response({'results': all_results})


class Search2(generics.ListAPIView):
    queryset = OdcResultsBins.objects.all()
    serializer_class = OdcResultsBinsSerializer

    def list(self, request, *args, **kwargs):
        query = self.queryset

        specs = None
        if self.request.query_params.get('specs') is not None:
            specs = self.request.query_params.get('specs').split(',')
            query = self.queryset.filter(spec_id__in=specs)

        highschool_id = self.kwargs['highschool']
        highschools = OdcInfoHighschool.objects.filter(id=highschool_id).values()

        query = query.filter(highschool_id=highschool_id).values('spec_id', 'result_type').annotate(
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
        all_results = []
        for item in highschools:
            item['specs'] = {}
            for q in query:
                item['specs'][q['spec_id']] = {}
            all_results.append(item)
        for item in highschools:
            for q in query:
                item['specs'][q['spec_id']][q['result_type']] = q
            # if result['id'] == item['highschool_id']:
            #     result[item['result_type_id']] = item

        russian = get_int_param(self.request, 'russian')
        math = get_int_param(self.request, 'math')
        physics = get_int_param(self.request, 'physics')
        chemistry = get_int_param(self.request, 'chemistry')
        informatics = get_int_param(self.request, 'informatics')
        biology = get_int_param(self.request, 'biology')
        history = get_int_param(self.request, 'history')
        geography = get_int_param(self.request, 'geography')
        foreign_language = get_int_param(self.request, 'foreign_language')
        social_science = get_int_param(self.request, 'social_science')
        literature = get_int_param(self.request, 'literature')

        if specs is None:
            plans = OdcPlan.objects.filter(highschool_id=highschool_id, commercial_type='1', form='1')
        else:
            plans = OdcPlan.objects.filter(highschool_id=highschool_id, spec_id__in=specs, commercial_type='1', form='1')
        user_points = {}
        user_points['highschool'] = highschools
        user_points['specs'] = {}
        for plan in plans:
            points = russian*plan.russian + math*plan.math + physics*plan.physics + \
                chemistry*plan.chemistry + informatics*plan.informatics + \
                biology*plan.biology + history*plan.history + geography*plan.geography + \
                foreign_language*plan.foreign_language + social_science*plan.social_science + \
                literature*plan.literature
            if plan.spec_id not in user_points.keys():
                user_points['specs'][plan.spec_id] = {}
            user_points['specs'][plan.spec_id] = {}
            user_points['specs'][plan.spec_id]['user_points'] = points
            user_points['specs'][plan.spec_id]['all1'] = 0
            user_points['specs'][plan.spec_id]['all2'] = 0
            user_points['specs'][plan.spec_id]['good1'] = 0
            user_points['specs'][plan.spec_id]['good2'] = 0

        if specs is None:
            results = OdcResults.objects.filter(highschool_id=highschool_id,result_type_id__in=(1,2), commercial_type='1', form='1')
        else:
            results = OdcResults.objects.filter(spec_id__in=specs, highschool_id=highschool_id,result_type_id__in=(1,2), commercial_type='1', form='1')
        all_students = results.values('highschool_id', 'spec_id', 'result_type').annotate(count=Count('result_type'))
        for a in all_students:
            user_points['specs'][a['spec_id']]['all' + str(a['result_type'])] = a['count']
        for a in all_students:
            for i in range(1,3):
                all_students = results.filter(highschool_id=highschool_id,
                    spec_id=a['spec_id'],
                    total__lte=user_points['specs'][a['spec_id']]['user_points'],
                    result_type_id=i).values_list('total')
                user_points['specs'][a['spec_id']]['good'+str(i)] = len(all_students)
                if user_points['specs'][a['spec_id']]['all'+str(i)] > 0:
                    user_points['specs'][a['spec_id']]['percent'+str(i)] = 100 * user_points['specs'][a['spec_id']]['good'+str(i)] / user_points['specs'][a['spec_id']]['all'+str(i)]
                else:
                    user_points['specs'][a['spec_id']]['percent'+str(i)] = 0

        for a in all_results[0]['specs'].keys():
            spec = all_results[0]['specs'][a]
            spec['points'] = {}
            if a in user_points['specs'].keys():
                spec['points'] = user_points['specs'][a]

        return Response({'results': all_results})


class Search3(generics.ListAPIView):
    queryset = OdcResultsBins.objects.all()
    serializer_class = OdcResultsBinsSerializer

    def list(self, request, *args, **kwargs):
        query = self.queryset
        if self.request.query_params.get('specs') is not None:
            specs = self.request.query_params.get('specs').split(',')
            query = self.queryset.filter(spec_id__in=specs)

        russian = get_int_param(self.request, 'russian')
        math = get_int_param(self.request, 'math')
        physics = get_int_param(self.request, 'physics')
        chemistry = get_int_param(self.request, 'chemistry')
        informatics = get_int_param(self.request, 'informatics')
        biology = get_int_param(self.request, 'biology')
        history = get_int_param(self.request, 'history')
        geography = get_int_param(self.request, 'geography')
        foreign_language = get_int_param(self.request, 'foreign_language')
        social_science = get_int_param(self.request, 'social_science')
        literature = get_int_param(self.request, 'literature')

        plans = OdcPlan.objects.filter(spec_id__in=specs, commercial_type='1', form='1')
        user_points = {}
        highschools = []
        for plan in plans:
            points = russian*plan.russian + math*plan.math + physics*plan.physics + \
                chemistry*plan.chemistry + informatics*plan.informatics + \
                biology*plan.biology + history*plan.history + geography*plan.geography + \
                foreign_language*plan.foreign_language + social_science*plan.social_science + \
                literature*plan.literature
            if plan.highschool_id not in user_points.keys():
                user_points[plan.highschool_id] = {}
            user_points[plan.highschool_id]['user_points'] = points
            user_points[plan.highschool_id]['all1'] = 0
            user_points[plan.highschool_id]['all2'] = 0
            user_points[plan.highschool_id]['good1'] = 0
            user_points[plan.highschool_id]['good2'] = 0
            highschools = user_points.keys()

        results = OdcResults.objects.filter(spec_id__in=specs, highschool_id__in=highschools,result_type_id__in=(1,2))
        all_students = results.values('highschool_id', 'result_type').annotate(count=Count('result_type'))
        for a in all_students:
            user_points[a['highschool_id']]['all' + str(a['result_type'])] = a['count']
        for a in all_students:
            for i in range(1,3):
                all_students = results.filter(highschool_id=a['highschool_id'],
                    total__lte=user_points[a['highschool_id']]['user_points'],
                    result_type_id=i).values_list('total')
                user_points[a['highschool_id']]['good'+str(i)] = len(all_students)
                if user_points[a['highschool_id']]['all'+str(i)] > 0:
                    user_points[a['highschool_id']]['percent'+str(i)] = 100 * user_points[a['highschool_id']]['good'+str(i)] / user_points[a['highschool_id']]['all'+str(i)]
                else:
                    user_points[a['highschool_id']]['percent'+str(i)] = 0

        return Response({'results': user_points})


class Search4(generics.ListAPIView):
    queryset = OdcResultsBins.objects.all()
    serializer_class = OdcResultsBinsSerializer

    def list(self, request, *args, **kwargs):
        query = self.queryset
        if self.request.query_params.get('specs') is not None:
            specs = self.request.query_params.get('specs').split(',')
            query = self.queryset.filter(spec_id__in=specs)
            
        highschool_id = self.kwargs['highschool']
        highschools = OdcInfoHighschool.objects.filter(id=highschool_id).values()

        russian = get_int_param(self.request, 'russian')
        math = get_int_param(self.request, 'math')
        physics = get_int_param(self.request, 'physics')
        chemistry = get_int_param(self.request, 'chemistry')
        informatics = get_int_param(self.request, 'informatics')
        biology = get_int_param(self.request, 'biology')
        history = get_int_param(self.request, 'history')
        geography = get_int_param(self.request, 'geography')
        foreign_language = get_int_param(self.request, 'foreign_language')
        social_science = get_int_param(self.request, 'social_science')
        literature = get_int_param(self.request, 'literature')

        plans = OdcPlan.objects.filter(highschool_id=highschool_id, spec_id__in=specs, commercial_type='1', form='1')
        user_points = {}
        user_points['highschool'] = highschools
        user_points['specs'] = {}
        for plan in plans:
            points = russian*plan.russian + math*plan.math + physics*plan.physics + \
                chemistry*plan.chemistry + informatics*plan.informatics + \
                biology*plan.biology + history*plan.history + geography*plan.geography + \
                foreign_language*plan.foreign_language + social_science*plan.social_science + \
                literature*plan.literature
            if plan.spec_id not in user_points.keys():
                user_points['specs'][plan.spec_id] = {}
            user_points['specs'][plan.spec_id] = {}
            user_points['specs'][plan.spec_id]['user_points'] = points
            user_points['specs'][plan.spec_id]['all1'] = 0
            user_points['specs'][plan.spec_id]['all2'] = 0
            user_points['specs'][plan.spec_id]['good1'] = 0
            user_points['specs'][plan.spec_id]['good2'] = 0

        results = OdcResults.objects.filter(spec_id__in=specs, highschool_id=highschool_id,result_type_id__in=(1,2))
        all_students = results.values('highschool_id', 'spec_id', 'result_type').annotate(count=Count('result_type'))
        for a in all_students:
            user_points['specs'][a['spec_id']]['all' + str(a['result_type'])] = a['count']
        for a in all_students:
            for i in range(1,3):
                all_students = results.filter(highschool_id=highschool_id,
                    spec_id=a['spec_id'],
                    total__lte=user_points['specs'][a['spec_id']]['user_points'],
                    result_type_id=i).values_list('total')
                user_points['specs'][a['spec_id']]['good'+str(i)] = len(all_students)
                if user_points['specs'][a['spec_id']]['all'+str(i)] > 0:
                    user_points['specs'][a['spec_id']]['percent'+str(i)] = 100 * user_points['specs'][a['spec_id']]['good'+str(i)] / user_points['specs'][a['spec_id']]['all'+str(i)]
                else:
                    user_points['specs'][a['spec_id']]['percent'+str(i)] = 0

        return Response({'results': user_points})