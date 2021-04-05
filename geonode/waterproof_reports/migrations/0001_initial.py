# Generated by Django 2.2.16 on 2021-04-05 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invest_indicators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('Type', models.CharField(max_length=250, verbose_name='type')),
                ('Path', models.CharField(max_length=250, verbose_name='Path')),
                ('value', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='value')),
                ('user_id', models.IntegerField(max_length=100, verbose_name='user id')),
                ('study_case_id', models.IntegerField(max_length=100, verbose_name='study_case_id')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='WB_intakes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_id', models.IntegerField(max_length=100, verbose_name='element id')),
                ('intake_id', models.IntegerField(max_length=100, verbose_name='intake id')),
                ('year', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('awy', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='awy')),
                ('Q', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Q')),
                ('cn_mg_l', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='cn_mg_l')),
                ('cp_mg_l', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='cp_mg_l')),
                ('csed_mg_l', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='csed_mg_l')),
                ('wn_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wn_kg')),
                ('wp_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wp_kg')),
                ('wsed_ton', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wsed_ton')),
                ('wn_ret_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wn_ret_kg')),
                ('wp_ret_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wp_ret_kg')),
                ('wsed_ret_ton', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wsed_ret_ton')),
            ],
        ),
        migrations.CreateModel(
            name='WB_PTAP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_id', models.IntegerField(max_length=100, verbose_name='element id')),
                ('PTAP_id', models.IntegerField(max_length=100, verbose_name='PTAP_id')),
                ('year', models.IntegerField(max_length=100, verbose_name='year')),
                ('user_id', models.IntegerField(max_length=100, verbose_name='user id')),
                ('awy', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='awy')),
                ('Q', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Q')),
                ('cn_mg_l', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='cn_mg_l')),
                ('cp_mg_l', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='cp_mg_l')),
                ('csed_mg_l', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='csed_mg_l')),
                ('wn_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wn_kg')),
                ('wp_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wp_kg')),
                ('wsed_ton', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wsed_ton')),
                ('wn_ret_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wn_ret_kg')),
                ('wp_ret_kg', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wp_ret_kg')),
                ('wsed_ret_ton', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='wsed_ret_ton')),
            ],
        ),
    ]
