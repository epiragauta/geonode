# Generated by Django 2.2.16 on 2021-01-26 14:17

from django.db import migrations, models
from django.utils.translation import ugettext_lazy as _

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('plant_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=_('Id Plant'))),
                ('plant_name', models.CharField(max_length=100,verbose_name=_('Name Plant'))),
                ('plant_description', models.CharField(max_length=300,verbose_name=_('Description Plant'))),
                ('plant_suggest', models.CharField(max_length=1,verbose_name=_('Suggest Plant'))),
                ('plant_user', models.CharField(max_length=100,verbose_name=_('User Plant'))),
                ('plant_date_create', models.DateTimeField(auto_now=False,verbose_name=_('Date Create Plant'))),
                ('plant_date_update', models.DateTimeField(auto_now=True,verbose_name=_('Date Update Plant'))),
                ('plant_city_id', models.IntegerField(verbose_name=_('Id City')))
            ],
            options={
                'ordering': ['plant_id', 'plant_name'],
            },
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('function_id',models.IntegerField(auto_created=True, primary_key=True,verbose_name=_('Id Function'))),
                ('function_name', models.CharField(max_length=100,verbose_name=_('Name Function'))),
                ('function_value', models.CharField(max_length=300,verbose_name=_('Value Function'))),
                ('function_currency', models.CharField(max_length=1,verbose_name=_('Currency Function'))),
                ('function_factor', models.CharField(max_length=100,verbose_name=_('Factor'))),
                ('function_id_sub_process', models.CharField(max_length=100,verbose_name=_('Sub Process'))),
                ('function_user', models.CharField(max_length=100,verbose_name=_('User'))),
                ('function_date_create', models.DateTimeField(auto_now=True,verbose_name=_('Date Create'))),
                ('function_date_update', models.DateTimeField(auto_now=False, verbose_name=_('Date Update'))),
                ('function_plant_id', models.IntegerField( verbose_name=_('Plant Id'))),
                ('function_transported_water', models.CharField(max_length=100,verbose_name=_('Water'))),
                ('function_sediments_retained', models.CharField(max_length=100,verbose_name=_('Sediments'))),
                ('function_nitrogen_retained', models.CharField(max_length=100,verbose_name=_('Nitrogen'))),
                ('function_phosphorus_retained', models.CharField(max_length=100,verbose_name=_('Phosphorus'))),
                ('function_technology', models.CharField(max_length=100,verbose_name=_('Technology')))
            ],
            options={
                'ordering': ['function_id'],
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('element_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=_('Id Element'))),
                ('element_normalize_category', models.CharField(max_length=100,verbose_name=_('Name Element'))),
                ('element_transported_water', models.CharField(max_length=100,verbose_name=_('Water Transported'))),
                ('element_sediments_retained', models.CharField(max_length=100,verbose_name=_('Retrainer Sediments'))),
                ('element_nitrogen_retained', models.CharField(max_length=100,verbose_name=_('Retrainer Nitrogen'))),
                ('element_phosphorus_retained', models.CharField(max_length=100,verbose_name=_('Retrainer Phosphorus'))),
                ('element_plant_id', models.IntegerField(verbose_name=_('Id Plant'))),
                ('element_graph_id', models.IntegerField(verbose_name=_('Id Graph'))),
                ('element_on_off', models.BooleanField(default=False, verbose_name=_('On off Element'))),
                ('element_q_l', models.IntegerField(verbose_name=_('Q L Element'))),
                ('element_awy', models.IntegerField(verbose_name=_('Awy Element'))),
                ('element_cn_mg_l', models.IntegerField(verbose_name=_('CN Mg L Element'))),
                ('element_cp_mg_l', models.IntegerField(verbose_name=_('CP Mg L Element'))),
                ('element_csed_mg_l', models.IntegerField(verbose_name=_('Mg L Csed Element'))),
                ('element_wn_kg', models.IntegerField(verbose_name=_('Wn Kg Element'))),
                ('element_wn_rent_kg', models.IntegerField(verbose_name=_('Wn Rent Kg Element'))),
                ('element_wp_rent_ton', models.IntegerField(verbose_name=_('Wn Rent Ton Element'))),
                ('element_wsed_tom', models.IntegerField(verbose_name=_('Wsed Ton Element'))),
                ('element_wp_kg', models.IntegerField(verbose_name=_('Wp Kg Element'))),
                ('element_user', models.CharField(max_length=100,verbose_name=_('User Element'))),
                ('element_date_create', models.DateTimeField(auto_now=False,verbose_name=_('Date Create Element'))),
                ('element_date_update', models.DateTimeField(auto_now=True,verbose_name=_('Date Update Element')))
            ],
            options={
                'ordering': ['element_id'],
            },
        ),
        migrations.CreateModel(
            name='Csinfra',
            fields=[
                ('csinfra_id', models.IntegerField(auto_created=True, primary_key=True,verbose_name=_('Id Csinfra'))),
                ('csinfra_plant_id', models.IntegerField(verbose_name=_('Plant Id'))),
                ('csinfra_user', models.CharField(max_length=100,verbose_name=_('User'))),
                ('csinfra_date_create', models.CharField(max_length=100,verbose_name=_('Date Create'))),
                ('csinfra_date_update', models.CharField(max_length=100,verbose_name=_('Date Update'))),
                ('csinfra_elementsystem_id', models.CharField(max_length=100,verbose_name=_('Element System')))
            ],
            options={
                'ordering': ['plant_id', 'plant_name'],
            },
        )
    ]


