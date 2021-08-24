from django.urls import path
from Questionnaire import views

urlpatterns = [
    path("getAnswerData",views.getAnswerData),
    path("deleteQuestionnaire",views.deleteQuestionnaire),
    path("getBackQuestionnaire",views.backQuestionnaire),
    path("getAnswer",views.getAnswer),
    path("getQuestionAnswer",views.getQuestionAnswer),
    path("saveQuestionnaire", views.saveQuestionnaire),
    path("releaseQuestionnaire", views.releaseQuestionnaire),
    path("stopReleaseQuestionnaire", views.stopReleaseQuestionnaire),
    path("getMyQuestionnaire", views.getMyQuestionnaire),
    path("getQuestionnaireDetails", views.getQuestionnaireDetails),
    path("editQuestionnaire", views.editQuestionnaire),
    path("modifyQuestionnaire", views.modifyQuestionnaire),
    path("sortByRecoveryAmount", views.sortByRecoveryAmount),
    path("sortByStartTime", views.sortByStartTime),
    path("sortBySetUpTime", views.sortBySetUpTime),
    path("submitQuestionnaire", views.submitQuestionnaire),
    # path("getQuestionnaireId",views.getQuestionnaireId),
    path("returnSession",views.returnSession),
    path("deleteCompletelyQuestionnaire",views.deleteCompletelyQuestionnaire)
]