import json
from Questionnaire.models import *
from django.http import JsonResponse, HttpResponse

from django.shortcuts import render

# Create your views here.

# 获取问卷结果的数据
def getAnswer(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("id");
        params = [];
        questionnaire = QuestionnaireInformation.objects.get(id = questionnaireId);
        questionAmount = questionnaire.questionAmount;
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId);
        # 所有该问卷中的题目
        questions = Questions.objects.filter(questionnaireId = questionnaireId)
        i = 1
        # 遍历题目
        for question in questions:
            myQuestion = [];
            myQuestion.append(++i);
            myQuestion.append(0);myQuestion.append(0);myQuestion.append(0);myQuestion.append(0);
            for answerQuestionnaire in answerQuestionnaires:
                answerQuestionId = AnswerQuestions.objects.get(questionId = question.id,answerQuestionnaireId = answerQuestionnaire.id).id
                optionContent = AnswerOptions.objects.get(answerQuestionId = answerQuestionId).optionContent
                if '1' in optionContent: myQuestion[1] += 1
                if '2' in optionContent: myQuestion[2] += 1
                if '3' in optionContent: myQuestion[3] += 1
                if '4' in optionContent: myQuestion[4] += 1

            params.append(myQuestion)

        return JsonResponse({
            "status":200,
            "data":params,
            "result":"获取问卷结果成功"
        })



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