from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

# Create your views here.


class PreacherView(ModelViewSet):
    queryset = Preacher.objects.all()
    serializer_class = PreacherSerializer
