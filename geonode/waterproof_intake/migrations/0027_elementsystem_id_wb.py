# Generated by Django 2.2.16 on 2021-01-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_intake', '0026_elementsystem_is_external'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementsystem',
            name='id_wb',
            field=models.IntegerField(default=0, verbose_name='Year'),
        ),
    ]
