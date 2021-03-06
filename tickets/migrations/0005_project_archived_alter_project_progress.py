# Generated by Django 4.0 on 2022-07-12 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticket_email_disable'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='progress',
            field=models.TextField(choices=[('opened', 'Opened'), ('in_progress', 'In Progress'), ('closed', 'Closed')], null=True),
        ),
    ]
