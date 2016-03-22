from django.http import HttpResponse
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response

from .serializers import HighSchoolSerializer, HighSchoolWithResultsSerializer, PlanSerializer, SpecSerializer, OdcResultsBinsSerializer, GroupSerializer, SpecGroupSerializer, SearchResultSerializer, OdcResultsSerializer, ShortOdcResultsSerializer
from .models import OdcInfoHighschool, OdcPlan, OdcInfoSpec, OdcInfoSpecGroup, OdcResults, OdcResultsBins, UserInfo, OdcPlanType, OdcInfoCommercialType, OdcInfoForm
from .helpers import *


# own views (not rest api)


# index page
def index(request):
    ctx = {}
    return render(request, 'index.html')

# one highschool page
def highschool(request, id):
    ctx = {}
    ctx['highschool'] = OdcInfoHighschool.objects.get(id=id)
    ctx['types'] = OdcPlanType.objects.all()
    ctx['selected_commercial_type'] = commercial = int(request.GET.get('commercial_type', 1))
    ctx['selected_plan_type'] = plan_type = int(request.GET.get('plan_type', 0))
    ctx['selected_form'] = form = int(request.GET.get('form', 1))

    ctx['selected_commercial_type_data'] = {}
    ctx['selected_plan_type_data'] = {}
    ctx['selected_form_data'] = {}

    user = request.user
    plans = OdcPlan.objects.select_related().filter(highschool_id=id)
    for plan in plans:
        ctx['selected_commercial_type_data'][plan.commercial_type.id] = plan.commercial_type
        ctx['selected_plan_type_data'][plan.plan_type.id] = plan.plan_type
        ctx['selected_form_data'][plan.form.id] = plan.form

    plans = plans.filter(commercial_type=commercial, plan_type=plan_type, form=form).order_by('spec_id')
    ctx['specs'] = []
    for plan in plans:
        p = {}
        p['plan'] = plan
        unit = get_user_units(request)
        p['user_points'] = count_user_points(unit, plan)
        p['all1'] = 0
        p['all2'] = 0
        p['good1'] = 0
        p['good2'] = 0

        results = OdcResults.objects.filter(spec_id=p['plan'].spec.id, highschool_id=id, result_type_id__in=(1,2), commercial_type=commercial, form=form)
        all_students = results.values('highschool_id', 'spec_id', 'result_type').annotate(count=Count('result_type'))
        for a in all_students:
            p['all' + str(a['result_type'])] = a['count']
        for a in all_students:
            for i in range(1,3):
                all_students = results.filter(highschool_id=id, spec_id = a['spec_id'], total__lte = p['user_points'], result_type_id=i).values_list('total')
                p['good'+str(i)] = len(all_students)
                if p['all'+str(i)] > 0:
                    p['percent'+str(i)] = 100 * p['good'+str(i)] / p['all'+str(i)]
                else:
                    p['percent'+str(i)] = 0

        ctx['specs'].append(p)

    return render(request, 'highschool.html', ctx)

