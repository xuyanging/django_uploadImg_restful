
#encoding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from . import mySerializers as serializers
from upload_test import models
from django.http import HttpResponse
import json
from rest_framework  import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import *
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView


class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)



class imageAPI(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = models.userHeadImage.objects.all()
    serializer_class = serializers.ImageSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        user_id = data['user_id']
        m = models.userHeadImage.objects.filter(uploaded_by_id__exact=user_id)
        for model in m:
            model.image.delete()
            print(model.image)
            model.delete()
        try:
            self.create(request, *args, **kwargs)
            image = models.userHeadImage.objects.get(uploaded_by_id__exact=user_id)
            return JSONResponse({'result':serializers.ImageSerializer(image).data,'desc':'upload success'}, status=HTTP_200_OK)
        except:
            return JSONResponse({'desc':'upload faile'},status=HTTP_400_BAD_REQUEST)

class UploadViewSet(imageAPI):
    queryset = models.userHeadImage.objects.all()
    serializer_class = serializers.ImageSerializer
    parser_classes = (MultiPartParser, )    

#用于登录

class UserLoginAPIView(APIView):
   queryset = models.haveFunUser.objects.all()
   serializer_class = serializers.UserSerializer
   permission_classes = (permissions.AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('name')
       password = data.get('passwd')
       if not models.haveFunUser.objects.filter(name__exact=username):
           return JSONResponse({'desc':'用户名不存在'},status=HTTP_200_OK,)
       user = models.haveFunUser.objects.get(name__exact=username)
       if user.passwd == password:
           serializer = serializers.UserSerializer(user)
           new_data = serializer.data
           print(new_data)
           # 记忆已登录用户
           self.request.session['user_id'] = user.user_id
           self.request.session['user_name'] = user.name
           return JSONResponse({'result':serializer.data,'desc':'登陆成功'}, status=HTTP_200_OK)
       return JSONResponse( {'desc':'password error'},status=HTTP_200_OK)

#用于注册

class UserRegisterAPIView(APIView):
   queryset = models.haveFunUser.objects.all()
   serializer_class = serializers.UserSerializer
   permission_classes = (permissions.AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('name')
       phone = data.get('phone')
       print('registrt--->',data)
       dic = {}
       if models.haveFunUser.objects.filter(name__exact=username):
           return JSONResponse({'desc':'用户名已存在'},status=HTTP_400_BAD_REQUEST)
       if models.haveFunUser.objects.filter(phone__exact=phone):
           return JSONResponse({'desc':'手机号码已存在'},status=HTTP_400_BAD_REQUEST)
       serializer = serializers.UserSerializer(data=data)
       if serializer.is_valid(raise_exception=True):
           serializer.save()
           dic['result'] = serializer.data
           dic['desc']='注册成功'
           return JSONResponse(dic,status=HTTP_200_OK)
       return JSONResponse({'desc':serializer.errors}, status=HTTP_400_BAD_REQUEST)
       