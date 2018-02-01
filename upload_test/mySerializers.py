# quickstart/serializers.py
from django.contrib.auth.models import *
from rest_framework import serializers
from . import models
import time
from django.conf import settings



class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)#use_url=True是否显示完整的路径
    def create(self, validated_data):
        data = self.context.get('request').data.dict()
        user_id = data['user_id']       
        print('xxxx=------',user_id,'xasaaaaa=---',validated_data)
        validated_data.update({'uploaded_by_id': user_id})
        return models.userHeadImage.objects.create(**validated_data)
    class Meta:
        model = models.userHeadImage
        fields = ('image_id','image')



#用户基本信息
class UserSerializer(serializers.ModelSerializer):
    time_join = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    def get_time_join(self,obj):
        t = obj.date_joined
        return t.strftime('%Y-%m-%d %X')
    def get_img(self,obj):
        image = ImageSerializer(models.userHeadImage.objects.filter(uploaded_by_id__exact=obj.user_id).first()).data
        if image:
            return image['image']
        else:
            return ''
    class Meta:
        model = models.haveFunUser
        fields = ('user_id','name', 'phone','time_join','sex','age','address','email','img','user_type','passwd')