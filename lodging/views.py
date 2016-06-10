from rest_framework.decorators import detail_route
from lodging.models import Lodging
from lodging.serializers import LodgingSerializer
from rest_framework import routers, serializers, viewsets


# Create your views here.
class LodgingViewSet(viewsets.ModelViewSet):
    queryset = Lodging.objects.all()
    serializer_class = LodgingSerializer
