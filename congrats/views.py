import requests
import json
import django_filters
import datetime as d

from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from congrats.models import CustomUser
from congrats.serializers import UsersSerializer
from celery import shared_task

from src import main


class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    


class BirthdayUsers(APIView):
    @swagger_auto_schema(responses={200: UsersSerializer(many=True)})
    def get(self, request):
        # time_threshold = datetime.now(timezone.utc)
        # b_users = CustomUser.objects.filter(date_created__gt=time_threshold)
        # serializer = UsersSerializer(b_users, many=True, read_only=True)
        today = d.datetime.today()
        b_users = CustomUser.objects.filter(date_of_birth_day__date=today)
        serializer = UsersSerializer(b_users, many=True)
        return Response(serializer.data)


class CongrateUsers(APIView):
    @swagger_auto_schema(responses={200: UsersSerializer(many=True)})
    def get(self, request):
        today = d.datetime.today()
        b_users = CustomUser.objects.filter(date_of_birth_day__date=today)
        serializer = UsersSerializer(b_users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: UsersSerializer(many=True)})    
    @shared_task
    def post(self, request):
        today = d.datetime.today()
        b_users = CustomUser.objects.filter(date_of_birth_day__date=today)
        serializer = UsersSerializer(b_users, many=True)
            
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

# def birthday_sms_send():
#     today = d.datetime.today()
#     b_users = CustomUser.objects.filter(date_of_birth_day__date=today)
#     for user in b_users:
#         user_token = main.sms_login()
#         user_sms_send = main.sms_send()
    