# search in highschools
def highschools_search(request):
    ctx = {}
    unit = set_user_units(request)

    specs = request.session['specs']
    if specs is not None and not specs == []:
        plans = OdcPlan.objects.select_related().filter(spec_id__in=specs, commercial_type=1, form=1)
    else:
        plans = OdcPlan.objects.select_related().filter(commercial_type=1, form=1)
    highschools_ids = plans.values('highschool_id').annotate(count=Count('highschool_id')).values_list('highschool_id', flat=True)
    highschools_info = OdcInfoHighschool.objects.filter(id__in=highschools_ids).values('name', 'raiting', 'id', 'website')
    if specs is None or specs == []:
        results = OdcResults.objects.filter(highschool_id__in=highschools_ids,result_type_id__in=(1,2), commercial_type=1, form=1)
    else:
        results = OdcResults.objects.filter(spec_id__in=specs, highschool_id__in=highschools_ids,result_type_id__in=(1,2), commercial_type=1, form=1)
    all_results = results.values('highschool_id', 'result_type', 'spec_id').annotate(count=Count('result_type'))

    final_results = {}
    points = {}

    for highschool in highschools_info:
        final_results[highschool['id']] = highschool
        final_results[highschool['id']]['specs'] = {}
        points = {}
        points['all1'] = 0
        points['all2'] = 0
        points['good1'] = 0
        points['good2'] = 0
        points['planned'] = 0
        points['min1'] = plans[0].min_sum_1
        points['min2'] = plans[0].min_sum_2
        final_results[highschool['id']]['points'] = points

    # считаем данные для ВУЗа в целом
    for plan in plans:
        spec_points = {}
        spec_points['plan'] = plan
        spec_points['all1'] = 0
        spec_points['all2'] = 0
        spec_points['good1'] = 0
        spec_points['good2'] = 0
        spec_points['user_points'] = count_user_points(unit, plan)

        final_results[plan.highschool_id]['points']['planned'] += plan.planned
        if plan.min_sum_1 and plan.min_sum_1 < final_results[plan.highschool_id]['points']['min1']:
            final_results[plan.highschool_id]['points']['min1'] = plan.min_sum_1
        if plan.min_sum_2 and plan.min_sum_2 < final_results[plan.highschool_id]['points']['min2']:
            final_results[plan.highschool_id]['points']['min2'] = plan.min_sum_2

        for a in all_results:
            i = str(a['result_type'])
            if not a['spec_id'] == plan.spec_id or not a['highschool_id'] == plan.highschool_id:
                continue
            spec_points['all' + i] = a['count']
            final_results[plan.highschool_id]['points']['all'+i] += a['count']
            count_good = results.filter(highschool_id=plan.highschool_id, spec_id=plan.spec_id, total__lte=spec_points['user_points'], result_type_id=a['result_type']).count()
            spec_points['good' + i] = count_good
            final_results[plan.highschool_id]['points']['good'+i] += count_good
            # процент для специальности
            if spec_points['all'+i] > 0:
                spec_points['percent'+i] = 100 * spec_points['good'+i] / spec_points['all'+i]
            else:
                spec_points['percent'+i] = 0
            # процент для вуза в целом
            if final_results[plan.highschool_id]['points']['all'+i] > 0:
                final_results[plan.highschool_id]['points']['percent'+i] = 100 * final_results[plan.highschool_id]['points']['good'+i] / final_results[plan.highschool_id]['points']['all'+i]
            else:
                final_results[plan.highschool_id]['points']['percent'+i] = 0

        # запоминаем результат
        final_results[plan.highschool_id]['specs'][plan.spec_id] = spec_points

    ctx['results'] = final_results
    return render(request, 'highschools_search.html', ctx)

