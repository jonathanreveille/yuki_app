# Generated by Django 3.2.4 on 2021-06-10 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(blank=True, choices=[('CLEANING', 'Cleaning'), ('FOOD', 'Food'), ('MEDICATION', 'Medication')], max_length=40, null=True, verbose_name='category of task'),
        ),
    ]
