# Generated by Django 4.0 on 2022-07-19 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_status_test_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
