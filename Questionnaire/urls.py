from django.urls import path
from Questionnaire import views

urlpatterns = [
    path("getAnswerData",views.getAnswerData),
    path("deleteQuestionnaire",views.deleteQuestionnaire),
    path("backQuestionnaire",views.backQuestionnaire),
    path("getAnswer",views.getAnswer),
    path("getquestionAnswer",views.getquestionAnswer),
    path("saveQuestionnaire", views.saveQuestionnaire),
    path("releaseQuestionnaire", views.releaseQuestionnaire),
    path("stopReleaseQuestionnaire", views.stopReleaseQuestionnaire),
    path("getMyQuestionnaire", views.getMyQuestionnaire),
]