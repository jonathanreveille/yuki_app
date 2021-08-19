# Generated by Django 3.2.4 on 2021-07-24 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('animals', '0003_pet_avatar'),
        ('friends', '0007_alter_friendrequest_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catsitter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(null=True)),
                ('end', models.DateTimeField(null=True)),
                ('is_catsitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_catsitter', to=settings.AUTH_USER_MODEL, verbose_name='catsitter')),
                ('is_owned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_cat_owner', to=settings.AUTH_USER_MODEL, verbose_name="cat's owner")),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catsitted', to='animals.pet', verbose_name='catsitted')),
            ],
        ),
    ]