# particular info for one cpec for exact highschool
def plan(request, plan_id):
    ctx = {}
    unit = get_user_units(request)

    plan = OdcPlan.objects.select_related().get(id=plan_id)
    hs_id = plan.highschool_id
    spec_id = plan.spec_id
    highschool_info = OdcInfoHighschool.objects.get(id=hs_id)
    results = OdcResults.objects.filter(spec_id=spec_id, highschool_id=hs_id,result_type_id__in=(1,2), commercial_type=plan.commercial_type, form=plan.form)
    all_results = results.values('highschool_id', 'result_type', 'spec_id').annotate(count=Count('result_type'))
    bins = OdcResultsBins.objects.filter(highschool_id=hs_id, spec_id=spec_id).values().annotate(count=Count('spec_id'))

    sums = bins.values('highschool_id', 'result_type_id').annotate(
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

    ctx = {}
    ctx['highschool'] = highschool_info
    ctx['plan'] = plan
    ctx['sums'] = {}
    for sum in sums:
        ctx['sums'][sum['result_type_id']] = sum

    # считаем данные для ВУЗа в целом
    spec_points = {}
    spec_points['all1'] = 0
    spec_points['all2'] = 0
    spec_points['good1'] = 0
    spec_points['good2'] = 0
    spec_points['user_points'] = count_user_points(unit, plan)

    for r in all_results:
        spec_points['all' + str(r['result_type'])] = r['count']
    for i in range(1,3):
        count_good = results.filter(total__lte=spec_points['user_points'], result_type_id=i).count()
        spec_points['good'+str(i)] = count_good
        # процент для специальности
        if spec_points['all'+str(i)] > 0:
            spec_points['percent'+str(i)] = 100 * spec_points['good'+str(i)] / spec_points['all'+str(i)]
        else:
            spec_points['percent'+str(i)] = 0

    # запоминаем результат
    ctx['specs'] = spec_points

    return render(request, 'highschools_spec.html', ctx)

# страница отдельной специальности
def spec(request, spec_id):
    ctx = {}
    ctx['spec'] = OdcInfoSpec.objects.select_related().get(id=spec_id)

    plans = OdcPlan.objects.select_related().filter(spec_id=spec_id).order_by('-highschool__raiting')
    ctx['highschools'] = []
    for plan in plans:
        hs = None
        for item in ctx['highschools']:
            if item['highschool'].id == plan.highschool_id:
                hs = item
                break
        if hs is None:
            hs = {'highschool': plan.highschool, 'plans': []}
            ctx['highschools'].append(hs)
        hs['plans'].append(plan)

    return render(request, 'spec.html', ctx)

# все специальности по группам на одном страничке
def specs(request):
    ctx = {}
    ctx['groups'] = {}
    specs = OdcInfoSpec.objects.select_related().all()
    for spec in specs:
        ctx['groups'].setdefault(spec.group.id, {'group': spec.group, 'specs': []})
        ctx['groups'][spec.group.id]['specs'].append(spec)
    return render(request, 'specialities.html', ctx)

# рейтинг топ-100 ВУЗов
def rating(request):
    ctx = {}
    ctx['highschools'] = OdcInfoHighschool.objects.order_by('-raiting')[:100]
    return render(request, 'rating.html', ctx)

# добавление/удаление в избранное
@login_required
def add_highschool(request):
    fav = request.user.user_info.getfavhs()
    id = int(request.GET['id'])
    if id in fav:
        fav.remove(id)
    else:
        fav.append(id)
    request.user.user_info.setfavhs(fav)
    request.user.user_info.save()
    return HttpResponse('ok')

# добавление/удаление в избранное
@login_required
def add_plan(request):
    fav = request.user.user_info.getfavpl()
    id = int(request.GET['id'])
    if id in fav:
        fav.remove(id)
    else:
        fav.append(id)
    request.user.user_info.setfavpl(fav)
    request.user.user_info.save()
    return HttpResponse('ok')

# страница избранного
@require_login(url='core.views.signup')
def favourites(request):
    ctx = {}

    highschools = {}
    hs_ids = request.user.user_info.getfavhs()
    all_hs = OdcInfoHighschool.objects.filter(id__in=hs_ids).order_by('-raiting')

    unit = get_user_units(request)
    highschools = []

    for hs in all_hs:
        plans = OdcPlan.objects.filter(highschool_id=hs.id)
        results = OdcResults.objects.filter(highschool_id=hs)

        from django.db.models import Min, Sum
        highschool = {}
        highschool['highschool'] = hs
        highschool['all1'] = results.filter(result_type_id=1).count()
        highschool['all2'] = results.filter(result_type_id=2).count()
        highschool['good1'] = 0
        highschool['good2'] = 0
        highschool['min1'] = plans.aggregate(Min('min_sum_1'))['min_sum_1__min']
        highschool['min2'] = plans.aggregate(Min('min_sum_2'))['min_sum_2__min']
        highschool['planned'] = plans.aggregate(Sum('planned'))['planned__sum']

        for plan in plans:
            user_points = count_user_points(unit, plan)

            for i in range(1,3):
                highschool['good' + str(i)] += results.filter(spec_id=plan.spec_id, result_type_id=i, total__lte=user_points, commercial_type=plan.commercial_type_id, form=plan.form).count()

        # процент для вуза в целом
        for i in range(1,3):
            if highschool['all'+str(i)] > 0:
                highschool['percent'+str(i)] = 100 * highschool['good'+str(i)] / highschool['all'+str(i)]
            else:
                highschool['percent'+str(i)] = 0

        # запоминаем результат
        highschools.append(highschool)
    ctx['highschools'] = highschools

    pl_ids = request.user.user_info.getfavpl()
    plans = []
    for pl_id in pl_ids:
        pl = OdcPlan.objects.select_related().get(id=pl_id)
        results = OdcResults.objects.filter(highschool_id=pl.highschool_id, spec_id=pl.spec_id)

        plan = {}
        plan['plan'] = pl
        plan['all1'] = 0
        plan['all2'] = 0
        plan['good1'] = 0
        plan['good2'] = 0
        plan['user_points'] = count_user_points(unit, pl)

        for i in range(1,3):
            plan['all' + str(i)] = results.filter(result_type_id=i).count()
            plan['good'+str(i)] = results.filter(total__lte=plan['user_points'], result_type_id=i).count()
            # процент для специальности
            if plan['all'+str(i)] > 0:
                plan['percent'+str(i)] = 100 * plan['good'+str(i)] / plan['all'+str(i)]
            else:
                plan['percent'+str(i)] = 0

        # запоминаем результат
        plans.append(plan)
    ctx['plans'] = plans

    return render(request, 'favourites.html', ctx)

# функция под внутренние нужды
@login_required
def debug(request):
    ctx = {}
    return HttpResponse('ok')

    # считаем, что количество мест равно суммарному числу поступивших в первую и вторую волну
    # plans = OdcPlan.objects.all()
    # for plan in plans:
    #     res = OdcResults.objects.filter(spec_id=plan.spec_id, highschool_id=plan.highschool_id, result_type_id__in=(1,2), commercial_type=plan.commercial_type_id, form=plan.form).count()
    #     plan.planned = res
    #     plan.save()

    # очищаем, а затем заполняем новыми данными рейтинги вузов
    # points = {161:4.179, 165:4.151, 147:4.056, 901:4.038, 296:3.922, 313:3.749, 294:3.510, 1507:3.499, 219:3.426, 59:3.425, 1519:3.419, 177:3.289, 222:3.237, 234:3.074, 209:3.068, 247:2.812, 251:2.774, 131:2.734, 337:2.726, 170:2.511, 212:2.481, 295:2.420, 130:2.388, 1520:2.378, 45:2.364, 301:2.307, 213:2.301, 148:2.274, 223:2.272, 310:2.265, 319:2.171, 336:2.164, 60:2.117, 199:2.101, 197:2.093, 252:2.086, 4:2.049, 1527:2.037, 129:2.028, 144:2.008, 16:2.005, 132:1.965, 253:1.960, 127:1.897, 169:1.889, 3:1.887, 79:1.887, 236:1.872, 36:1.868, 17:1.841, 160:1.791, 258:1.787, 243:1.762, 271:1.746, 217:1.739, 293:1.735, 183:1.725, 302:1.718, 113:1.684, 242:1.641, 1544:1.618, 85:1.609, 108:1.606}
    # highschools = OdcInfoHighschool.objects.all()
    # for hs in highschools:
    #     hs.raiting = None
    #     hs.save()
    # highschools = OdcInfoHighschool.objects.filter(id__in = points.keys())
    # for hs in highschools:
    #     hs.raiting = points[hs.id]
    #     hs.save()

    # ctx['test'] = [str(hs.id) + '|' + hs.website for hs in OdcInfoHighschool.objects.all()]

    return render(request, 'highschools_search.html', ctx)


# rest api

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

def login(request):
    ctx = {}
    from .forms import RegistrationForm
    ctx['form'] = RegistrationForm
    return render(request, 'login.html', ctx)

@unauthenticated_only(url='core.views.index')
def signup(request):
    ctx = {}
    from .forms import RegistrationForm
    ctx['form'] = RegistrationForm
    return render(request, 'signup.html', ctx)

@require_post(url='core.views.index')
@unauthenticated_only(url='core.views.index')
def do_login(request):
    username = request.POST['email']
    password = request.POST['password']
    from django.contrib.auth import authenticate, login
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            put_user_info_into_session(request)
            return redirect('core.views.index')
        else:
            return redirect(reverse('core.views.login') + '?error=inactive')
    else:
        return redirect(reverse('core.views.login') + '?error=incorrect')

@require_post(url='core.views.index')
@unauthenticated_only(url='core.views.index')
def do_register(request):
    ctx = {}
    email = request.POST['email']
    password = request.POST['password']
    if not email or not password:
        return redirect(reverse('core.views.signup') + '?error=fields_empty')
    if len(password) < 6:
        return redirect(reverse('core.views.signup') + '?error=password_short')
    try:
        User.objects.get(email = email)
        return redirect(reverse('core.views.signup') + '?error=email_used')
    except:
        user = User.objects.create_user(email, email, password)
        user.user_info = UserInfo(user=user)
        user.user_info.save()
        user.is_active = True
        user.save()
        from django.contrib.auth import authenticate, login
        user = authenticate(username=email, password=password)
        login(request, user)
        ctx.update({'response': 'success', 'message': u'You are successfully registered you user'})
    return redirect('core.views.index')

@require_login(url='core.views.index')
def do_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('core.views.index')