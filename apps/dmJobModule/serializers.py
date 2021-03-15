from rest_framework import serializers
from .models import dmJobDescription


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = dmJobDescription
        fields = '__all__'
