# Generated by Django 2.2.16 on 2020-12-18 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_nbs_ca', '0025_auto_20201217_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='countries',
            name='code',
            field=models.CharField(default=1, max_length=5, verbose_name='Code'),
            preserve_default=False,
        ),
    ]