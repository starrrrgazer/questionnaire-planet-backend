import json
import random

from django.utils import timezone

from Questionnaire.models import *
from django.http import JsonResponse, HttpResponse
from user.views import *

from django.shortcuts import render
# Create your views here.


from user.models import user

# 获取问卷结果的数据
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
            myQuestion = []

            # 选择题
            if question.questionTypeId == 1 or question.questionTypeId == 6:
                myQuestion.append(
                    {'num': i, 'id': question.id,'type':1, 'answernum': 0, "question": question.questionTitle,
                     'name':'A:'+Options.objects.get(questionId=question.id,optionOrder=1).optionContent,
                     'Num': 0})
                k = 'B'
                for index in range(2, question.choiceAmount + 1):
                    myQuestion.append({ 'name':k+':'+Options.objects.get(questionId=question.id,optionOrder=index).optionContent, 'Num': 0})
                    m = ord(k)
                    m += 1
                    k = chr(m)
                i += 1
                for answerQuestionnaire in answerQuestionnaires:
                    answerQuestion = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                   answerQuestionnaireId=answerQuestionnaire.id)
                    answerQuestionId = answerQuestion.id
                    AnswerOption = AnswerOptions.objects.get(answerQuestionId=answerQuestionId)
                    optionContent = AnswerOption.optionContent
                    if '1' in optionContent: myQuestion[0]['Num'] += 1
                    for index in range(2,question.choiceAmount+1):
                        if str(index) in optionContent: myQuestion[index-1]['Num'] += 1
                    myQuestion[0]['answernum'] += 1
                # params.append({'answernum':k});#每道题填写人数
                params.append(myQuestion)

            elif question.questionTypeId == 5:
                myQuestion.append(
                    {'num': i, 'id': question.id, 'type': 1, 'answernum': 0, "question": question.questionTitle,
                     'name':'A:'+Options.objects.get(questionId=question.id,optionOrder=1).optionContent,
                     'Num': 0})
                k = 'B'
                for index in range(2, question.choiceAmount + 1):
                    myQuestion.append({'name':k+':'+Options.objects.get(questionId=question.id,optionOrder=index).optionContent, 'Num': 0})
                    m = ord(k)
                    m += 1
                    k = chr(m)
                i += 1
                for answerQuestionnaire in answerQuestionnaires:
                    answerQuestion = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                 answerQuestionnaireId=answerQuestionnaire.id)
                    answerQuestionId = answerQuestion.id
                    AnswerOptions1 = AnswerOptions.objects.filter(answerQuestionId=answerQuestionId)
                    AnswerOption1 = AnswerOptions1[0]
                    optionContent = AnswerOption1.optionContent
                    if '1' in optionContent: myQuestion[0]['Num'] += 1
                    for index in range(2, question.choiceAmount + 1):
                        if str(index) in optionContent: myQuestion[index - 1]['Num'] += 1
                    myQuestion[0]['answernum'] += 1
                # params.append({'answernum':k});#每道题填写人数
                params.append(myQuestion)
            #     填空题
            elif question.questionTypeId == 2:
                questionAmounts = len(answerQuestionnaires)
                answerQuestionId = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                               answerQuestionnaireId=answerQuestionnaires[0].id).id
                answer1 = AnswerOptions.objects.get(answerQuestionId=answerQuestionId).completionContent
                myQuestion.append(
                    {'num': i, 'id': question.id,'type':2, 'answernum': 0, "question": question.questionTitle,'answer':answer1})
                for index in range(1,questionAmounts):
                    answerQuestionnaire = answerQuestionnaires[index]
                    answerQuestionId = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                   answerQuestionnaireId=answerQuestionnaire.id).id

                    completionContent = AnswerOptions.objects.get(answerQuestionId=answerQuestionId).completionContent
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
                    optionScore1 = int(AnswerOptions.objects.get(answerQuestionId=answerQuestionId,answerOptionOrder = 1).optionScore)
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
                    optionScore1 = int(AnswerOptions.objects.get(answerQuestionId=answerQuestionId,
                                                             answerOptionOrder=1).optionScore)
        #             取得评价
                    optionScoreText1 = AnswerOptions.objects.get(answerQuestionId=answerQuestionId,
                                                             answerOptionOrder=1).optionScoreText

                    myQuestion[optionScore1-1]['Num'] += 1
                    myQuestion[optionScore1-1]['comment'].append({'cont':optionScoreText1})
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
# def getAnswer(request):
#     if request.method == 'POST':
#         questionnaireId = json.loads(request.body).get("questionnaireId");
#         params = [];
#         answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId)
#         # 遍历每个答卷
#         for answerQuestionnaire in answerQuestionnaires:
#             answers = [];
#             answerQuestions = AnswerQuestions.objects.filter(answerQuestionnaireId = answerQuestionnaire.id)
#             i = 1;
#             # 答卷中的每道题
#             for answerQuestion in answerQuestions:
#
#                 myOption = AnswerOptions.objects.get(answerQuestionId = answerQuestion.id)
#                 if myOption.optionType == 1:
#
#                     answers.append({"answer": myOption.optionContent});
#                     i+=1
#                 if myOption.optionType == 2:
#                     answers.append({"answer": myOption.completionContent});
#                     i += 1
#                 if myOption.optionType == 3:
#                     answers.append({"answer": myOption.optionScore});
#                     i += 1
#
#             params.append(answers)
#
#         return JsonResponse({
#             "status":200,
#             "data":params,
#             "result":"获取答题情况成功"
#         })
#     else:
#         return JsonResponse({
#             "status": 401,
#             "result": "请求方式错误"
#         })


