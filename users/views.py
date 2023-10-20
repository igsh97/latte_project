from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import (
    Userserializer,
)
from .models import User

# Create your views here.
class UserView(APIView):
    def get(self,request):
        return Response(Userserializer(request.user).data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"},status=status.HTTP_400_BAD_REQUEST)
        

    
    
