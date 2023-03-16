from rest_framework import serializers
from api.models import *

class DoctorSerializer(serializers.ModelSerializer):
    class Meta():
        model = Doctor
        fields = '__all__'
class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = ('file', 'timestamp')

class PatientUserSerializer(serializers.ModelSerializer):
    class Meta():
        model = PatientUser
        fields = '__all__'

class PatientUserChatsSerializer(serializers.ModelSerializer):
    class Meta():
        model = PatientUserChats
        fields = '__all__'
        
class PatientUserChatMessagesSerializer(serializers.ModelSerializer):
    class Meta():
        model = PatientUserChatMessages
        fields = '__all__'