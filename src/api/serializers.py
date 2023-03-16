from rest_framework import serializers
from api.models import *

class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = ('file', 'timestamp')