def getAnswer(request):
    if request.method == 'POST':
        questionnaireId = json.loads(request.body).get("questionnaireId");
        params = [];
        questions = Questions.objects.filter(questionnaireId=questionnaireId)
        answerQuestionnaires = AnswerQuestionnaire.objects.filter(questionnaireId = questionnaireId)
        cnt = 1;count=0;
        for question in questions :
            params.append({'id':cnt})
            cnt += 1
            i = 1

            for answerQuestionnaire in answerQuestionnaires:
                if question.questionTypeId == 1  or question.questionTypeId == 6:
                    AnswerQuestion = AnswerQuestions.objects.get(answerQuestionId=question.id,answerQuestionnaireId=answerQuestionnaire.id)
                    AnswerOption = AnswerOptions.objects.get(answerQuestionId=AnswerQuestion.id)
                    params[count]['answer'+str(i)] =AnswerOption.optionContent
                    i+=1
                if question.questionTypeId == 5:
                    AnswerQuestion = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                 answerQuestionnaireId=answerQuestionnaire.id)
                    AnswerOptions1 = AnswerOptions.objects.filter(answerQuestionId=AnswerQuestion.id)
                    AnswerOption = AnswerOptions1[0]
                    params[count]['answer' + str(i)] = AnswerOption.optionContent
                    i += 1
                if question.questionTypeId == 2:
                    AnswerQuestion = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                 answerQuestionnaireId=answerQuestionnaire.id)
                    params[count]['answer' + str(i)] = AnswerQuestion.answerText;i+=1
                if question.questionTypeId == 3:
                    AnswerQuestion = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                 answerQuestionnaireId=answerQuestionnaire.id)
                    AnswerOption = AnswerOptions.objects.get(answerQuestionId=AnswerQuestion.id)
                    params[count]['answer' + str(i)] = AnswerOption.optionScore
                    i += 1
                if question.questionTypeId == 4 :
                    AnswerQuestion = AnswerQuestions.objects.get(answerQuestionId=question.id,
                                                                 answerQuestionnaireId=answerQuestionnaire.id)
                    AnswerOption = AnswerOptions.objects.get(answerQuestionId=AnswerQuestion.id)
                    params[count]['answer' + str(i)] = AnswerOption.optionScore
                    params[count]['comment' + str(i)] = AnswerOption.optionScoreText
                    i += 1

            count += 1
        return JsonResponse({
            "status":200,
            "data":params,
            "result":"获取答题结果成功"
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

# 时间倒序
def sortBySetUpTimeDesc(request):
    if request.method == "GET":
        Questionnaires = QuestionnaireInformation.objects.all().order_by('setUpTime')
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
        Questionnaire = QuestionnaireInformation.objects.get(id = params.get("questionnaireId"))
        Questionnaire.recoveryAmount += 1;


        answerQuestionnaire.commitTime = datetime.datetime.now()

        if Questionnaire.questionnaireType == 2:
            answerQuestionnaire.answerId = params.get("examinee")
            # 防止重复答卷
            if len(AnswerQuestionnaire.objects.filter(answerId=answerQuestionnaire.answerId,
                                                      questionnaireId=params.get("questionnaireId"))) >=1:
                return JsonResponse({
                    "status":302,
                    "result":"请勿重复答卷"
                })
            # 选择题得分
            choiceQuestionScore = 0
            myScore = 0
        Questionnaire.save()
        answerQuestionnaire.save()
        for index in range(0,questionAmount):
            newAnswerQuestion = AnswerQuestions()
            newAnswerQuestion.answerQuestionnaireId = answerQuestionnaire.id
            newAnswerQuestion.answerQuestionId = Questions.objects.get(questionnaireId=answerQuestionnaire.questionnaireId,
                                                                       questionOrder=index+1).id
            newAnswerQuestion.questionTypeId = Questions.objects.get(id = newAnswerQuestion.answerQuestionId).questionTypeId
            newAnswerQuestion.answerOrder = index + 1

            if newAnswerQuestion.questionTypeId == 2:
                newAnswerQuestion.answerText = newAnswerQuestions[index]['answer']
            newAnswerQuestion.save()

            if newAnswerQuestion.questionTypeId == 1 or newAnswerQuestion.questionTypeId == 6 :
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType = 1;
                newAnswerOption.optionContent = newAnswerQuestions[index]['answer']
                newAnswerOption.answerOptionOrder = newAnswerQuestions[index]['answer']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                newAnswerOption.answerOptionId = Options.objects.get(questionId= newAnswerQuestion.answerQuestionId,
                                                                     optionOrder= newAnswerOption.answerOptionOrder).id
                # 考试问卷 选择题评分
                if Questionnaire.questionnaireType == 2:
                    question = Questions.objects.get(id = newAnswerQuestion.answerQuestionId)
                    if newAnswerQuestions[index]['answer'] == question.key:
                        myScore += question.score
                        newAnswerQuestion.thisScore = question.score
                    else:
                        newAnswerQuestion.thisScore = 0
                    choiceQuestionScore += question.score
                    newAnswerQuestion.save()
                newAnswerOption.save()
            elif newAnswerQuestion.questionTypeId == 5 :
                answer = newAnswerQuestions[index]['answer']
                answerAmount = len(answer)
                for i in range(0,answerAmount):
                    newAnswerOption = AnswerOptions()
                    newAnswerOption.optionType = 1;
                    newAnswerOption.optionContent = newAnswerQuestions[index]['answer']
                    newAnswerOption.answerOptionOrder = newAnswerQuestions[index]['answer'][i]
                    newAnswerOption.answerQuestionId = newAnswerQuestion.id
                    newAnswerOption.answerOptionId = Options.objects.get(questionId=newAnswerQuestion.answerQuestionId,
                                                                         optionOrder=newAnswerOption.answerOptionOrder).id
                    # 考试问卷 多选题评分
                    if Questionnaire.questionnaireType == 2:
                        question = Questions.objects.get(id=newAnswerQuestion.answerQuestionId)
                        if newAnswerQuestions[index]['answer'] == question.key:
                            myScore += question.score
                            newAnswerQuestion.thisScore = question.score
                        elif newAnswerQuestions[index]['answer'] in question.key:
                            myScore += question.score//2
                            newAnswerQuestion.thisScore = question.score//2
                        else:
                            newAnswerQuestion.thisScore = 0
                        choiceQuestionScore += question.score
                        newAnswerQuestion.save()
                    newAnswerOption.save()


            elif newAnswerQuestion.questionTypeId == 2:
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType = 2;
                newAnswerOption.optionContent = 1
                newAnswerOption.answerOptionOrder = 1
                newAnswerOption.completionContent = newAnswerQuestions[index]['answer']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                # newAnswerOption.answerOptionId = Options.objects.get(questionId=newAnswerQuestion.answerQuestionId,
                #                                                      ).id
                newAnswerOption.answerOptionId = -1
                newAnswerOption.save()
            elif newAnswerQuestion.questionTypeId == 3:
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType = 3;
                newAnswerOption.optionContent = 1
                newAnswerOption.answerOptionOrder = 1
                newAnswerOption.optionScore = newAnswerQuestions[index]['answer']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                # newAnswerOption.answerOptionId = Options.objects.get(questionId=newAnswerQuestion.answerQuestionId,
                #                                                      ).id
                newAnswerOption.answerOptionId = -1
                newAnswerOption.save()
            elif newAnswerQuestion.questionTypeId == 4:
                newAnswerOption = AnswerOptions()
                newAnswerOption.optionType = 3;
                newAnswerOption.optionContent = 1
                newAnswerOption.answerOptionOrder = 1
                newAnswerOption.optionScore = newAnswerQuestions[index]['answer']
                newAnswerOption.optionScoreText = newAnswerQuestions[index]['comment']
                newAnswerOption.answerQuestionId = newAnswerQuestion.id
                # newAnswerOption.answerOptionId = Options.objects.get(questionId=newAnswerQuestion.answerQuestionId,
                #                                                      ).id
                newAnswerOption.answerOptionId = -1
                newAnswerOption.save()

        if Questionnaire.questionnaireType == 2:
            return JsonResponse({
                "status" : 200,
                "result" : "提交问卷成功",
                "totalChoiceScore":choiceQuestionScore,
                "myChoiceScore":myScore
            })
        else:
            return JsonResponse({
            "status" : 200,
            "result" : "提交问卷成功"
        })
    else:
        return JsonResponse({
            'status':400,
            'result':"请求方式错误"
        })


# 考试问卷评分
def markQuestionnaire(request):
    if request.method == 'POST':
        totalScore = 0
        params = json.loads(request.body)
        studentId = params.get("studentId")
        questionnaireId = params.get("questionnaireId")
        scores = params.get("scores")
        answerQuestionnaire = AnswerQuestionnaire.objects.get(answerId=studentId,questionnaireId=questionnaireId)
        answerQuestions = AnswerQuestions.objects.filter(answerQuestionnaireId=answerQuestionnaire.id)
        index = 0
        for answerQuestion in answerQuestions:
            question = Questions.objects.get(id=answerQuestion.answerQuestionId)
            # 选择题分数自动评价
            if question.questionTypeId == 1 or question.questionTypeId ==5 or question.questionTypeId ==6:
                totalScore += answerQuestion.thisScore
            # 其他题分数教师评价
            else:
                totalScore += scores[index]['score']
                answerQuestion.thisScore = scores[index]['score']
        answerQuestionnaire.myScore = totalScore
        answerQuestionnaire.save()
        return JsonResponse({
            "status":200,
            "result":"评分成功",
            "totalScore":totalScore
        })

# 保存问卷（创建问卷）
def saveQuestionnaire(request):
    if request.method == 'POST':
        information = json.loads(request.body.decode())
        authorId = information.get('authorId')
        print(authorId)
        problems = information.get('questionList')
        questionAmount = len(problems)
        questionnaireType = information.get("questionnaireType");
        if questionnaireType is None:
                questionnaireType = 1
        try:
            questionnaire = QuestionnaireInformation(
                authorId=authorId,
                questionnaireTitle=information.get('questionnaireTitle'),
                questionnaireInformation=information.get('questionnaireInformation'),
                maxRecovery=information.get('maxRecovery'),
                questionAmount=questionAmount,
                currentState=False,
                questionnaireType=questionnaireType,
                insertQuestionNumber=information.get('insertQuestionNumber'),
                outOfOrder=information.get('outOfOrder')
            )
            if questionnaireType == 2:
                questionnaire.totalScore = information.get("totalScore")
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
                    questionOrder=i,
                    questionInformation=problem.get('questionInformation'),
                    outOfOrder=problem.get('outOfOrder'),
                )
                if questionnaireType == 2:
                    question.key = problem.get("key")
                    question.score = problem.get("score")
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
                        if questionnaireType == 3:
                            op.maxQuota = option.get('maxQuota')
                            op.currentQuota = option.get('currentQuota')
                            op.limitNumber = option.get('limitNumber')
                        op.save()
                        j=j+1
            return JsonResponse({'status': 200, 'result': "保存成功"})
        except Exception:
            return JsonResponse({'status': 300, 'result': "保存问卷失败"})
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
            return JsonResponse({'status': 300, 'result': "没有找到问卷"})
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
        authorId = req.get('authorId')
        if True:
            res = {}
            try:
                if method == 1:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('setUpTime')
                elif method == -1:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('-setUpTime')
                elif method == 2:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('startTime')
                elif method == -2:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('-startTime')
                elif method == 3:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('recoveryAmount')
                elif method == -3:
                    questionnaires = QuestionnaireInformation.objects.filter(authorId=authorId).order_by('-recoveryAmount')
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
                                'latestAlterTime': questionnaire.latestAlterTime,
                                'lastEndTime': questionnaire.lastEndTime,
                            }
                        )
                    res['questionnaireList'] = questionnaireList
                    res['status'] = 200
                    res['result'] = "获取成功"
                    return JsonResponse(res)
                else:
                    return JsonResponse({'status': 300, 'result': "用户没有创建问卷记录"})
            except Exception:
                return JsonResponse({'status': 301, 'result': "获取信息出错"})
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
                            'selectNumber': option.selectNumber,
                            'maxQuota': option.maxQuota,
                            'currentQuota': option.currentQuota,
                            'limitNumber': option.limitNumber
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
                        'questionInformation': question.questionInformation,
                        'outOfOrder': question.outOfOrder,
                        'score': question.score,
                        'key': question.key,
                        'optionList': optionList,
                    }
                )
            res = {
                'questionnaireTitle': questionnaire.questionnaireTitle,
                'questionnaireInformation': questionnaire.questionnaireInformation,
                'questionAmount': questionnaire.questionAmount,
                'lastEndTime': questionnaire.lastEndTime,
                'insertQuestionNumber': questionnaire.insertQuestionNumber,
                'outOfOrder': questionnaire.outOfOrder,
                'questionnaireType': questionnaire.questionnaireType,
                'totalScore': questionnaire.totalScore,
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
        if True:
            try:
                information = json.loads(request.body.decode())
                oldQuestionnaireId = information.get('questionnaireId')
                print(oldQuestionnaireId)
                oldQuestions = Questions.objects.filter(questionnaireId=oldQuestionnaireId)
                for oldQuestion in oldQuestions:
                    oldQuestion.delete()
                problems = information.get('questionList')
                questionAmount = len(problems)
                questionnaire = QuestionnaireInformation.objects.get(id=oldQuestionnaireId)
                questionnaire.questionnaireTitle = information.get('questionnaireTitle')
                questionnaire.questionnaireInformation = information.get('questionnaireInformation')
                questionnaire.maxRecovery = information.get('maxRecovery')
                questionnaire.questionAmount = questionAmount
                questionnaireType = information.get('questionnaireType')
                if questionnaireType is None:
                    questionnaireType = 1
                if questionnaireType == 2:
                    totalScore = information.get('totalScore')
                    questionnaire.totalScore = totalScore
                questionnaire.insertQuestionNumber = information.get('insertQuestionNumber')
                questionnaire.outOfOrder = information.get('outOfOrder')
                questionnaire.questionnaireType = questionnaireType
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
                        questionOrder=i,
                        questionInformation=problem.get('questionInformation'),
                        outOfOrder=problem.get('outOfOrder'),
                    )
                    if questionnaireType == 2:
                        question.score = problem.get('score')
                        question.key = problem.get('key')
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
                            if questionnaireType == 3:
                                op.limitNumber = option.get('limitNumber')
                                op.maxQuota = option.get('maxQuota')
                            op.save()
                            j = j+1
                return JsonResponse({'status': 200, 'result': "保存成功"})
            except Exception:
                return JsonResponse({'status': 400, 'result': "保存问卷失败"})
        else:
            return JsonResponse({'status': 401, 'result': "用户未登录"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})

