# Generated by Django 2.2.16 on 2021-04-10 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0055_auto_20210322_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hierarchicalkeyword',
            name='depth',
            field=models.PositiveIntegerField(default=1),
        ),
    ]