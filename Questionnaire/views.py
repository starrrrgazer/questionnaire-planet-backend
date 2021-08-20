import json
from Questionnaire.models import *
from django.http import JsonResponse, HttpResponse

from django.shortcuts import render

# Create your views here.

# 获取问卷结果的数据
def getAnswer(request):
    if request.method=='POST':
        questionnaireId = json.loads(request.body).get("id");
        pass

# 删除问卷
def deleteQuestionnaire(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("id");
        questionnaire = QuestionnaireInformation.objects.get(id = questionnaireId);
        questionnaire.deleted = True;
        questionnaire.save();
        return JsonResponse({
            "status":200,
            "result":"删除成功"
        })