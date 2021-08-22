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
        questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId);
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId=questionnaireId);
        # 所有该问卷中的题目
        questions = Questions.objects.filter(questionnaireId=questionnaireId)
        i = 1;
        # 遍历题目
        for question in questions:
            k = 0
            myQuestion = [];
            myQuestion.append(str(i));
            i += 1;  # 第几题
            myQuestion.append(str(question.id))  # 题目id
            myQuestion.append(0);
            myQuestion.append(0);
            myQuestion.append(0);
            myQuestion.append(0);
            for answerQuestionnaire in answerQuestionnaires:
                answerQuestionId = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                               answerQuestionnaireId=answerQuestionnaire.id).id
                optionContent = AnswerOptions.objects.get(answerQuestionId=answerQuestionId).optionContent
                if '1' in optionContent: myQuestion[2] += 1
                if '2' in optionContent: myQuestion[3] += 1
                if '3' in optionContent: myQuestion[4] += 1
                if '4' in optionContent: myQuestion[5] += 1
                k += 1

            params.append(str(k));  # 每道题填写人数
            params.append(myQuestion)

        return JsonResponse({
            "status": 200,
            "data": params,
            "answerAmount": questionnaire.recoveryAmount,
            "result": "获取问卷结果成功"
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
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId=questionnaireId)
        # 遍历每个答卷
        for answerQuestionnaire in answerQuestionnaires:
            answers = [];
            answers.append("答题者id:")
            answers.append(str(answerQuestionnaire.answerId));
            answerQuestions = AnswerQuestions.objects.filter(answerQuestionnaireId=answerQuestionnaire.id)
            # 答卷中的每道题
            for answerQuestion in answerQuestions:
                i = 1;
                myOption = AnswerOptions.objects.get(answerQuestionId=answerQuestion.id)
                if myOption.optionType == 1:
                    answers.append("题号：")
                    answers.append(str(i))
                    answers.append("答案：")
                    answers.append(myOption.optionContent)
                    answers.append("id")
                    answers.append(str(answerQuestion.id));
                    i += 1
                if myOption.optionType == 2:
                    answers.append("题号：")
                    answers.append(str(i))
                    answers.append("答案：")
                    answers.append(myOption.completionContent)
                    answers.append("id")
                    answers.append(str(answerQuestion.id));
                    i += 1
                if myOption.optionType == 3:
                    answers.append("题号：")
                    answers.append(str(i))
                    answers.append("答案：")
                    answers.append(myOption.optionScore)
                    answers.append("id")
                    answers.append(str(answerQuestion.id));
                    i += 1
            params.append(answers)
        return JsonResponse({
            "status": 200,
            "data": params,
            "result": "获取答题情况成功"
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

        question = AnswerQuestions.objects.get(answerQuestionnaireId=questionnaireId, answerQuestionId=answerId)
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId=questionnaireId)

        # 遍历每个答卷
        for answerQuestionnaire in answerQuestionnaires:
            answers = [];
            answers.append("答题者id:")
            answers.append(str(answerQuestionnaire.answerId));
            myOption = AnswerOptions.objects.get(answerQuestionId=question.id)
            if myOption.optionType == 1:
                answers.append("答案:")
                answers.append(myOption.optionContent)
            if myOption.optionType == 2:
                answers.append("答案:")
                answers.append(myOption.completionContent)
            if myOption.optionType == 3:
                answers.append("答案:")
                answers.append(myOption.optionScore)
            data.append(answers)
        return JsonResponse({
            "status": 200,
            "result": "查询成功",
            "data": data
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
            "status": 200,
            "result": "删除成功"
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
            "status": 200,
            "result": "还原成功"
        })
    else:
        return JsonResponse({
            "status": 401,
            "result": "请求方式错误"
        })


# 保存问卷
def saveQuestionnaire(request):
    if request.method == 'POST':
        if request.session.get('id'):
            authorId = request.session.get('id')
            try:
                information = json.loads(request.body.decode())
                print(1)
                questionnaire = QuestionnaireInformation(
                    authorId=authorId,
                    questionnaireTitle=information.get('questionnaireTitle'),
                    questionnaireInformation=information.get('questionnaireInformation'),
                    maxRecovery=information.get('maxRecovery'),
                    questionAmount=information.get('questionAmount')
                )
                print(2)
                questionnaire.save()
                print(2.5)
                questionnaireId = questionnaire.id
                print(questionnaireId)
                problems = information.get('questionList')
                print(3)
                for problem in problems:
                    question = Questions(
                        questionnaireId=questionnaireId,
                        questionTitle=problem.get('questionTitle'),
                        required=problem.get('questionRequired'),
                        questionTypeId=problem.get('questionTypeId'),
                        multipleChoice=problem.get('multipleChoice'),
                        choiceAmount=problem.get('choiceAmount'),
                        questionOrder=problem.get('questionOrder')
                    )
                    print(3.5)
                    question.save()
                    questionId = question.id
                    # 判断是否有optionList
                    print(4)
                    if question.choiceAmount > 0:
                        options = problem.get('optionList')
                        for option in options:
                            op = Options(
                                questionId=questionId,
                                optionOrder=option.get('optionOrder'),
                                required=option.get('optionRequired'),
                                optionContent=option.get('optionContent'),
                                optionType=option.get('optionType'),
                                optionScore=option.get('optionScore'),
                                optionText=option.get('optionText')
                            )
                            op.save()
                            print(5)
                return JsonResponse({'status': 200, 'result': "保存成功"})
            except Exception:
                return JsonResponse({'status': 400, 'result': "保存问卷失败"})
        else:
            return JsonResponse({'status': 400, 'result': "用户未登录"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})


# 问卷发放
def releaseQuestionnaire(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        questionnaireId = req.get('questionnaireId')
        try:
            questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId)
        except Exception:
            return JsonResponse({'status': 400, 'result': "没有找到问卷"})
        else:
            if questionnaire.recoveryAmount >= questionnaire.maxRecovery:
                questionnaire.currentState = False
                questionnaire.save()
                return JsonResponse({'status': 400, 'result': "已经达到回收数量上限"})
            else:
                questionnaire.currentState = True
                questionnaire.startTime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                questionnaire.save()
                return JsonResponse({'status': 200, 'result': "发布成功"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})


# 问卷停止发放
def stopReleaseQuestionnaire(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        questionnaireId = req.get('questionnaireId')
        try:
            questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId)
        except Exception:
            return JsonResponse({'status': 400, 'result': "没有找到问卷"})
        else:
            questionnaire.currentState = False
            questionnaire.endTime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            questionnaire.save()
            return JsonResponse({'status': 200, 'result': "发布成功"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})


# 查看我的问卷
def getMyQuestionnaire(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        method = req.get('method')
        if request.session.get('id'):
            authorId = request.session.get('id')
            res = {}
            try:
                if method == 1:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('setUpTime')
                elif method == -1:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('-setUpTime')
                else:
                    return JsonResponse({'status': 400, 'result': "排序方法出错"})
                if questionnaires.exists():
                    questionnaireList = []
                    for questionnaire in questionnaires:
                        questionnaireList.append(
                            {
                                'questionnaireId': questionnaire.id,
                                'questionnaireTitle': questionnaire.questionnaireTitle,
                                'currenState': questionnaire.currentState,
                                'deleted': questionnaire.deleted,
                                'answerAmount': questionnaire.recoveryAmount,
                                'setUpTime': questionnaire.setUpTime,
                                'startTime': questionnaire.startTime,
                                'latestAlterTime': questionnaire.latestAlterTime
                            }
                        )
                    res['questionnaireList'] = questionnaireList
                    res['status'] = 200
                    res['result'] = "获取成功"
                    return JsonResponse(res)
                else:
                    return JsonResponse({'status': 200, 'result': "用户没有创建问卷记录"})
            except Exception:
                return JsonResponse({'status': 400, 'result': "获取信息出错"})
        else:
            return JsonResponse({'status': 400, 'result': "用户未登录"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})


# 查看问卷详细内容
def getQuestionnaireDetails(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        questionnaireId = req.get('questionnaireId')
        try:
            questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId)
        except Exception:
            return JsonResponse({'status': 400, 'result': "找不到该问卷"})
        else:
            questionList = []
            questions = Questions.objects.filter(questionnaireId=questionnaireId).order_by('questionOrder')
            for question in questions:
                questionId = question.id
                optionList = []
                options = Options.objects.filter(questionId=questionId).order_by('optionOrder')
                for option in options:
                    optionList.append(
                        {
                            'optionId': option.id,
                            'optionOrder': option.optionOrder,
                            'required': option.required,
                            'optionContent': option.optionContent,
                            'optionType': option.optionType,
                            'optionScore': option.optionScore,
                            'optionText': option.optionText,
                        }
                    )
                questionList.append(
                    {
                        'questionId': question.id,
                        'questionTitle': question.questionTitle,
                        'questionTypeId': question.questionTypeId,
                        'required': question.required,
                        'multipleChoice': question.multipleChoice,
                        'choiceAmount': question.choiceAmount,
                        'questionOrder': question.questionOrder,
                        'optionList':optionList
                    }
                )
            res = {
                'questionnaireTitle': questionnaire.questionnaireTitle,
                'questionnaireInformation': questionnaire.questionnaireInformation,
                'questionAmount': questionnaire.questionAmount,
                'questionList': questionList,
                'status': 200,
                'result': "获取问卷信息成功"
            }
            return JsonResponse(res)
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})


# 问卷编辑（发布前）
def editQuestionnaire(request):
    if request.method == 'POST':
        if request.session.get('id'):
            try:
                information = json.loads(request.body.decode())
                print(1)
                oldQuestionnaireId = information.get('questionnaireId')
                print(oldQuestionnaireId)
                oldQuestions = Questions.objects.filter(questionnaireId=oldQuestionnaireId)
                for oldQuestion in oldQuestions:
                    oldQuestion.questionnaireId = -1
                    oldQuestion.save()
                questionnaire = QuestionnaireInformation.objects.get(id=oldQuestionnaireId)
                questionnaire.questionnaireTitle=information.get('questionnaireTitle')
                questionnaire.questionnaireInformation=information.get('questionnaireInformation')
                questionnaire.maxRecovery=information.get('maxRecovery')
                questionnaire.questionAmount=information.get('questionAmount')
                questionnaire.save()
                questionnaireId = oldQuestionnaireId
                problems = information.get('questionList')
                for problem in problems:
                    question = Questions(
                        questionnaireId=questionnaireId,
                        questionTitle=problem.get('questionTitle'),
                        required=problem.get('questionRequired'),
                        questionTypeId=problem.get('questionTypeId'),
                        multipleChoice=problem.get('multipleChoice'),
                        choiceAmount=problem.get('choiceAmount'),
                        questionOrder=problem.get('questionOrder')
                    )
                    question.save()
                    questionId = question.id
                    # 判断是否有optionList
                    if question.choiceAmount > 0:
                        options = problem.get('optionList')
                        for option in options:
                            op = Options(
                                questionId=questionId,
                                optionOrder=option.get('optionOrder'),
                                required=option.get('optionRequired'),
                                optionContent=option.get('optionContent'),
                                optionType=option.get('optionType'),
                                optionScore=option.get('optionScore'),
                                optionText=option.get('optionText')
                            )
                            op.save()
                return JsonResponse({'status': 200, 'result': "保存成功"})
            except Exception:
                return JsonResponse({'status': 400, 'result': "保存问卷失败"})
        else:
            return JsonResponse({'status': 400, 'result': "用户未登录"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})

# 问卷修改（发布后）
def modifyQuestionnaire(request):
    if request.method == 'POST':
        if request.session.get('id'):
            try:
                information = json.loads(request.body.decode())
                questionnaireId = information.get('questionnaireId')
                questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId)
                questionnaire.questionnaireTitle=information.get('questionnaireTitle')
                questionnaire.questionnaireInformation=information.get('questionnaireInformation')
                questionnaire.maxRecovery=information.get('maxRecovery')
                questionnaire.save()
                questions = information.get('questionList')
                for question in questions:
                    questionId = question.get('questionId')
                    myQuestion = Questions.objects.get(id=questionId)
                    myQuestion.questionTitle = question.get('questionTitle')
                    myQuestion.save()
                    options = question.get('optionList')
                    for option in options:
                        optionId = option.get('optionId')
                        myOption = Options.objects.get(id=optionId)
                        myOption.optionContent = option.get('optionContent')
                        myOption.save()
                return JsonResponse({'status': 200, 'result': "修改成功"})
            except Exception:
                return JsonResponse({'status': 400, 'result': "修改失败"})
        else:
            return JsonResponse({'status': 400, 'result': "用户未登录"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})