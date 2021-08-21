from django.db import models


# Create your models here.

# 问卷信息
class QuestionnaireInformation(models.Model):
    # 发起者Id
    authorId = models.IntegerField(null=False,unique=True)
    # 问卷标题
    questionnaireTitle = models.CharField(max_length=32,null=False),
    # 问卷介绍
    questionnaireInformation = models.CharField(max_length=255),
    # 创建时间
    setUpTime = models.DateField(auto_now_add=True),
    # 最近修改时间
    latestAlterTime = models.DateField(auto_now=True),
    # 问卷发布时间
    startTime = models.DateField,
    # 问卷结束时间(设定的结束时间)
    endTime = models.DateField,
    # 问卷截止时间（最终真正结束时间）
    lastEndTime = models.DateField,
    # 回收问卷上限
    maxRecovery = models.IntegerField(default=9999),
    # 当前问卷状态（是否可回收）
    currentState = models.BooleanField(default=True),
    # 题目数量
    questionAmount = models.IntegerField(default=0),
    # 回收问卷数量
    recoveryAmount = models.IntegerField(default=0),
#     是否已删除
    deleted = models.BooleanField(default=False)
#     题目是否乱序

# 问卷中的题目
class Questions(models.Model):
    # 所属问卷id
    questionnaireId = models.IntegerField(null=False,unique=True),
    # 题干
    questionTitle = models.CharField(max_length=255),
    # 题目类型id
    questionTypeId = models.IntegerField(null=False,unique=True),
    # 是否必填
    required = models.BooleanField(null=False),
    # 是否多选
    multipleChoice = models.BooleanField(null=True),
    # 选项数
    choiceAmount = models.IntegerField(null=True),
    # 所属问卷中的顺序
    questionOrder = models.IntegerField
#     选项是否乱序


# 题目类型
class QuestionType(models.Model):
    # 题目类型id
    # 1：选择题 2.填空题 3.简单评分 4.高级评分
    questionTypeId = models.IntegerField(primary_key=True, null=False),
    # 题目类型名
    questionTypeName = models.CharField(null=False,max_length=255)


# 选项内容设置
class Options(models.Model):
    # 所属题目id
    questionId = models.IntegerField(null=False,unique=True),
    # 在所属题目中的顺序
    optionOrder = models.IntegerField(null=False),
    # 是否必填
    required = models.BooleanField,
    # 选项文字描述
    optionContent = models.CharField(max_length=255),
    # 选项类型 1选择，2填空，3评分
    optionType = models.IntegerField,
    # 选项评分 -1表示这个选项没有评分的功能，其他正数表示评分最大是多少
    optionScore = models.IntegerField(default=-1),
    # 评分是否有评价
    optionText = models.BooleanField


# 回收问卷信息
class AnswerQuestionnaire(models.Model):
    # 所属问卷id
    questionnaireId = models.IntegerField(null=False,unique=True),
    # 填写者Id 匿名时为空
    answerId = models.IntegerField(null=True,unique=True),
    # 提交时间
    commitTime = models.DateField(auto_now_add=True)


# 回收问卷的题目信息
class AnswerQuestions(models.Model):
    # 填写问卷时要获取题目，返回填写结果时要把题目id也返回
    # id为自增
    # 回收题目id
    answerQuestionId = models.IntegerField(unique=True),
    # 所属回收问卷id
    answerQuestionnaireId = models.IntegerField(unique=True),
    # 所属回收问卷中的顺序
    answerOrder = models.IntegerField,
    # 题目类型id
    questionTypeId = models.IntegerField(unique=True),
    # 填写的内容(填空题)
    answerText = models.TextField(null=True)


# 回收题目的选项信息
class AnswerOptions(models.Model):
    # 所属回收题目id
    answerQuestionId = models.IntegerField,
    # 回收选项id
    answerOptionId = models.IntegerField(unique=True),
#     所属回收题目中的顺序
    answerOptionOrder = models.IntegerField,
#     选项类型 1选择，2填空，3评分
    optionType = models.IntegerField,
#     选择内容
    optionContent = models.CharField(max_length=255),
#     填空内容
    completionContent = models.CharField(null=True,max_length=255),
#     选项评分
    optionScore = models.CharField(null=True,max_length=255),
#     选项评分的评价
    optionScoreText = models.TextField(null=True)


