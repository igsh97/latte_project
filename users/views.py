from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import (
    UserCreateSerializer,
    UserInfoSerializer,
    ChangePasswordSerializer,
)
import requests
import base64
import io
from django.core.files.images import ImageFile
from .models import User,Temp_Profile_Image

# Create your views here.
class UserView(APIView):
    # permission_classes = [AllowAny]

    # 프로필 정보
    def get(self, request, user_id, format=None):
        user = get_object_or_404(get_user_model(), pk=user_id)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data['profile_img'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        if not request.user.is_authenticated:
            Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserCreateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        password = request.data.get("password", "")
        auth_user = authenticate(username=user.username, password=password)
        if auth_user:
            auth_user.delete()
            return Response({"message": "회원 탈퇴 완료."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "비밀번호 불일치."}, status=status.HTTP_403_FORBIDDEN)

class UserListView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserInfoSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ChangePasswordView(UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
    
class ChangeProfileImageView(APIView):
    def get(self,request):
        target=request.data['target']
        image_route=request.FILES['image_route']
        url = "https://www.ailabapi.com/api/portrait/effects/face-attribute-editing"
        #print(target)
        #print(image_route)
        payload={'action_type': 'V2_AGE',
            'target':target,
            'quality_control': 'NONE',
            #'face_location': ''
        }
        files=[
            ('image',('file',image_route,'application/octet-stream'))
        ]
        headers = {
            'ailabapi-api-key': 'your api key'
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        #print(response.text)
        data=response.json()
        image_data = data['result']['image']
        imgdata = base64.b64decode(str(image_data))
        image = ImageFile(io.BytesIO(imgdata), name='foo.jpg')  # << the answer!
        changed_image = Temp_Profile_Image.objects.create(image_file=image)
        changed_image_url=changed_image.image_file.url
        # changed_image_path=changed_image.image_file.path
        print(changed_image_url)
        # print(changed_image_path)
        return Response({"changed_image_url": changed_image_url},status=status.HTTP_200_OK)
