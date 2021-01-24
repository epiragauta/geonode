# Generated by Django 2.2.16 on 2020-12-17 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_nbs_ca', '0023_auto_20201217_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterproofnbsca',
            name='unit_implementation_cost',
            field=models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Unit implementation costs (US $/ha)'),
        ),
        migrations.AlterField(
            model_name='waterproofnbsca',
            name='unit_maintenance_cost',
            field=models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Unit maintenance costs (US $/ha)'),
        ),
        migrations.AlterField(
            model_name='waterproofnbsca',
            name='unit_oportunity_cost',
            field=models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Unit oportunity costs (US $/ha)'),
        ),
    ]