import json
from Questionnaire.models import *
from django.http import JsonResponse, HttpResponse

from django.shortcuts import render

# Create your views here.

# 获取问卷结果的数据
def getAnswerData(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("id");
        params = [];
        questionnaire = QuestionnaireInformation.objects.get(id = questionnaireId);
        questionAmount = questionnaire.questionAmount;
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId);
        # 所有该问卷中的题目
        questions = Questions.objects.filter(questionnaireId = questionnaireId)
        i = 0
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


# 获取答题情况
def getAnswer(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("id");
        params = [];
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId)
        # 遍历每个答卷
        for answerQuestionnaire in answerQuestionnaires:
            answers = [];
            answers.append("答题者id:"+answerQuestionnaire.answerId);
            answerQuestions = AnswerQuestions.objects.filter(answerQuestionnaireId = answerQuestionnaire.id)
            # 答卷中的每道题
            for answerQuestion in answerQuestions:
                i = 0;
                myOption = AnswerOptions.objects.get(answerQuestionId = answerQuestion.id)
                if myOption.optionType == 1: answers.append("第"+ ++i +"题答案是"+myOption.optionContent)
                if myOption.optionType == 2: answers.append("第" + ++i + "题答案是" + myOption.completionContent)
                if myOption.optionType == 3: answers.append("第" + ++i + "题答案是" + myOption.optionScore)

            params.append(answers)

        return JsonResponse({
            "status":200,
            "data":params,
            "result":"获取答题情况成功"
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