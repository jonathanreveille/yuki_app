# Generated by Django 3.2.4 on 2021-06-25 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar_profile.jpg', upload_to='upload/img/'),
        ),
    ]