# 问卷修改（发布后）
def modifyQuestionnaire(request):
    if request.method == 'POST':
        information = json.loads(request.body.decode())
        if information.get('authorId'):
            try:
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
                return JsonResponse({'status': 300, 'result': "修改失败"})
        else:
            return JsonResponse({'status': 400, 'result': "用户未登录"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})


# def returnSession(request):
#     return JsonResponse({
#         "myid":myId
#     })

# 获取问卷id

# def getQuestionnaireId(request):
#     if request.method == 'GET':
#         global myId
#         k = myId
#         questionnaireIds = QuestionnaireInformation.objects.filter(authorId=myId)
#         myId = k
#         data = []
#         for questionnaireId in questionnaireIds:
#             data.append({'id':questionnaireId.id})
#         return JsonResponse({
#             "status":200,
#             "data":data,
#             "result":"获取成功"
#         })

# 彻底删除问卷
def deleteCompletelyQuestionnaire(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        questionnaireId = req.get('questionnaireId')
        questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId)
        questionnaire.delete()
        return JsonResponse({'status': 200, 'result': "删除成功"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})

# 复制问卷
def copyQuestionnaire(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        questionnaireId = req.get('questionnaireId')
        oldQuestionnaire = QuestionnaireInformation.objects.get(id=questionnaireId)
        newQuestionnaire = QuestionnaireInformation(
            authorId=oldQuestionnaire.authorId,
            questionnaireTitle=oldQuestionnaire.questionnaireTitle + "-副本",
            questionnaireInformation=oldQuestionnaire.questionnaireInformation,
            maxRecovery=oldQuestionnaire.maxRecovery,
            questionAmount=oldQuestionnaire.questionAmount,
            totalScore=oldQuestionnaire.totalScore,
            insertQuestionNumber=oldQuestionnaire.insertQuestionNumber,
            outOfOrder=oldQuestionnaire.outOfOrder,
            questionnaireType=oldQuestionnaire.questionnaireType,
            currentState=False
        )
        newQuestionnaire.save()
        newQuestionnaireId = newQuestionnaire.id
        oldQuestions = Questions.objects.filter(questionnaireId=questionnaireId)
        for oldQuestion in oldQuestions:
            oldQuestionId = oldQuestion.id
            newQuestion = Questions(
                questionnaireId=newQuestionnaireId,
                questionTitle=oldQuestion.questionTitle,
                questionTypeId=oldQuestion.questionTypeId,
                required=oldQuestion.required,
                multipleChoice=oldQuestion.multipleChoice,
                choiceAmount=oldQuestion.choiceAmount,
                questionOrder=oldQuestion.questionOrder,
                questionInformation=oldQuestion.questionInformation,
                outOfOrder=oldQuestionnaire.outOfOrder,
                score=oldQuestion.score,
                key=oldQuestion.key
            )
            newQuestion.save()
            newQuestionId = newQuestion.id
            oldOptions = Options.objects.filter(questionId=oldQuestionId)
            for oldOption in oldOptions:
                newOption = Options(
                    questionId=newQuestionId,
                    optionOrder=oldOption.optionOrder,
                    required=oldOption.required,
                    optionContent=oldOption.optionContent,
                    optionType=oldOption.optionType,
                    optionScore=oldOption.optionScore,
                    optionText=oldOption.optionText,
                    selectNumber=oldOption.selectNumber,
                    maxQuota=oldOption.maxQuota,
                    currentQuota=oldOption.currentQuota,
                    limitNumber=oldOption.limitNumber
                )
                newOption.save()
        return JsonResponse({'status': 200, 'result': "复制成功"})
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})

