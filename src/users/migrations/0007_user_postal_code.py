# Generated by Django 3.2.4 on 2021-06-15 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
