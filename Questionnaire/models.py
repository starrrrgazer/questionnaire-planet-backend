from django.db import models
import datetime


# Create your models here.

# 问卷信息
class QuestionnaireInformation(models.Model):
    # 发起者Id
    authorId = models.IntegerField(null=False)
    # 问卷标题
    questionnaireTitle = models.CharField(max_length=256, null=False)
    # 问卷介绍
    questionnaireInformation = models.CharField(max_length=1024)
    # 创建时间
    setUpTime = models.DateTimeField(auto_now_add=True,null=True)
    # 最近修改时间
    latestAlterTime = models.DateTimeField(auto_now=True,null=True)
    # 问卷发布时间
    startTime = models.DateTimeField(null=True)
    # 问卷结束时间(最近一次停止发布的时间)
    endTime = models.DateTimeField(null=True)
    # 问卷截止时间（最终真正结束时间）
    lastEndTime = models.DateTimeField(null=True)
    # 回收问卷上限
    maxRecovery = models.IntegerField(default=9999)
    # 当前问卷状态（是否可回收）
    currentState = models.BooleanField(default=False)
    # 题目数量
    questionAmount = models.IntegerField(default=0)
    # 回收问卷数量
    recoveryAmount = models.IntegerField(default=0)
#     是否已删除
    deleted = models.BooleanField(default=False)
#     总分
    totalScore = models.IntegerField(null=True)
    # 问卷种类
    questionnaireType = models.IntegerField(default=1)
#     题目是否乱序
    outOfOrder = models.BooleanField(default=False)
    # 是否插入题号
    insertQuestionNumber = models.BooleanField(default=True)
#     考试时间
    examTime = models.IntegerField(null=True)

# 问卷中的题目
class Questions(models.Model):
    # 所属问卷id
    questionnaireId = models.IntegerField(null=False,unique=False)
    # 题干
    questionTitle = models.CharField(max_length=512)
    # 题目描述
    questionInformation = models.CharField(max_length=512,null=True)
    # 题目类型id
    questionTypeId = models.IntegerField(null=False,unique=False)
    # 是否必填
    required = models.BooleanField(null=False,default=False)
    # 是否多选
    multipleChoice = models.BooleanField(null=True)
    # 选项数
    choiceAmount = models.IntegerField(null=True)
    # 所属问卷中的顺序
    questionOrder = models.IntegerField(default=1)
#   本题分数
    score = models.IntegerField(null=True)
#    本题答案
    key = models.CharField(null=True,max_length=255)
#     选项是否乱序
    outOfOrder = models.BooleanField(default=False)


# 题目类型
class QuestionType(models.Model):
    # 题目类型id
    id = models.IntegerField()
    # 1：选择题 2.填空题 3.简单评分 4.高级评分
    questionTypeId = models.IntegerField(primary_key=True, null=False)
    # 题目类型名
    questionTypeName = models.CharField(null=False,max_length=255)


# 选项内容设置
class Options(models.Model):
    # 所属题目id
    questionId = models.IntegerField(null=False,unique=False)
    # 在所属题目中的顺序
    optionOrder = models.IntegerField(null=False)
    # 是否必填
    required = models.BooleanField(default=False)
    # 选项文字描述
    optionContent = models.CharField(max_length=255)
    # 选项类型 1选择，2填空，3评分
    optionType = models.IntegerField()
    # 选项评分 -1表示这个选项没有评分的功能，其他正数表示评分最大是多少
    optionScore = models.IntegerField(default=-1)
    # 评分是否有评价
    optionText = models.BooleanField(default=False)
    # 最大名额
    maxQuota = models.IntegerField(null=True)
    # 当前剩余名额
    currentQuota = models.IntegerField(null=True)
    # 是否限额
    limitNumber = models.BooleanField(default=False)
    # 已选该选项的人数
    selectNumber = models.IntegerField(default=0)

# 回收问卷信息
class AnswerQuestionnaire(models.Model):
    # 所属问卷id
    questionnaireId = models.IntegerField(null=False)
    # 填写者Id 匿名时为空
    answerId = models.IntegerField(null=True,unique=True)
    # 提交时间
    commitTime = models.DateTimeField(auto_now_add=True)
#     问卷得分
    myScore = models.IntegerField(null=True)
    # 定位信息
    position = models.CharField(max_length=256,null=True)


# 回收问卷的题目信息
class AnswerQuestions(models.Model):
    # 填写问卷时要获取题目，返回填写结果时要把题目id也返回
    # id为自增
    # 题目id
    answerQuestionId = models.IntegerField(unique=False)
    # 所属回收问卷id
    answerQuestionnaireId = models.IntegerField(unique=False)
    # 所属回收问卷中的顺序
    answerOrder = models.IntegerField(null=True)
    # 题目类型id
    questionTypeId = models.IntegerField(unique=False,default=1)
    # 填写的内容(填空题)
    answerText = models.TextField(null=True)
#     本题得分(考试问卷)
    thisScore = models.IntegerField(null=True)


# 回收题目的选项信息
class AnswerOptions(models.Model):
    # 所属回收题目id
    answerQuestionId = models.IntegerField()
    # 回收选项
    answerOptionId = models.IntegerField(unique=False)
#     所属回收题目中的顺序
    answerOptionOrder = models.IntegerField()
#     选项类型 1选择，2填空，3评分
    optionType = models.IntegerField(null=False)
#     选择内容
    optionContent = models.CharField(max_length=255)
#     填空内容
    completionContent = models.CharField(null=True,max_length=255)
#     选项评分
    optionScore = models.IntegerField(null=True)
#     选项评分的评价
    optionScoreText = models.TextField(null=True)


