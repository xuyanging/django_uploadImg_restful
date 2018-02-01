from django.conf.urls import url,include
from . import views

urlpatterns = [

    url(r'^upload_head_image$', views.UploadViewSet.as_view()),

    url(r'^register$', views.UserRegisterAPIView.as_view()),
    url(r'^login$', views.UserLoginAPIView.as_view()),

]

