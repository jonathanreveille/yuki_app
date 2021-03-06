# Generated by Django 3.2.4 on 2021-06-16 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('friends', '0007_alter_friendrequest_options'),
        ('messenger', '0002_alter_messenger_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('friend_request',
                 models.ForeignKey(blank=True,
                                   null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   related_name='+',
                                   to='friends.friendrequest')),
                ('from_user',
                 models.ForeignKey(blank=True,
                                   null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   related_name='notification_from',
                                   to=settings.AUTH_USER_MODEL)),
                ('message',
                 models.ForeignKey(blank=True,
                                   null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   related_name='+',
                                   to='messenger.messenger')),
                ('to_user',
                 models.ForeignKey(blank=True,
                                   null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   related_name='notification_to',
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
