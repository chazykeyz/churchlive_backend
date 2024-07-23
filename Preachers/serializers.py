from rest_framework import serializers
from .models import *


class PreacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preacher
        fields = "__all__"
