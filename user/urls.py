from django.urls import path
from user import views

urlpatterns = [
    path("login",views.login),
    path("register",views.register),
    path("getCode",views.getCode),
    path("getMyInfo",views.getMyInfo)
]