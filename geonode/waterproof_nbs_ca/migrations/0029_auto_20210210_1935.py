# Generated by Django 2.2.16 on 2021-02-10 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_nbs_ca', '0028_auto_20210210_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterproofnbsca',
            name='activity_shapefile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waterproof_nbs_ca.ActivityShapefile'),
        ),
    ]
