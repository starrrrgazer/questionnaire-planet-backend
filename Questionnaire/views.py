import json
from Questionnaire.models import *
from user.models import *
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from django.shortcuts import render

# Create your views here.

# 获取问卷结果的数据
def getAnswerData(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("questionnaireId");
        params = [];
        questionnaire = QuestionnaireInformation.objects.get(id = questionnaireId);
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId);
        # 所有该问卷中的题目
        questions = Questions.objects.filter(questionnaireId = questionnaireId)
        i = 1;
        # 遍历题目
        for question in questions:
            # 查询选项内容
            # options = Options.objects.filter(questionId = question)
            myQuestion = []
            # myQuestion.append({})
            myQuestion.append({'num': i,'id': question.id,'answernum': 0,"question": question.questionTitle,'name':'A','Num': 0})
            myQuestion.append({'name':'B','Num': 0})
            myQuestion.append({'name':'C','Num': 0})
            myQuestion.append({'name':'D','Num': 0})
            i+=1
            # myQuestionAnswers = {'num': i, 'id': question.id, 'answernum': 0,"question":question.questionTitle
            #     , 'A': 0, 'B': 0, 'C': 0, 'D': 0};i+=1
            for answerQuestionnaire in answerQuestionnaires:
                answerQuestionId = AnswerQuestions.objects.get(answerQuestionId = question.id,answerQuestionnaireId = answerQuestionnaire.id).id
                optionContent = AnswerOptions.objects.get(answerQuestionId = answerQuestionId).optionContent

                if '1' in optionContent: myQuestion[0]['Num'] += 1
                if '2' in optionContent: myQuestion[1]['Num'] += 1
                if '3' in optionContent: myQuestion[2]['Num'] += 1
                if '4' in optionContent: myQuestion[3]['Num'] += 1
                myQuestion[0]['answernum']+=1
            # params.append({'answernum':k});#每道题填写人数
            params.append(myQuestion)

        return JsonResponse({
            "status":200,
            "data":params,
            "answerAmount":questionnaire.recoveryAmount,
            "result":"获取问卷结果成功"
        })
    else:
        return JsonResponse({
            "status": 401,
            "result": "请求方式错误"
        })


# 获取答题情况
def getAnswer(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("questionnaireId");
        params = [];
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId)
        # 遍历每个答卷
        for answerQuestionnaire in answerQuestionnaires:
            answers = [];
            answers.append({"answerId":answerQuestionnaire.answerId})
            answerQuestions = AnswerQuestions.objects.filter(answerQuestionnaireId = answerQuestionnaire.id)
            # 答卷中的每道题
            for answerQuestion in answerQuestions:
                i = 1;
                myOption = AnswerOptions.objects.get(answerQuestionId = answerQuestion.id)
                if myOption.optionType == 1:
                    answers.append({"num":i,"answer": myOption.optionContent,"id":answerQuestion.id});i+=1
                    # answers.append({"answer": myOption.optionContent})
                    # answers.append({"id":answerQuestion.id});i+=1
                if myOption.optionType == 2:
                    answers.append({"num": i, "answer": myOption.completionContent, "id": answerQuestion.id});
                    i += 1
                    # answers.append({"num":i})
                    # answers.append({"answer": myOption.completionContent})
                    # answers.append({"id":answerQuestion.id});i+=1
                if myOption.optionType == 3:
                    answers.append({"num": i, "answer": myOption.optionScore, "id": answerQuestion.id});
                    i += 1
                    # answers.append({"num":i})
                    # answers.append({"answer": myOption.optionScore})
                    # answers.append({"id":answerQuestion.id});i+=1

            params.append(answers)

        return JsonResponse({
            "status":200,
            "data":params,
            "result":"获取答题情况成功"
        })
    else:
        return JsonResponse({
            "status": 401,
            "result": "请求方式错误"
        })


# 筛选功能
def getQuestionAnswer(request):
    if request.method == 'POST':
        params = json.loads(request.body);
        questionnaireId = params.get("questionnaireId")
        answerId = params.get("answerId")
        data = [];

        question = AnswerQuestions.objects.get(answerQuestionnaireId = questionnaireId,answerQuestionId = answerId)
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId=questionnaireId)

        # 遍历每个答卷
        for answerQuestionnaire in answerQuestionnaires:
            answers = [];
            answers.append({"answerId":answerQuestionnaire.answerId})
            myOption = AnswerOptions.objects.get(answerQuestionId=question.id)
            if myOption.optionType == 1:
                answers.append({"answer":myOption.optionContent} )
            if myOption.optionType == 2:
                answers.append({"answer":myOption.completionContent})
            if myOption.optionType == 3:
                answers.append({"answer":myOption.optionScore})
            data.append(answers)
        return JsonResponse({
            "status": 200,
            "result": "查询成功",
            "data":data
        })
    else:
        return JsonResponse({
            "status": 401,
            "result": "请求方式错误"
        })


