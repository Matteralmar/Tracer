# Generated by Django 4.0 on 2022-07-22 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0015_remove_notification_recipient_user_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='notification',
        ),
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='tickets.user'),
        ),
    ]
