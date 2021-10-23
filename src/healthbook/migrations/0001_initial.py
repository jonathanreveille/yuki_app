# Generated by Django 3.2.4 on 2021-06-10 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('animals', '0002_initial'),
        ('schedules', '0004_rename_cat_schedule_pet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('med_name', models.CharField(max_length=100)),
                ('med_start', models.DateField(default='Everyday', null=True)),
                ('med_end', models.DateField(null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_medication', to='animals.pet')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_medication', to='schedules.timeofday', verbose_name='time of day for medication')),
            ],
        ),
        migrations.CreateModel(
            name='HealthBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sterilize', models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=20, null=True, verbose_name='sterilized')),
                ('vaccine', models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=20, null=True, verbose_name='vaccinated')),
                ('last_vaccine', models.DateField(blank=True, null=True, verbose_name='last vaccination')),
                ('next_vaccine', models.DateField(blank=True, null=True, verbose_name='next vaccination')),
                ('veterinary_name', models.CharField(blank=True, max_length=100, null=True)),
                ('veterinary_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_healthbook', to='animals.pet')),
            ],
        ),
    ]