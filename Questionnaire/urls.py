from django.urls import path
from Questionnaire import views

urlpatterns = [
    path("getAnswerData",views.getAnswerData),
    path("deleteQuestionnaire",views.deleteQuestionnaire),
    path("backQuestionnaire",views.backQuestionnaire),
    path("getAnswer",views.getAnswer),
    path("getQuestionAnswer",views.getQuestionAnswer),
    path("sortByRecoveryAmount",views.sortByRecoveryAmount),
    path("sortByStartTime",views.sortByStartTime),
    path("sortBySetUpTime",views.sortBySetUpTime)
]