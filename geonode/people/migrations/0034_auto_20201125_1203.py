# Generated by Django 2.2.16 on 2020-11-25 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0033_profile_other_analysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='delivery',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='fax',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='position',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='voice',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='zipcode',
        ),
        migrations.AlterField(
            model_name='profile',
            name='use_analysis',
            field=models.CharField(blank=True, choices=[('ACDMC', 'Academic'), ('GNRL', 'General'), ('BSNSS', 'Business'), ('OTHER', 'Other')], help_text='Use Analysis', max_length=8, null=True, verbose_name='UseAnalysis'),
        ),
    ]