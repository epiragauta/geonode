# Generated by Django 2.2.16 on 2021-07-07 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_study_cases', '0005_remove_studycases_currency_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='studycases',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Is public'),
        ),
        migrations.AddField(
            model_name='studycases',
            name='path_study_case_error_log',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='studycases',
            name='path_study_case_pdf',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