# 生成回答界面所需的数据
def getAnswerQuestionnaireInterface(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        questionnaireId = req.get('questionnaireId')
        try:
            questionnaire = QuestionnaireInformation.objects.get(id=questionnaireId)
        except Exception:
            return JsonResponse({'status': 400, 'result': "找不到该问卷"})
        else:
            questionOutOfOrder = questionnaire.outOfOrder
            questionList = []
            questions = Questions.objects.filter(questionnaireId=questionnaireId).order_by('questionOrder')
            for question in questions:
                questionId = question.id
                optionOutOfOrder = question.outOfOrder
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
                            'selectNumber': option.selectNumber,
                            'maxQuota': option.maxQuota,
                            'currentQuota': option.currentQuota,
                            'limitNumber': option.limitNumber
                        }
                    )
                if optionOutOfOrder == True:
                    random.shuffle(optionList)
                questionList.append(
                    {
                        'questionId': question.id,
                        'questionTitle': question.questionTitle,
                        'questionTypeId': question.questionTypeId,
                        'required': question.required,
                        'multipleChoice': question.multipleChoice,
                        'choiceAmount': question.choiceAmount,
                        'questionOrder': question.questionOrder,
                        'questionInformation': question.questionInformation,
                        'outOfOrder': question.outOfOrder,
                        'score': question.score,
                        'key': question.key,
                        'optionList': optionList,
                    }
                )
            if questionOutOfOrder == True:
                random.shuffle(questionList)
            res = {
                'questionnaireTitle': questionnaire.questionnaireTitle,
                'questionnaireInformation': questionnaire.questionnaireInformation,
                'questionAmount': questionnaire.questionAmount,
                'lastEndTime': questionnaire.lastEndTime,
                'insertQuestionNumber': questionnaire.insertQuestionNumber,
                'outOfOrder': questionnaire.outOfOrder,
                'questionnaireType': questionnaire.questionnaireType,
                'totalScore': questionnaire.totalScore,
                'questionList': questionList,

                'status': 200,
                'result': "获取问卷信息成功"
            }
            return JsonResponse(res)
    else:
        return JsonResponse({'status': 401, 'result': "请求方式错误"})
