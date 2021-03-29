# Generated by Django 2.2.16 on 2021-03-25 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('waterproof_intake', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('element_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id Element')),
                ('element_normalize_category', models.CharField(max_length=100, verbose_name='Name Element')),
                ('element_transported_water', models.CharField(max_length=100, verbose_name='Water Transported')),
                ('element_sediments_retained', models.CharField(max_length=100, verbose_name='Retrainer Sediments')),
                ('element_nitrogen_retained', models.CharField(max_length=100, verbose_name='Retrainer Nitrogen')),
                ('element_phosphorus_retained', models.CharField(max_length=100, verbose_name='Retrainer Phosphorus')),
                ('element_plant_id', models.IntegerField(verbose_name='Id Plant')),
                ('element_graph_id', models.IntegerField(verbose_name='Id Graph')),
                ('element_on_off', models.BooleanField(default=False, verbose_name='On off Element')),
                ('element_q_l', models.FloatField(blank=True, default=None, null=True, verbose_name='Q L Element')),
                ('element_awy', models.FloatField(blank=True, default=None, null=True, verbose_name='Awy Element')),
                ('element_cn_mg_l', models.FloatField(blank=True, default=None, null=True, verbose_name='CN Mg L Element')),
                ('element_cp_mg_l', models.FloatField(blank=True, default=None, null=True, verbose_name='CP Mg L Element')),
                ('element_csed_mg_l', models.FloatField(blank=True, default=None, null=True, verbose_name='Mg L Csed Element')),
                ('element_wn_kg', models.FloatField(blank=True, default=None, null=True, verbose_name='Wn Kg Element')),
                ('element_wn_rent_kg', models.FloatField(blank=True, default=None, null=True, verbose_name='Wn Rent Kg Element')),
                ('element_wp_rent_ton', models.FloatField(blank=True, default=None, null=True, verbose_name='Wn Rent Ton Element')),
                ('element_wsed_tom', models.FloatField(blank=True, default=None, null=True, verbose_name='Wsed Ton Element')),
                ('element_wp_kg', models.FloatField(blank=True, default=None, null=True, verbose_name='Wp Kg Element')),
                ('element_wsed_ret_ton', models.FloatField(blank=True, default=None, null=True, verbose_name='ElementWSED_RET_TON')),
                ('element_user', models.CharField(max_length=100, verbose_name='User Element')),
                ('element_date_create', models.DateTimeField(verbose_name='Date Create Element')),
                ('element_date_update', models.DateTimeField(auto_now=True, verbose_name='Date Update Element')),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('function_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id Function')),
                ('function_name', models.CharField(max_length=100, verbose_name='Name Function')),
                ('function_graph_id', models.CharField(max_length=100, verbose_name='Graph Id Function')),
                ('function_value', models.CharField(max_length=300, verbose_name='Value Function')),
                ('function_currency', models.CharField(max_length=1, verbose_name='Currency Function')),
                ('function_factor', models.CharField(max_length=100, verbose_name='Factor')),
                ('function_id_sub_process', models.CharField(max_length=100, verbose_name='Sub Process')),
                ('function_user', models.CharField(max_length=100, verbose_name='User')),
                ('function_date_create', models.DateTimeField(auto_now=True, verbose_name='Date Create')),
                ('function_date_update', models.DateTimeField(verbose_name='Date Update')),
                ('function_plant_id', models.IntegerField(verbose_name='Plant Id')),
                ('function_transported_water', models.CharField(max_length=100, verbose_name='Water')),
                ('function_sediments_retained', models.CharField(max_length=100, verbose_name='Sediments')),
                ('function_nitrogen_retained', models.CharField(max_length=100, verbose_name='Nitrogen')),
                ('function_phosphorus_retained', models.CharField(max_length=100, verbose_name='Phosphorus')),
                ('function_technology', models.CharField(max_length=100, verbose_name='Technology')),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('plant_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id Plant')),
                ('plant_name', models.CharField(max_length=100, verbose_name='Name Plant')),
                ('plant_description', models.CharField(max_length=300, verbose_name='Description Plant')),
                ('plant_suggest', models.CharField(max_length=1, verbose_name='Suggest Plant')),
                ('plant_user', models.CharField(max_length=100, verbose_name='User Plant')),
                ('plant_date_create', models.DateTimeField(verbose_name='Date Create Plant')),
                ('plant_date_update', models.DateTimeField(auto_now=True, verbose_name='Date Update Plant')),
                ('plant_city_id', models.IntegerField(verbose_name='Id City')),
            ],
        ),
        migrations.CreateModel(
            name='Ptap',
            fields=[
                ('ptap_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id Csinfra')),
                ('ptap_plant_id', models.IntegerField(verbose_name='Plant Id')),
                ('ptap_user', models.CharField(max_length=100, verbose_name='User')),
                ('ptap_type', models.CharField(max_length=100, verbose_name='Type ptap')),
                ('ptap_date_create', models.CharField(max_length=100, verbose_name='Date Update')),
                ('ptap_awy', models.FloatField(blank=True, default=None, null=True, verbose_name='Awy ptap')),
                ('ptap_cn', models.FloatField(blank=True, default=None, null=True, verbose_name='Cn ptap')),
                ('ptap_cp', models.FloatField(blank=True, default=None, null=True, verbose_name='Cp ptap')),
                ('ptap_cs', models.FloatField(blank=True, default=None, null=True, verbose_name='Cs ptap')),
                ('ptap_wn', models.FloatField(blank=True, default=None, null=True, verbose_name='Wn ptap')),
                ('ptap_wp', models.FloatField(blank=True, default=None, null=True, verbose_name='Wp ptap')),
                ('ptap_ws', models.FloatField(blank=True, default=None, null=True, verbose_name='Ws ptap')),
            ],
        ),
        migrations.CreateModel(
            name='Csinfra',
            fields=[
                ('csinfra_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id Csinfra')),
                ('csinfra_plant_id', models.IntegerField(verbose_name='Plant Id')),
                ('csinfra_user', models.CharField(max_length=100, verbose_name='User')),
                ('csinfra_date_create', models.CharField(max_length=100, verbose_name='Date Create')),
                ('csinfra_date_update', models.CharField(max_length=100, verbose_name='Date Update')),
                ('csinfra_elementsystem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.ElementSystem')),
            ],
        ),
    ]