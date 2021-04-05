# Generated by Django 2.2.16 on 2021-04-03 22:47

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('waterproof_parameters', '0003_auto_20210329_1316'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Basins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326, verbose_name='geom')),
                ('continent', models.CharField(max_length=254, verbose_name='Continent')),
                ('symbol', models.CharField(max_length=254, verbose_name='Symbol')),
                ('code', models.IntegerField(default=0, verbose_name='Code')),
                ('label', models.CharField(max_length=50, verbose_name='Label')),
                ('x_min', models.FloatField(default=None, verbose_name='Xmin')),
                ('x_max', models.FloatField(default=None, verbose_name='Xmax')),
                ('y_min', models.FloatField(default=None, verbose_name='Ymin')),
                ('y_max', models.FloatField(default=None, verbose_name='Ymax')),
            ],
        ),
        migrations.CreateModel(
            name='CostFunctionsProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=5, verbose_name='Symbol')),
                ('categorys', models.CharField(max_length=100, verbose_name='Categorys')),
                ('energy', models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Energy')),
                ('labour', models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Labour')),
                ('mater_equipment', models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Materials equipment')),
                ('function_value', models.CharField(max_length=1000, verbose_name='Function')),
                ('function_name', models.CharField(max_length=250, verbose_name='Function name')),
                ('function_description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Function description')),
                ('sub_process', models.CharField(blank=True, max_length=100, null=True, verbose_name='Sub Proccess')),
                ('default_function', models.BooleanField(default=False, verbose_name='Default Function')),
            ],
        ),
        migrations.CreateModel(
            name='DemandParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interpolation_type', models.CharField(max_length=30, verbose_name='Interpolation type')),
                ('initial_extraction', models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Initial extraction')),
                ('ending_extraction', models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Ending extraction')),
                ('years_number', models.IntegerField(verbose_name='Years number')),
                ('is_manual', models.BooleanField(default=False, verbose_name='Manual')),
            ],
        ),
        migrations.CreateModel(
            name='ElementSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graphId', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('normalized_category', models.CharField(max_length=100, verbose_name='Normalized category')),
                ('transported_water', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Extraction value')),
                ('sediment', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Extraction value')),
                ('nitrogen', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Extraction value')),
                ('phosphorus', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Extraction value')),
                ('is_external', models.BooleanField(default=False, verbose_name='External')),
                ('awy', models.FloatField(blank=True, default=None, null=True, verbose_name='Awy')),
                ('q_l_s', models.FloatField(blank=True, default=None, null=True, verbose_name='Qls')),
                ('wsed_ton', models.FloatField(blank=True, default=None, null=True, verbose_name='WsedTon')),
                ('wn_kg', models.FloatField(blank=True, default=None, null=True, verbose_name='WnKg')),
                ('wp_kg', models.FloatField(blank=True, default=None, null=True, verbose_name='WnKg')),
                ('csed_mg_l', models.FloatField(blank=True, default=None, null=True, verbose_name='CsedMgL')),
                ('cn_mg_l', models.FloatField(blank=True, default=None, null=True, verbose_name='Cn')),
                ('cp_mg_l', models.FloatField(blank=True, default=None, null=True, verbose_name='CpMgl')),
                ('wsed_ret_ton', models.FloatField(blank=True, default=None, null=True, verbose_name='WsedRetTon')),
                ('wn_ret_kg', models.FloatField(blank=True, default=None, null=True, verbose_name='WnRetKg')),
                ('wp_ret_ton', models.FloatField(blank=True, default=None, null=True, verbose_name='WpRetTon')),
            ],
        ),
        migrations.CreateModel(
            name='Intake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.CharField(max_length=1024, verbose_name='Description')),
                ('water_source_name', models.CharField(max_length=100, verbose_name='Source name')),
                ('xml_graph', models.TextField(null=True, verbose_name='Graph')),
                ('is_complete', models.BooleanField(default=False, verbose_name='Is complete')),
                ('creation_date', models.DateField()),
                ('updated_date', models.DateField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_parameters.Cities')),
                ('demand_parameters', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.DemandParameters')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessEfficiencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('unitary_process', models.CharField(max_length=100, verbose_name='Unitary process')),
                ('symbol', models.CharField(max_length=100, verbose_name='Symbol')),
                ('categorys', models.CharField(max_length=100, verbose_name='Categorys')),
                ('normalized_category', models.CharField(max_length=100, verbose_name='Normalized category')),
                ('id_wb', models.IntegerField(default=0, verbose_name='ID Wb')),
                ('minimal_sediment_perc', models.IntegerField(default=0, verbose_name='Minimal sediment')),
                ('predefined_sediment_perc', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Predefined sediment')),
                ('maximal_sediment_perc', models.IntegerField(default=0, verbose_name='Maximal sediment')),
                ('minimal_nitrogen_perc', models.IntegerField(default=0, verbose_name='Minimal nitrogen')),
                ('predefined_nitrogen_perc', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Predefined nitrogen')),
                ('maximal_nitrogen_perc', models.IntegerField(default=0, verbose_name='Maximal nitrogen')),
                ('minimal_phoshorus_perc', models.IntegerField(default=0, verbose_name='Minimal phosphorus')),
                ('predefined_phosphorus_perc', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Predefined phosphorus')),
                ('maximal_phosphorus_perc', models.IntegerField(default=0, verbose_name='Maximal phosphorus')),
                ('minimal_transp_water_perc', models.IntegerField(default=0, verbose_name='Minimal transported water')),
                ('predefined_transp_water_perc', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Predefined transported water')),
                ('maximal_transp_water_perc', models.IntegerField(default=0, verbose_name='Maximal transported water')),
            ],
        ),
        migrations.CreateModel(
            name='UserCostFunctions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('function', models.TextField(blank=True, null=True, verbose_name='Function')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waterproof_parameters.Countries')),
                ('template_function', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='waterproof_intake.CostFunctionsProcess')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaterExtraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0, verbose_name='Year')),
                ('value', models.DecimalField(decimal_places=4, max_digits=14, verbose_name='Extraction value')),
                ('demand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.DemandParameters')),
            ],
        ),
        migrations.CreateModel(
            name='ValuesTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=1980, verbose_name='Year')),
                ('water_volume', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Water_volume')),
                ('sediment', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Extraction value')),
                ('nitrogen', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Extraction value')),
                ('phosphorus', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Extraction value')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.ElementSystem')),
            ],
        ),
        migrations.CreateModel(
            name='UserLogicalFunctions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function1', models.TextField(verbose_name='Function1')),
                ('condition1', models.TextField(verbose_name='Condition1')),
                ('function2', models.TextField(verbose_name='Function2')),
                ('condition2', models.TextField(verbose_name='Condition2')),
                ('function3', models.TextField(verbose_name='Function3')),
                ('condition3', models.TextField(verbose_name='Condition3')),
                ('mainFunction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.UserCostFunctions')),
            ],
        ),
        migrations.CreateModel(
            name='Polygon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.FloatField(blank=True, default=None, null=True, verbose_name='Area')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326, verbose_name='geom')),
                ('geomIntake', models.TextField(verbose_name='Geom intake')),
                ('geomPoint', models.TextField(verbose_name='Geom point')),
                ('delimitation_date', models.DateField(auto_now=True)),
                ('delimitation_type', models.CharField(max_length=30, null=True, verbose_name='Delimitation type')),
                ('basin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.Basins')),
                ('intake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.Intake')),
            ],
        ),
        migrations.AddField(
            model_name='elementsystem',
            name='intake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.Intake'),
        ),
        migrations.CreateModel(
            name='ElementConnections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='waterproof_intake.ElementSystem')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='waterproof_intake.ElementSystem')),
            ],
        ),
        migrations.AddField(
            model_name='costfunctionsprocess',
            name='process_efficiencies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.ProcessEfficiencies'),
        ),
    ]
