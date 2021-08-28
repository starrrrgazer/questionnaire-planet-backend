from django.urls import path
from user import views

urlpatterns = [
    path("login",views.login),
    path("register",views.register),
    # path("getCode",views.getCode),
    path("getMyInfo",views.getMyInfo),
    path("retrievePassword",views.retrievePassword),
    path("changePassword",views.changePassword),
    path("changePhoneNumber",views.changePhoneNumber)
]