# Generated by Django 2.2.16 on 2020-12-12 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_nbs_ca', '0018_auto_20201212_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='factor',
            field=models.CharField(max_length=50, verbose_name='Factor'),
        ),
    ]