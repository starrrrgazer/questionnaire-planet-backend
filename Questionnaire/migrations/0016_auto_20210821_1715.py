# Generated by Django 3.2.5 on 2021-08-21 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0015_auto_20210821_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaireinformation',
            name='endTime',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='questionnaireinformation',
            name='lastEndTime',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='questionnaireinformation',
            name='startTime',
            field=models.DateField(),
        ),
    ]