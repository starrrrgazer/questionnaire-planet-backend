import json

from django.utils import timezone

from Questionnaire.models import *
from django.http import JsonResponse, HttpResponse

from django.shortcuts import render


# Create your views here.

# 获取问卷结果的数据
from user.models import user


def getAnswerData(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("questionnaireId");
        params = [];
        questionnaire = QuestionnaireInformation.objects.get(id = questionnaireId);
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId);
        # 所有该问卷中的题目
        questions = Questions.objects.filter(questionnaireId = questionnaireId)
        i = 1;i1 = 1;
        # 遍历题目
        for question in questions:
            # 查询选项内容
            # options = Options.objects.filter(questionId = question)
            myQuestion = []
            # myQuestion.append({})

            # 选择题
            if question.questionTypeId == 1:
                myQuestion.append(
                    {'num': i, 'id': question.id,'type':1, 'answernum': 0, "question": question.questionTitle, 'name': 'A',
                     'Num': 0})
                myQuestion.append({'name': 'B', 'Num': 0})
                myQuestion.append({'name': 'C', 'Num': 0})
                myQuestion.append({'name': 'D', 'Num': 0})
                i += 1
                # myQuestionAnswers = {'num': i, 'id': question.id, 'answernum': 0,"question":question.questionTitle
                #     , 'A': 0, 'B': 0, 'C': 0, 'D': 0};i+=1
                for answerQuestionnaire in answerQuestionnaires:
                    answerQuestionId = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                   answerQuestionnaireId=answerQuestionnaire.id).id
                    optionContent = AnswerOptions.objects.get(answerQuestionId=answerQuestionId).optionContent

                    if '1' in optionContent: myQuestion[0]['Num'] += 1
                    if '2' in optionContent: myQuestion[1]['Num'] += 1
                    if '3' in optionContent: myQuestion[2]['Num'] += 1
                    if '4' in optionContent: myQuestion[3]['Num'] += 1
                    myQuestion[0]['answernum'] += 1
                # params.append({'answernum':k});#每道题填写人数
                params.append(myQuestion)

            #     填空题
            elif question.questionTypeId == 2:
                myQuestion.append(
                    {'num': i, 'id': question.id,'type':2, 'answernum': 0, "question": question.questionTitle,'answer':''})
                for answerQuestionnaire in answerQuestionnaires:
                    answerQuestionId = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                   answerQuestionnaireId=answerQuestionnaire.id).id

                    completionContent = AnswerOptions.objects.get(answerQuestionId=answerQuestionId).completionContent
                    # if answerQuestionnaires.index(answerQuestionnaire) == 0:
                    #     myQuestion[0]['answer'] = completionContent
                    # else:
                    myQuestion.append({"answer": completionContent})
                    myQuestion[0]['answernum'] += 1;
                    i1 += 1
                params.append(myQuestion)
                # 简单评分
            elif question.questionTypeId == 3:
                myQuestion.append(
                    {'num': i, 'id': question.id,'type':3, 'answernum': 0,
                     "question": question.questionTitle,'name': '一星','Num':0,'averageScore':0})
                myQuestion.append({'name': '二星', 'Num': 0})
                myQuestion.append({'name': '三星', 'Num': 0})
                myQuestion.append({'name': '四星', 'Num': 0})
                myQuestion.append({'name': '五星', 'Num': 0})
                for answerQuestionnaire in answerQuestionnaires:
                    answerQuestionId = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                   answerQuestionnaireId=answerQuestionnaire.id).id
                    # 取得评分
                    optionScore1 = AnswerOptions.objects.get(answerQuestionId=answerQuestionId,answerOptionOrder = 1).optionScore
                    myQuestion[optionScore1-1]['Num'] += 1
                    myQuestion[0]['averageScore'] += optionScore1
                    myQuestion[0]['answernum'] += 1
                myQuestion[0]['averageScore'] /= myQuestion[0]['answernum']
                params.append(myQuestion)

            #     高级评分
            elif question.questionTypeId == 4:
                myQuestion.append(
                    {'num': i, 'id': question.id, 'type':4,'answernum': 0, 'question': question.questionTitle,
                        'averageScore':0,'name': '一星', 'Num': 0,'comment':[]})
                myQuestion.append({'name': '二星', 'Num': 0,'comment':[]})
                myQuestion.append({'name': '三星', 'Num': 0,'comment':[]})
                myQuestion.append({'name': '四星', 'Num': 0,'comment':[]})
                myQuestion.append({'name': '五星', 'Num': 0,'comment':[]})

                for answerQuestionnaire in answerQuestionnaires:
                    answerQuestionId = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                   answerQuestionnaireId=answerQuestionnaire.id).id

                    # 取得评分
                    optionScore1 = AnswerOptions.objects.get(answerQuestionId=answerQuestionId,
                                                             answerOptionOrder=1).optionScore
        #             取得评价
                    optionScoreText1 = AnswerOptions.objects.get(answerQuestionId=answerQuestionId,
                                                             answerOptionOrder=1).optionScoreText

                    myQuestion[optionScore1-1]['Num'] += 1
                    myQuestion[optionScore1-1]['comment'].append(optionScoreText1)
                    myQuestion[0]['averageScore'] += optionScore1
                    myQuestion[0]['answernum'] += 1



                myQuestion[0]['averageScore'] /= myQuestion[0]['answernum']
                params.append(myQuestion)


        return JsonResponse({
            'status':200,
            'data':params,
            'answerAmount':questionnaire.recoveryAmount,
            'result':"获取问卷结果成功"
        })
    else:
        return JsonResponse({
            'status': 401,
            'result': "请求方式错误"
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


# 提交问卷
def submitQuestionnaire(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        # 数组
        newAnswerQuestions = params.get("answerQuestions")
        questionAmount = len(newAnswerQuestions)
        answerQuestionnaire = AnswerQuestionnaire()
        answerQuestionnaire.questionnaireId = params.get("questionnaireId")
        answerQuestionnaire.commitTime = datetime.datetime.now()
        answerQuestionnaire.save()

        for index in range(0,questionAmount):
            newAnswerQuestion = AnswerQuestions()
            newAnswerQuestion.answerQuestionnaireId = answerQuestionnaire.id
            newAnswerQuestion.answerQuestionId = Questions.objects.get(questionnaireId=answerQuestionnaire.questionnaireId,
                                                                       questionOrder=index+1).id
            newAnswerQuestion.questionTypeId = Questions.objects.get(id = newAnswerQuestion.answerQuestionId).questionTypeId
            newAnswerQuestion.answerOrder = index
            if newAnswerQuestion.questionTypeId == 2:
                newAnswerQuestion.answerText = newAnswerQuestions[index]['answer']
            newAnswerQuestion.save()
            if newAnswerQuestion.questionTypeId == 1:
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType =1;
                newAnswerOption.optionContent = newAnswerQuestions[index]['answer']
                newAnswerOption.answerOptionOrder = newAnswerQuestions[index]['answer']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                newAnswerOption.answerOptionId = Options.objects.get(questionId= newAnswerQuestion.answerQuestionId,
                                                                     optionOrder= newAnswerOption.answerOptionOrder).id
                newAnswerOption.save()
            elif newAnswerQuestion.questionTypeId == 2:
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType = 2;
                newAnswerOption.optionContent = 1
                newAnswerOption.answerOptionOrder = 1
                newAnswerOption.completionContent = newAnswerQuestions[index]['answer']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                newAnswerOption.answerOptionId = Options.objects.get(questionId=newAnswerQuestion.answerQuestionId,
                                                                     optionOrder=newAnswerOption.answerOptionOrder).id
                newAnswerOption.save()
            elif newAnswerQuestion.questionTypeId == 3:
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType = 3;
                newAnswerOption.optionContent = 1
                newAnswerOption.answerOptionOrder = 1
                newAnswerOption.optionScore = newAnswerQuestions[index]['answer']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                newAnswerOption.answerOptionId = Options.objects.get(questionId=newAnswerQuestion.answerQuestionId,
                                                                     optionOrder=newAnswerOption.answerOptionOrder).id
                newAnswerOption.save()
            elif newAnswerQuestion.questionTypeId == 4:
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType = 3;
                newAnswerOption.optionContent = 1
                newAnswerOption.answerOptionOrder = 1
                newAnswerOption.optionScore = newAnswerQuestions[index]['answer']
                newAnswerOption.optionScoreText = newAnswerQuestions[index]['comment']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                newAnswerOption.answerOptionId = Options.objects.get(questionId=newAnswerQuestion.answerQuestionId,
                                                                     optionOrder=newAnswerOption.answerOptionOrder).id
                newAnswerOption.save()
        return JsonResponse({
            'status':200,
            'result':"创建问卷成功"
        })
    else:
        return JsonResponse({
            'status':400,
            'result':"请求方式错误"
        })


# 保存问卷
def saveQuestionnaire(request):
    if request.method == 'POST':
        if request.session.get('id'):
            authorId = request.session.get('id')
            try:
                information = json.loads(request.body.decode())
                problems = information.get('questionList')
                questionAmount = len(problems)
                questionnaire = QuestionnaireInformation(
                    authorId=authorId,
                    questionnaireTitle=information.get('questionnaireTitle'),
                    questionnaireInformation=information.get('questionnaireInformation'),
                    maxRecovery=information.get('maxRecovery'),
                    questionAmount=questionAmount
                )
                questionnaire.save()
                questionnaireId = questionnaire.id
                i = 1
                for problem in problems:
                    options = problem.get('optionList')
                    choiceAmount = len(options)
                    question = Questions(
                        questionnaireId=questionnaireId,
                        questionTitle=problem.get('questionTitle'),
                        required=problem.get('questionRequired'),
                        questionTypeId=problem.get('questionTypeId'),
                        multipleChoice=problem.get('multipleChoice'),
                        choiceAmount=choiceAmount,
                        questionOrder=i
                    )
                    question.save()
                    i = i+1
                    questionId = question.id
                    if choiceAmount > 0:
                        j = 1
                        for option in options:
                            op = Options(
                                questionId=questionId,
                                optionOrder=j,
                                required=option.get('optionRequired'),
                                optionContent=option.get('optionContent'),
                                optionType=option.get('optionType'),
                                optionScore=option.get('optionScore'),
                                optionText=option.get('optionText')
                            )
                            op.save()
                            j=j+1
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
                problems = information.get('questionList')
                questionAmount = len(problems)
                questionnaire = QuestionnaireInformation.objects.get(id=oldQuestionnaireId)
                questionnaire.questionnaireTitle = information.get('questionnaireTitle')
                questionnaire.questionnaireInformation = information.get('questionnaireInformation')
                questionnaire.maxRecovery = information.get('maxRecovery')
                questionnaire.questionAmount = questionAmount
                questionnaire.save()
                questionnaireId = oldQuestionnaireId
                i=1
                for problem in problems:
                    options = problem.get('optionList')
                    choiceAmount = len(options)
                    question = Questions(
                        questionnaireId=questionnaireId,
                        questionTitle=problem.get('questionTitle'),
                        required=problem.get('questionRequired'),
                        questionTypeId=problem.get('questionTypeId'),
                        multipleChoice=problem.get('multipleChoice'),
                        choiceAmount=choiceAmount,
                        questionOrder=i
                    )
                    question.save()
                    i = i+1
                    questionId = question.id
                    # 判断是否有optionList
                    if choiceAmount > 0:
                        j = 1
                        for option in options:
                            op = Options(
                                questionId=questionId,
                                optionOrder=j,
                                required=option.get('optionRequired'),
                                optionContent=option.get('optionContent'),
                                optionType=option.get('optionType'),
                                optionScore=option.get('optionScore'),
                                optionText=option.get('optionText')
                            )
                            op.save()
                            j = j+1
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

# 测试session
def testSession(request):
    print(request.session.items())
    return JsonResponse({'status':0})