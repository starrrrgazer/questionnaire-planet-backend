# Generated by Django 3.2.5 on 2021-08-21 08:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0011_alter_answerquestions_answerquestionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaireinformation',
            name='endTime',
            field=models.DateField(default=datetime.datetime(2021, 8, 21, 16, 53, 44, 269697)),
        ),
        migrations.AddField(
            model_name='questionnaireinformation',
            name='lastEndTime',
            field=models.DateField(default=datetime.datetime(2021, 8, 21, 16, 53, 44, 269697)),
        ),
        migrations.AddField(
            model_name='questionnaireinformation',
            name='startTime',
            field=models.DateField(default=datetime.datetime(2021, 8, 21, 16, 53, 44, 269697)),
        ),
        migrations.AddField(
            model_name='questions',
            name='questionOrder',
            field=models.IntegerField(default=1),
        ),
    ]