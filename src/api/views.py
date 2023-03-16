from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import FileSerializer
from config import BASE_PATH

import datetime
import requests
import json
import os

# Create your views here.

class AddMeetingFileAPI(APIView):
    
    @csrf_exempt
    def post(self, request, meeting_id):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            pathOfFile = file_serializer.data['file']
            newPath = BASE_PATH + '/' + pathOfFile
            
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)