from django.http import HttpResponse

from rest_framework import viewsets, generics

from serializers import HighSchoolSerializer, OdcPlanSerializer
from models import OdcInfoHighschool, OdcPlan, OdcInfoSpec

def index(request):
    return HttpResponse("ok")

class HighSchoolsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcInfoHighschool.objects.all()
    serializer_class = HighSchoolSerializer

class OdcPlanSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdcPlan.objects.all()
    serializer_class = OdcPlanSerializer

class SpecsList(generics.ListAPIView):
    queryset = OdcPlan.objects.all()
    serializer_class = OdcPlanSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_set = OdcInfoSpec.objects.filter(group_id=group_id).values_list('id', flat=True)
        print(group_set)
        return OdcPlan.objects.filter(spec_id__in=group_set)