# 删除问卷
def deleteQuestionnaire(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("id");
        try:
            questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId);
        except Exception as e:
            return JsonResponse({
                "status": 400,
                "result": "找不到该问卷"
            })
        questionnaire.deleted = True;
        questionnaire.save();
        return JsonResponse({
            "status":200,
            "result":"删除成功"
        })
    else:
        return JsonResponse({
            "status": 401,
            "result": "请求方式错误"
        })


# 还原问卷
def backQuestionnaire(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("id");
        try:
            questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId);
        except Exception as e:
            return JsonResponse({
                "status": 400,
                "result": "找不到该问卷"
            })
        questionnaire.deleted = False;
        questionnaire.save();
        return JsonResponse({
            "status":200,
            "result":"还原成功"
        })
    else:
        return JsonResponse({
            "status": 401,
            "result": "请求方式错误"
        })

# 按问卷回收量排序
def sortByRecoveryAmount(request):
    if request.method == "GET":
        Questionnaires = QuestionnaireInformation.objects.all().order_by('-recoveryAmount')
        myData = []
        # Questionnaires = QuestionnaireInformation.objects.all().order_by('-recoveryAmount')
        for questionnaire in Questionnaires:
            myData.append({"id":questionnaire.id,
                           "author":user.objects.get(id = questionnaire.authorId).id,
                           "title":questionnaire.questionnaireTitle,
                           "content":questionnaire.questionnaireInformation,
                           "setUpTime": questionnaire.setUpTime,
                           "latestAlterTime":questionnaire.latestAlterTime,
                           "startTime":questionnaire.startTime,
                           "endTime":questionnaire.endTime,
                           "deadline":questionnaire.lastEndTime,
                           "maxRecovery":questionnaire.maxRecovery,
                           "currentState":questionnaire.currentState,
                           "questionAmount":questionnaire.questionAmount,
                           "answerAmount":questionnaire.recoveryAmount})

        return JsonResponse({
            "status":200,
            "result":"排序成功",
            "data":myData
        })

# 按发布时间排序
def sortByStartTime(request):
    if request.method == "GET":
        Questionnaires = QuestionnaireInformation.objects.all().order_by('-startTime')
        myData = []
        # Questionnaires = QuestionnaireInformation.objects.all().order_by('-recoveryAmount')
        for questionnaire in Questionnaires:
            myData.append({"id":questionnaire.id,
                           "author":user.objects.get(id = questionnaire.authorId).id,
                           "title":questionnaire.questionnaireTitle,
                           "content":questionnaire.questionnaireInformation,
                           "setUpTime": questionnaire.setUpTime,
                           "latestAlterTime":questionnaire.latestAlterTime,
                           "startTime":questionnaire.startTime,
                           "endTime":questionnaire.endTime,
                           "deadline":questionnaire.lastEndTime,
                           "maxRecovery":questionnaire.maxRecovery,
                           "currentState":questionnaire.currentState,
                           "questionAmount":questionnaire.questionAmount,
                           "answerAmount":questionnaire.recoveryAmount})

        return JsonResponse({
            "status":200,
            "result":"排序成功",
            "data":myData
        })

# 按创建时间排序
def sortBySetUpTime(request):
    if request.method == "GET":
        Questionnaires = QuestionnaireInformation.objects.all().order_by('-setUpTime')
        myData = []
        # Questionnaires = QuestionnaireInformation.objects.all().order_by('-recoveryAmount')
        for questionnaire in Questionnaires:
            myData.append({"id":questionnaire.id,
                           "author":user.objects.get(id = questionnaire.authorId).id,
                           "title":questionnaire.questionnaireTitle,
                           "content":questionnaire.questionnaireInformation,
                           "setUpTime": questionnaire.setUpTime,
                           "latestAlterTime":questionnaire.latestAlterTime,
                           "startTime":questionnaire.startTime,
                           "endTime":questionnaire.endTime,
                           "deadline":questionnaire.lastEndTime,
                           "maxRecovery":questionnaire.maxRecovery,
                           "currentState":questionnaire.currentState,
                           "questionAmount":questionnaire.questionAmount,
                           "answerAmount":questionnaire.recoveryAmount})

        return JsonResponse({
            "status":200,
            "result":"排序成功",
            "data":myData
        })