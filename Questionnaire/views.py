import json

from django.utils import timezone

from Questionnaire.models import *
from django.http import JsonResponse, HttpResponse

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
            k = 0
            myQuestion = [];
            myQuestion.append(str(i));i+=1;#第几题
            myQuestion.append(str(question.id))#题目id
            myQuestion.append(0);myQuestion.append(0);myQuestion.append(0);myQuestion.append(0);
            for answerQuestionnaire in answerQuestionnaires:
                answerQuestionId = AnswerQuestions.objects.get(answerQuestionId = question.id,answerQuestionnaireId = answerQuestionnaire.id).id
                optionContent = AnswerOptions.objects.get(answerQuestionId = answerQuestionId).optionContent
                if '1' in optionContent: myQuestion[2] += 1
                if '2' in optionContent: myQuestion[3] += 1
                if '3' in optionContent: myQuestion[4] += 1
                if '4' in optionContent: myQuestion[5] += 1
                k+=1

            params.append(str(k));#每道题填写人数
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
            answers.append("答题者id:")
            answers.append(str(answerQuestionnaire.answerId));
            answerQuestions = AnswerQuestions.objects.filter(answerQuestionnaireId = answerQuestionnaire.id)
            # 答卷中的每道题
            for answerQuestion in answerQuestions:
                i = 1;
                myOption = AnswerOptions.objects.get(answerQuestionId = answerQuestion.id)
                if myOption.optionType == 1:
                    answers.append("题号：")
                    answers.append(str(i))
                    answers.append("答案：")
                    answers.append(myOption.optionContent)
                    answers.append("id")
                    answers.append(str(answerQuestion.id));i+=1
                if myOption.optionType == 2:
                    answers.append("题号：")
                    answers.append(str(i))
                    answers.append("答案：")
                    answers.append(myOption.completionContent)
                    answers.append("id")
                    answers.append(str(answerQuestion.id));i+=1
                if myOption.optionType == 3:
                    answers.append("题号：")
                    answers.append(str(i))
                    answers.append("答案：")
                    answers.append(myOption.optionScore)
                    answers.append("id")
                    answers.append(str(answerQuestion.id));i+=1

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
def getquestionAnswer(request):
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
            answers.append("答题者id:" )
            answers.append(str(answerQuestionnaire.answerId));
            myOption = AnswerOptions.objects.get(answerQuestionId=question.id)
            if myOption.optionType == 1:
                answers.append("答案:" )
                answers.append( myOption.optionContent)
            if myOption.optionType == 2:
                answers.append("答案:" )
                answers.append( myOption.completionContent)
            if myOption.optionType == 3:
                answers.append("答案:")
                answers.append(myOption.optionScore)
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

# 保存问卷
def saveQuestionnaire(request):
    if request.method == 'POST':
        try:
            information = json.loads(request.body.decode())
            questionnaire = QuestionnaireInformation(
                authorId=information.authorId,
                questionnaireTitle=information.questionnaireTitle,
                questionnaireInformation=information.questionnaireInformation,
                maxRecovery=information.maxRecovery,
                questionAmount=information.questionnaireAmount
            );
            questionnaire.save()
            questionnaireId = questionnaire.id
            problems = information.questionList
            for problem in problems:
                question = Questions(
                    questionnaireId=questionnaireId,
                    questionTitle=problem.questionTitle,
                    required=problem.questionRequired,
                    questionTypeId=problem.questionTypeId,
                    multipleChoice=problem.multipleChoice,
                    choiceAmount=problem.choiceAmount,
                    questionOrder=problem.questionOrder
                )
                question.save()
                questionId=question.id
                # 判断是否有optionList
                if "optionList" in problem:
                    options = problem.optionList
                    for option in options:
                        op = Options(
                            questionId=questionId,
                            optionOrder=option.optionOrder,
                            required=option.optionRequired,
                            optionContent=option.optionContent,
                            optionType=option.optionType,
                            optionScore=option.optionScore,
                            optionText=option.optionText
                        )
            return JsonResponse({'status': 200, 'result':"保存成功"})
        except Exception:
            return JsonResponse({'status': 400, 'result':"保存问卷失败"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})

# 问卷发放
def releaseQuestionnaire(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        questionnaireId = req.questionnaireId
        try:
            questionnaire = QuestionnaireInformation.objects.get(questionnaireId=questionnaireId)
        except Exception:
            return JsonResponse({'status': 400, 'result': "没有找到问卷"})
        else:
            if questionnaire.answerAmount >= questionnaire.maxRecovery:
                questionnaire.currentState = False
                questionnaire.save()
                return JsonResponse({'status': 400, 'result': "已经达到回收数量上限"})
            else:
                questionnaire.currentState = True
                questionnaire.startTime = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
                questionnaire.save()
                return JsonResponse({'status': 200, 'result': "发布成功"})

    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})
