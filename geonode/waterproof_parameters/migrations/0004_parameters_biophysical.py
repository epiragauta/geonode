# Generated by Django 2.2.16 on 2021-05-05 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_intake', '0002_auto_20210504_2159'),
        ('waterproof_study_cases', '0003_studycases_currency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waterproof_parameters', '0003_auto_20210329_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameters_Biophysical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lucode', models.IntegerField(blank=True, null=True)),
                ('lulc_desc', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('kc', models.FloatField(blank=True, null=True)),
                ('root_depth', models.FloatField(blank=True, null=True)),
                ('usle_c', models.FloatField(blank=True, null=True)),
                ('usle_p', models.FloatField(blank=True, null=True)),
                ('load_n', models.FloatField(blank=True, null=True)),
                ('eff_n', models.FloatField(blank=True, null=True)),
                ('load_p', models.FloatField(blank=True, null=True)),
                ('eff_p', models.FloatField(blank=True, null=True)),
                ('crit_len_n', models.IntegerField(blank=True, null=True)),
                ('crit_len_p', models.IntegerField(blank=True, null=True)),
                ('proportion_subsurface_n', models.FloatField(blank=True, null=True)),
                ('cn_a', models.FloatField(blank=True, null=True)),
                ('cn_b', models.FloatField(blank=True, null=True)),
                ('cn_c', models.FloatField(blank=True, null=True)),
                ('cn_d', models.FloatField(blank=True, null=True)),
                ('kc_1', models.FloatField(blank=True, null=True)),
                ('kc_2', models.FloatField(blank=True, null=True)),
                ('kc_3', models.FloatField(blank=True, null=True)),
                ('kc_4', models.FloatField(blank=True, null=True)),
                ('kc_5', models.FloatField(blank=True, null=True)),
                ('kc_6', models.FloatField(blank=True, null=True)),
                ('kc_7', models.FloatField(blank=True, null=True)),
                ('kc_8', models.FloatField(blank=True, null=True)),
                ('kc_9', models.FloatField(blank=True, null=True)),
                ('kc_10', models.FloatField(blank=True, null=True)),
                ('kc_11', models.FloatField(blank=True, null=True)),
                ('kc_12', models.FloatField(blank=True, null=True)),
                ('c_above', models.FloatField(blank=True, null=True)),
                ('c_below', models.FloatField(blank=True, null=True)),
                ('c_soil', models.FloatField(blank=True, null=True)),
                ('c_dead', models.FloatField(blank=True, null=True)),
                ('sed_exp', models.FloatField(blank=True, null=True)),
                ('sed_ret', models.FloatField(blank=True, null=True)),
                ('rough_rank', models.FloatField(blank=True, null=True)),
                ('cover_rank', models.FloatField(blank=True, null=True)),
                ('p_ret', models.FloatField(blank=True, null=True)),
                ('p_exp', models.FloatField(blank=True, null=True)),
                ('n_ret', models.FloatField(blank=True, null=True)),
                ('n_exp', models.FloatField(blank=True, null=True)),
                ('native_veg', models.IntegerField(blank=True, null=True)),
                ('lulc_veg', models.IntegerField(blank=True, null=True)),
                ('macro_region', models.TextField(blank=True, null=True)),
                ('default', models.TextField(blank=True, null=True)),
                ('intake', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='waterproof_intake.Intake')),
                ('study_case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='waterproof_study_cases.StudyCases')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'waterproof_parameters_biophysical',
                'managed': True,
            },
        ),
    ]
