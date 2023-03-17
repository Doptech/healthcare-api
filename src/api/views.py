from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import *
from config import BASE_PATH
from decouple import config

import datetime
import requests
import json
import uuid
import os

DEBUG = config('DEBUG', cast=bool)

# Create your views here.

class AddFileAPI(APIView):
    
    @csrf_exempt
    def post(self, request, meeting_id):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            pathOfFile = file_serializer.data['file']
            newPath = BASE_PATH + '/' + pathOfFile
            
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    
class OnboardingAPI(APIView): 
    
    @csrf_exempt
    def get(self, request):
        # main_queryset = PatientUser.objects.filter(user_id=)
        #main_queryset_serializer = Summary_Serializers(main_queryset)
        #content = main_queryset_serializer.data
        
        res = "hello"
        return Response(res,status=status.HTTP_200_OK)
    
    @csrf_exempt
    def post(self, request):
        data = (JSONParser().parse(request))['data']
        if data['user_type'] == 'patient':
            PatientUser.objects.create(user_id = data['user_id'],
                                                    name = data['name'],
                                                    birth_date = data['birth_date'],
                                                    age = data['age'],
                                                    sex = data['sex'],
                                                    blood_type = data['blood_type'],
                                                    height = data['height'],
                                                    weight = data['weight'],
                                                    alegries = data['alegries'].join(','),
                                                    known_disease = data['known_disease'].join(','))
        else:
            Doctor.objects.create(docter_user_id = data['user_id'],
                                  name = data['name'],
                                  studies = data['studies'],
                                  specality = data['specality'],
                                  hospital = data['hospital'],
                                  yrs_of_exp = data['yrs_of_exp'],
                                  qr_id = str(uuid.uuid4()))
                    
        return Response({"data":
                        {"message": data['user_type'],
                        "user_id":data['user_type']}
                        },status=status.HTTP_200_OK)
    
class DashboardAPI(APIView): 
    
    @csrf_exempt
    def get(self, request, user_id):
        
        # check if user is doctor or patient
        is_doctor = Doctor.objects.filter(docter_user_id=user_id).exists()
        if is_doctor:
            main_queryset = Doctor.objects.filter(docter_user_id=user_id)
            main_queryset_serializer = DoctorSerializer(main_queryset, many=True)
            
            # check from patient how many patients are assigned to this doctor
            main_queryset_patient = PatientUser.objects.filter(doctor_id=user_id)
            main_queryset_patient_serializer = PatientUserSerializer(main_queryset_patient, many=True)
            
            # check how many alerts are there for this doctor in 24 hours
            alert_query_set = PatientUserChatMessages.objects.filter(doctor_id=user_id, timestamp__gte=datetime.datetime.now()-datetime.timedelta(days=1))
            alert_query_set_serializer = PatientUserChatMessagesSerializer(alert_query_set, many=True)
            return Response({"data":{"user_data":main_queryset_serializer.data,
                                    "no_of_patient_assigened":len(main_queryset_patient),
                                    "no_of_alerts":len(alert_query_set),
                                    "alerts": alert_query_set_serializer.data,
                                    "patient":main_queryset_patient_serializer.data
                                    }},status=status.HTTP_200_OK)
        else:
            main_queryset = PatientUser.objects.filter(user_id=user_id)
            main_queryset_serializer = PatientUserSerializer(main_queryset)
            
            # Chats of the patient
            main_queryset_patient_chats = PatientUserChats.objects.filter(user_id=user_id)
            main_queryset_patient_chats_selizer = PatientUserChatsSerializer(main_queryset_patient_chats, many=True)
            res_chats = []
            for i in range(len(main_queryset_patient_chats_selizer.data)):
                main_queryset_patient_chats_messages = PatientUserChatMessages.objects.filter(chat_id=user_id).first()
                main_queryset_patient_chats_messages_serlizer = PatientUserChatMessagesSerializer(main_queryset_patient_chats_messages)
                res_chats.append(main_queryset_patient_chats_messages_serlizer.data)
                
            main_queryset_patient_chats_messages = PatientUserChatMessages.objects.filter(chat_id=user_id)
            main_queryset_patient_chats_messages_serlizer = PatientUserChatMessagesSerializer(main_queryset_patient_chats_messages, many=True)
            
            return Response({"data":{"user_data":main_queryset_serializer.data,"chat_data":main_queryset_patient_chats_messages_serlizer.data}})
            
        
class PatientUserInfo(APIView):
    
    @csrf_exempt
    def get(self, request):
        data = (JSONParser().parse(request))['data']
        main_queryset = PatientUser.objects.all()
        main_queryset_serializer = PatientUserSerializer(main_queryset)
        return Response({"data":main_queryset_serializer.data},status=status.HTTP_200_OK)
        
class PatientUserInfoByID(APIView):
    
    @csrf_exempt
    def get(self, request, patient_id):
        main_queryset = PatientUser.objects.filter(user_id=patient_id)
        main_queryset_serializer = PatientUserSerializer(main_queryset)
        return Response({"data":main_queryset_serializer.data},status=status.HTTP_200_OK)
    
class DoctorAPI(APIView):
    
    @csrf_exempt
    def post(self, request):
        data = (JSONParser().parse(request))['data']
        main_queryset = Doctor.objects.filter(docter_user_id=data['user_id'])
        main_queryset_serializer = DoctorSerializer(main_queryset, many=True)
        return Response({"data":main_queryset_serializer.data},status=status.HTTP_200_OK)
    
class DoctorAlerts(APIView):
    
    @csrf_exempt
    def get(self, request):
        main_queryset = PatientUserChatMessages.objects.filter(alert = True,timestamp__gte=datetime.datetime.now()-datetime.timedelta(days=1)).all()
        main_queryset_data = PatientUserChatMessagesSerializer(main_queryset, many=True)
        return Response({"data":main_queryset_data.data},status=status.HTTP_200_OK)
        
class UserHomePage(APIView):
    
    @csrf_exempt
    def get(self, request, user_id):
        main_queryset_chats = PatientUserChats.objects.filter(user_id = user_id).all()
        main_queryset_chats_serlizer = PatientUserChatsSerializer(main_queryset_chats)
        
        main_queryset_PatientUser = PatientUser.objects.filter(user_id = user_id)
        main_queryset_PatientUser_serlizer = PatientUserSerializer(main_queryset_PatientUser)
        return Response({"data":{"chat_history": main_queryset_chats_serlizer.data, 
                                 "user_info": main_queryset_PatientUser_serlizer.data}},
                                status=status.HTTP_200_OK)