# Generated by Django 2.2.16 on 2021-01-15 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_intake', '0020_auto_20210114_0347'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementConnections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waterproof_intake.ElementSystem')),
            ],
        ),
    ]
