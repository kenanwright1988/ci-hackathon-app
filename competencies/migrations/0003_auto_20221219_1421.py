# Generated by Django 3.1.13 on 2022-12-19 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0002_auto_20220808_1029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competencyassessment',
            options={'verbose_name': 'Competency Self Assessment', 'verbose_name_plural': 'Competency Self Assessments'},
        ),
        migrations.AlterModelOptions(
            name='competencyassessmentrating',
            options={'verbose_name': 'Competency Self Assessment Rating', 'verbose_name_plural': 'Competency Self Assessment Ratings'},
        ),
    ]
