# Generated by Django 3.2.5 on 2021-08-21 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0017_auto_20210821_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaireinformation',
            name='startTime',
            field=models.DateField(null=True),
        ),
    ]